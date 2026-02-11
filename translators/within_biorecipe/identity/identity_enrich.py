import os 
import sys
import re 
import json 
from typing import List, Dict, Iterable, Tuple, Union
from collections import abc
from .name_fetch import NameFetcher
from indra.databases import (hgnc_client, uniprot_client, chebi_client)
import gilda 

CROSS_REF_MAP = {
    'chebi': {'funct': chebi_client.get_pubchem_id, 'database': 'pubchem'},
    'hgnc': {'funct': hgnc_client.get_uniprot_id, 'database': 'uniprot'}
}

nf = NameFetcher()

# Return the key and value which have the most length of list in the dict 
pick_most = lambda x: sorted(x.items(), key=lambda item: len(item[1]) if isinstance(item[1], list) else 0, reverse=True)[0]

def update_dict_list(main_dict:dict, updates:dict): 
    for k, v in updates.items():
        if k not in main_dict:
            main_dict[k] = []
        updated = main_dict[k] + v 
        main_dict[k] = list(set(updated))
    return main_dict

def tokenize_name(name: str, entity_type:str=None, tokenizer='regex') -> List[str]:
    tokens = []

    if tokenizer == 'regex':
        if not entity_type: 
            tokens = re.findall(r'[A-Za-z0-9\u0370-\u03FF\-\ ]+', name)
        else:
            if entity_type.lower().strip() == 'chemical':
                tokens = re.findall(r'[A-Za-z0-9\u0370-\u03FF\-\(\)\,\ \+]+', name)
    else:
        # TODO: more domain specific tokenizers could be implemented
        raise NotImplementedError(f"Tokenizer {tokenizer} not implemented.")
    
    return tokens 

def replace_w_cross_ref(db: str, id: str) -> tuple:

    """
    replace to primary identifier if database is a secondary database,
    e.g. chebi -> pubchem, hgnc -> uniprot
    
    Parameters
    ----------
    db : str
        Database name, e.g. 'chebi', 'hgnc', 'pubchem', 'uniprot', etc.
    id : str
        Identifier in the database, e.g. 'CHEBI:12345', 'HGNC:12345', 'P12345', etc.
    
    Returns
    -------
    tuple
        A tuple of (primary_id, primary_db) if cross reference is successful, else (id, db)
    """

    if db.lower() in CROSS_REF_MAP:
        cross_ref = CROSS_REF_MAP[db.lower()]['funct'](id)
        cross_ref_db = CROSS_REF_MAP[db.lower()]['database']
        if cross_ref:
            return cross_ref, cross_ref_db
    
    return id, db


def map_id_to_name(id: str, db: str) -> Union[str, None]:
    """
    Fetch name based on identifier

    Parameters
    ----------
    id : str
        The identifier in the database, e.g. 'P12345'
    db : str
        The database name, e.g. 'uniprot'

    Return 
    -------
    str or None
        The name corresponding to the identifier or None if not found.
    """
    name = nf.fetch_name_by_id(db, id)
    if isinstance(name, list):
        return name[0] if len(name) > 0 else None
    return name


def map_name_to_id(name: str, 
                   context: str=None, 
                   organism: Union[list, str]=None, 
                   term:bool=False,
                   type:str='protein') -> Union[Dict[str, List[str]], None]:
    """
    Normalize a name to an identifier from databases such as HGNC, UniProt, ChEBI, PubChem 

    Parameters
    ----------
    name : str
        The name to be normalized, e.g. 'TP53', 'p53', etc.
    context : str, optional
        The context in which the name is used
    organism : list, optional
        The NCBI taxonomy IDs for targeting species, e.g. ['9606'] for homo sapiens.
    term: bool, optional
        whether to fetch the standard name from the database according to normalized ID
    type: str, optional
        if type specified, return the ids of prefered database, default is None.

    Returns
    -------
    dict or None
        A dictionary of matched identifiers or None if no match is found.
    """
    matches = gilda.ground(name, context=context, organisms=organism)

    xref_dict = {}
    if matches: 
        for match in matches:
            term_curie = match.term.get_curie()
            term_db, term_id = term_curie.split(':', 1)

            term_db, term_id = replace_w_cross_ref(term_db, term_id)
            if term_db not in xref_dict:
                xref_dict[term_db] = []
            xref_dict[term_db].append(term_id if term_db.lower() != 'go' else term_curie)
        if not term:
            term_name = name

        else:
            term_name = nf.fetch_name_by_id(term_db, term_id) 
            
            if term_name == None: 
                term_name = name

        return {
            'xref_dict': xref_dict, 
            'entity_name': term_name
        }
    
    return {
        'xref_dict': None, 
        'entity_name': name
    }

