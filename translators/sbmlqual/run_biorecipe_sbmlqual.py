import argparse
from processor import SBMLQual

def biorecipe_to_sbmlqual(input, output):
    sbml_qual = SBMLQual()
    sbml_qual.to_sbmlqual(input, output)
    print("Finished: {0}".format(output))

def main():
    parser = argparse.ArgumentParser()

    # required arguments
    required_args = parser.add_argument_group('required input arguments')

    required_args.add_argument('-i', '--input', type=str, required=True,
                               help='Path of the input BioRECIPE model file (.xlsx)')
    required_args.add_argument('-o', '--output', type=str, required=True,
                               help='Path of the output file (.xml)')

    args = parser.parse_args()
    biorecipe_to_sbmlqual(args.input, args.output)

if __name__ == "__main__":
    main()