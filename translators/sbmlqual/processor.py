# -*- python -*-
#
#  This file is part of the cinapps.tcell package
#
#  Copyright (c) 2012-2013 - EMBL-EBI
#
#  File author(s): Thomas Cokelaer (cokelaer@ebi.ac.uk)
#
#  Distributed under the GLPv3 License.
#  See accompanying file LICENSE.txt or copy at
#      http://www.gnu.org/licenses/gpl-3.0.html
#
#  website: www.cellnopt.org
#
#  Updated by Difei Tang for BioRECIPE translation
##############################################################################
from __future__ import print_function

__all__ = ["SBML"]

import pandas as pd


class SBMLReader(object):
    def __init__(self, filename):
        self.filename = filename

class SBMLWrite(object):
    def __init__(self, filename):
        self.filename = filename


class SBML(object):
    """Creates SBMLQual file given

    sbml = SBML(c, model_name="test")
    note = sbml.create_note()
    vcard = sbml.create_vcard("john", "smith")
    annotation = sbml.create_annotation(vcards = [vcard])


    """
    def __init__(self, data, version="1", model_name=None, xmlversion="1.0"):
        """Note that version are integer but xmlversion can be X.Y"""
        self.data = data # ! a reference
        self.annotation = None
        self.note = None
        self.version = version
        self.xmlversion = xmlversion
        self.header = None
        self.footer = None
        self.model_name = None

    def create_header(self):
        header = """<?xml version='%s' encoding='UTF-8' standalone='no'?>
<sbml xmlns="http://www.sbml.org/sbml/level3/version1/core" qual:required="true" level="3"
xmlns:qual="http://www.sbml.org/sbml/level3/version1/qual/version1"
version="%s">""" % (self.xmlversion, self.version)
        self.header = header
        return header

    def create_model_name(self):
        self.model = """<model id="%s"> """ % self.model_name
        return self.model

    def create_compartment(self, constant="true", id="main"):
        self.compartment = """
     <listOfCompartments>
       <compartment id="%s" constant="%s">
       </compartment>
     </listOfCompartments>\n""" %(id, constant)
        return self.compartment

    def create_footer(self):
        self.footer = "</sbml>"
        return self.footer

    def create_note(self, htmlcode ):
        text = """
  <notes>...
    <body xmlns="http://www.w3.org/1999/xhtml">
      %s
    </body>
  </notes>""" % htmlcode
        self.note = text
        return text

    def create_vcard(self, firstname, lastname, organism="", email=""):
        params = {
            'firstname':firstname, 'lastname':lastname,
            'organism':organism, 'email':email}

        vcard = """
              <rdf:li rdf:parseType="Resource">
                <vCard:N rdf:parseType="Resource">
                  <vCard:Family>%(lastname)s</vCard:Family>
                  <vCard:Given>%(firstname)s</vCard:Given>
                </vCard:N>
                <vCard:EMAIL>%(email)s</vCard:EMAIL>
                <vCard:ORG rdf:parseType="Resource">
                  <vCard:Orgname>%(organism)s</vCard:Orgname>
                </vCard:ORG>
              </rdf:li>""" % params
        return vcard

    def create_annotation(self, vcards=None):
        """

        """

        if vcards == None:
            raise ValueError("you must provided a list of vcards to fill the annotation")

        text = """
  <annotation>
   <rdf:RDF xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"
            xmlns:dc="http://purl.org/dc/elements/1.1/"
            xmlns:vCard="http://www.w3.org/2001/vcard-rdf/3.0#">

    <rdf:Description rdf:about="my_metaid">
        <dc:creator>
            <rdf:Bag>\n"""

        for vcard in vcards:
            text += vcard + "\n"

        text += """
            </rdf:Bag>
          </dc:creator>
    </rdf:Description>
   </rdf:RDF>
  </annotation>\n"""
        self.annotation = text
        return text

from translators.sbmlqual.mathml_translator import MATH_CONVERTER, get_score_logic_expr, get_score_mathml
import xml.etree.ElementTree as ET
import lxml
from translators.utils import get_model, model_to_dict, interactions_to_model

__all__ = ["SBMLQual"]

name = ['Akt', 'CD4']

class SBMLQual(object):
    """Class to write SBML-qual file (logical models only)
    """
    def __init__(self):
        self.and_symbol = "^"

    def to_sbmlqual_interactions(self, input_file, filename):
        """Exports BioRECIPE interaction lists to SBMLqual format.

        :return: the SBML text
        This is a level3, version 1 exporter.

        """

        biorecipe_interactions = pd.read_excel(input_file)
        biorecipe_model = interactions_to_model(biorecipe_interactions)
        biorecipe_dict = model_to_dict(biorecipe_model)

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
        """Exports BioRECIPE model to SBMLqual format.

        :return: the SBML text
        This is a level3, version 1 exporter.

        """

        biorecipe_model = get_model(input_file)
        biorecipe_dict = model_to_dict(biorecipe_model)

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
                    reg_mathml = get_score_mathml(reg_expr)
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


