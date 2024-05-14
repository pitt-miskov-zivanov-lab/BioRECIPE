import xml.etree.ElementTree as ET
import re
import logging
import copy

logger = logging.getLogger(__name__)
logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)

positive_regulator_type = ('ONT::ACTIVATE' ,'ONT::INCREASE', 'ONT::STIMULATE')
negative_regulator_type = ('ONT::INHIBIT', 'ONT::DECREASE' , 'ONT::DEACTIVATE')


class TripsTranslator(object):

	def __init__(self, ekb_data):
		# creating root of extraction tree
		try:
			self.root = ET.fromstring(ekb_data)
		except ET.ParseError:
			logger.error('could not parse XML file')
			self.root = None
			return

		# initilizing top level dictionaries
		self.term_dict = {}
		self.event_dict = {}
		self.group_dict = {}
		self.cc_dict = {}


	#Converts XML tree to dictionaries so that they can be transformed into .csv format
	def xml_to_dict(self):
		
		# scans through each primary element and sorts into dictionaries
		for element in self.root:
			logger.debug(element.tag)
			
			# records ELEMENT type attributes
			if (element.tag == 'TERM'):

				# term is a SINGLE term
				if (element.attrib['rule'] == '-SIMPLE-REF'):
					
					# setting attributes
					attrib_dict = {}
					term_id = element.attrib['id']					
					attrib_dict['term_id'] = [term_id]
					try:
						database_id = element.attrib['dbid']
						database_id = re.findall(r'UP:([A-Z0-9]*)',database_id)
						attrib_dict['database_id'] = database_id
					except KeyError:
						database_id = []
						attrib_dict['database_id'] = database_id
					paragraph = element.attrib['paragraph']
					attrib_dict['paragraph'] = paragraph
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
					attrib_dict['parent_event'] = []

					# adds attributes to term id
					self.term_dict[term_id] = attrib_dict
					logger.debug(self.term_dict[term_id])
				
				# term is a GROUP of terms
				elif (element.attrib['rule'] == '-LOGICALOP-REF'):					
					
					# setting attributes
					attrib_dict = {}
					group_id = element.attrib['id']
					attrib_dict['group_id'] = group_id
					paragraph = element.attrib['paragraph']
					attrib_dict['paragraph'] = paragraph
					group_type = element.find('type').text
					attrib_dict['group_type'] = group_type
					group_members = []			
					for member in element.find('aggregate').findall('member'):
						group_members.append(member.attrib['id'])
					attrib_dict['group_members'] = group_members

					# adds attributes to group id
					self.group_dict[group_id] = attrib_dict
					logger.debug(self.group_dict[group_id])

			# records EVENT type attributes		
			elif (element.tag == 'EVENT'):				
				
				# setting attributes
				attrib_dict = {}
				event_id = element.attrib['id']
				attrib_dict['event_id'] = event_id
				paragraph = element.attrib['paragraph']
				attrib_dict['paragraph'] = paragraph
				event_type = element.find('type').text
				attrib_dict['event_type'] = event_type

				if event_type in positive_regulator_type:
					attrib_dict['event_polarity'] = 1
				elif event_type in negative_regulator_type:
					attrib_dict['event_polarity'] = -1
				else:
					attrib_dict['event_polarity'] = 0
				attrib_dict['parent_event'] = []
				try:
					arg_role = element.find('arg1').attrib['role']
					arg_id = element.find('arg1').attrib['id']
					attrib_dict[arg_role] = arg_id
				except:
					logger.debug('no event AGENT!')
					attrib_dict[':AGENT'] = None
				try:
					arg_role = element.find('arg2').attrib['role']
					arg_id = element.find('arg2').attrib['id']
					attrib_dict[arg_role] = arg_id
				except:
					logger.debug('no event AFFECTED!')
					attrib_dict[':AFFECTED'] = None

				# adds attributes to event dictionary
				self.event_dict[event_id] = attrib_dict
				logger.debug(self.event_dict[event_id])

			# records INPUT type attributes
			elif (element.tag == 'input'):
				
				#Stores input text and id for each paragraph
				paragraphs = element.find('paragraphs')
				paragraph = paragraphs.find('paragraph')
				paragraph_id = paragraph.attrib['id']
				paragraph_text = paragraph.text
				logger.debug(paragraph_id + ': ' + paragraph_text)

			# records CC type attributes
			elif (element.tag == 'CC'):
				
				# setting attributes
				attrib_dict = {}
				cc_id = element.attrib['id']
				attrib_dict['event_id'] = cc_id
				cc_args=element.findall('arg')
				for arg in cc_args:
					arg_role = arg.attrib['role']
					arg_id = arg.attrib['id']
					if (arg_role == ':OUTCOME'):
						attrib_dict[':AFFECTED'] = arg_id
					elif (arg_role == ':FACTOR'):
						attrib_dict[':AGENT'] = arg_id

				# setting more attributes
				#cc_type = element.find('type').text #Assuming this is always equivalent to ONT::ACTIVATE
				attrib_dict['event_type'] = 'ONT::CC-ACTIVATE'
				attrib_dict['event_polarity'] = 0
				attrib_dict['parent_event'] = []

				# storing attributes in dictionary
				self.cc_dict[cc_id] = attrib_dict
				logger.debug(self.cc_dict[cc_id])


			else:
				logger.debug('other element \n')


	def refine_dict(self):

		# extracts the id's from group terms
		for event_id, attrib_dict in self.event_dict.items():
			agent_id = attrib_dict[':AGENT']
			self.event_dict[event_id][':AGENT'] = []
			self.__group_agents(agent_id, event_id)
			affected_id = attrib_dict[':AFFECTED']
			self.event_dict[event_id][':AFFECTED'] = []
			self.__group_affecteds(affected_id, event_id)

		# reassigns causal connective elements
		for cc_id, attrib_dict in self.cc_dict.items():
			factor_id = attrib_dict[':AGENT']
			outcome_id = attrib_dict[':AFFECTED']
			self.__reassign_cc(cc_id, factor_id, outcome_id)


	def __group_agents(self, agent_id, event_id):

		# if the agent is a term or event, assign directly to the parent event
		if (agent_id in self.term_dict) or (agent_id in self.event_dict):
			self.event_dict[event_id][':AGENT'].append(agent_id)

		# if agent is a group, method must convert the members into one string
		elif (agent_id in self.group_dict):
			for member in self.group_dict[agent_id]['group_members']:
				self.__group_agents(member, event_id)


	def __group_affecteds(self, affected_id, event_id):

		# if the affected is a term or event, assign directly to the parent event
		if (affected_id in self.term_dict) or (affected_id in self.event_dict):
			self.event_dict[event_id][':AFFECTED'].append(affected_id)

		# if affected is a group, method must extract them
		elif (affected_id in self.group_dict):
			for member in self.group_dict[affected_id]['group_members']:
				self.__group_affecteds(member, event_id)


	def __reassign_cc(self, cc_id, factor_id, outcome_id):

		# if the factor is a group, method must first convert its members to a single string
		self.cc_dict[cc_id][':AGENT'] = []
		if (factor_id in self.event_dict) or (factor_id in self.term_dict):
			self.cc_dict[cc_id][':AGENT'].append(factor_id)

		elif (factor_id in self.group_dict):
			for member in self.group_dict[factor_id]['group_members']:
				self.cc_dict[cc_id][':AGENT'].append(member)

		# makes a special causal event in the event dictionary
		self.event_dict[cc_id] = copy.deepcopy(self.cc_dict[cc_id])

		# reassigns the agent of outcome event to the affected of causal event
		self.event_dict[cc_id][':AFFECTED'] = self.event_dict[outcome_id][':AGENT']

		# assigns our new causal event to be the outcome event's agent
		self.event_dict[outcome_id][':AGENT'] = [cc_id]

	def get_dicts(self):
		#returns relevant dictionaries
		return self.term_dict, self.event_dict

