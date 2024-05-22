import os
import pandas as pd
import glob
from indra.belief import SimpleScorer
from indra.sources import indra_db_rest as idr
from indra.statements import *
from translators.within_biorecipe.biorecipe_std import biorecipe_int_cols

def parse_pmc(input, outdir):
	if os.path.isdir(input):
		files = glob.glob(input + "/*.csv")
		for infile in files:
			get_biorecipeI_from_pmcids(infile, outdir)
	else:
		infile = input
		get_biorecipeI_from_pmcids(infile, outdir)

def get_biorecipeI_from_pmcids(infile, outdir):
	"""
	This function queries PMCIDs using INDRA database api and
	outputs the reading file from INDRA statements

	Parameters
	----------
	inflie:
		input file that has "PMCID" column header

	Returns
	-------
	By default, it will output the extracted interactions in BioRECIPE format
	"""

	#infile = sys.argv[1] #comma-separated file with at least one column with header "PMCID"
	infile_ = os.path.splitext(os.path.basename(infile))[0]
	fName = outdir
	#fName = os.path.join(outdir, f'{infile_}_reading.xlsx')

	papers_df = pd.read_csv(infile,usecols=["PMCID"]).dropna()
	papers = list(papers_df.values.reshape(-1,))

	# Reading output in BioRECIPE format
	fOut= pd.DataFrame(columns=biorecipe_int_cols)

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
	#print(papers)

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

	#print("Finished.")
	#np.savetxt(fName,networkArray,fmt="%s",encoding="utf-8",delimiter="\t", header=h,comments="")

def get_INDRAstmts_from_biorecipeI(infile, outfile):
    """
    Translate BioRECIPE interaction lists to INDRA statements

    Parameters
	----------
	inflie : str
		Name and path of input BioRECIPE interaction lists file (.xlsx)

	Returns
	-------
    outfile : str
		Name and path of output json file (contains INDRA statements)
    """

    df = pd.read_excel(infile, dtype=">U50", keep_default_na=False)

    # TODO: map to INDRA statments representing post-translational modifications
    # TODO: add database attributes to db_ref
    stmts_mapping = {
        "phosphorylation": Phosphorylation,
        "dephosphorylation": Dephosphorylation,
        "ubiquitination": Ubiquitination,
        "activation": Activation,
        "inhibition": Inhibition,
        "increaseamount": IncreaseAmount,
        "DecreaseAmount": DecreaseAmount
    }

    stmts = []
    for i in range(len(df)):
        t = df.loc[i, 'Regulated Name']
        s = df.loc[i, 'Regulator Name']
        sign = df.loc[i, 'Sign']
        m = df.loc[i, 'Mechanism']

        ta = Agent(t)
        sa = Agent(s)

        if not m and m.lower() not in stmts_mapping.keys():
            # default statements decided by interaction sign
            if sign == 'positive':
                stmt = Activation(ta, sa)
            elif sign == 'negative':
                stmt = Inhibition(ta, sa)
            else:
                raise ValueError('Invalid value was found in Sign column')
        else:
            # find an indra statement
              stmt = stmts_mapping[m.lower()](ta, sa)

        stmts.append(stmt)

        # TODO: other output formats
        stmts_to_json_file(stmts, outfile)


