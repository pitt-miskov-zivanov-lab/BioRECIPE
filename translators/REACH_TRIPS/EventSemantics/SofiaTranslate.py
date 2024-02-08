from ModelNodes import *
import argparse
import pandas as pd

relations_dict={}
events_dict={}
entities_dict={}
final = ExtractionMap()

def convert_sofia(input_file, allEvents=False):
	"""Convert automated reading output from SOFIA reader 
	"""
	global relations_dict, events_dict, entities_dict
	global final

	# get relations
	relations = pd.read_excel(input_file,sheet_name = 0,na_values='NaN',keep_default_na=False)
	relations = relations.rename(index=str,
		columns={
			'Relation' : 'text',
			'Relation_Type' : 'type',
			'Source_File' : 'source',
			'Sentence' : 'evidence',
			'Score' : 'score',
			'Cause Index' : 'cause',
			'Effect Index' : 'effect'
		})
	relations_dict = relations.to_dict(orient='index')

	# get events 
	events = pd.read_excel(input_file,sheet_name = 1,na_values='NaN',keep_default_na=False)
	events.set_index('Event Index',inplace=True)
	events = events.rename(index=str,
		columns={
			'Relation' : 'text',
			'Event_Type' : 'type',
			'Sentence' : 'evidence',
			'Agent' : 'agent',
			'Agent Index' : 'agent_id',
			'Patient' : 'patient',
			'Patient Index' : 'patient_id',
			'Location' : 'location',
			'Time' : 'timing'
		})
	events_dict = events.to_dict(orient='index')

	# get entities
	entities = pd.read_excel(input_file,sheet_name = 2,na_values='NaN',keep_default_na=False)
	entities.set_index('Entity Index',inplace=True)
	entities = entities.rename(index=str,
		columns={
			'Entity' : 'text',
			'Entity_Type' : 'type',
			'Sentence' : 'evidence',
			'Qualifier' : 'degree'
		})
	entities_dict = entities.to_dict(orient='index')

	# # iterate through events and add if they are complete (agent and patient)
	# for key, event in events_dict.items():
	# 	if event['agent_id'] != '' and event['patient_id'] != '': # check for complete event
	# 		thisEvent = addSofiaEvent(key)

	# iterate through relations and add associated events
	if not allEvents:
		for key, relation in relations_dict.items():
			if relation['type'] == 'CausalRelation': # TODO: add PreventRelation type
				thisCause = addSofiaEvent(relation['cause'])
				thisEffect = addSofiaEvent(relation['effect'])
				thisEffect.addCausal(thisCause)	
			else:
				print("relation is "+relation['type']+" type")
	# in the extended mode, iterate through all complete events
	else:
		for key, event in events_dict.items():
			if event['agent'] is not None and event['patient'] is not None:
				addSofiaEvent(key)

	return final

def addSofiaEvent(key):
	global events_dict, entities_dict, final

	# make sure event is not already in the dictionary
	if key in final.extractions:
		return final.extractions[key]
	event = events_dict[key]

	thisEvent = Event(event['text'], event['evidence'], eventID=key)
	# splitting up combinations of entities
	agents = [x.strip() for x in event['agent_id'].split(',')]
	affecteds = [x.strip() for x in event['patient_id'].split(',')]

	# # TODO: Entities in both agent and affected slots, currently removing from affected
	# if len(set(agents) & set(affecteds)) !=0: 
	# 	affecteds = [x for x in affecteds if x not in set(agents) & set(affecteds)] 
	
	# first handling all agents of this event
	for agent in agents:
		if agent == '': # empty, skip this
			continue
		if 'E' in agent: # this is an event
			thisAgent = addSofiaEvent(agent)
		elif 'N' in agent: # this is an entity
			if agent in final.extractions:
				thisAgent = final.extractions[agent]
			else:
				thisAgent = Entity(entities_dict[agent]['text'], entities_dict[agent]['evidence'], entityID=agent)	
		final.addExtraction(agent, thisAgent)
		thisEvent.addAgent(thisAgent)
	# now handling all affected children of the event	
	for affected in affecteds:
		if affected == '': # empty, skip this
			continue
		if 'E' in affected: # this is an event
			thisAffected = addSofiaEvent(affected)
			thisAffected.addEvent(thisEvent)
		elif 'N' in affected: # this is an entity
			if affected in final.extractions:
				thisAffected = final.extractions[affected]
				thisAffected.addEvent(thisEvent)
			else:
				thisAffected = Entity(entities_dict[affected]['text'], entities_dict[affected]['evidence'], eventParent=thisEvent, entityID=agent)
		# adding this event to the extraction dictionary
		final.addExtraction(affected, thisAffected)
		thisEvent.addAffected(thisAffected)
	
	final.addExtraction(key, thisEvent)
	return thisEvent

def main():

	# Parse command line arguments
	parser = argparse.ArgumentParser(
		description='Translate sofia automated reading output into event-entity-relationship format',
		formatter_class=argparse.RawTextHelpFormatter)
	parser.add_argument('input_file', type=str, 
						help='sofia"s automated reading output to convert to event-entity-relationship format')
	parser.add_argument('all_events', type=bool, default=False,
						help='boolean flag to include all events, not just causal relations')

	args = parser.parse_args()
	final = convert_sofia(args.input_file, args.all_events)

	# write out to a text file for debugging
	with open("Output.txt","w") as text_file:
		for key, extraction in final.extractions.items():
			text_file.write(""+key+"--->"+str(extraction)+"\n")

if __name__ == '__main__':
	main()