def map_names_to_ids(names: Iterable[str], 
                     contexts: Iterable[str]=None, 
                     organisms:Union[Iterable, List[str], None]=['9606'], 
                     terms: Union[Iterable[bool], bool]=False,
                     tokenize_query: bool=False, 
                     k: int=5, 
                     na_mask=None) -> Tuple[List, List, List]:
    
    """
    Map a list of names to their corresponding identifiers in databases such as HGNC, UniProt, ChEBI, PubChem

    Parameters
    ----------
    names : Iterable[str]
        An iterable of names to be normalized, e.g. ['TP53', 'p53', etc.]
    contexts : Union[Iterable[str], None], optional
        A list of contexts corresponding for element name
    organisms : Union[List[str], None], optional
        A list of NCBI taxonomy IDs for targeting species, e.g. ['9606'] or a single list to be applied to all names.
    terms : Union[Iterable[bool], bool], optional
        A list of booleans indicating whether to fetch the standard name from the database according to normalized ID for each name
    tokenize_query : bool, optional
        Whether to tokenize the query name before searching IDs 
    k : int, optional 
        The number of returning matches at most for each name 
    na_mask : Any, optional
        A value to replace names that cannot be mapped to any identifier.

    Returns
    -------
    Iterable[Union[Dict[str, str], None]]
        A list of dictionaries containing matched identifiers for each name or None if no match is found.
    """
    org_flag = False; term_flag = False
    assert contexts is None or len(contexts) == len(names), "Length of contexts must match length of names"
    if isinstance(organisms, abc.Iterable):
        if all(isinstance(x, list) for x in organisms):
            assert len(organisms) == len(names), "Length of organisms must match length of names"
            org_flag = True
    if isinstance(terms, abc.Iterable):
        if all(isinstance(x, list) for x in terms):
            assert len(terms) == len(names), "Length of terms must match length of names"
            term_flag = True
    

    dbs_container = []; ids_container = []
    for i, name in enumerate(names):
        # Normalize parameter setting
        context = contexts[i] if contexts is not None else None
        organism = organisms[i] if org_flag else organisms
        term = terms[i] if term_flag else terms

        # To support complex name, such as IL27/IL27RA, STAT3 (dimer), we seperate the names 
        # to get comprehensive IDs for each token.
        if tokenize_query: 
            token_names = tokenize_name(name)
        else: 
            token_names = [name]

        xref = {}
        for token in token_names: 
            d = map_name_to_id(token, context=context, organism=organism, term=term)
            token_xref = d['xref_dict']
            if not token_xref:
                continue 
            xref = update_dict_list(xref, token_xref)

        names[i] = d['entity_name'] if d else name
        db, ids = pick_most(xref) if xref else (None, None)
        dbs_container.append(db if db else na_mask)
        ids_container.append(ids[:min(k, len(ids))] if ids else na_mask)

    return list(names), dbs_container, ids_container


def map_ids_to_names(ids: Iterable[str], dbs: Iterable[str], na_mask=None) -> Tuple[List, List, List]: 
    """
    Map a list of id to their corresponding identifiers in databases such as HGNC, UniProt, ChEBI, PubChem

    Parameters
    ----------
    ids : Iterable[str]
        An iterable of ids to be mapped, e.g. ['P04637', '7157', etc.]
    dbs: Iterable[str]
        An iterable of database names corresponding to each id, e.g. ['uniprot', 'hgnc', etc.]
    na_mask : Any, optional
        A value to replace names that cannot be mapped to any identifier.
    
    Returns
    -------
    Tuple[List, List, List]
        A tuple of three lists: (names, dbs, ids), where names are the mapped names corresponding to each id and db.
    """
    assert len(ids) == len(dbs), "Length of ids must match length of dbs"

    names_container = []; 
    for id, db in zip(ids, dbs):
        name = map_id_to_name(id, db) if id and db else na_mask
        names_container.append(name)

    return names_container, dbs, ids