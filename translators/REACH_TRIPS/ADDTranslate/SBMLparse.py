import xml.etree.ElementTree as ET
import csv
from tkinter import filedialog
from subprocess import call

# This script is currently designed to parse out mass action reaction rules
# from SBML files. Complex rate functions are not supported at this time


# ask user for filepath
filePath = filedialog.askopenfilename(initialdir = "./",title = "Select SBML file",
	filetypes = [("SBML files","*.xml")])

# Open the file and read data
try:
  text_data = open(filePath,'r')
  sbml_data = text_data.read()
except:
  print('ERROR: incompatible file format!')
  sbml_data = None

# Main parsing functions
if (sbml_data != None):

	species_dict = {}
	rate_dict = {}
	init_dict = {}
	
	# creating root of xml tree
	try:
		root = ET.fromstring(sbml_data)
		assert (int(root.attrib["version"]) == 3 and int(root.attrib["level"]) == 2)
		ns = "{http://www.sbml.org/sbml/level2/version3}"
		mns = "{http://www.w3.org/1998/Math/MathML}"
	except ET.ParseError:
		print('could not parse XML file')
		root = None
	except AssertionError:
		print('SBML version does not match')
		root = None

	# picking out species id and initial concentrations
	for species in root.iter(ns+"species"):
		species_dict[species.attrib["id"]] = {}
		init_dict[species.attrib["id"]] = {"init":species.attrib["initialConcentration"]}

	# defining rate constants
	for parameter in root.iter(ns+"parameter"):
		if "value" in parameter.attrib:
			rate_dict[parameter.attrib["id"]] = parameter.attrib["value"]

	# picking out reaction rules
	for reaction in root.iter(ns+"reaction"):
		# each reaction will be in this form: [K, r1, r2, r3...]
		reaction_array = []
		reaction_id = reaction.attrib["id"]

		# appending rate constant and reactants to array
		kinetic_law = reaction.find(ns+"kineticLaw")
		applied = kinetic_law[0].find(mns+"apply")
		for ci in applied.findall(mns+"ci"):
			if ci.text[1:-1] in rate_dict:
				reaction_array.append(rate_dict[ci.text[1:-1]])
			else:
				reaction_array.append(ci.text)

		# assigning this rate for all products
		product_list = reaction.find(ns+"listOfProducts")
		if product_list != None:
			for product in product_list.findall(ns+"speciesReference"):
				species_dict[product.attrib["species"]][reaction_id] = reaction_array

	# writing out data as a textfile
	print(species_dict)
	with open('reaction_data.txt', 'wb') as f:  # Just use 'w' mode in 3.x
	   for species, species_data in species_dict.items():
	   		print("species is: "+species)
	   		f.write(species+" |")
	   		for k,reaction in species_data.items():
	   			for component in reaction:
	   				f.write(component)
	   			f.write("|")
	   		f.write("\n")

	# calling CUDD script to build ADD's
	# print("Switching over to CUDD builder...")
	# call(["./testprogram", str(len(species_dict))])