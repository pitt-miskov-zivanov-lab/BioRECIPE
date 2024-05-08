# updated by Difei on 6/25
# NOTE: BioRECIPE columns are updated, while FLUTE and VIOLIN remain the old version

import sys, os
import numpy as np
from indra.belief import BeliefEngine
from indra.statements import statements
from indra.statements import Agent
from indra.tools import assemble_corpus as ac
import requests
from indra.sources import indra_db_rest as idr
from indra.sources import reach
from indra import config
from indra.tools import assemble_corpus as ac
from indra.belief import SimpleScorer
import time
import json
import pandas as pd
import glob
import argparse

# latest version of BioRECIPE Reading Output
BioRECIPE_reading_col = ['Regulator Name', 'Regulator Type', 'Regulator Subtype',
						 'Regulator HGNC Symbol', 'Regulator Database', 'Regulator ID',
						 'Regulator Compartment', 'Regulator Compartment ID',
						 'Regulated Name', 'Regulated Type', 'Regulated Subtype',
						 'Regulated HGNC Symbol', 'Regulated Database', 'Regulated ID',
						 'Regulated Compartment', 'Regulated Compartment ID',
						 'Sign', 'Connection Type', 'Mechanism', 'Site',
						 'Cell Line', 'Cell Type', 'Tissue Type', 'Organism',
						 'Score', 'Source', 'Statements', 'Paper IDs', 'Database Source', 'Database ID']

def parse_pmc(input, outdir):

	if os.path.isdir(input):
		files = glob.glob(input + "/*.csv")
		for infile in files:
			parse_pmc_by_indra(infile, outdir)
	else:
		infile = input
		parse_pmc_by_indra(infile, outdir)

