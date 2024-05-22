import argparse
from translators.indra_engine.to_from import get_INDRAstmts_from_biorecipeI

def main():
    parser = argparse.ArgumentParser()

    # required arguments
    required_args = parser.add_argument_group('required input arguments')

    required_args.add_argument('-i', '--input', type=str, required=True,
                               help='Path of the input BioRECIPE interaction lists file (.xlsx)')
    required_args.add_argument('-o', '--output', type=str, required=True,
                               help='Path of the output json file (.json)')

    args = parser.parse_args()
    get_INDRAstmts_from_biorecipeI(args.input, args.output)

if __name__ == "__main__":
    main()