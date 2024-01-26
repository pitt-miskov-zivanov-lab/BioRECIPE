# -*- coding: utf-8 -*-
#
# This file is a part of INDRA translator for BioRECIPE format.
#
# __author__ = "Difei Tang"
# __email__ = "DIT18@pitt.edu"

import argparse
from processor import INDRA

def biorecipe_to_indra(input, output):
    indra = INDRA()
    indra.biorecipeI_stmts(input, output)
    print("Finished: {0}".format(output))

def main():
    parser = argparse.ArgumentParser()

    # required arguments
    required_args = parser.add_argument_group('required input arguments')

    required_args.add_argument('-i', '--input', type=str, required=True,
                               help='Path of the input BioRECIPE interaction lists file (.xlsx)')
    required_args.add_argument('-o', '--output', type=str, required=True,
                               help='Path of the output json file (.json)')

    args = parser.parse_args()
    biorecipe_to_indra(args.input, args.output)

if __name__ == "__main__":
    main()

