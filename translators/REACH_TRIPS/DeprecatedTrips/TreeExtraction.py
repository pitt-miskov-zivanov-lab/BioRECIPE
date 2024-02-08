import re
import logging
import copy

logger = logging.getLogger(__name__)
logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)

and_type_event = ('ONT::ACTIVATE' ,'ONT::INCREASE', 'ONT::STIMULATE', 'ONT::CC-ACTIVATE')
not_type_event = ('ONT::INHIBIT', 'ONT::DECREASE' , 'ONT::DEACTIVATE')
accepted_term_type = ('ONT::PROTEIN', 'ONT::PROTEIN_FAMILY', 'ONT::GENE-PROTEIN', 'ONT::GENE', 
					  'ONT::MACROMOLECULAR-COMPLEX', 'ONT::CELL-PART', 'ONT::BIOLOGICAL-PROCESS', 'ONT::MOLECULE', 
					  'ONT::CHEMICAL', 'ONT::PHARMACOLOGIC-SUBSTANCE', 'ONT::CELL')

class TreeExtractor(object):

	def __init__(self, term_dict, event_dict):
		self.term_dict = copy.deepcopy(term_dict)
		self.event_dict = copy.deepcopy(event_dict)
		self.melody_dict = {}

	def condense_tree(self):
		
		for event_id, attrib_dict in self.event_dict.items():
			
			# attaches parent id's to each affected term
			for affected_id in attrib_dict[':AFFECTED']:
				self.__assign_parent(event_id, affected_id)
			self.event_dict[event_id]['parent_event'] = ','.join(self.event_dict[event_id]['parent_event'])
			
			# attaches hybrid agent id's to each event, turns affected term into one string
			agent_list = []
			for agent_id in attrib_dict[':AGENT']:
				hybrid_agent = self.__assign_agent(event_id, agent_id)
				agent_list.append(hybrid_agent)

			self.event_dict[event_id][':AGENT'] = ','.join(agent_list)
			self.event_dict[event_id][':AFFECTED'] = ','.join(attrib_dict[':AFFECTED'])

	def __assign_parent(self, event_id, affected_id):

		# determines whether affected is a term or event
		if affected_id in self.term_dict:
			self.term_dict[affected_id]['parent_event'].append(event_id)

		elif affected_id in self.event_dict:
			self.event_dict[affected_id]['parent_event'].append(event_id)

	def __assign_agent(self, event_id, agent_id):

		logger.debug('Event is: ' + event_id)
		logger.debug('Agent is: ' + agent_id)

		# if the agent is a term, simply assigns the id
		if agent_id in self.term_dict:
			return agent_id

		# if the agent is an event, method groups its children as the new agent
		elif agent_id in self.event_dict:
			
			event_type = self.event_dict[agent_id]['event_type']
			agents_final = []
			affecteds_final = []
			combination_list = []
			
			agents = self.event_dict[agent_id][':AGENT']
			if isinstance(agents, list):
				for agent_part in agents:
					agent_part = self.__assign_agent(event_id, agent_part)
					agents_final.append(agent_part)
			else:
				agents_final.append(agents)
			
			affecteds = self.event_dict[agent_id][':AFFECTED']
			if isinstance(affecteds, list):
				for affected_part in affecteds:
					affected_part = self.__assign_agent(event_id, affected_part)
					affecteds_final.append(affected_part)
			else:
				affecteds_final.append(affecteds)

			agent_str = ','.join(agents_final)
			affected_str = ','.join(affecteds_final)

			if event_type in and_type_event:
				combination_list=['(',agent_str,')','*','(', affected_str,')']

			elif event_type in not_type_event:
				combination_list=['(',agent_str,')','*','!','(', affected_str,')']
			
			agent_id =''.join(combination_list)
			return agent_id

	def convert_tree(self):
		
		# assigns terms to positive and negative regulators
		for term_id, attrib_dict in self.term_dict.items():
			regulator_ids = None
			parent_id = attrib_dict['parent_event']	
			logger.debug(parent_id)	

			if (parent_id == []):
				logger.debug(attrib_dict['term_name'] + ' has no parent event')

			elif (len(parent_id) > 1):
				logger.error('term has multiple parents!')

			else:

				# **currently assumes each term only has one parent**
				parent_id = parent_id[0]
				regulator_actions = self.event_dict[parent_id]['event_type']
				regulator_ids, regulator_actions = self.__assign_interaction(term_id, parent_id, regulator_ids, regulator_actions)

				if (self.event_dict[parent_id]['event_polarity'] == 1):
					logger.debug(attrib_dict['term_name'] +' has a parent event of positve interaction type')
					self.term_dict[term_id]['positive_reg_id'].append(regulator_ids)
					self.term_dict[term_id]['positive_reg_action'].append(regulator_actions)
					self.term_dict[term_id]['positive_reg_name'].append(re.sub(r'[A-Z0-9]*', 
																				lambda x: self.__id_to_name(x.group(0)),regulator_ids))
				
				elif (self.event_dict[parent_id]['event_polarity'] == -1):
					logger.debug(attrib_dict['term_name'] +' has a parent event of negative interaction type')
					self.term_dict[term_id]['negative_reg_id'].append(regulator_ids)
					self.term_dict[term_id]['negative_reg_action'].append(regulator_actions)
					self.term_dict[term_id]['negative_reg_name'].append(re.sub(r'[A-Z0-9]*', 
																				lambda x: self.__id_to_name(x.group(0)),regulator_ids))

				else:
					logger.debug(attrib_dict['term_name'] +' has a parent event of "other" interaction type')

	def __assign_interaction(self, term_id, parent_id, regulator_ids, regulator_actions):

		# adds direct agent motifs
		reg_id_string = self.event_dict[parent_id][':AGENT']
		reg_action_list = []
		logger.debug('current reg_id is ' + reg_id_string)

		# adds complex interaction motifs
		if (regulator_ids != None):

			if self.event_dict[parent_id]['event_polarity'] == 1:
				
				reg_id_array = ['{',regulator_ids,'}','[', reg_id_string,']']
				reg_id_string = [0]
				reg_id_string[0] = ''.join(reg_id_array)
				reg_id_string.insert(0,'(')
				reg_id_string.append(')')
				reg_id_string = ''.join(reg_id_string)
				logger.debug('current reg_id is ' + reg_id_string)

			elif self.event_dict[parent_id]['event_polarity'] == -1:
				
				reg_id_array = ['(',regulator_ids,',','!', reg_id_string,')']
				reg_id_string = [0]
				reg_id_string[0] = ''.join(reg_id_array)
				reg_id_string.insert(0,'(')
				reg_id_string.append(')')
				reg_id_string = ''.join(reg_id_string)
				logger.debug('current reg_id is ' + reg_id_string)

		# determines whether there are any more assignments to make and returns regulator attributes
		regulator_ids = reg_id_string
		
		if (self.event_dict[parent_id]['parent_event'] == ''):	# no more parent events	
			return regulator_ids, regulator_actions
		
		else: # additional parents need to be assigned, function called recursively
			parent_id = self.event_dict[parent_id]['parent_event']
			logger.debug('current parent id is: ' + parent_id)
			reg_action_list = [regulator_actions, self.event_dict[parent_id]['event_type']]
			regulator_actions = '<--'.join(reg_action_list)
			regulator_ids, regulator_actions = self.__assign_interaction(term_id, parent_id, regulator_ids, regulator_actions)
			return regulator_ids, regulator_actions

	def __id_to_name(self, x):
		
		#substitutes the term name into the regulator list for each id 
		if x in self.term_dict:
			return self.term_dict[x]['term_name']
		else:
			logger.error('ID could not be found')

	def finalize_melody(self):
		
		for key, attrib_dict in self.term_dict.items():
			
			#Only copies to melody format if the term is of a biological type
			if (attrib_dict['term_type'] in accepted_term_type):
				
				#Checks term name is a duplicate and if so merges the attributes   
				if (attrib_dict['term_name'] not in self.melody_dict):
					self.melody_dict[attrib_dict['term_name']] = attrib_dict
				
				else:
					
					#Appends on alternate TRIPS id
					self.melody_dict[attrib_dict['term_name']]['term_id'].append(attrib_dict['term_id'][0])
					
					#Appends on additional regulators if they exist
					if (len(attrib_dict['positive_reg_id']) == 1):
						self.melody_dict[attrib_dict['term_name']]['positive_reg_id'].append(attrib_dict['positive_reg_id'][0])
						self.melody_dict[attrib_dict['term_name']]['positive_reg_name'].append(attrib_dict['positive_reg_name'][0])
						self.melody_dict[attrib_dict['term_name']]['positive_reg_action'].append(attrib_dict['positive_reg_action'][0])
					if (len(attrib_dict['negative_reg_id']) == 1):
						self.melody_dict[attrib_dict['term_name']]['negative_reg_id'].append(attrib_dict['negative_reg_id'][0])
						self.melody_dict[attrib_dict['term_name']]['negative_reg_name'].append(attrib_dict['negative_reg_name'][0])
						self.melody_dict[attrib_dict['term_name']]['negative_reg_action'].append(attrib_dict['negative_reg_action'][0])
					if (len(attrib_dict['positive_reg_id']) > 1) or (len(attrib_dict['negative_reg_id']) > 1):
						logger.error('single term has multiple parents!')
		
		#Converts the list of regulators to one string
		for key, attrib_dict in self.melody_dict.items():
			positive_str_id = ','.join(attrib_dict['positive_reg_id'])
			self.melody_dict[key]['positive_reg_id'] = positive_str_id
			positive_str_name = ','.join(attrib_dict['positive_reg_name'])
			self.melody_dict[key]['positive_reg_name'] = positive_str_name
			positive_str_action = ','.join(attrib_dict['positive_reg_action'])
			self.melody_dict[key]['positive_reg_action'] = positive_str_action
			negative_str_id = ','.join(attrib_dict['negative_reg_id'])
			self.melody_dict[key]['negative_reg_id'] = negative_str_id
			negative_str_name = ','.join(attrib_dict['negative_reg_name'])
			self.melody_dict[key]['negative_reg_name'] = negative_str_name
			negative_str_action = ','.join(attrib_dict['negative_reg_action'])
			self.melody_dict[key]['negative_reg_action'] = negative_str_action
				

	def get_dicts(self):
		return self.term_dict, self.event_dict, self.melody_dict







