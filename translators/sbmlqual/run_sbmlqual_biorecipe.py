# -*- coding: utf-8 -*-
#
# This file is part of translator for BioRECIPE format.
#
# __author__ = "Difei Tang"
# __email__ = "DIT18@pitt.edu"

# To use this translator
# python run_sbmlqual_biorecipe.py -i [SBMLQual] -o [BioRECIPE]

# where you need to have the terminal work in the directory of this python script
# and [SBMLQual] is the path and name of SBMLQual file, and [BioRECIPE] is the generated file in BioRecipes format

import bs4
import pandas as pd
import argparse

model_cols = ['#', 'Element Name', 'Element Type', 'Element Subtype',
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

class SBMLQual():
    """SBMLQual processor

    """
    def sbmlqual_biorecipe(self, input_file, output_file):
        """translate SBMLQual XML file to BioRECIPE format

        :param str input_file: the filename of the SBMLQual
        :param str output_file: the filename of the translated BioRECIPE

        SBMLQual XML file was downloaded from https://cellcollective.org/#
        """

        # initialize a model dataframe in BioRECIPE format
        biorecipe_df = pd.DataFrame(columns=model_cols)

        # XML.etree has some issues of parsing the SBMLQual XML file. BeautifulSoup loses the upper cases while reading
        res = bs4.BeautifulSoup(open(input_file).read(), 'lxml')

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

            biorecipe_df = biorecipe_df.append(new_row, ignore_index=True)
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

        biorecipe_df.to_excel(output_file, index=False)

    def _get_reaction_from_mathml(self, contents):
        # TODO: we assume sop here

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

def sbmlqual_to_biorecipe(input, output):
    sbml_qual = SBMLQual()
    sbml_qual.sbmlqual_biorecipe(input, output)
    print("Finished: {0}".format(output))

def main():
    parser = argparse.ArgumentParser()

    # required arguments
    required_args = parser.add_argument_group('required input arguments')

    required_args.add_argument('-i', '--input', type=str, required=True,
                               help='Path of the input file (.xml)')
    required_args.add_argument('-o', '--output', type=str, required=True,
                               help='Path of the output file (.xlsx)')

    args = parser.parse_args()
    sbmlqual_to_biorecipe(args.input, args.output)
    # casq.map_to_model(args.input, args.output)

if __name__ == "__main__":
    main()
