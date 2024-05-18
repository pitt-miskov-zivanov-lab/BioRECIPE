# -*- coding: utf-8 -*-
#
# This file is a part of translator for BioRECIPE format.
#
# __author__ = "Difei Tang"
# __email__ = "DIT18@pitt.edu"

import argparse
import pandas as pd
import math
import re
import logging
from libsbml import *

map_sign_reaction_type = {'positive': 'Activation',
                          'negative': 'Inhibition'}
def urlify(s):
    # remove invalid characters
    s = re.sub(r"[^\w\s]", '', s)
    s = re.sub(r"\s+",'_',s)
    return s

def check(value, message):
    """If 'value' is None, prints an error message constructed using
    'message' and then exits with status code 1.  If 'value' is an integer,
    it assumes it is a libSBML return status code.  If the code value is
    LIBSBML_OPERATION_SUCCESS, returns without further action; if it is not,
    prints an error message constructed using 'message' along with text from
    libSBML explaining the meaning of the code, and exits with status code 1.
    """
    if value is None:
        raise SystemExit('LibSBML returned a null value trying to ' + message + '.')
    elif type(value) is int:
        if value == LIBSBML_OPERATION_SUCCESS:
            return
        else:
            err_msg = 'Error encountered trying to ' + message + '.' \
                      + 'LibSBML returned error code ' + str(value) + ': "' \
                      + OperationReturnValue_toString(value).strip() + '"'
            raise SystemExit(err_msg)
    else:
        return

def get_sbml_from_biorecipeI(input_file, output_file):
    DOCUMENT = create_document(input_file)

    # write sbml file
    writeSBMLToFile(DOCUMENT, output_file)

    model = DOCUMENT.getModel()

    if model is None:
        print("No model present.")
        return 1

    if model.isSetSBOTerm():
        logging.info("      model sboTerm: " + str(model.getSBOTerm()))

    logging.info("functionDefinitions: " + str(model.getNumFunctionDefinitions()))
    logging.info("    unitDefinitions: " + str(model.getNumUnitDefinitions()))
    logging.info("   compartmentTypes: " + str(model.getNumCompartmentTypes()))
    logging.info("        specieTypes: " + str(model.getNumSpeciesTypes()))
    logging.info("       compartments: " + str(model.getNumCompartments()))
    logging.info("            species: " + str(model.getNumSpecies()))
    logging.info("         parameters: " + str(model.getNumParameters()))
    logging.info(" initialAssignments: " + str(model.getNumInitialAssignments()))
    logging.info("              rules: " + str(model.getNumRules()))
    logging.info("        constraints: " + str(model.getNumConstraints()))
    logging.info("          reactions: " + str(model.getNumReactions()))
    logging.info("             events: " + str(model.getNumEvents()))

    return

def print_sbml(filename):
    DOCUMENT = readSBML(filename)

    model = DOCUMENT.getModel()

    if model is None:
        print("No model present.")
        return 1

    if model.isSetSBOTerm():
        logging.info("      model sboTerm: " + str(model.getSBOTerm()))

    logging.info("functionDefinitions: " + str(model.getNumFunctionDefinitions()))
    logging.info("    unitDefinitions: " + str(model.getNumUnitDefinitions()))
    logging.info("   compartmentTypes: " + str(model.getNumCompartmentTypes()))
    logging.info("        specieTypes: " + str(model.getNumSpeciesTypes()))
    logging.info("       compartments: " + str(model.getNumCompartments()))
    logging.info("            species: " + str(model.getNumSpecies()))
    logging.info("         parameters: " + str(model.getNumParameters()))
    logging.info(" initialAssignments: " + str(model.getNumInitialAssignments()))
    logging.info("              rules: " + str(model.getNumRules()))
    logging.info("        constraints: " + str(model.getNumConstraints()))
    logging.info("          reactions: " + str(model.getNumReactions()))
    logging.info("             events: " + str(model.getNumEvents()))

