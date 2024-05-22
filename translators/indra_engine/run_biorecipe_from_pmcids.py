import argparse
from translators.indra_engine.to_from import get_biorecipeI_from_pmcids

def main():
	parser = argparse.ArgumentParser(description='parse PMCIDs using INDRA database API and output an interaction file in BioRECIPE format')

	# required arguments
	required_args = parser.add_argument_group('required input arguments')
	required_args.add_argument('-i', '--input', type=str, required=True,
		help='path and name of file that includes PMCID column header')
	required_args.add_argument('-o', '--output', type=str, required=True,
		help='path and name of output file in BioRECIPE format')

	args = parser.parse_args()
	input = args.input
	output = args.output
	get_biorecipeI_from_pmcids(input, output)

if __name__ == '__main__':
	main()

