import argparse
from processor import SIF

def biorecipeM_to_sbmlqual(input, output):
    sbml_qual = SIF()
    sbml_qual.biorecipeM_sif(input, output)
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
    biorecipeM_to_sbmlqual(args.input, args.output)

if __name__ == "__main__":
    main()

