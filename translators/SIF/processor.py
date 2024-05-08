# -*- coding: utf-8 -*-
#
# This file is a part of translator for BioRECIPE format.
#
# __author__ = "Difei Tang", "Emilee Holtzapple"
# __email__ = "DIT18@pitt.edu"

import sys
sys.path.append("..")

import networkx as nx
import pandas as pd
import re
from translators.utils import get_model, model_to_networkx, biorecipe_reading_col

class SIF():
    """SBMLQual processor
    """

    # def biorecipeM_sif(self, input_file, output_file):
    #     """Translate BioRECIPE model to SIF"""
    #     df_model = get_model(input_file)
    #     graph = model_to_networkx(df_model)
    #
    #     self.write_sif(output_file, graph)

    # def write_sif(self, sbml_filename: str, graph: nx.DiGraph):
    #     """Write a SIF file.
    #
    #     http://www.cbmc.it/fastcent/doc/SifFormat.htm
    #     """
    #     with open(sbml_filename, "w", encoding="utf-8", newline="") as f:
    #
    #         for source, target, sign in graph.edges.data("interaction"):
    #             print(
    #                 source.replace(" ", "_"),
    #                 sign.upper(),
    #                 target.replace(" ", "_"),
    #                 file=f,
    #             )

    def biorecipeM_sif(self, infile, outfile):
        """Translate BioRECIPE model to SIF"""

        df = pd.read_excel(infile, dtype=">U50", keep_default_na=False)

        rules = df[['Variable', 'Positive Regulation Rule', 'Negative Regulation Rule', 'Element Type']]

        rulesMat = rules.values

        with open(outfile, 'w+') as ofile:

            for r in rulesMat:

                if (r[1]):

                    r[1] = r[1].replace('[', ",")
                    tmp1 = str(r[1])
                    tmp2 = re.sub(r'[\[{}()\]]', '', tmp1)
                    tmp3 = re.sub(r'.\*', '', tmp2)
                    tmp4 = re.sub(r'\^', '', tmp3)
                    tmp5 = re.sub(r'=\d\b', '', tmp4)
                    regs = re.split(',', tmp5)

                    for nm in regs:

                        if (nm.find("!") == -1):

                            ofile.write(str(r[0].strip()) + "\t" + nm.strip() + '\t' + 'POSITIVE')

                        else:
                            ofile.write(str(r[0].strip()) + "\t" + str(nm.replace("!", '').strip()) + '\t' + 'NEGATIVE')

                        ofile.write("\t")
                        ofile.write(r[3])
                        ofile.write("\t")
                        ofile.write('\n')

                if (r[2]):

                    r[2] = r[2].replace('[', ",")
                    tmp1 = str(r[2])
                    tmp2 = re.sub(r'[\[{}()\]]', '', tmp1)
                    tmp3 = re.sub(r'.\*', '', tmp2)
                    tmp4 = re.sub(r'\^', '', tmp3)
                    tmp5 = re.sub(r'=\d\b', '', tmp4)
                    regs = re.split(',', tmp5)

                    for nm in regs:

                        if (nm.find("!") == -1):

                            ofile.write(str(r[0].rstrip()) + "\t" + nm.strip() + '\t' + 'NEGATIVE')

                        else:
                            ofile.write(
                                str(r[0].rstrip()) + "\t" + str(nm.replace("!", '').strip()) + '\t' + 'POSITIVE')

                        ofile.write("\t")
                        ofile.write(r[3])
                        ofile.write("\t")
                        ofile.write('\n')

                if (r[1] == '' and r[2] == ''):
                    ofile.write(str(r[0].rstrip()) + "\t\t\t")
                    ofile.write(r[3])
                    ofile.write("\t")
                    ofile.write('\n')

        ofile.close()

    def biorecipeI_sif(self, infile, outfile):
        """Translate BioRECIPE model to SIF"""
        df = pd.read_excel(infile, dtype=">U50", keep_default_na=False)

        reading_df = df[['Regulator Name', 'Regulated Name', 'Regulated Type', 'Sign']]
        with open(outfile, 'w+') as ofile:
            for i in range(len(reading_df)):
                r = df.loc[i, 'Regulated Name']
                nm = df.loc[i, 'Regulator Name']
                sign = df.loc[i, 'Sign']
                rtype = df.loc[i, 'Regulated Type']

                ofile.write(str(r.rstrip()) + "\t" + nm.strip() + '\t' + sign.upper())

                ofile.write("\t")
                ofile.write(rtype)
                ofile.write("\t")
                ofile.write('\n')


    def sif_biorecipeI(self, input_file, output_file):
        """Translate SIF to BioRECIPE interaction lists """

        df = pd.read_csv(input_file, sep="\t", header=None, keep_default_na=False)
        output_df = pd.DataFrame(columns=biorecipe_reading_col)

        row = 0
        for i in range(len(df)):
            s = df.loc[i, 0]
            t = df.loc[i, 1]
            sign = df.loc[i, 2]
            type = df.loc[i, 3]

            if not t:
                continue
            elif sign:
                output_df.loc[row, 'Regulator Name'] = s
                output_df.loc[row, 'Regulated Name'] = t
                output_df.loc[row, 'Regulated Type'] = type
                output_df.loc[row, 'Sign'] = sign.lower()
                row += 1
            else:
                raise ValueError("Empty value for relationType")

        with pd.ExcelWriter(output_file) as writer:
            output_df.to_excel(writer, index=False)