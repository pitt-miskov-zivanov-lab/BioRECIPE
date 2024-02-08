import xml.etree.ElementTree as ET
import csv
from tkinter.filedialog import askopenfilename

#EVENT AND TERM TYPES
positive_regulator_type = ('ONT::ACTIVATE' ,'ONT::INCREASE', 'ONT::STIMULATE')
negative_regulator_type = ('ONT::INHIBIT', 'ONT::DECREASE' , 'ONT::DEACTIVATE')
accepted_term_type = ('ONT::PROTEIN', 'ONT::PROTEIN_FAMILY', 'ONT::GENE-PROTEIN', 'ONT::GENE', 'ONT::MACROMOLECULAR-COMPLEX', 'ONT::CELL-PART', 'ONT::BIOLOGICAL-PROCESS', 'ONT::MOLECULE', 'ONT::CHEMICAL', 'ONT::PHARMACOLOGIC-SUBSTANCE', 'ONT::CELL')


#FUNCTIONS:

#Exports data as .csv file (in similar form to MeLoDy lab format)
def dict_to_csv (term_dict):

	toCSV = []
	for k,v in term_dict.items():
		toCSV.append(term_dict[k])
	keys = ['term_id','term_name','term_type','database_id','paragraph','positive_reg_id', 'positive_reg_name', 'positive_reg_action', 'negative_reg_id','negative_reg_name','negative_reg_action']

	with open('term_output.csv', 'w', newline='') as output_file:
		dict_writer = csv.DictWriter(output_file,keys)
		dict_writer.writeheader()

		firstrow = {}
		for i in range(0,len(keys)):
			firstrow[keys[i]]=keys[i]

		dict_writer.writerows(toCSV)

#Converts XML tree to dictionaries so that they can be easily transformed into .csv format
def xml_to_dict(ekb_data):

	#Creating the root of our extraction tree
	root = ET.fromstring(ekb_data)
	print ('The root of the XML tree is', root.tag)
	print()

	#Initilizing top level dictionaries
	term_dict = {}
	event_dict = {}
	group_dict = {}

	#Scans through each primary element
	for element in root:
		print (element.tag)
		
		#If the element is a term type
		if (element.tag == 'TERM'):

			#If the term is a single term
			if (element.attrib['rule'] == '-SIMPLE-REF'):
				
				#Unique term identifier
				term_id = element.attrib['id']

				#Setting attributes
				attrib_dict = {}
				attrib_dict['term_id'] = [term_id]
				try:
					database_id = element.attrib['dbid']
					attrib_dict['database_id'] = database_id
				except:
					pass

				paragraph = element.attrib['paragraph']
				attrib_dict['paragraph'] = paragraph
				# paragraph_section = [ element.attrib['start'], element.attrib['end']]
				# attrib_dict['paragraph_section'] = paragraph_section
				term_type = element.find('type').text
				attrib_dict['term_type'] = term_type
				term_name = element.find('name').text
				attrib_dict['term_name'] = term_name
				attrib_dict['positive_reg_id'] = []
				attrib_dict['positive_reg_name'] = []
				attrib_dict['positive_reg_action'] = []
				attrib_dict['negative_reg_id'] = []
				attrib_dict['negative_reg_name'] = []
				attrib_dict['negative_reg_action'] = []

				#Adds attributes to term id
				term_dict[term_id] = attrib_dict
				print (term_dict[term_id])
			
			#If the term is a grouping of terms
			elif (element.attrib['rule'] == '-LOGICALOP-REF'):
				
				#Unique group identifier
				group_id = element.attrib['id']
				
				#Setting attributes
				attrib_dict = {}
				paragraph = element.attrib['paragraph']
				attrib_dict['paragraph'] = paragraph
				paragraph_section = [ element.attrib['start'], element.attrib['end']]
				attrib_dict['paragraph_section'] = paragraph_section
				group_type = element.find('type').text
				attrib_dict['group_type'] = group_type
				group_members = []			
				for member in element.find('aggregate').findall('member'):
					group_members.append(member.attrib['id'])
				attrib_dict['group_members'] = group_members

				#Adds attributes to group id
				group_dict[group_id] = attrib_dict
				print (group_dict[group_id])


		#If the element is event type		
		elif (element.tag == 'EVENT'):
			
			#Unique event identifier
			event_id = element.attrib['id']
			
			#Setting attributes
			attrib_dict = {}
			paragraph = element.attrib['paragraph']
			attrib_dict['paragraph'] = paragraph
			paragraph_section = [ element.attrib['start'], element.attrib['end']]
			attrib_dict['paragraph_section'] = paragraph_section
			event_type = element.find('type').text
			attrib_dict['event_type'] = event_type
			
			arg_dict = {}
			try:
				arg_role = element.find('arg1').attrib['role']
				arg_id = element.find('arg1').attrib['id']
				arg_dict[arg_role] = arg_id
				arg_role = element.find('arg2').attrib['role']
				arg_id = element.find('arg2').attrib['id']
				arg_dict[arg_role] = arg_id
			except:
				print ('Warning: no event children!')
				arg_dict[':AGENT'] = None
				arg_dict[':AFFECTED'] = None

			attrib_dict['arg_dict'] = arg_dict

			#Adds attributes to group id
			event_dict[event_id] = attrib_dict
			print (event_dict[event_id])

		elif (element.tag == 'input'):
			
			#Stores input text and id for each paragraph
			paragraphs = element.find('paragraphs')
			paragraph = paragraphs.find('paragraph')
			paragraph_id = paragraph.attrib['id']
			paragraph_text = paragraph.text
			print(paragraph_id,': ',paragraph_text)

		else:
			print ('other element')

		print ()

	return [term_dict, event_dict, group_dict]

