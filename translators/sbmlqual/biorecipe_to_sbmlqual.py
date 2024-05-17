# -*- coding: utf-8 -*-
#
# This file is part of translator for BioRECIPE format.
#
# __author__ = "Difei Tang"
# __email__ = "DIT18@pitt.edu"

# To use this translator directly in terminal
# import sys, os
# sys.path.insert(0, os.path.abspath(os.path.join(os.getcwd(), os.pardir)))
# python biorecipe_to_sbmlqual.py --input [BioRECIPE] --output [SBMLQual] --input_format [model/interactions]

# where you need to have the terminal work in the directory of this python script
# [BioRECIPE] is the model/interactions in BioRecipes format
# and [SBMLQual] is the path and name of generated SBMLQual file

import pandas as pd
import re
import argparse
from sympy import symbols, And, Or, Not, printing
from sympy.printing.mathml import mathml
from sbmlqual.sbml import SBML #offline import of code /sbml.py and /sbmlqual.py from https://github.com/cellnopt/cellnopt/tree/master/cno/io
from sbmlqual.sbmlqual import QualitativeSpecies, ListOfTransitions, Transition, ListOfInputs, ListOfOutputs, ListOfFunctionTerms, FunctionTerm
from within_biorecipe.biorecipe_std import get_model
from within_biorecipe.md_and_int import interactions_to_model

__all__ = ["SBMLQual_rcp"]

