# -*- coding: utf-8 -*-
#
# This file is a part of translator for BioRECIPE format.
#
# __author__ = "Difei Tang"
# __email__ = "DIT18@pitt.edu"

import re
import argparse
import casq.celldesigner2qual as casq
from typing import Optional
import xml.etree.ElementTree as etree
import pandas as pd
import networkx as nx

# TODO: multiple scenario translation
scenario_detailed_col = ['Element Name', 'Element Type', 'Element Subtype',
       'Element HGNC Symbol', 'Element Database', 'Element IDs', 'Compartment',
       'Compartment ID', 'Cell Line', 'Cell Type', 'Tissue Type', 'Organism',
       'Positive Regulator List', 'Positive Connection Type List',
       'Positive Mechanism List', 'Positive Site List',
       'Negative Regulator List', 'Negative Connection Type List',
       'Negative Mechanism List', 'Negative Site List', 'Score List',
       'Source List', 'Statements List', 'Paper IDs List',
       'Positive Regulation Rule', 'Negative Regulation Rule', 'Variable',
       'Value Type', 'Levels', 'State List 0', 'State List 1', 'Const OFF',
       'Const ON', 'Increment', 'Spontaneous', 'Balancing', 'Delay',
       'Update Group', 'Update Rate', 'Update Rank']

NS = {
        "sbml": "http://www.sbml.org/sbml/level2/version4",
        "cd": "http://www.sbml.org/2001/ns/celldesigner",
        "sbml3": "http://www.sbml.org/sbml/level3/version1/core",
        "layout": "http://www.sbml.org/sbml/level3/version1/layout/version1",
        "qual": "http://www.sbml.org/sbml/level3/version1/qual/version1",
        "mathml": "http://www.w3.org/1998/Math/MathML",
        "rdf": "http://www.w3.org/1999/02/22-rdf-syntax-ns#",
        "dc": "http://purl.org/dc/elements/1.1/",
        "dcterms": "http://purl.org/dc/terms/",
        "vCard": "http://www.w3.org/2001/vcard-rdf/3.0#",
        "bqbiol": "http://biomodels.net/biology-qualifiers/",
        "bqmodel": "http://biomodels.net/model-qualifiers/",
        "xhtml": "http://www.w3.org/1999/xhtml",
    }

def urlify(s):
    s = re.sub(r"[^\w\s]", '_', s)
    s = re.sub(r"\s+",'_',s)
    return s

def find_pos_regulators(math: Optional[etree.Element], info) -> str:
    if math is None:
        raise ValueError("Empty math element")
    if math.tag != "apply":
        raise ValueError(etree.tostring(math))
    children = list(math)
    if children[0].tag == "or":
        return ",".join(find_pos_regulators(x, info) for x in children[1:])
    if children[0].tag == "and":
        return "(" + ",".join(find_pos_regulators(x, info) for x in children[1:]) + ")"
    if children[0].tag == "eq":
        species = children[1].text
        species = urlify(info[species]["name"]+'_'+species)
        if species is None or children[2].text == "0":
            species = ""
        return species
    raise ValueError(etree.tostring(math))

def find_neg_regulators(math: Optional[etree.Element], info) -> str:
    if math is None:
        raise ValueError("Empty math element")
    if math.tag != "apply":
        raise ValueError(etree.tostring(math))
    children = list(math)

    neg_list = []
    for c in children:
        if c.tag == "apply" and list(c)[0].tag == "eq":
            species = list(c)[1].text
            species = urlify(info[species]["name"]+'_'+species)
            if list(c)[2].text == "0":
                neg_list.append(species)

    return ','.join(filter(None, neg_list))

def add_transitions_modified(tlist: etree.Element, info, graph: nx.DiGraph):

    """
    Create transition elements, modified from celldesigner2qual.py
    """

    known = list(info.keys())
    for species, data in info.items():
        if data["transitions"]:
            trans = etree.SubElement(
                tlist, "qual:transition", {"qual:id": "tr_" + species}
            )
            ilist = etree.SubElement(trans, "qual:listOfInputs")
            casq.add_inputs(ilist, data["transitions"], species, known, graph)

            if len(ilist) == 0:
                tlist.remove(trans)
                info[species]["transitions"] = []
                posfunc, negfunc = info[species]["function"], ""
                info[species]["function"] = (posfunc, negfunc)
                casq.add_function_as_rdf(info, species, posfunc + " " + negfunc)  # FIXME
            else:
                olist = etree.SubElement(trans, "qual:listOfOutputs")
                etree.SubElement(
                    olist,
                    "qual:output",
                    {
                        "qual:qualitativeSpecies": species,
                        "qual:transitionEffect": "assignmentLevel",
                        "qual:id": f"tr_{species}_out",
                    },
                )
                flist = etree.SubElement(trans, "qual:listOfFunctionTerms")
                etree.SubElement(flist, "qual:defaultTerm", {"qual:resultLevel": "0"})
                func = etree.SubElement(
                    flist, "qual:functionTerm", {"qual:resultLevel": "1"}
                )
                casq.add_function(func, data["transitions"], known)

                posfunc, negfunc = mathml_to_biorecipes(func.find("./math/*", NS), info)
                info[species]["function"] = (posfunc, negfunc)
                casq.add_function_as_rdf(info, species, posfunc + " " + negfunc) # FIXME: rdf?
                casq.add_notes(trans, data["transitions"])
                casq.add_annotations(trans, data["transitions"])

        else:
            casq.add_function_as_rdf(info, species, info[species]["function"]) # no regulators