def create_document(input_file):
    """ map interactions to SBML activity flow """
    try:
        document = SBMLDocument(2, 4)
    except ValueError:
        raise SystemExit('Could not create SBMLDocument object')

    map_eid_sid = {}

    # create model
    model = document.createModel()
    check(model, "create model")

    # create compartment by default in case no compartment is found
    c1 = model.createCompartment()
    check(c1, 'create compartment')
    check(c1.setId('c1'), 'set compartment id')

    df = pd.read_excel(input_file)

    sid = 1
    for i in range(len(df)):
        source_name = df.loc[i, 'Regulator Name']
        source_id = urlify(df.loc[i, 'Regulator ID'])
        source_compartment = df.loc[i, 'Regulator Compartment']

        target_name = df.loc[i, 'Regulated Name']
        target_id = urlify(df.loc[i, 'Regulated ID'])
        target_compartment = df.loc[i, 'Regulated Compartment']

        if source_id not in map_eid_sid.keys():
            map_eid_sid[source_id] = f's{sid}'

            # create source species
            species = model.createSpecies()
            check(species, 'create target species')
            check(species.setId(f's{sid}'), 'set species id')
            check(species.setMetaId("metaid_" + f's{sid}'), 'set meta ID')
            check(species.setName(source_name), "set species name")

            check(species.appendNotes("<p xmlns=\"http://www.w3.org/1999/xhtml\">{0}</p>".format(f'Regulator ID:{source_id}')),
                  'append notes of regulator id')

            if type(source_compartment) is str:
                check(species.setCompartment(source_compartment), 'set species compartment')
            else:
                check(species.setCompartment('c1'), 'set species compartment')

            sid += 1

        if target_id not in map_eid_sid.keys():
            map_eid_sid[target_id] = f's{sid}'

            species = model.createSpecies()
            check(species, 'create source species')
            check(species.setId(f's{sid}'), 'set species id')
            check(species.setMetaId("metaid_" + f's{sid}'), 'set meta ID')
            check(species.setName(target_name), "set species name")

            check(species.appendNotes("<p xmlns=\"http://www.w3.org/1999/xhtml\">{0}</p>".format(f'Regulater ID:{target_id}')),
                  'append notes of regulated id')

            if type(target_compartment) is str:
                check(species.setCompartment(target_compartment), 'set species compartment')
            else:
                check(species.setCompartment('c1'), 'set species compartment')

            sid += 1

        mechanism = df.loc[i, 'Mechanism']
        sign = df.loc[i, 'Sign']

        # for each interaction, create a reaction
        reaction = model.createReaction()
        check(reaction, 'create reaction')
        check(reaction.setId(f'r{i+1}'), 'set reaction id')

        if type(mechanism) is not str and math.isnan(mechanism):
            rt = map_sign_reaction_type[sign]
            check(reaction.setName(rt), 'set reaction name')
        else:
            check(reaction.setName(mechanism), 'set reaction name')

        check(reaction.setMetaId("metaid_" + f'r{i+1}'), 'set meta ID')
        check(reaction.setReversible(False), 'make irreversible')

        s_species = model.getSpecies(map_eid_sid[source_id])
        t_species = model.getSpecies(map_eid_sid[target_id])
        reaction = model.getReaction(f'r{i+1}')

        reactant_ref = reaction.createReactant()
        check(reactant_ref, 'create reactant')
        check(reactant_ref.setSpecies(s_species.getId()), 'assign reactant species')

        product_ref = reaction.createProduct()
        check(product_ref, 'create product reference')
        check(product_ref.setSpecies(t_species.getId()), 'assign product species')

    return document

def main():
    parser = argparse.ArgumentParser()

    # required arguments
    required_args = parser.add_argument_group('required input arguments')

    required_args.add_argument('-i', '--input', type=str, required=True,
                               help='Path of the input BioRECIPE interaction lists file (.xlsx)')
    required_args.add_argument('-o', '--output', type=str, required=True,
                               help='Path of the output SBML file (.xml)')

    args = parser.parse_args()
    get_sbml_from_biorecipeI(args.input, args.output)

if __name__ == "__main__":
    main()