class SBMLQual_rcp(object):

    """
    Class to write SBML-qual file (from BioRECIPE logical models only)
    """

    def __init__(self):
        self.and_symbol = "^"

    def to_sbmlqual_interactions(self, input_file, filename):

        """
        Exports BioRECIPE interaction lists to SBMLqual format, returns the SBML text
        This is a level3, version 1 exporter.

        """

        biorecipe_interactions_df = pd.read_excel(input_file)
        biorecipe_model_df = interactions_to_model(biorecipe_interactions_df)
        biorecipe_model_df = biorecipe_model_df.set_index('Element Name')
        biorecipe_dict = biorecipe_model_df.to_dict(orient='index')

        s = SBML(self, version="1", model_name='model')

        sbml = s.create_header()
        sbml += s.create_model_name()
        sbml += s.create_compartment(id="main", constant="true")

        # Starting list of transitions
        list_of_transition = ListOfTransitions()
        sbml += list_of_transition.open()

        # add the qualitativeSpecies list
        qualitativeSpecies = QualitativeSpecies(list(biorecipe_dict.keys()))
        sbml += qualitativeSpecies.create()

        # Loop over all transitions
        tid = 0
        for ele, value in biorecipe_dict.items():

            identifier = "t{0}".format(ele)

            pos = value['Positive Regulator List']
            neg = value['Negative Regulator List']

            regulators = {'+': None, '-': None}

            if pos and type(pos) == str:
                regulators['+'] = pos.split(',')

            if neg and type(neg) == str:
                regulators['-'] = neg.split(',')

            # regulators found and create a Transition for a regulated element
            transition = Transition(identifier)
            sbml += transition.open()

            # regulators -> list of inputs
            list_of_inputs = ListOfInputs(regulators, ele)
            if not list_of_inputs.species['+']:
                list_of_inputs.species['+']=''
            if not list_of_inputs.species['-']:
                list_of_inputs.species['-']=''
            sbml += list_of_inputs.create()

            # regulated -> the output (only one)
            list_of_outputs = ListOfOutputs(ele)
            sbml += list_of_outputs.create()

            sbml += transition.close()

        # The end
        sbml += list_of_transition.close()
        sbml += """</model>\n"""
        sbml += s.create_footer()

        with open(filename, 'w') as f:
            f.write(sbml)

    def to_sbmlqual(self, input_file, filename):

        """
        Exports BioRECIPE model to SBMLqual format, returns the SBML text
        This is a level3, version 1 exporter.

        """

        biorecipe_model = get_model(input_file)
        biorecipe_dict = biorecipe_model.to_dict(orient='index')

        s = SBML(self, version="1", model_name='model')

        sbml = s.create_header()
        sbml += s.create_model_name()
        sbml += s.create_compartment(id="main", constant="true")

        # Starting list of transitions
        list_of_transition = ListOfTransitions()
        sbml += list_of_transition.open()

        # add the qualitativeSpecies list
        qualitativeSpecies = QualitativeSpecies(list(biorecipe_dict.keys()))
        sbml += qualitativeSpecies.create()

        # Loop over all transitions
        tid = 0
        for ele, value in biorecipe_dict.items():

            identifier = "t{0}".format(ele)

            pos_rule = value['Positive Regulation Rule']
            neg_rule = value['Negative Regulation Rule']

            regulators = {'+': None, '-': None}

            if pos_rule or neg_rule:

                reg_mathml = ""
                if pos_rule and neg_rule:
                    reg_expr = get_score_logic_expr(pos_rule, neg_rule)
                    reg_mathml = mathml(reg_expr)
                else:
                    if pos_rule:
                        pos_converter = MATH_CONVERTER(pos_rule)
                        regulators['+'] = pos_converter.regulator_list
                        reg_mathml = pos_converter.convert2mathml()
                    elif neg_rule:
                        neg_converter = MATH_CONVERTER(neg_rule)
                        regulators['-'] = neg_converter.regulator_list
                        reg_mathml = neg_converter.convert2mathml()
                    else:
                        raise ValueError('unable to parse regulation rules')

                # regulators found and create a Transition for a regulated element
                transition = Transition(identifier)
                sbml += transition.open()

                # regulators -> list of inputs
                list_of_inputs = ListOfInputs(regulators, ele)
                if not list_of_inputs.species['+']:
                    list_of_inputs.species['+']=''
                if not list_of_inputs.species['-']:
                    list_of_inputs.species['-']=''
                sbml += list_of_inputs.create()

                # regulated -> the output (only one)
                list_of_outputs = ListOfOutputs(ele)
                sbml += list_of_outputs.create()

                sbml += transition.close()

                # start creating functionTerms
                list_of_function_terms = ListOfFunctionTerms()

                sbml += list_of_function_terms.open()
                sbml += list_of_function_terms.create_default_term()

                function_term = FunctionTerm()
                sbml += function_term.open()

                # map logic functions to mathml and add to functionTerms
                sbml +=  """<math xmlns="http://www.w3.org/1998/Math/MathML">"""

                sbml += reg_mathml

                sbml += "</math>"
                sbml += function_term.close()
                sbml += list_of_function_terms.close()

        # The end
        sbml += list_of_transition.close()
        sbml += """</model>\n"""
        sbml += s.create_footer()

        with open(filename, 'w') as f:
            f.write(sbml)


