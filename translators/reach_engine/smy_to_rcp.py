#Created by Difei May 2023

# Usage
###############
# python smy_to_rcp.py -i JSON_FILE -o BioRECIPE_FILE
###############

# Function
###############
# process a JSON file using INDRA engine, and return outputs in BioRECIPEs format
###############

import argparse
import os
import numpy as np
from indra.sources import reach
from indra.belief import SimpleScorer
import pandas as pd
from translators.within_biorecipe.biorecipe_std import biorecipe_int_cols

def get_indra_stmts_by_reach(file_name: str=None, file_str: str=None, citation=None, organism_priority=None):

	"""
	Return indra statements by processing the input REACH json file.
	NOTE these required parameters by indra interface

	Parameters
	----------
	file_name : str
        The name of the json file to be processed.
    file_str : str
        The string content of the json file to be processed.
    citation : Optional[str]
        A PubMed ID passed to be used in the evidence for the extracted INDRA
        Statements. Default: None
    organism_priority : Optional[list of str]
        A list of Taxonomy IDs providing prioritization among organisms
        when choosing protein grounding. If not given, the default behavior
        takes the first match produced by Reach, which is prioritized to be
        a human protein if such a match exists.

    Returns
    -------
    rp : ReachProcessor
        A ReachProcessor containing the extracted INDRA Statements in rp.statements.
	"""
	if file_name is not None:
		rp = reach.process_json_file(file_name)
	else:
		rp = reach.process_json_str(file_str)
	return rp

