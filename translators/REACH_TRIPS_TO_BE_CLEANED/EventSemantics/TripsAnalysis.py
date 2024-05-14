import os
import argparse
import pandas as pd
from TripsTranslate import TripsTranslator
from ModelNodes import *

# Counts events, sentences, from reading outputs and writes debugging output to csv
def runAnalysis(PMCID):
	totalSent = 0
	totalEvent = 0
	totalNested = 0
	totalExtractions = {}

	for filename in os.listdir(os.getcwd()):
		if PMCID in filename:
			print(filename)
			translator = TripsTranslator(filename)
			translator.nested_count()
			totalSent+=translator.sentenceCount
			totalEvent+=translator.eventCount
			totalNested+=translator.nestedCount
			totalExtractions.update(translator.tripsExtractions.extractions)

	print("\nThe final nested event count is: "+ str(totalNested))
	print("The final event count is: "+str(totalEvent))
	print("The final sentence count is: "+str(totalSent))
	# write out to a csv for full debugging output
	df = pd.DataFrame.from_dict(totalExtractions, orient='index')
	df.to_csv('output.csv')


def main():
	# Parse command line arguments
	parser = argparse.ArgumentParser(
		description='analyzing all trips extractions from a single pubmed paper',
		formatter_class=argparse.RawTextHelpFormatter)
	parser.add_argument('PMCID', type=str, 
						help='PMC paper ID, whose extractions are in the current directory')

	args = parser.parse_args()
	runAnalysis(args.PMCID)

if __name__ == '__main__':
	main()