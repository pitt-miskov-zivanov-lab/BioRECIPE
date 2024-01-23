import argparse
import celldesigner2qual as casq

def main():
    parser = argparse.ArgumentParser()

    # required arguments
    required_args = parser.add_argument_group('required input arguments')

    required_args.add_argument('-i', '--input', type=str, required=True,
                               help='Path of the input file (.xml)')
    required_args.add_argument('-o', '--output', type=str, required=True,
                               help='Path of the output file (.xlsx)')

    args = parser.parse_args()

    casq.map_to_model(args.input, args.output)

if __name__ == "__main__":
    main()