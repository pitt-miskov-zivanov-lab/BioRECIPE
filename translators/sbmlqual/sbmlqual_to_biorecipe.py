# -*- coding: utf-8 -*-
#
# This file is part of translator for BioRECIPE format.
#
# __author__ = "Difei Tang"
# __email__ = "DIT18@pitt.edu"

# To use this translator
# python run_sbmlqual_biorecipe.py -i [SBMLQual] -o [BioRECIPE]

# where you need to have the terminal work in the directory of this python script
# and [SBMLQual] is the path and name of SBMLQual file, and [BioRECIPE] is the generated model in BioRecipes format

import bs4
import pandas as pd
import argparse
from translators.within_biorecipe.biorecipe_std import biorecipe_mdl_cols

class SBMLQualMath():

    """
    SBMLQual processor
    """

    def sbmlqual_biorecipe(self, input_file=None, input_str=None, output_file=None):

        """
        translate SBMLQual XML file to BioRECIPE format

        :param str input_file: the filename of the SBMLQual
        :param str output_file: the filename of the translated BioRECIPE

        SBMLQual XML file was downloaded from https://cellcollective.org/#
        """

        # initialize a model dataframe in BioRECIPE format
        biorecipe_df = pd.DataFrame(columns=biorecipe_mdl_cols)

        # XML.etree has some issues of parsing the SBMLQual XML file. BeautifulSoup loses the upper cases while reading
        if input_file:
            res = bs4.BeautifulSoup(open(input_file).read(), 'lxml')
        elif input_str:
            res = bs4.BeautifulSoup(input_str, 'lxml')
        else:
            raise ValueError("Either input_file or input_str must be provided.")

        self.model = res.findAll("model")[0]
        self.model_dict = dict()
        idx = 1

        for species in res.findChildren("qual:qualitativespecies"):
            sid = species.get('qual:id')
            name = species.get('qual:name')
            compartment = species.get('qual:compartment')
            initial_level = species.get('qual:initiallevel')
            max_level = species.get('qual:maxlevel')
            self.model_dict[sid] = name

            #TODO: thersholdLevel & geq equation for value update
            if initial_level is None:
                initial_level = 'r'
            if max_level is None:
                max_level = 1

            new_row = {'#':idx, 'Element Name':name, 'Element IDs':sid, 'Compartment': compartment,
                       'Variable':name, 'Levels': int(max_level)+1, 'State List 0':initial_level}
            new_df = pd.DataFrame([new_row])

            biorecipe_df = pd.concat([biorecipe_df, new_df], ignore_index=True)
            idx += 1

        # Then, we go through all function terms
        for transition in res.findChildren("qual:transition"):
            inputs = [x['qual:qualitativespecies'] for x in transition.findChildren("qual:input")]
            signs = [x['qual:sign'] for x in transition.findChildren("qual:input")]
            output = [x['qual:qualitativespecies'] for x in transition.findChildren("qual:output")]
            assert len(output) == 1
            assert len(inputs) == len(signs)
            outputs = output * len(signs)

            # there may be different functions so we will need to loop over them
            functions = transition.findChildren("qual:functionterm")
            if len(functions) > 1:
                print("does not handle multiple functions")
            contents = functions[0].findChild('apply')

            reaction = self._get_reaction_from_mathml(contents)
            update_rule = ",".join(reaction)

            biorecipe_df.loc[biorecipe_df['Element IDs'] == outputs[0], 'Positive Regulation Rule'] = update_rule

        if output_file: 
            biorecipe_df.to_excel(output_file, index=False)
        else:
            return biorecipe_df

    def _get_reaction_from_mathml(self, contents):

        # TODO: we assume sop boolean expression here
        # only have one or two regulators
        if contents.find('and') and not contents.find('or'):
            lhs = self._get_lhs_from_mathml(contents)
            reaction = lhs
        elif contents.find('or') is None and contents.find('and') is None:
            lhs = self._get_lhs_from_mathml(contents)
            reaction = lhs
        else:
            # multiple ORs
            reaction = []
            for content in contents.findChildren('apply', recursive=False):
                lhs = self._get_reaction_from_mathml(content)
                for unit in lhs:
                    reaction.append(unit)

        return reaction

    def _get_lhs_from_mathml(self, xml):
        entries = xml.findChildren('apply', recursive=False)
        if len(entries) == 0:
            entries = [xml]
        lhs = []
        for entry in entries:
            if entry.find('not') is not None:
                name = entry.find('ci').text.strip()
                lhs.append("!" + self.model_dict[name])
            else:
                name = entry.find('ci').text.strip()
                lhs.append(self.model_dict[name])
        if xml.find('and') is not None:
            lhs = ",".join(list(set(lhs)))
            lhs = ["(" + lhs + ")"]
        return lhs

def get_biorecipeM_from_sbmlqual(input_filename: str=None,input_str: str=None, output_filename:str=None):
    sbmlqual_math = SBMLQualMath()
    if output_filename:
        sbmlqual_math.sbmlqual_biorecipe(input_file=input_filename, input_str=input_str, output_file=output_filename)
    else:
        return sbmlqual_math.sbmlqual_biorecipe(input_file=input_filename, input_str=input_str, output_file=output_filename)

def main():
    parser = argparse.ArgumentParser()

    parser.add_argument('--input_file', '-i', type=str, help='Path and name of input file (.xml)')
    parser.add_argument('--output_file','-o', type=str, help='Path and name of model output (.xlsx)')

    args = parser.parse_args()

    get_biorecipeM_from_sbmlqual(input_filename=args.input_file, input_str=None, output_filename=args.output_file)

if __name__ == "__main__":
    main()
