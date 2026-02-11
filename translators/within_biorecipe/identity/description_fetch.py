import os
import sys
import glob 
import json
import pandas as pd
import numpy as np
from tqdm import tqdm

from argparse import ArgumentParser

import requests
from bioregistry import parse_curie, normalize_curie
from Bio import Entrez, SeqIO

class DescriptionFetcher:
    """
    A class to fetch descriptions from various biological databases. The class fetch the descriptions
    with url requests. Supported databases include UniProt, ChEBI, PubChem, GO, InterPro, Pfam, RefSeq, and MeSH.
    Ensembl and GENCODE does not include auxiliary information for entities, so they are not included in this class.
    """

    def __init__(self):

        self.uniprot_url = "https://rest.uniprot.org/uniprotkb/"
        self.pubchem_url = "https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/cid/"
        self.go_url = "http://www.ebi.ac.uk/QuickGO/services/ontology/go/"
        self.interpro_url = "https://www.ebi.ac.uk/interpro/api/entry/interpro/"
        self.pfam_url = "https://www.ebi.ac.uk/interpro/api/entry/pfam/"
        self.refseq_url = "https://clinicaltables.nlm.nih.gov/api/refseqs/v3/search"
        self.mesh_query = ""

    def error_handler(self, response):
        """
        Handle errors from API responses.
        """
        if response.status_code == 404:
            return "ID not found.", -1
        elif response.status_code == 400: 
            return "Bad request. Please check the ID format.", -1
        elif response.status_code == 500:
            return "Internal server error.", -1
        elif not response.ok:
            return f"Error fetching data: {response.status_code} - {response.reason}", -1
        elif response.status_code == 200:
            return "Success", response
        else:
            return f"Unknown error({response.status_code}).", -1
    
    def get_description_by_id(self, database: str, id: str) -> str:
        """
        Fetches the description of a given ID from the specified database.
        Args:
            database (str): The name of the database to query ('uniprot', 'chebi', 'pubchem', 'go', 'interpro', 'pfam', 'mesh').
            id (str): The identifier for the entity in the specified database.
        Returns:
            str: The description of the entity, or an empty string if not found.
        """
        db = self.map_database(database)

        if db == 'uniprot':
            data = self.fetch_uniprot_by_id(id)
            if data == "":
                return ""
            else:
                comments = data.get("comments", [])
                func = next((c for c in comments if c.get("commentType") == "FUNCTION"), None)
                if func and "texts" in func and func["texts"]:
                    return func["texts"][0].get("value", "").strip()

        elif db == 'chebi':
            data = self.fetch_chebi_by_id(id)
            if data == "":
                return ""
            else:
                return data.get("definition", "")
            
        elif db == 'pubchem':
            data = self.fetch_pubchem_by_id(id)
            if data == "":
                return ""
            else:
                info = data.get("InformationList", [])
                data_description = ""
                if info and "Information" in info:
                    for item in info["Information"]:
                        if "Description" in item.keys():
                            data_description += item["Description"] + "\n"
                    return data_description.strip()
    
        elif db == 'go':
        
            data = self.fetch_go_by_id(id)
            if data == "":
                return ""
            else:
                if 'results' in data and len(data['results']) > 0:
                    if id in [x["id"] for x in data['results']]:
                        return data['results'][0]['definition'].get('text', '').strip()
                else:
                    return ""
                
        elif db == 'interpro':
            data = self.fetch_interpro_by_id(id)
            if data == "":
                return ""
            else:
                text = ""
                if 'metadata' in data and 'description' in data['metadata']:
                    description = data['metadata']['description']
                    if isinstance(description, list) and len(description) > 0:
                        for desc in description: 
                            if isinstance(desc, dict) and 'text' in desc:
                                text += desc['text'] + "\n"
                        return text.strip()
                return ""
            
        elif db == 'pfam':
            data = self.fetch_pfam_by_id(id)
            if data == "":
                return ""
            else:
                text = ""
                if 'metadata' in data and 'description' in data['metadata']:
                    description = data['metadata']['description']
                    if isinstance(description, list) and len(description) > 0:
                        for desc in description: 
                            if isinstance(desc, dict) and 'text' in desc:
                                text += desc['text'] + "\n"
                        return text.strip()
                else: 
                    return ""
                
        elif db == 'refseq':
            data = self.fetch_refseq_by_id(id)
            if data == "":
                return ""
            else:
                return data.annotations['comment']

        elif db == 'mesh':
            data = self.fetch_mesh_by_id(id)
            if data == "":
                return ""
            else:
                if 'results' in data and 'bindings' in data['results'] and len(data['results']['bindings']) > 0:
                    return data['results']['bindings'][0]['scopeNote']['value'].strip()
                else:
                    return ""

        # For unseen database or 'other' database
        else:
            return ""
        
    def fetch_uniprot_by_id(self, id: str) -> str:
        """
        Fetches the description from UniProt for a given ID.
        """
        url = f"{self.uniprot_url}{id}.json"
        response = requests.get(url, timeout=10)
        status, res = self.error_handler(response)
        try:
            if res != -1:
                data = res.json()
                return data
            else:
                return ""
        except Exception as e:
            print(f"Error parsing JSON response for {id} from UniProt: {e}")
            print(res)
            sys.exit(1)
            return ""

    def fetch_chebi_by_id(self, id: str) -> str:
        """
        Fetches the description from ChEBI for a given ID.
        """
        url = f"https://www.ebi.ac.uk/chebi/backend/api/public/compound/{id}"
        response = requests.get(url, timeout=10)
        status, res = self.error_handler(response)
        try:
            if res != -1:
                data = res.json()
                return data
            else:
                return ""
        except Exception as e:
            print(f"Error parsing JSON response for {id} from UniProt: {e}")
            print(res)
            sys.exit(1)
            return ""


    def fetch_pubchem_by_id(self, id: str) -> str:
        """
        Fetches the description from PubChem for a given ID.
        """
        url = f"{self.pubchem_url}{id}/description/JSON"
        response = requests.get(url, timeout=10)
        status, res = self.error_handler(response)
        if res != -1:
            data = res.json()
            return data
        else:
            print(f"Error fetching data for {id} from PubChem.")
            return ""

    def fetch_go_by_id(self, id: str) -> str:
        """
        Fetches the description from GO for a given ID.
        """
        if id.startswith('GO:') or id.startswith('go:'):
            pass
        else:
            id = f"GO:{id}"

        url = f"{self.go_url}search?query={id}"
        response = requests.get(url, timeout=10)
        status, res = self.error_handler(response)
        if res != -1:
            return res.json()
        else:
            print(f"Error fetching data for {id} from GO.")
            return ""

    def fetch_interpro_by_id(self, id: str) -> str:
        """
        Fetches the description from InterPro for a given ID.
        """
        url = f"{self.interpro_url}{id}/"
        response = requests.get(url, timeout=10)
        status, res = self.error_handler(response)
        if res != -1:
            return res.json()
        else:
            print(f"Error fetching data for {id} from InterPro.")
            return ""

    def fetch_pfam_by_id(self, id: str) -> str:
        """
        Fetches the description from Pfam for a given ID.
        """
        url = f"{self.pfam_url}{id}/"
        response = requests.get(url, timeout=10)
        status, res = self.error_handler(response)
        if res != -1:
            return res.json()
        else:
            print(f"Error fetching data for {id} from Pfam.")
            return ""

    def fetch_refseq_by_id(self, id: str) -> str:
        """
        Fetches the data from Ensembl for a given ID.
        """
        handle = Entrez.efetch(db="nucleotide", id=id, rettype="gb", retmode="text")
        if handle is None:
            print(f"Error fetching data for {id} from RefSeq.")
            return ""
        else:
            try:
                record = SeqIO.read(handle, "genbank")
                return record 
            except Exception as e:
                print(f"Error parsing data for {id} from RefSeq: {e}")
                handle.close()
            return ""
        
    def fetch_mesh_by_id(self, id: str) -> str:
        """
        Fetches the description from MeSH for a given ID.
        """
        if not id.startswith('D') and not id.startswith('d'):
            # raise ValueError(f"MeSH ID should start with 'D', got {id}")
            print(f"MeSH ID should start with 'D', got {id}")

        url = f"https://id.nlm.nih.gov/mesh/sparql"
        q = f"""
        PREFIX meshv: <http://id.nlm.nih.gov/mesh/vocab#>
        PREFIX mesh: <http://id.nlm.nih.gov/mesh/>
        SELECT ?name ?scopeNote
        WHERE {{
            mesh:{id} meshv:preferredConcept ?concept .
            ?concept meshv:preferredTerm/meshv:prefLabel ?name .
            ?concept meshv:scopeNote ?scopeNote .
        }}
        """
        response = requests.get(url, params={"query": q}, headers={"Accept": "application/sparql-results+json"}, timeout=10)
        status, res = self.error_handler(response)
        if res != -1:
            try:
                results = res.json()
                print(f'find results for {id}')
            except requests.exceptions.JSONDecodeError:
                # print(res)
                # print(id)
                results = ""
            return results
        else:
            print(f"Error fetching data for {id} from MeSH.")
            return ""
    

    @staticmethod
    def map_database(db) -> str:
        """
        Maps the database name to a standardized format.
        """
        db = DescriptionFetcher._lower_n_strip(db)
        if db in ['uniprot', 'up']:
            return 'uniprot'
        elif db in ['chebi']:
            return 'chebi'
        elif db in ['pubchem', 'pubchem.compound', 'pubchem.compounds']:
            return 'pubchem'
        elif db in ['go']:
            return 'go'
        elif db in ['interpro']:
            return 'interpro'
        elif db in ['pfam']:
            return 'pfam'
        elif db in ['mesh']:
            return 'mesh'
        elif db in ['ensembl', 'ensembl.gene', 'ensembl.bacteria', 'ensembl.fungi']:
            return 'ensembl'
        elif db in ['other', 'text', 'txt', 'famplex']:
            return 'other'
        elif db in ['fplx']:
            return 'fplx'
        else:
            print(f"Database '{db}' is not supported.")
            return 'other'

    @staticmethod
    def _lower_n_strip(s) -> str:
        if isinstance(s, str):
            return s.lower().strip()
        else:
            return str(s).lower().strip()
        
    @staticmethod 
    def _id2query(database: str, id: str) -> str:
        """
        Convert id to a valid query string for the respective database.
        """
        db, id = parse_curie(database + ':' + id)
        
        return db, id