def mathml_to_biorecipes(math: Optional[etree.Element], info):
    """Convert a MATHML boolean formula into its BIORECIPES representation."""
    pos = find_pos_regulators(math, info)
    neg = find_neg_regulators(math, info)

    # cleanup regulation
    pos = list(filter(lambda item: len(item) > 0, pos.split(',')))
    pos = ','.join(pos)
    if ',)' in pos:
        pos = pos.replace(',)', ')')

    if neg == ",":
        # no inhibitor is found
        neg = ""
    return pos, neg

def write_biorecipes(filename, info):
    df = pd.DataFrame(columns=scenario_detailed_col)

    for species, data in sorted(info.items()):
        if data["transitions"]:
            new_row = {"Element Name": urlify(data["name"]), "Element IDs": species, "Element Type": data["type"], "Compartment": data["compartment"],
                            "Variable": urlify(data["name"]+'_'+species), "Positive Regulation Rule": data["function"][0], "Negative Regulation Rule": data["function"][1],
                            "Levels": 2, "State List 0": 'r'}
            new_df = pd.DataFrame([new_row])
            df = pd.concat([df, new_df], ignore_index=True)
        else:
            new_row = {"Element Name": urlify(data["name"]), "Element IDs": species, "Element Type": data["type"], "Compartment": data["compartment"],
                            "Variable": urlify(data["name"]+'_'+species), "Levels": 2, "State List 0": 'r'}
            new_df = pd.DataFrame([new_row])
            df = pd.concat([df, new_df], ignore_index=True)

    df.to_excel(filename, index=True)

def write_qual_modified(
    filename: str, info, width: str, height: str, remove: int = 0
):
    """
    Write the SBML qual with layout file, modified from celldesigner2qual.py
    """

    for name, space in NS.items():
        etree.register_namespace(name, space)
    root = etree.Element(
        "sbml",
        {
            "level": "3",
            "version": "1",
            "layout:required": "false",
            "xmlns": NS["sbml3"],
            "qual:required": "true",
            "xmlns:layout": NS["layout"],
            "xmlns:qual": NS["qual"],
        },
    )
    model = etree.SubElement(root, "model", id="model_id")
    notes = etree.SubElement(model, "notes")
    html = etree.SubElement(notes, "html", xmlns=NS["xhtml"])
    body = etree.SubElement(html, "body")
    p = etree.SubElement(body, "p")
    p.text = "Created by CaSQ 1.2.0"
    clist = etree.SubElement(model, "listOfCompartments")
    etree.SubElement(clist, "compartment", constant="true", id="comp1")
    llist = etree.SubElement(model, "layout:listOfLayouts")
    layout = etree.SubElement(llist, "layout:layout", id="layout1")
    etree.SubElement(layout, "layout:dimensions", width=width, height=height)
    qlist = etree.SubElement(model, "qual:listOfQualitativeSpecies")
    tlist = etree.SubElement(model, "qual:listOfTransitions")
    graph = nx.DiGraph()
    add_transitions_modified(tlist, info, graph)
    casq.remove_connected_components(tlist, info, graph, remove)
    casq.add_qual_species(layout, qlist, info)

def get_biorecipeM_from_sbml(map_filename: str, model_filename: str):
    with open(map_filename, "r", encoding="utf-8") as f:
        info, width, height = casq.read_celldesigner(f)
    casq.simplify_model(info, [], [])
    write_qual_modified(model_filename, info, width, height)
    write_biorecipes(model_filename, info)
    #print("Finished: {}".format(model_filename.split('/')[-1]))

def main():
    parser = argparse.ArgumentParser()

    # required arguments
    required_args = parser.add_argument_group('required input arguments')

    required_args.add_argument('-i', '--input', type=str, required=True,
                               help='Path and name of the input SBML file (.xml)')
    required_args.add_argument('-o', '--output', type=str, required=True,
                               help='Path and name of the output BioRECIPE model file (.xlsx)')

    args = parser.parse_args()

    get_biorecipeM_from_sbml(args.input, args.output)

if __name__ == "__main__":
    main()
