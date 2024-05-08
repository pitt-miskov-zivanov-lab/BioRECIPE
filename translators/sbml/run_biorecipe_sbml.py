import argparse
from processor import write_sbml

def biorecipe_to_sbml(input, output):
    write_sbml(input, output)
    print("Finished: {0}".format(output))

def main():
    parser = argparse.ArgumentParser()

    # required arguments
    required_args = parser.add_argument_group('required input arguments')

    required_args.add_argument('-i', '--input', type=str, required=True,
                               help='Path of the input BioRECIPE interaction lists file (.xlsx)')
    required_args.add_argument('-o', '--output', type=str, required=True,
                               help='Path of the output SBML file (.xml)')

    args = parser.parse_args()
    biorecipe_to_sbml(args.input, args.output)

if __name__ == "__main__":
    main()