def parse_pmc_by_indra(infile, outdir):
	"""This function queries PMCIDs using INDRA database api and
	outputs the reading file from INDRA statements

	Parameters
	----------
	inflie:
		input file with PMCIDs column
	indra_stats : boolean
		lists of indra statements in spreadsheet
	flute : boolean
		lists of interactions in FLUTE supported format
	violin : boolean
		reading output supported by VIOLIN old version

	Returns
	-------
	by default, it will output the extracted interactions in BioRECIPE format
	"""

	#infile = sys.argv[1] #comma-separated file with at least one column with header "PMCID"
	infile_ = os.path.splitext(os.path.basename(infile))[0]
	fName = os.path.join(outdir, f'{infile_}_reading.xlsx')

	papers_df = pd.read_csv(infile,usecols=["PMCID"]).dropna()
	papers = list(papers_df.values.reshape(-1,))

	# Reading output in BioRECIPE format
	fOut= pd.DataFrame(columns=BioRECIPE_reading_col)

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

	print(papers)

	for p in papers:

		idrp = idr.get_statements_for_papers(ids=[('pmcid',p)],)

		stmts = idrp.statements

		if(stmts):

			for s in stmts:

				bs = SimpleScorer()

				j =  s.to_json()

				intType = j["type"]

				bScore=bs.score_statement(s)

				valid_st = False

				upstrDbFlag = False # check regulator db info
				try:
					# Regulator
					upstr = j["subj"]
					upstrName = upstr["name"]
					fOut.loc[rowCount, "Regulator Name"] = upstrName
					upstrDbRefs = upstr["db_refs"]

					fOut.loc[rowCount, "Score"] = bScore
					fOut.loc[rowCount, "Mechanism"] = intType
					fOut.loc[rowCount, "Paper IDs"] = p
					valid_st=True

					try:
						paperStats = j["evidence"]
						fOut.loc[rowCount, "Statements"] = paperStats[0]["text"]

						epi_var = paperStats[0]["epistemics"]

						fOut.loc[rowCount, "Connection Type"] = str(epi_var['direct'])

					except Exception as e:
						pass

					# HGNC Symbol
					try:
						upstrHNGC = upstrDbRefs['HGNC']
						fOut.loc[rowCount, "Regulator HGNC Symbol"] = upstrHNGC
					except:
						pass

					for db_name, db_data in db_refs_dict.items():
						try:
							upstrDb= upstrDbRefs[db_name]
							fOut.loc[rowCount, "Regulator Database"] = db_data[0]
							fOut.loc[rowCount, "Regulator Type"] = db_data[1]
							fOut.loc[rowCount, "Regulator ID"] = upstrDb
							upstrDbFlag = True
							break
						except:
							pass

					# other type/element info should be assigned
					if not upstrDbFlag:
						db_name = list(upstrDbRefs.keys())[0]
						upstrDb = upstrDbRefs[db_name]

						fOut.loc[rowCount, "Regulator Database"] = db_name
						fOut.loc[rowCount, "Regulator Type"] = "other"
						fOut.loc[rowCount, "Regulator ID"] = upstrDb

					if fOut.loc[rowCount, "Regulator Database"] == 0:
						fOut.loc[rowCount, "Regulator ID"] = upstrName

				except Exception as e:
					try:
						upstr = j["enz"]
						upstrName = upstr["name"]

						fOut.loc[rowCount, "Regulator Name"] = upstrName

						upstrDbRefs = upstr["db_refs"]
						fOut.loc[rowCount, "Score"] = bScore
						fOut.loc[rowCount, "Mechanism"] = intType
						fOut.loc[rowCount, "Paper IDs"] = p
						valid_st=True

						# HGNC Symbol
						try:
							upstrHNGC = upstrDbRefs['HGNC']
							fOut.loc[rowCount, "Regulator HGNC Symbol"] = upstrHNGC
						except:
							pass

						for db_name, db_data in db_refs_dict.items():
							try:
								upstrDb = upstrDbRefs[db_name]
								fOut.loc[rowCount, "Regulator Database"] = db_name
								fOut.loc[rowCount, "Regulator Type"] = "other"
								fOut.loc[rowCount, "Regulator ID"] = upstrDb
								break
							except:
								pass

						# other type/element info should be assigned
						if not upstrDbFlag:
							db_name = list(upstrDbRefs.keys())[0]
							upstrDb = upstrDbRefs[db_name]
							fOut.loc[rowCount, "Regulator Database"] = db_name
							fOut.loc[rowCount, "Regulator Type"] = "other"
							fOut.loc[rowCount, "Regulator ID"] = upstrDb

						if fOut.loc[rowCount, "Regulator Database"] == 0:
							fOut.loc[rowCount, "Regulator ID"] = upstrName

					except Exception as e:
						pass

				downstrDbFlag = False  # check regulated db info
				try:
					# Regulated
					downstr = j["obj"]
					downstrName = downstr["name"]
					fOut.loc[rowCount, "Regulated Name"] = downstrName
					downstrDbRefs = downstr["db_refs"]

					# HGNC Symbol
					try:
						downstrHNGC = downstrDbRefs['HGNC']
						fOut.loc[rowCount, "Regulated HGNC Symbol"] = downstrHNGC
					except:
						pass

					for db_name, db_data in db_refs_dict.items():
						try:
							downstrDb = downstrDbRefs[db_name]
							fOut.loc[rowCount, "Regulated Database"] = db_data[0]
							fOut.loc[rowCount, "Regulated Type"] = db_data[1]
							fOut.loc[rowCount, "Regulated ID"] = downstrDb
							break
						except:
							pass

					# other type/element info should be assigned
					if not downstrDbFlag:
						db_name = list(downstrDbRefs.keys())[0]
						downstrDb = downstrDbRefs[db_name]
						fOut.loc[rowCount, "Regulated Database"] = db_name
						fOut.loc[rowCount, "Regulated Type"] = "other"
						fOut.loc[rowCount, "Regulated ID"] = downstrDb

					if fOut.loc[rowCount, "Regulated Database"] == 0:
						fOut.loc[rowCount, "Regulated ID"] = downstrName

				except Exception as e:
					try:
						downstr = j["sub"]
						downstrName = downstr["name"]
						fOut.loc[rowCount, "Regulated Name"] = downstrName
						downstrDbRefs = downstr["db_refs"]

						# HGNC Symbol
						try:
							downstrHNGC = downstrDbRefs['HGNC']
							fOut.loc[rowCount, "Regulated HGNC Symbol"] = downstrHNGC
						except:
							pass

						for db_name, db_data in db_refs_dict.items():
							try:
								downstrDb = downstrDbRefs[db_name]
								fOut.loc[rowCount, "Regulated Database"] = db_data[0]
								fOut.loc[rowCount, "Regulated Type"] = db_data[1]
								fOut.loc[rowCount, "Regulated ID"] = downstrDb
								break
							except:
								pass

						# other type/element info should be assigned
						if not downstrDbFlag:
							db_name = list(downstrDbRefs.keys())[0]
							downstrDb = downstrDbRefs[db_name]
							fOut.loc[rowCount, "Regulated Database"] = db_name
							fOut.loc[rowCount, "Regulated Type"] = "other"
							fOut.loc[rowCount, "Regulated ID"] = downstrDb

						if fOut.loc[rowCount, "Regulated Database"] == 0:
							fOut.loc[rowCount, "Regulated ID"] = downstrName

					except Exception as e:
						pass

				if(valid_st):

					# translate for some columns here
					if fOut.loc[rowCount, "Mechanism"] in ["Activation", "IncreaseAmount", "Phosphorylation"]:
						fOut.loc[rowCount, "Sign"] = "positive"
					elif fOut.loc[rowCount, "Mechanism"] in ["Inhibition", "DecreaseAmount", "Dephosphorylation"]:
						fOut.loc[rowCount, "Sign"] = "negative"
					else:
						print("Unspecified Regulation Type: {0}".format(fOut.loc[rowCount, "Mechanism"]))
						fOut.loc[rowCount, "Sign"] = "positive"

					if fOut.loc[rowCount, "Connection Type"] not in ["True", "False"]:
						print("Unspecified Connection Type: {0}".format(fOut.loc[rowCount, "Connection Type"]))
						fOut.loc[rowCount, "Connection Type"] = "False"

					fOut.loc[rowCount, "Source"] = "INDRA"

					# next row count
					rowCount+=1

		else:
			noStatements.append(str(p))

	if(len(noStatements)>0):

		print("No statements found for papers: ")

		for n in noStatements:
			print(n)

	with pd.ExcelWriter(fName) as writer:
		fOut.to_excel(writer, sheet_name="statements", index=False)

		noStatements = pd.DataFrame(noStatements)
		noStatements.to_excel(writer, sheet_name="Paper Not Found", index=False)


	print("Finished.")
	# np.savetxt(fName,networkArray,fmt="%s",encoding="utf-8",delimiter="\t", header=h,comments="")

def main():
	parser = argparse.ArgumentParser(description='parse PMCIDs using INDRA database api and output a reading file')

	# required arguments
	required_args = parser.add_argument_group('required input arguments')
	required_args.add_argument('-i', '--input', type=str, required=True,
		help='name of a single PMCIDs file')
	required_args.add_argument('-o', '--output', type=str, required=False, default=os.getcwd(),
		help='name of the directory containing PMCIDs files')

	args = parser.parse_args()
	input = args.input
	output = args.output
	parse_pmc(input, output)

if __name__ == '__main__':
	main()