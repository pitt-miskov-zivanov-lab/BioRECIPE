# INDRA-BioRECIPE Translator

This repository contains a set of instructions and scripts: 1) retrieve statements from the INDRA database based on literature queries using PMC (PubMed Central) to BioRECIPE interaction lists; 2) convert BioRECIPE interaction lists into INDRA statements.

### 1. Retrieving Statements from the INDRA DB and Converting to BioRECIPE interaction lists

#### Table of Contents

1. [Literature Queries for PMC](#literature-queries-for-pmc)
2. [Retrieve Literature Corpus from PMC](#retrieve-literature-corpus-from-pmc)
3. [Save PMCIDs List](#save-pmcids-list)
4. [Search INDRA Database for Statements](#search-indra-database-for-statements)

#### Literature Queries for PMC

1. Write one or more literature queries for use with PMC:
   - Combine terms with AND, OR, or NOT
   - Use quotation marks for phrases containing whitespace
   - Example: `E2F AND "cell cycle progression"`

2. Retrieve literature corpus from PMC by entering the query into the search box.

## Save PMCIDs List

3. Save the results as a list of PMCIDs:
   - First, filter to "Open access."
   - Select "File" as the destination and "PMCID List" as the format.

## Search INDRA Database for Statements

4. Use the script to search the INDRA database for all statements from the literature corpus.

### Setup Instructions

- Install INDRA with pip or by cloning the git repository.
- Install any other dependencies (you can skip Pyjnius; there are workarounds needed for Mac users).
- Set up the config file for Mac users:
  1. Open the config file using the following command:
     ```bash
     nano indra_config.ini
     ```
  2. Set the URL key; the API key can remain blank.

### Run Script

- Run the script with the following command:
  ```bash
   python run_biorecipe_from_pmcids.py -i input/ids.csv -o output/ids_biorecipe.xlsx

This command will extract statements from INDRA database given pmcids for query and convert them into our BioRECIPE interaction lists file named as ids_biorecipe.xlsx in this example. 

### 2. Convert BioRECIPE interaction lists into INDRA statements

Run the script with the following command:

```bash
python run_indra_from_biorecipe.py -i input/interaction_biorecipe.xlsx -o output/indra_stmts.json
```