#Assigns Regulator information to the term dictionary
def asgn_reg(term_dict, event_dict, group_dict):
	for event_id, attrib_dict in event_dict.items():
	
		#Checks if the agent is a group or event
		agents = []
		agent_id = attrib_dict['arg_dict'][':AGENT']
		find_agents = True
		
		while (find_agents == True):
			if (agent_id in term_dict):
				agents.append(agent_id)
				find_agents = False

			elif (agent_id in group_dict):
				for member in group_dict[agent_id]['group_members']:
					agents.append(member)
				find_agents = False

			elif (agent_id in event_dict):
				agents.append(event_dict[agent_id])
				find_agents = False
				raise Exception('nested events not implemented yet')

			else:
				print('cannot find agent')
				find_agents = False	

		#Checks if the affected is a term, group, or event
		affecteds = []
		affected_id = attrib_dict['arg_dict'][':AFFECTED']
		find_affecteds = True
		
		while (find_affecteds == True):
			
			if (affected_id in term_dict):
				affecteds.append(affected_id)
				find_affecteds =  False

			elif (affected_id in group_dict):
				for member in group_dict[affected_id]['group_members']:
					affecteds.append(member)
				find_affecteds =  False

			elif (affected_id in event_dict):
				affecteds.append(event_dict[affected_id])
				find_affecteds =  False
				raise Exception('nested events not implemented yet')

			else:
				print('cannot find affected')
				find_affecteds =  False	
		
		#If event is a positve regulator
		if (attrib_dict['event_type'] in positive_regulator_type):
			
			for agent_id in agents:
				print (agent_id)
				for affected_id in affecteds:
					print(affected_id)
					term_dict[affected_id]['positive_reg_id'].append(agent_id)
					term_dict[affected_id]['positive_reg_name'].append(term_dict[agent_id]['term_name'])
					term_dict[affected_id]['positive_reg_action'].append(attrib_dict['event_type'])
					

		#If event is a negative regulator
		elif (attrib_dict['event_type'] in negative_regulator_type):

			for agent_id in agents:
				print (agent_id)
				for affected_id in affecteds:
					print(affected_id)
					term_dict[affected_id]['negative_reg_id'].append(agent_id)
					term_dict[affected_id]['negative_reg_name'].append(term_dict[agent_id]['term_name'])
					term_dict[affected_id]['negative_reg_action'].append(attrib_dict['event_type'])
					
	
	return (term_dict)

def term_reduction(term_dict):
	protein_dict={}
	for key, attrib_dict in term_dict.items():
		
		#Only copies to csv if the term is of a biological type
		if (attrib_dict['term_type'] in accepted_term_type):
			
			#Checks term name is a duplicate and if so merges the attributes   
			if (attrib_dict['term_name'] not in protein_dict):
				protein_dict[attrib_dict['term_name']] = attrib_dict
			
			else:
				
				#Appends on alternate TRIPS id
				protein_dict[attrib_dict['term_name']]['term_id'].append(attrib_dict['term_id'][0])
				
				#Appends on additional regulators if they exist
				if (len(attrib_dict['positive_reg_id']) != 0):
					protein_dict[attrib_dict['term_name']]['positive_reg_id'].append(attrib_dict['positive_reg_id'][0])
					protein_dict[attrib_dict['term_name']]['positive_reg_name'].append(attrib_dict['positive_reg_name'][0])
					protein_dict[attrib_dict['term_name']]['positive_reg_action'].append(attrib_dict['positive_reg_action'][0])
				if (len(attrib_dict['negative_reg_id']) != 0):
					protein_dict[attrib_dict['term_name']]['negative_reg_id'].append(attrib_dict['negative_reg_id'][0])
					protein_dict[attrib_dict['term_name']]['negative_reg_name'].append(attrib_dict['negative_reg_name'][0])
					protein_dict[attrib_dict['term_name']]['negative_reg_action'].append(attrib_dict['negative_reg_action'][0])

	return (protein_dict)

def file_input():
	
	#User selects text file
	filename = askopenfilename(title = "Select Text File")
	try:
		#Reading XML in string format
		text_data = open(filename,'r')
		ekb_data = text_data.read()
	except:
		print('ERROR: incompatible file format!')
		ekb_data = None

	return (ekb_data)


#############################################################################################
#                                        Main Script                                        #
#############################################################################################

#User selects a text file containing XML data from TRIPS
ekb_data = file_input()

if (ekb_data != None):
	#Converts xml data into dictionaries
	[term_dict, event_dict, group_dict] = xml_to_dict(ekb_data)

	#Assigns regulators to the term dictionary
	term_dict = asgn_reg(term_dict, event_dict, group_dict)

	#Removes non-protein terms and duplicate proteins
	protein_dict = term_reduction(term_dict)

	#Exports to excel
	dict_to_csv(protein_dict)

##############################################################################################
##############################################################################################


	