def indra_stmts_to_interactions(processor, output_file=None, indra_stats=False, flute=False, violin=False):

	"""
	This function outputs a reading file from indra statements

	Parameters
	----------
	processor: ReachProcessor
		Different types of processor containing the extracted INDRA Statements
	output_file: str
		The name of output file containing the extracted interactions
	indra_stats : Boolean
		If true, also return lists of indra statements in spreadsheet
	flute : Boolean
		If true, also return lists of interactions in FLUTE supported format
	violin : Boolean
		If true, also return lists of interactions supported by VIOLIN old version

	Returns
	-------
	By default, it will output the extracted interactions in BioRECIPE format
	"""

	# TODO: rewrite this setting

	# rename file suffix to .xlsx
	if output_file is not None:
		pathname, suffix = os.path.splitext(output_file)
		if suffix != '.xlsx':
			fName = output_file.replace(suffix, ".xlsx")
		else:
			fName = output_file
		fName_stats = output_file.replace(".csv","_statements.xlsx")
		fName_VIOLIN = output_file.replace(".csv", "_statements_VIOLIN.xlsx")
		fName_FLUTE = output_file.replace(".csv", "_statements_FLUTE.xlsx")


	networkArray = np.empty((6000, 13),dtype=">U250")
	rowCount = 0
	noStatements = []

	db_refs_dict = {
		'UP': ('uniprot', 'protein'),
		'UPPRO': ('uniprot', 'protein'),
		'PF': ('pfam', 'family'),
		'CHEBI': ('chebi', 'simple-chemical'),
		'PUBCHEM': ('pubchem', 'simple-chemical'),
		'GO': ('go', 'bioprocess'),
		'MESH': ('mesh', 'bioprocess'),
		'HGNC': ('hgnc', 'gene'),
	}

	try:
		stmts = processor.statements
	except:
		raise ValueError("Processor is not supported by INDRA")

	if (stmts):
		for s in stmts:
			bs = SimpleScorer()
			j = s.to_json()
			intType = j["type"]
			bScore = bs.score_statement(s)
			valid_st = False
			try:
				# Regulator
				upstr = j["subj"]
				upstrName = upstr["name"]
				networkArray[rowCount, 0] = upstrName
				upstrDbRefs = upstr["db_refs"]

				networkArray[rowCount, 9] = bScore
				networkArray[rowCount, 8] = intType
				#networkArray[rowCount, 12] = p
				valid_st = True

				try:
					paperStats = j["evidence"]
					networkArray[rowCount, 11] = paperStats[0]["text"]
					epi_var = paperStats[0]["epistemics"]
					networkArray[rowCount, 10] = str(epi_var['direct'])

				except Exception as e:
					pass

				for db_name, db_data in db_refs_dict.items():
					try:
						upstrDb = upstrDbRefs[db_name]
						networkArray[rowCount, 1] = db_data[0]
						networkArray[rowCount, 2] = db_data[1]
						networkArray[rowCount, 3] = upstrDb
						break
					except:
						pass

				if networkArray[rowCount, 1] == 0:
					networkArray[rowCount, 3] = upstrName

			except Exception as e:
				try:
					upstr = j["sub"]
					upstrName = upstr["name"]

					networkArray[rowCount, 0] = upstrName
					upstrDbRefs = upstr["db_refs"]

					networkArray[rowCount, 9] = bScore
					networkArray[rowCount, 8] = intType
					#networkArray[rowCount, 12] = p
					valid_st = True

					try:
						paperStats = j["evidence"]
						networkArray[rowCount, 11] = paperStats[0]["text"]

						epi_var = paperStats[0]["epistemics"]

						networkArray[rowCount, 10] = str(epi_var['direct'])

					except Exception as e:
						pass

					for db_name, db_data in db_refs_dict.items():
						try:
							upstrDb = upstrDbRefs[db_name]
							networkArray[rowCount, 1] = db_data[0]
							networkArray[rowCount, 2] = db_data[1]
							networkArray[rowCount, 3] = upstrDb
							break
						except:
							pass

					if networkArray[rowCount, 1] == 0:
						networkArray[rowCount, 3] = upstrName

				except Exception as e:
					pass

			try:
				# Regulated
				downstr = j["obj"]
				downstrName = downstr["name"]
				networkArray[rowCount, 4] = downstrName
				downstrDbRefs = downstr["db_refs"]

				for db_name, db_data in db_refs_dict.items():
					try:
						downstrDb = downstrDbRefs[db_name]
						networkArray[rowCount, 5] = db_data[0]
						networkArray[rowCount, 6] = db_data[1]
						networkArray[rowCount, 7] = downstrDb
						break
					except:
						pass

				if networkArray[rowCount, 5] == 0:
					networkArray[rowCount, 7] = downstrName

			except Exception as e:
				try:
					downstr = j["enz"]
					downstrName = downstr["name"]
					networkArray[rowCount, 4] = downstrName
					downstrDbRefs = downstr["db_refs"]

					for db_name, db_data in db_refs_dict.items():
						try:
							downstrDb = downstrDbRefs[db_name]
							networkArray[rowCount, 5] = db_data[0]
							networkArray[rowCount, 6] = db_data[1]
							networkArray[rowCount, 7] = downstrDb
							break
						except:
							pass

					if networkArray[rowCount, 5] == 0:
						networkArray[rowCount, 7] = downstrName

				except Exception as e:
					pass

			if (valid_st):
				rowCount += 1

	else:
		print("No statements found")

	# h = "Regulator Name \tRegulator ID \tRegulated Name \tRegulated ID \tRegulation Type \tBelief score \tDirect? \tText"

	# original output
	fOut = pd.DataFrame(networkArray)
	fOut.columns = ["Regulator Name", "Regulator Database", "Regulator Type", "Regulator ID", "Regulated Name",
					"Regulated Database",
					"Regulated Type", "Regulated ID", "Regulation Type", "Belief score", "Connection Type", "Evidence",
					"PMCID"]

	fOut_FLUTE = pd.DataFrame(
		columns=["RegulatedName", "RegulatedDatabase", "RegulatedType", "RegulatedID", "RegulatorName",
				 "RegulatorDatabase",
				 "RegulatorID", "RegulatorType", "InteractionType", "PaperID"])

	# old VIOLIN version
	fOut_VIOLIN = pd.DataFrame(
		columns=["Element Name", "Element Type", "Database Name", "Element ID", "Location", "Location ID", "Cell Line",
				 "Cell Type", "Organism", "Positive Reg Name",
				 "Positive Reg Type", "Positive Reg ID", "Positive Reg Location", "Positive Reg Location ID",
				 "Negative Reg Name", "Negative Reg Type",
				 "Negative Reg ID", "Negative Reg Location", "Negative Reg Location ID", "Connection Type", "Mechanism",
				 "Paper ID", "Evidence"])

	# Reading output in BioRECIPE format
	fOut_BioRECIPE = pd.DataFrame(columns=biorecipe_int_cols)

	# convert INDRA statements to VIOLN & FLUTE formats
	for i in range(len(fOut)):
		if not fOut.loc[i, "Regulator Name"]:
			break

		fOut_FLUTE.loc[i, "RegulatedName"] = fOut.loc[i, "Regulated Name"]
		fOut_FLUTE.loc[i, "RegulatedDatabase"] = fOut.loc[i, "Regulated Database"]
		fOut_FLUTE.loc[i, "RegulatedType"] = fOut.loc[i, "Regulated Type"]
		fOut_FLUTE.loc[i, "RegulatedID"] = fOut.loc[i, "Regulated ID"]
		fOut_FLUTE.loc[i, "RegulatorName"] = fOut.loc[i, "Regulator Name"]
		fOut_FLUTE.loc[i, "RegulatorDatabase"] = fOut.loc[i, "Regulator Database"]
		fOut_FLUTE.loc[i, "RegulatorType"] = fOut.loc[i, "Regulator Type"]
		fOut_FLUTE.loc[i, "RegulatorID"] = fOut.loc[i, "Regulator ID"]

		fOut_VIOLIN.loc[i, "Element Name"] = fOut.loc[i, "Regulated Name"]
		fOut_VIOLIN.loc[i, "Element Type"] = fOut.loc[i, "Regulated Type"]
		fOut_VIOLIN.loc[i, "Element ID"] = fOut.loc[i, "Regulated ID"]

		fOut_BioRECIPE.loc[i, "Regulated Name"] = fOut.loc[i, "Regulated Name"]
		fOut_BioRECIPE.loc[i, "Regulated Type"] = fOut.loc[i, "Regulated Type"]
		fOut_BioRECIPE.loc[i, "Regulated ID"] = fOut.loc[i, "Regulated ID"]
		fOut_BioRECIPE.loc[i, "Regulated Database"] = fOut.loc[i, "Regulated Database"]
		fOut_BioRECIPE.loc[i, "Regulator Name"] = fOut.loc[i, "Regulator Name"]
		fOut_BioRECIPE.loc[i, "Regulator Type"] = fOut.loc[i, "Regulator Type"]
		fOut_BioRECIPE.loc[i, "Regulator ID"] = fOut.loc[i, "Regulator ID"]
		fOut_BioRECIPE.loc[i, "Regulator Database"] = fOut.loc[i, "Regulator Database"]

		fOut_BioRECIPE.loc[i, "Mechanism"] = fOut.loc[i, "Regulation Type"]

		if fOut.loc[i, "Regulation Type"] in ["Activation", "IncreaseAmount", "Phosphorylation"]:
			fOut_FLUTE.loc[i, "InteractionType"] = "increases"

			fOut_VIOLIN.loc[i, "Positive Reg Name"] = fOut.loc[i, "Regulator Name"]
			fOut_VIOLIN.loc[i, "Positive Reg Type"] = fOut.loc[i, "Regulator Type"]
			fOut_VIOLIN.loc[i, "Positive Reg ID"] = fOut.loc[i, "Regulator ID"]

			fOut_BioRECIPE.loc[i, "Sign"] = "positive"
		elif fOut.loc[i, "Regulation Type"] in ["Inhibition", "DecreaseAmount", "Dephosphorylation"]:
			fOut_FLUTE.loc[i, "InteractionType"] = "decreases"

			fOut_VIOLIN.loc[i, "Negative Reg Name"] = fOut.loc[i, "Regulator Name"]
			fOut_VIOLIN.loc[i, "Negative Reg Type"] = fOut.loc[i, "Regulator Type"]
			fOut_VIOLIN.loc[i, "Negative Reg ID"] = fOut.loc[i, "Regulator ID"]

			fOut_BioRECIPE.loc[i, "Sign"] = "negative"
		else:
			#print("Unspecified Regulation Type: {0}".format(fOut.loc[i, "Regulation Type"]))
			fOut_FLUTE.loc[i, "InteractionType"] = "increases"

			fOut_VIOLIN.loc[i, "Positive Reg Name"] = fOut.loc[i, "Regulator Name"]
			fOut_VIOLIN.loc[i, "Positive Reg Type"] = fOut.loc[i, "Regulator Type"]
			fOut_VIOLIN.loc[i, "Positive Reg ID"] = fOut.loc[i, "Regulator ID"]

			fOut_BioRECIPE.loc[i, "Sign"] = "positive"

		if fOut.loc[i, "Connection Type"] == "True":
			fOut_VIOLIN.loc[i, "Connection Type"] = "D"
			fOut_BioRECIPE.loc[i, "Connection Type"] = "True"
		elif fOut.loc[i, "Connection Type"] == "False":
			fOut_VIOLIN.loc[i, "Connection Type"] = "I"
			fOut_BioRECIPE.loc[i, "Connection Type"] = "False"
		else:
			#print("Unspecified Connection Type: {0}".format(fOut.loc[i, "Connection Type"]))
			fOut_VIOLIN.loc[i, "Connection Type"] = "I"
			fOut_BioRECIPE.loc[i, "Connection Type"] = "False"

		fOut_FLUTE.loc[i, "PaperID"] = fOut.loc[i, "PMCID"]

		fOut_VIOLIN.loc[i, "Evidence"] = fOut.loc[i, "Evidence"]
		fOut_VIOLIN.loc[i, "Paper ID"] = fOut.loc[i, "PMCID"]

		if fOut.loc[i, "Belief score"]:
			fOut_BioRECIPE.loc[i, "Score"] = fOut.loc[i, "Belief score"]
		fOut_BioRECIPE.loc[i, "Statements"] = fOut.loc[i, "Evidence"]
		fOut_BioRECIPE.loc[i, "Paper IDs"] = fOut.loc[i, "PMCID"]

	if output_file is not None:
		fOut_BioRECIPE.to_excel(fName, index=False)
	else:
		return fOut_BioRECIPE

	if indra_stats:
		fOut.to_excel(fName_stats, index=False)
	if flute:
		fOut_FLUTE = fOut_FLUTE.replace(r'^\s*$', "None", regex=True)
		fOut_FLUTE.to_excel(fName_FLUTE, index=False)
	if violin:
		fOut_VIOLIN.to_excel(fName_VIOLIN, index=False)

	#print("Finished.")
	# np.savetxt(fName,networkArray,fmt="%s",encoding="utf-8",delimiter="\t", header=h,comments="")

def get_biorecipeI_from_reach_smy(json_file_name, output_file_name):
	rp = get_indra_stmts_by_reach(json_file_name)
	indra_stmts_to_interactions(processor=rp, output_file=output_file_name)

def get_biorecipeI_from_reach_smy_str(json_file_str, output_file_name=None):
	rp = get_indra_stmts_by_reach(file_str=json_file_str)
	if output_file_name is not None:
		indra_stmts_to_interactions(processor=rp, output_file=output_file_name)
	else:
		return indra_stmts_to_interactions(processor=rp)


def main():
	parser = argparse.ArgumentParser(description='translate reach file using INDRA to a BioRECIPE interaction lists file')

	parser.add_argument('-i', '--input', type=str, required=True,
	                     help='Path of REACH json file')
	parser.add_argument('-o', '--output', type=str, required=True,
	                     help='Path of the output interaction file (.xlsx)')
	args = parser.parse_args()
	get_biorecipeI_from_reach_smy(args.input, args.output)

if __name__ == '__main__':
	main()
