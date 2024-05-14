
# TODO: entity and event should probably inherit from the same class
class Entity:
	
	def __init__(self, name, text, entityID, causalParent=None, 
				 eventParent=None):
		self.name = name
		self.text = text
		self.entityID = entityID
		self.causalParent = []
		self.addCausal(causalParent)
		self.eventParent = []
		self.addEvent(eventParent)

	def addCausal(self, newCause):
		if isinstance(newCause, list):
			for cause in newCause:
				self.causalParent.append(cause)
		elif newCause is not None:
			self.causalParent.append(newCause)

	def addEvent(self, newEvent):
		if isinstance(newEvent, list):
			for event in newEvent:
				self.eventParent.append(event)
		elif newEvent is not None:
			self.eventParent.append(newEvent)

	def combineWith(self, otherEntity):
		# make sure we're really talkin' bout the same thing
		assert self.name == otherEntity.name
		# rectifying causal differences
		if self.causalParent.sort() != otherEntity.causalParent.sort():
			self.addCausal(otherEntity.causalParent)
		# rectifying event parent differences
		if self.eventParent.sort() != otherEntity.eventParent.sort():
			self.addEvent(otherEntity.eventParent)

	def __str__(self):
		return("ENTITY: %-30s|| Text: %-30s|| Event Parent: %-25s|| Causal: %-25s" 
				% (str(self.entityID)+','+self.name, self.text, str(self.eventParent), str(self.causalParent)))
	
	def __repr__(self):
		return str(self.name)+'('+str(self.entityID)+')'


class Event:

	def __init__(self, name, text, eventID, causalParent=None, eventParent=None, 
				 agentParent=None, affectedChild=None):
		self.name = name
		self.text = text
		self.eventID = eventID
		self.causalParent = []
		self.addCausal(causalParent)
		self.eventParent = []
		self.addEvent(eventParent)
		self.agentParent = []
		self.addAgent(agentParent)
		self.affectedChild = []
		self.addAffected(affectedChild)

	def addAgent(self, newAgent):
		if isinstance(newAgent, list):
			for agent in newAgent:
				self.agentParent.append(agent)
		elif newAgent is not None:
			self.agentParent.append(newAgent)

	def addAffected(self, newAffected):
		if isinstance(newAffected, list):
			for affected in newAffected:
				self.affectedChild.append(affected)
		if newAffected is not None:
			self.affectedChild.append(newAffected)

	def addCausal(self, newCause):
		if isinstance(newCause, list):
			for cause in newCause:
				self.causalParent.append(cause)
		elif newCause is not None:
			self.causalParent.append(newCause)

	def addEvent(self, newEvent):
		if isinstance(newEvent, list):
			for event in newEvent:
				self.eventParent.append(event)
		elif newEvent is not None:
			self.eventParent.append(newEvent)


	def combineWith(self, otherEvent):
		# make sure we're really talkin' bout the same thing
		assert self.name == otherEvent.name
		# rectifying causal differences
		if self.causalParent.sort() != otherEvent.causalParent.sort():
			self.addCausal(otherEntity.causalParent)
		# rectifying event parent differences
		if self.eventParent.sort() != otherEvent.eventParent.sort():
			self.addEvent(otherEntity.eventParent)
		# rectifying agent diffs
		if self.agentParent.sort() != otherEvent.agentParent.sort():
			self.addAgent(otherEvent.agentParent)
		# rectifying affected diffs		
		if self.affectedChild.sort() != otherEvent.affectedChild.sort():
			self.addAffected(otherEvent.affectedChild)

	def __str__(self):
		return("EVENT:  %-30s|| Text: %-30s|| Event Parent: %-25s|| Causal: %-25s|| Agent: %-25s|| Affected: %-25s" 
				% (str(self.eventID)+','+self.name, self.text, str(self.eventParent), str(self.causalParent), str(self.agentParent), str(self.affectedChild)))
	
	def __repr__(self):
		return str(self.name)+'('+str(self.eventID)+')'


class ExtractionMap:

	def __init__(self):
		self.extractions = {}

	def addExtraction(self, extID, extractionNode):
		if extID in self.extractions:
			# makes sure we don't overwrite information
			if self.extractions[extID] != extractionNode:
				self.extractions[extID].combineWith(extractionNode)

		if isinstance(extractionNode, (Entity, Event)):
			self.extractions[extID] = extractionNode

		else:
			print("WARNING: not an event or entity")

	def getExtraction(self, extID):
		if extID in self.extractions:
			return self.extractions[extID]
		else:
			return None


class Element:

	def __init__(self, name=None):
		self.name = name
		self.posRegulators = []
		self.negRegulators = []
		self.directRegulators = []

	def addPositive(self, newPos):
		self.posRegulators.append(newPos)

	def addNegative(self, newNeg):
		self.negRegulators.append(newNeg)

	def addDirect(self, newDirect):
		self.directRegulators.append(newDirect)

	def __str__(self):
		return ("[ELEMENT:"+self.name+"||  positive reg: "+str(self.posRegulators)+
				"||  negative reg: "+str(self.negRegulators)+ "||  direct reg: " +str(self.directRegulators)+ "]")


class InfluenceSet:

	def __init__(self):
		self.set = {}

	def addElement(self, elementID, elementNode):
		assert isinstance(elementNode, Element)
		self.set[elementID] = elementNode

	def __str__(self):
		output = ""
		for key, value in self.set.items():
			output = output+str(key)+"--->"+str(value)+"\n"
		return output