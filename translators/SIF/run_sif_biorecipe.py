
import argparse
from translators.SIF.api import sif_to_biorecipeI

def main():
    parser = argparse.ArgumentParser()

    # required arguments
    required_args = parser.add_argument_group('required input arguments')

    required_args.add_argument('-i', '--input', type=str, required=True,
                               help='Path of the input SIF file (.sif)')
    required_args.add_argument('-o', '--output', type=str, required=True,
                               help='Path of the output BioRECIPE interaction lists file (.xlsx)')

    args = parser.parse_args()
    sif_to_biorecipeI(args.input, args.output)

if __name__ == "__main__":
    main()

