# This is a part of SBMLqual translator

import pandas as pd
#import libsbml
import re
from sympy import *
from sympy import symbols
from sympy.printing.mathml import mathml

class MATH_CONVERTER:
    """
    This is a conversion from regulation rule to SymPy logical expression.
    Logical expression can be exported to mathml
    """

    def __init__(self, rule):
        self.reg_rule = rule
        self.regulator_list = [reg.strip() for reg in set(self.get_element(self.reg_rule, 0))]
        self.symbol_list = symbols(' '.join(self.regulator_list))

    def get_symbol_by_index(self,name):
        if name[0] == '!':
            name = name.replace('!', '')
        else:
            pass
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

def get_score_mathml(score_expr):
    return mathml(score_expr)

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    ### test
    reg_expr = get_score_logic_expr('(AKt,CD4),(DDB,(!KD3,ERK))', '(Akt,CD28),(DDB,AKT)')
    reg_mathml = get_score_mathml(reg_expr)
    print(reg_expr)
    print_mathml(reg_expr)