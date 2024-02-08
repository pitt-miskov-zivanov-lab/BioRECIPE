import requests
import json
import logging
import argparse
from ModelNodes import *


logger = logging.getLogger(__name__)
logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)

class ReachTranslator(object):

	def __init__(self, fileName):
		
		# creating extraction map
		self.tripsExtractions = ExtractionMap()
		self.nestedCount = 0
		self.nestList = []
		self.eventCount = 0
		self.sentenceCount = 0

		if 'txt' in fileName:
			# using Reach API to retrieve extractions as .json file
			with open(fileName,"r") as inFile:
				inString = inFile.read()
			
			inString = inString.split('\n')
			print(inString)

			# looping through each sentence and counting if nested
			for this_string in inString:
				data = {
		 		 	'text': this_string,
		  			'output': 'fries'
				}
				response = requests.post('http://agathon.sista.arizona.edu:8080/odinweb/api/text', data=data)
				print(response.text)
				self.reading = json.loads(response.text)
				self.nested_count()

		elif 'json' in fileName:
			# loading entire paper
			with open(fileName,"r") as inFile:
				self.reading = json.load(inFile)
				self.nested_count()

		print("The final nested event count is: "+ str(self.nestedCount))
		print("The final event count is: "+str(self.eventCount))
		print("The final sentence count is: "+str(self.sentenceCount))

	def nested_count(self):
		if 'events' not in self.reading:
			return

		for this_event in self.reading['events']['frames']:
			print(this_event['text'])
			print(this_event['type'])
			print(this_event['frame-id'])
			print(this_event['arguments'])
			for argument in this_event['arguments']:
				if ('event' in argument['argument-type'] 
					and 'controlled' in argument['type'] 
					and this_event['frame-id'] not in self.nestList
					and this_event['sentence'] not in self.nestList):
					print("nested event!")
					self.nestedCount = self.nestedCount+1 # TODO: sometimes may count the same sentence twice because of weird subevents
					self.nestList.append(argument['arg'])
					self.nestList.append(this_event['sentence'])
			print('\n')
			self.eventCount = self.eventCount+1

		for this_sentence in self.reading['events']['frames']:
			self.sentenceCount = self.sentenceCount +1
		# for this_entity in self.reading['entities']['frames']:
		# 	print(this_entity['text'])
		# 	print(this_entity['type'])
		# 	print(this_entity['frame-id'])
		# 	print(this_entity['xrefs'])
		# 	print('\n')


def main():

	# Parse command line arguments
	parser = argparse.ArgumentParser(
		description='Translate text snippet through Reach"s API into event-entity-relationship format',
		formatter_class=argparse.RawTextHelpFormatter)
	parser.add_argument('input_file', type=str, 
						help='text file for processing through Reach')
	args = parser.parse_args()
	
	# convert text to event-entity format
	if 'txt' in args.input_file or 'json' in args.input_file:
		translator = ReachTranslator(args.input_file)

		# write out to a text file for debugging
		with open("Output.txt","w") as text_file:
			for key, extraction in translator.tripsExtractions.extractions.items():
				text_file.write(""+key+"--->"+str(extraction)+"\n")

	else:
		logger.error("Wrong file type!")

if __name__ == '__main__':
	main()