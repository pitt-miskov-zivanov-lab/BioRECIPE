import argparse
from translators.sbmlqual.api import biorecipeM_to_sbmlqual, biorecipeI_to_sbmlqual

def main():
    parser = argparse.ArgumentParser(
        description='Process BioRECIPE model/interaction lists file and convert to SBMLQual.',
        formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('input_file', type=str,
        help='Input file name')
    parser.add_argument('output_file', type=str,
        help='Output file name')
    parser.add_argument('--input_format', '-i', type=str, choices=['model','interactions'],
        default='model',
        help='Input file format \n'
        '\t model (default): BioRECIPE model tabular format \n'
        '\t interactions: BioRECIPE interaction lists format \n')

    args = parser.parse_args()
    if args.input_format == 'model':
        biorecipeM_to_sbmlqual(args.input_file, args.output_file)
    elif args.input_format == 'interactions':
        biorecipeI_to_sbmlqual(args.input_file, args.output_file)

if __name__ == "__main__":
    main()