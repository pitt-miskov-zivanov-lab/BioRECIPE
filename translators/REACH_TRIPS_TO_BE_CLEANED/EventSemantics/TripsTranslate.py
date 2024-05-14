import xml.etree.ElementTree as ET
import re
import logging
from ModelNodes import *
import argparse

logger = logging.getLogger(__name__)
logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)

class TripsTranslator(object):

	def __init__(self, ekb_file):
		# creating extraction map
		self.tripsExtractions = ExtractionMap()
		self.nestedCount = 0
		self.nestList = []
		self.eventCount = 0
		self.sentenceCount = 0
		# reading in xml string from file
		with open(ekb_file, 'r') as inFile:
			ekb_data = inFile.read()
		# creating extraction tree from xml string
		try:
			self.root = ET.fromstring(ekb_data)
			self.root = self.root.find('ekb')
		except ET.ParseError:
			logger.error('could not parse XML file')
			self.root = None
			return
		# main conversion
		self.convert_trips()


	def nested_count(self): # this method is just for analysis of reading
		# runs conversion just in case it hasnt run already
		self.convert_trips()
		# count sentences
		for sentence in self.root.iter('sentence'): #TODO: TRIPS sentence count not accurate
			self.sentenceCount +=1
		# count events and nested events
		for event in self.root.iter('EVENT'):
			# using extraction dictionary to test for nested events
			eventID = event.get('id')
			assert eventID in self.tripsExtractions.extractions
			eventNode = self.tripsExtractions.getExtraction(eventID)
			if (len(eventNode.eventParent) > 0
				and eventNode not in self.nestList):
				self.nestList.append(eventNode)
				self.nestedCount +=1
			# regardless of nested type, event counter will increment
			self.eventCount +=1


	#Converts XML tree to dictionaries so that they can be transformed into .csv format
	def convert_trips(self):
		
		# scans through each primary extraction and stores as Event/Entity objects
		for extraction in self.root:
			logger.debug(extraction.tag)
			# records TERM type attributes
			if (extraction.tag == 'TERM'):
				logger.debug(extraction.attrib)
			# records EVENT type attributes		
			elif (extraction.tag == 'EVENT'):				
				logger.debug(extraction.attrib)
				self.addTripsEvent(extraction)
			# records CC type attributes
			elif (extraction.tag == 'CC'):
				logger.debug(extraction.attrib)
				self.addTripsCausal(extraction)
			# other extraction type
			else:
				logger.debug(extraction.attrib)


	def addTripsEvent(self, extNode):
		# make sure event is not already in the dictionary
		key = extNode.get('id')
		if key in self.tripsExtractions.extractions:
			return self.tripsExtractions.extractions[key]

		thisEvent = Event(extNode.find('type').text, text=extNode.find('text').text ,eventID=key)

		for child in extNode:
			if 'arg' in child.tag:
				argID = child.get('id')
				
				# adding agents
				if child.get('role') == ":AGENT":
					searchString = "./*[@id='"+argID+"']"
					agent = self.root.find(searchString)
					# handling different agent types
					agentList = []
					if agent is not None:
						if agent.tag == 'EVENT':
							agentList = [self.addTripsEvent(agent)]
						elif agent.tag == 'TERM':
							agentList = self.deaggregate(agent)
						for agentNode in agentList:
						 	thisEvent.addAgent(agentNode)
				
				# adding affecteds
				if child.get('role') == ":AFFECTED":
					searchString = "./*[@id='"+argID+"']"
					affected = self.root.find(searchString)
					# handling different affected types
					affectedList = []
					if affected is not None:
						if affected.tag =='EVENT':
							affectedList = [self.addTripsEvent(affected)]
						elif affected.tag =='TERM':
							affectedList = self.deaggregate(affected)
						for affectedNode in affectedList:
							affectedNode.addEvent(thisEvent)
							thisEvent.addAffected(affectedNode)

		self.tripsExtractions.addExtraction(key, thisEvent)
		return thisEvent

	def deaggregate(self, extNode):
		aggList = []
		# node is an aggregate of multiple other entities
		if extNode.find('aggregate') is not None:
			for member in extNode.findall(".//member"):
				memID=member.get('id')
				searchString = "./*[@id='"+memID+"']"
				memNode = self.root.find(searchString)
				if memNode.tag == 'EVENT':
					aggList.append(self.addTripsEvent(memNode))
				elif memNode.tag == 'TERM':
					aggList.append(self.addTripsEntity(memNode)) # TODO: are there nested aggregations that we need to handle?
		# just a single entity
		else:
			aggList = [self.addTripsEntity(extNode)]

		return aggList

	def addTripsEntity(self, extNode):
		# Just adding text/name and ID at this point
		key = extNode.get('id')
		name = extNode.find('name').text if extNode.find('name') is not None else extNode.find('type').text
		thisEntity = Entity(name, text= extNode.find('text').text, entityID=key)
		self.tripsExtractions.addExtraction(key, thisEntity)
		return thisEntity

	def addTripsCausal(self, extNode):
		# check that cuasal is of correct type
		assert(extNode.find('type').text in ['ONT::CAUSE', 'ONT::DEPENDENT']) # TODO: check for negation

		factorList=[]
		outcomeList=[]
		for child in extNode:
			if 'arg' in child.tag:
				argID = child.get('id')

				# adding factor
				if child.get('role') ==":FACTOR":
					searchString = "./*[@id='"+argID+"']"
					factor = self.root.find(searchString)
					# handling different factor types
					if factor is None:
						factorList = [self.addTripsEntity(child)]
					elif factor.tag == 'EVENT':
						factorList = [self.addTripsEvent(factor)]
					elif factor.tag == 'TERM':
						factorList = self.deaggregate(factor)
					 	
				# adding outcome
				if child.get('role') ==":OUTCOME":
					searchString = "./*[@id='"+argID+"']"
					outcome = self.root.find(searchString)
					# handling different outcome types
					if outcome is None:
						outcomeList = [self.addTripsEntity(child)]
					elif outcome.tag == 'EVENT':
						outcomeList = [self.addTripsEvent(outcome)]
					elif outcome.tag == 'TERM':
						outcomeList = self.deaggregate(outcome)

		for outcome in outcomeList:
			for factor in factorList:
				outcome.addCausal(factor)


def main():

	# Parse command line arguments
	parser = argparse.ArgumentParser(
		description='Translate TRIPS automated reading output into event-entity-relationship format',
		formatter_class=argparse.RawTextHelpFormatter)
	parser.add_argument('input_file', type=str, 
						help='TRIPS" automated reading output for conversion to event-entity-relationship format')

	args = parser.parse_args()
	translator = TripsTranslator(args.input_file)

	# write out to a text file for debugging
	with open("Output.txt","w") as text_file:
		for key, extraction in translator.tripsExtractions.extractions.items():
			text_file.write(""+key+"--->"+str(extraction)+"\n")

if __name__ == '__main__':
	main()