def main(input=None, input_dir=None, output_file=None):
    if input is None and input_dir is None:
        raise ValueError("Either input file or input directory must be provided.")
    
    if input is not None and input_dir is not None:
        raise ValueError("Only one of input file or input directory should be provided, not both.")
    
    if input is not None:
        input = [input]

    else:
        input = glob.glob(os.path.join(input_dir, '*.csv'))

    desc_fetcher = DescriptionFetcher()
    desc_dict = {}
    for f in input:
        if not os.path.isfile(f):
            raise ValueError(f"File {f} does not exist.")
        input_df = pd.read_csv(f, index_col=None)
        pbar = tqdm(input_df.iterrows(), total=input_df.shape[0], desc=f"Processing {os.path.basename(f)}")

        for row in pbar:
            _, v = row

            if v['Regulator ID'] in desc_dict:
                pass
            else:
                desc_dict[v['Regulator ID']] = {}
                rr = desc_fetcher.get_description_by_id(v['Regulator Database'], v['Regulator ID'])
                desc_dict[v['Regulator ID']]['description'] = rr
                desc_dict[v['Regulator ID']]['name'] = v['Regulator Name']
                desc_dict[v['Regulator ID']]['database'] = desc_fetcher.map_database(v['Regulator Database'])
            if v['Regulator ID'] == v['Regulated ID']:
                pass
            else:
                if v['Regulated ID'] in desc_dict:
                    continue
                desc_dict[v['Regulated ID']] = {}
                rd = desc_fetcher.get_description_by_id(v['Regulated Database'], v['Regulated ID'])
                desc_dict[v['Regulated ID']]['description'] = rd
                desc_dict[v['Regulated ID']]['name'] = v['Regulated Name']
                desc_dict[v['Regulated ID']]['database'] = desc_fetcher.map_database(v['Regulated Database'])

        with open(output_file, 'w') as out_f:
            json.dump(desc_dict, out_f, indent=4)
            
        


if __name__ == "__main__":
    arguments = ArgumentParser("A parser to fetch description from different databases.")

    arguments.add_argument('--input_file', type=str, required=False, help='Input CSV file containing IDs and database names.')
    arguments.add_argument('--input_dir', type=str, required=False, help='Input directory containing multiple CSV files with IDs and database names.')
    arguments.add_argument('--output_dir', type=str, required=False, help='Output directory to save the results.')

    args = arguments.parse_args()

    main(input=args.input_file, input_dir=args.input_dir, output_file=args.output_dir)

    