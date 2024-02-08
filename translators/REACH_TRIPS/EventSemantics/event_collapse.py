from ModelNodes import *
from SofiaTranslate import *
from TripsTranslate import *
from ReachTranslate import *
import argparse

# TODO: give the option to load in different dictionaries from a file
positiveDict = ["phosphorylation","transcription", "positive-activation", "positive-regulation","increase", "forced", "improved", "increased", "increasing", "ONT::ACTIVATE", "ONT::STIMULATE", "ONT::PHOSPHORYLATION"]
negativeDict = ["negative-activation","negative-regulation","decrease","prevented","reduced", "reducing", "decreased", "ONT::INHIBIT", "ONT::DECREASE"]
melodySet = InfluenceSet()

def collapse(extraction, nodeList):

	def collapseEntity(entity, nodeList):		
		currentNode = Element(entity.name)

		if len(entity.causalParent) != 0:
			for causalParent in entity.causalParent:
				causalNode = collapse(causalParent, nodeList)
				currentNode.addPositive(causalNode.name)
		if len(entity.eventParent) != 0:
			for eventParent in entity.eventParent:
				eventNode = collapseRegulating(eventParent, nodeList)
				if eventParent.name in positiveDict:
					currentNode.addPositive(eventNode.name)
				elif eventParent.name in negativeDict:
					currentNode.addNegative(eventNode.name)
				else:
					print("event not in dictionary: "+eventParent.name+"\n")

		return currentNode

	def collapseEvent(event, nodeList):
		global melodySet		
		currentNode = Element()

		agentNodes=""
		affectedNodes=""
		for agent in event.agentParent:
			currAgent = collapse(agent, nodeList)
			agentNodes = AND(agentNodes, currAgent.name)
		for affected in event.affectedChild:
			currAffected = collapse(affected, nodeList)
			affectedNodes = AND(affectedNodes, currAffected.name)

		if len(event.agentParent) != 0:
			if event.name in positiveDict:
				currentNode = Element(AND(agentNodes, affectedNodes))
			elif event.name in negativeDict:
				currentNode = Element(AND(agentNodes, NOT(affectedNodes)))
			else:
				currentNode = Element(event.name) # TODO: figure out what happens when event is not positive or negative
		elif len(event.affectedChild) != 0:
			if event.name in positiveDict:
				currentNode = Element(affectedNodes)
			elif event.name in negativeDict:
				currentNode = Element(NOT(affectedNodes)) # TODO: figure out what happens when event is not positive or negative
			else:
				currentNode = Element(event.name)
		else:
			currentNode = Element(event.name)

		if len(event.causalParent) != 0:
			causalNode = collapse(event.causalParent[0], nodeList) # TODO: currently assuming only one causal parent
			currentNode = Element(AND(currentNode.name,causalNode.name))

		if len(event.eventParent) != 0:
			currentNode.addDirect(currentNode.name)
			currentNode.name = "(Reg Node)"+currentNode.name 
			parentNode = collapseRegulating(event.eventParent[0], nodeList)
			if event.eventParent[0].name in positiveDict:
				currentNode.addPositive(parentNode.name)
			elif event.eventParent[0].name in negativeDict:
				currentNode.addNegative(parentNode.name)
			melodySet.addElement(currentNode.name, currentNode) # TODO: verify that regulator nodes are being stored correctly

		return currentNode

	# Checks for recursive loops
	if extraction in nodeList:
		return Element("(loop)"+extraction.name)
	else:
		nodeList.append(extraction)	
	# Calling nested functions
	if isinstance(extraction, Entity):
		return collapseEntity(extraction, nodeList)
	elif isinstance(extraction, Event):
		return collapseEvent(extraction, nodeList)

def collapseRegulating(event, nodeList):
	global melodySet

	agentNodes=""
	causalNodes=""
	for agent in event.agentParent:
		currAgent = collapse(agent, nodeList)
		agentNodes = AND(agentNodes, currAgent.name)
	for causal in event.causalParent:
		currCausal = collapse(causal, nodeList)
		causalNodes = AND(causalNodes, currCausal.name)	
	currentNode = Element(AND(agentNodes, causalNodes))

	if not currentNode.name:
		currentNode.name = event.name+" of "+event.affectedChild[0].name # TODO: assuming one affected

	if len(event.eventParent) != 0:
		currentNode.addDirect(currentNode.name)
		print("This event has an event parent: "+currentNode.name)
		currentNode.name = "(Reg Node)"+currentNode.name 
		print("New intermediate node created: "+currentNode.name)
		parentNode = collapseRegulating(event.eventParent[0], nodeList) # TODO: currently assuming only one event parent when there are cases of multiple
		print("Regulating Event is: "+event.eventParent[0].name+", simplified to the regulating node: "+parentNode.name+"\n")
		if event.eventParent[0].name in positiveDict:
			currentNode.addPositive(parentNode.name)
		elif event.eventParent[0].name in negativeDict:
			currentNode.addNegative(parentNode.name)
		else:
			print("regulating event is not in dictionary\n")
		melodySet.addElement(currentNode.name, currentNode) # TODO: verify that regulator nodes are being stored correctly

	return currentNode

def AND(str1, str2):
	assert isinstance(str1, str)
	assert isinstance(str2, str)
	if not str1: return str2
	if not str2: return str1
	output = ""+str1+"&"+str2
	return output

def NOT(str1):
	assert isinstance(str1, str)
	output= "!("+str1+")"
	return output

def main():
	global melodySet

	# temporary code to get sofia/trips event-entity data
	# Parse command line arguments
	parser = argparse.ArgumentParser(
		description='Translate machine reading output into influence sets (tabular form)',
		formatter_class=argparse.RawTextHelpFormatter)
	parser.add_argument('input_file', type=str, 
						help='machine reading output to be used for translation')

	args = parser.parse_args()

	if '.xlsx' in args.input_file:
		final = convert_sofia(args.input_file)
	elif '.txt' in args.input_file:
		translator = TripsTranslator(args.input_file)
		final = translator.tripsExtractions
	elif '.json' in args.input_file:
		translator = ReachTranslator(args.input_file)
		final = translator.reachExtractions
	else:
		raise NameError("Invalid filename")

	# looping through extractions and making an influence set for each entity
	for key, extraction in final.extractions.items():
		if isinstance(extraction, Entity):
			if(len(extraction.causalParent)!=0 or len(extraction.eventParent)!=0):
				melodySet.addElement(key, collapse(extraction, []))
		if isinstance(extraction, Event):
			if (not extraction.agentParent and not extraction.affectedChild
				and (len(extraction.causalParent)!=0 or len(extraction.eventParent)!=0)):
				eventFragment = Entity(extraction.name, entityID=extraction.eventID, causalParent=extraction.causalParent, eventParent=extraction.eventParent)
				melodySet.addElement(key, collapse(eventFragment, []))

	# print out entire set
	print('\nFinal Output:')
	print(str(melodySet))

if __name__ == '__main__':
	main()