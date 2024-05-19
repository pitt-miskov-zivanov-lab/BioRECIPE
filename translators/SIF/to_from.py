# -*- coding: utf-8 -*-
#
# This file is a part of translator for BioRECIPE format.

# To use this translator directly in terminal
# import sys, os
# sys.path.insert(0, os.path.abspath(os.path.join(os.getcwd(), os.pardir)))
# python to_from.py --input [input_file] --output [output_file] --input_format [model/interactions/sif]

# __author__ = "Difei Tang", "Emilee Holtzapple"
# __email__ = "DIT18@pitt.edu"

import argparse
import pandas as pd
import re
from within_biorecipe.biorecipe_std import biorecipe_int_cols

class SIF():

    """
    SBMLQual processor
    """

    def biorecipeM_sif(self, infile, outfile):

        """
        Translate BioRECIPE model to SIF
        """

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

        """
        Translate BioRECIPE model to SIF
        """

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

        """
        Translate SIF to BioRECIPE interaction lists
        """

        df = pd.read_csv(input_file, sep="\t", header=None, keep_default_na=False)
        output_df = pd.DataFrame(columns=biorecipe_int_cols)

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

def get_sif_from_biorecipeM(input, output):
    sif = SIF()
    sif.biorecipeM_sif(input, output)

def get_sif_from_biorecipeI(input, output):
    sif = SIF()
    sif.biorecipeI_sif(input, output)

def get_biorecipeI_from_sif(input, output):
    sif = SIF()
    sif.sif_biorecipeI(input, output)

def main():

    parser = argparse.ArgumentParser(
        description='Convert between BioRECIPE model/interaction file and SIF format',
        formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('--input_file', type=str,
        help='Path and name of input file')
    parser.add_argument('--output_file', type=str,
        help='Path and name of output file')
    parser.add_argument('--input_format', '-i', type=str, choices=['model','interactions', 'sif'],
        default='model',
        help='Input file format \n'
        '\t model (default): BioRECIPE model format, output will be sif \n'
        '\t interactions: BioRECIPE interaction format, output will be sif \n'
        '\t sif: sif format, output will be BioRECIPE interaction format \n'
        )

    args = parser.parse_args()
    if args.input_format == 'model':
        get_sif_from_biorecipeM(args.input_file, args.output_file)
    elif args.input_format == 'interactions':
        get_sif_from_biorecipeI(args.input_file, args.output_file)
    elif args.input_format == 'sif':
        get_biorecipeI_from_sif(args.input_file, args.output_file)

if __name__ == "__main__":
    main()