class MATH_CONVERTER:
    """
    This is a conversion from regulation rule to SymPy logical expression.
    Logical expression can be exported to mathml
    """

    def __init__(self, rule):
        self.reg_rule = rule
        if all(operator not in self.reg_rule for operator in [',','(', ')']): self.regulator_list = [rule.strip()]
        else: self.regulator_list = [reg.strip() for reg in set(self.get_element(self.reg_rule, 0))]
        self.symbol_list = symbols(' '.join(self.regulator_list))

    def get_symbol_by_index(self,name):
        if name[0] == '!':
            name = name.replace('!', '')
        else:
            pass
        if len(self.regulator_list) == 1:
            symbol_name = self.symbol_list
        else:
            symbol_name = self.symbol_list[self.regulator_list.index(name)]
        return symbol_name

    def split_comma_out_parentheses(self, reg_rule):
        reg_list = list()
        parentheses = 0
        start = 0
        for index, char in enumerate(reg_rule):
            if index == len(reg_rule) - 1:
                reg_list.append(reg_rule[start:index + 1])
            elif char == '(' :
                parentheses += 1
            elif char == ')' :
                parentheses -= 1
            elif (char == ',' and parentheses == 0):
                if reg_rule[start] == ' ':
                    reg_list.append(reg_rule[start+1:index])
                else:
                    reg_list.append(reg_rule[start:index])
                start = index + 1
        return reg_list

    def funct(self, reg_list):
        if type(reg_list) != list: reg_list = [reg_list]
        else: pass
        if len(reg_list) == 1:
            if all(parentheses not in reg_list[0] for parentheses in ['(', ')']):
                reg_expr = reg_list[0]
                expr = self.get_symbol_by_index(reg_list[0])
                if reg_expr[0] == '!':
                    return Not(expr)
                else:
                    return expr
            else:
                expr_list = self.split_comma_out_parentheses(''.join(reg_list[0])[1:-1])
                return And(self.funct(expr_list[0]), self.funct(expr_list[1]))

        elif len(reg_list) == 2:
            if all(parentheses not in reg_list[0] for parentheses in ['(', ')']) and \
                    all(parentheses not in reg_list[1] for parentheses in ['(', ')']):
                return Or(self.get_symbol_by_index(reg_list[0]), self.get_symbol_by_index((reg_list[1])))

            elif all(parentheses not in reg_list[0] for parentheses in ['(', ')']) and \
                    any(parentheses in reg_list[1] for parentheses in ['(', ')']):
                if '!' in reg_list[1]:
                    return Or(self.get_symbol_by_index(reg_list[0]), Not(self.funct(reg_list[1])))
                else:
                    return Or(self.get_symbol_by_index(reg_list[0]), self.funct(reg_list[1]))

            elif any(parentheses in reg_list[0] for parentheses in ['(', ')']) and \
                    all(parentheses not in reg_list[1] for parentheses in ['(', ')']):
                if '!' in reg_list[0]:
                    return Or(Not(self.funct(reg_list[0])), self.get_symbol_by_index(reg_list[1]))
                else:
                    return Or(self.funct(reg_list[0]), self.get_symbol_by_index(reg_list[1]))

            else:
                return Or(self.funct(reg_list[0]), self.funct(reg_list[1]))

        elif len(reg_list) >= 3:
            return Or(self.funct(reg_list[0]), self.funct(reg_list[1:]))

    def convert2logic(self):
        if any(operator_i in self.reg_rule for operator_i in ['[', '{', '^', '=', '+', '~']):
            raise ValueError(
                'Can only translate logical model, other models will be updated soon...'
            )
        else:
            reg_list = self.split_comma_out_parentheses(self.reg_rule)
            expr = self.funct(reg_list)
            return expr

    def convert2mathml(self):
        logic_expr = mathml(self.convert2logic())
        return logic_expr

    def get_element(self, reg_rule, layer):
        """Convert a regulation rule to a regulator list
        """
        if reg_rule:
            regulator_list = []

            if '+' not in reg_rule:
                reg_list = self.split_comma_out_parentheses(reg_rule)
            else:
                if ',' in reg_rule:
                    raise ValueError(
                        'Found mixed commas and plus sign in regulation function'
                    )
                elif reg_rule[-1] == '+':
                    raise ValueError(
                        'Regulation rule is not correct'
                    )
                else:
                    reg_list = reg_rule.split('+')

            for reg_element in reg_list:
                if reg_element[0] == '{' and reg_element[-1] == '}':
                    assert (layer == 0)
                    if '*' in reg_element:
                        weight, name = reg_element[1:-1].split('*')
                        regulator_list = regulator_list + self.get_element(name, 1)
                    else:
                        regulator_list = regulator_list + self.get_element(reg_element, 1)

                elif reg_element[0] == '{' and reg_element[-1] == ']':
                    # This is a necessary pair
                    # check the point between {} and []
                    parentheses = 0
                    cutpoint = 0
                    for index, char in enumerate(reg_element):
                        if char == '{':
                            parentheses += 1
                        elif char == '}':
                            parentheses -= 1

                        if parentheses == 0:
                            cutpoint = index
                            break

                    necessary_element = reg_element[1: cutpoint]
                    enhence_element = reg_element[cutpoint + 2:-1]
                    if '*' in necessary_element:
                        weight, name = necessary_element.split('*')
                        regulator_list = regulator_list + self.get_element(name, 1)
                    else:
                        regulator_list = regulator_list + self.get_element(necessary_element, 1)

                    if '*' in necessary_element:
                        weight, name = necessary_element.split('*')
                        regulator_list = regulator_list + self.get_element(name, 1)
                    else:
                        regulator_list = regulator_list + self.get_element(necessary_element, 1)

                elif reg_element[0] == '(' and reg_element[-1] == ')':
                    list = [element for ele_list in self.split_comma_out_parentheses(reg_element[1:-1]) \
                            for element in self.get_element(ele_list, 1)]
                    regulator_list += list
                else:

                    if reg_element[-1] == '^':
                        regulator_list.append(reg_element[0:-1])
                    elif '&' in reg_element:
                        regulator_list.append(reg_element[1:-1])
                    elif '*' in reg_element:
                        multiply_reg_list = reg_element.split('*')
                        for reg_ in multiply_reg_list:
                            if not re.search(r'[a-zA-Z0-9\ !]]+', reg_):
                                pass
                            else:
                                regulator_list.append(reg_)
                    elif reg_element[0] == '!':
                        if '~' in reg_element[1:]:
                            delay, reg_delay = reg_element[1:].split('~')
                            regulator_list.append(reg_delay)
                        else:
                            regulator_list.append(reg_element[1:])

                    elif '=' in reg_element:
                        name, target_state = reg_element.split('=')
                        regulator_list.append(target_state)
                    elif '~' in reg_element:
                        delay, state = reg_element.split('~')
                        regulator_list.append(state)

                    else:
                        regulator_list.append(reg_element)

            return regulator_list

