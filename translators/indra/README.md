# INDRA-BioRECIPE Translator

# Retrieving Statements from the INDRA DB

This repository contains a set of instructions and scripts to retrieve statements from the INDRA database based on literature queries using PMC (PubMed Central).

## Table of Contents

1. [Literature Queries for PMC](#literature-queries-for-pmc)
2. [Retrieve Literature Corpus from PMC](#retrieve-literature-corpus-from-pmc)
3. [Save PMCIDs List](#save-pmcids-list)
4. [Search INDRA Database for Statements](#search-indra-database-for-statements)

## Literature Queries for PMC

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
  python .\run_indra_pmcids_biorecipe.py -i .\ids.csv -o ..\..\examples\interaction_lists

The extracted statements file will be named as ids_reading.xlsx in this example. 
