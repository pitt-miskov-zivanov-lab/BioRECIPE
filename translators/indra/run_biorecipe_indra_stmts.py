# -*- coding: utf-8 -*-
#
# This file is a part of INDRA translator for BioRECIPE format.
#
# __author__ = "Difei Tang"
# __email__ = "DIT18@pitt.edu"

import argparse
from translators.indra.api import biorecipe_to_indra

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

