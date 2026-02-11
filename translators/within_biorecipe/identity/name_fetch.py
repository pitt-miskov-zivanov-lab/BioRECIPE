import time
import requests 
from typing import Union
from .description_fetch import DescriptionFetcher


TYPE_DB_MAP = {
    'protein': ['hgnc', 'uniprot'], 
    'chemical': ['chebi', 'pubchem', 'mesh'],
    'bioprocess': ['go'],
    'protein family': ['hgnc', 'interpro', 'pfam', 'fplx'],
    'protein complex': ['hgnc', 'uniprot', 'interpro', 'fplx'],
    'rna': ['refseq'],
    'gene': ['hgnc', 'gencode', 'ensembl', 'refseq']
}

class NameFetcher(DescriptionFetcher):
    def __init__(self):
        super().__init__()
    
    def fetch_name_by_id(self, db: str, id:str, return_num: Union[str, int]='all') -> Union[str, list, None]:
        db = self.map_database(db)

        if db.lower() == 'hgnc':
            data = self.fetch_hgnc_by_id(id)
            if data == "":
                return None 
            
        elif db.lower() == 'uniprot':
            data = self.fetch_uniprot_by_id(id)
            if data == "":
                return None
            else:
                name_list = []
                name_dict = data.get('proteinDescription', {})

                if 'recommendedName' in name_dict:
                    name_list.append(name_dict['recommendedName'].get('fullName', {}).get('value', ''))
                
                if 'alternativeNames' in name_dict:
                    if isinstance(name_dict['alternativeNames'], list):
                        for alt_name in name_dict['alternativeNames']:
                            name_list.append(alt_name.get('fullName', {}).get('value', ''))
                    
                    else:
                        return None
                

                name_list = [n for n in name_list if n != '']

                if isinstance(return_num, int):
                    return name_list[:min(return_num, len(name_list))] if len(name_list) > 0 else None

                elif return_num == 'all':
                    return name_list 
                else: 
                    raise ValueError('Unable to recognize number of name return...')
            
        elif db.lower() == 'chebi':
            url = f"https://www.ebi.ac.uk/chebi/backend/api/public/compound/{id}"
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()
                return data.get('name', None)
            
            elif response.status_code == 429:
                print("Too many requests...resending")
                time.sleep(5)
                self.fetch_name_by_id('chebi', id)

            else:
                return None
            
            
        elif db.lower() == 'pubchem':
            data = self.fetch_pubchem_by_id(id)
            if data == "":
                return None
            else:
                data = data.json()
                if 'InformationList' not in data:
                    return None
                else:
                
                    if isinstance(data['InformationList'].get('Information', None), list):
                        return data['InformationList']['Information'][0].get('Title', None)
                    else: 
                        return None

        
        elif db.lower() == 'go':
            data = self.fetch_go_by_id(id)
            if data == "":
                return None
            else:
                data = data.json()
                if 'results' not in data:
                    return None
                else:
                    if isinstance(data['results'], list) and len(data['results']) > 0:
                        return data['results'][0].get('name', None)
                    else:
                        return None
            
        elif db.lower() == 'mesh':
            data = self.fetch_mesh_by_id(id)
            if data == "":
                return None
            else:
                if 'results' in data and 'bindings' in data['results'] and len(data['results']['bindings']) > 0:
                    return data['results']['bindings'][0]['name']['value'].strip()
            return None
            
        elif db.lower() == 'interpro':
            data = self.fetch_interpro_by_id(id)
            if data == "":
                return None
            else:
                try:
                    metadata = data['metadata']
                    return metadata['name']['short'] if 'short' in metadata['name'].keys() else metadata['name']['name']
                    
                except KeyError as e:
                    print(e)
                    return None

        elif db.lower() == 'pfam':
            data = self.fetch_pfam_by_id(id)
            if data == '':
                return None
            else:
                try:
                    metadata = data['metadata']
                    return metadata['name']['name']
                except KeyError as e:
                    print(e)
                    return None
        
        else:
            print(f'No implementation of fetching data from {db}.')
            return None