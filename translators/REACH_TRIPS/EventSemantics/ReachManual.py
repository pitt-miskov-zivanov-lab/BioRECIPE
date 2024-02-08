import json
import argparse
import pandas as pd




def read_out(fileName):
	# extractions already in json format
	if 'json' in fileName:
		with open(fileName,"r") as inFile:
			reading = json.load(inFile)


		sent_dict ={}
		for frame in reading['sentences']['frames']:
			if frame['frame-type'] == 'sentence':
				sent_dict[frame['frame-id']] = frame['text']



		df = pd.DataFrame.from_dict(sent_dict, orient="index")
		df.to_csv("manual.csv")
				

def main():

	# Parse command line arguments
	parser = argparse.ArgumentParser(
		description='Translate text snippet through Reach"s API into event-entity-relationship format',
		formatter_class=argparse.RawTextHelpFormatter)
	parser.add_argument('input_file', type=str, 
						help='text file for processing through Reach')
	args = parser.parse_args()
	
	# convert text to event-entity format
	if 'json' in args.input_file:
		read_out(args.input_file)
	else:
		logger.error("Wrong file type!")

if __name__ == '__main__':
	main()