def get_score_logic_expr(pos_rule:str, neg_rule:str):
    """
    This is a function convert string to logic expression. To be noticed, the string should not contain 'space' nearby parentheses
    :param pos_rule:
    :param neg_rule:
    :return: logic expression
    """
    pos_expr = MATH_CONVERTER(pos_rule).convert2logic()
    neg_expr = MATH_CONVERTER(neg_rule).convert2logic()
    return Or(pos_expr, Not(neg_expr))

def get_sbmlqual_from_biorecipeM(input, output):
    sbmlqualRCP = SBMLQual_rcp()
    sbmlqualRCP.to_sbmlqual(input, output)

def get_sbmlqual_from_biorecipeI(input, output):
    sbmlqualRCP = SBMLQual_rcp()
    sbmlqualRCP.to_sbmlqual_interactions(input, output)

def main():
    parser = argparse.ArgumentParser(
        description='Process BioRECIPE model/interaction file and convert to SBMLQual.',
        formatter_class=argparse.RawTextHelpFormatter)

    parser.add_argument('--input_file', type=str, help='Path and name of input model/interaction file (.xlsx)')
    parser.add_argument('--output_file', type=str, help='Path and name of output sbmlqual file (.xml)')
    parser.add_argument('--input_format', type=str, choices=['model','interactions'],
        default='model',
        help='Input file format \n'
        '\t model (default): BioRECIPE model format \n'
        '\t interactions: BioRECIPE interaction format \n')

    args = parser.parse_args()
    if args.input_format == 'model':
        get_sbmlqual_from_biorecipeM(args.input_file, args.output_file)
    elif args.input_format == 'interactions':
        get_sbmlqual_from_biorecipeI(args.input_file, args.output_file)

if __name__ == "__main__":
    main()