# SBML-qual classes for logical modelling
class Qual(object):
    version = "http://www.sbml.org/sbml/level3/version1/qual/version1"

    def __init__(self, tag, xmlns=False):
        self.tag = tag
        self.xmlns = xmlns
        self.open_attribute = {}
        self.indent = ""
        #self.version = '1'

    def open(self):
        if self.xmlns is False:
            txt = """<qual:{0}""".format(self.tag)
            for k,v in self.open_attribute.items():
                txt+= """ qual:{0}="{1}" """.format(k,v) # note the space before 'qual'
            txt += ">\n"
        else:
            txt = """<qual:{0} xmlns:qual="{1}">""".format(self.tag, self.version)
        txt += "\n"
        return txt

    def close(self):
        return """</qual:{0}>\n""".format(self.tag)

    def indentation(self, sbml):
        sbml = "".join([self.indent + x for x in sbml.split("\n")])
        return sbml

class QualitativeSpecies(Qual):
    def __init__(self, species):
        super(QualitativeSpecies, self).__init__("listOfQualitativeSpecies", xmlns=True)
        self.species = species
        self.compartment = 'main'
        self.constant = 'false'

    def add_species(self, name):
        sbml = """<qual:qualitativeSpecies """
        sbml += """qual:constant="{0}" """.format(self.constant)
        sbml += """qual:compartment="{0}" """.format(self.compartment)
        sbml += """qual:id="{0}"/>\n""".format(name)
        # id or name??
        return sbml

    def close(self):
        return """</qual:{0}>\n""".format(self.tag)

    def create(self):
        sbml = self.open()
        for name in self.species:
            if "^" not in name:
                sbml += self.add_species(name)
        sbml += self.close()
        sbml = self.indentation(sbml)
        return sbml

class ListOfTransitions(Qual):
    def __init__(self):
        super(ListOfTransitions, self).__init__("listOfTransitions", xmlns=True)

class Transition(Qual):
    """A transition contains at most one ListOfOnputs and one ListofOutputs and
    exactly one ListOfFunctionTerms
    """
    def __init__(self, identifier):
        super(Transition, self).__init__("transition")
        self.identifier = identifier
        self.open_attribute = {'id':self.identifier}

class ListOfInputs(Qual):
    """The ListOfInputs contains at least one element of type Input.

    The input parameter **species** is a dictionay with keys + and - containing list
    of species in each category. A species could be in both categories.

    """
    def __init__(self, species, identifier):
        super(ListOfInputs, self).__init__("listOfInputs")
        self.species = species
        self.identifier = identifier
        assert '+' in self.species.keys()
        assert '-' in self.species.keys()
        self.threshold = 1
        self.transitionEffect = 'none'

    def create(self):
        txt = self.open()

        # positive and then negative:
        prefix = """<qual:input qual:thresholdLevel="{0}" """.format(self.threshold)
        prefix += """ qual:transitionEffect="{0}" """.format(self.transitionEffect)
        if self.species['+']:
            for name in self.species['+']:
                txt += prefix
                txt += """ qual:sign="positive" """
                txt += """ qual:qualitativeSpecies="{0}" """.format(name)
                txt += """ qual:id="theta_{0}_{1}"/>""".format(self.identifier, name)
        if self.species['-']:
            for name in self.species['-']:
                txt += prefix
                txt += """ qual:sign="negative" """
                txt += """ qual:qualitativeSpecies="{0}" """.format(name)
                txt += """ qual:id="theta_{0}_{1}"/>""".format(self.identifier, name)

        txt += self.close()
        return txt

class ListOfOutputs(Qual):
    """In logical model, there is only one output

    * thresholdLevel is set to 1
    * transitionEffect is set to assignmentLevel
    """
    def __init__(self, node):
        super(ListOfOutputs, self).__init__('listOfOutputs')
        self.name = node

    def create(self):
        txt = self.open()
        txt += """<qual:output """
        txt += """ qual:transitionEffect="assignmentLevel" """
        txt += """ qual:qualitativeSpecies="{0}"/>\n""".format(self.name)
        txt += self.close()
        return txt

class ListOfFunctionTerms(Qual):
    """
    contains 1 default terms and any number of function terms
    """
    def __init__(self):
        super(ListOfFunctionTerms, self).__init__('listOfFunctionTerms')

    def create_default_term(self):
        default = DefaultTerm()
        return default.create()

class FunctionTerm(Qual):
    """associated with a result and to a boolean function inside a math element
    that can be used to set the conditions inder which this term is selected
    """
    def __init__(self):
        super(FunctionTerm, self).__init__('functionTerm')
        self.open_attribute = {'resultLevel': '1'}

class DefaultTerm(Qual):
    """resultLevel is set to 0"""
    def __init__(self):
        super(DefaultTerm, self).__init__('defaultTerm')
        self.open_attribute = {'resultLevel': 0}

    def create(self):
        txt = self.open()
        txt += self.close()
        return txt




