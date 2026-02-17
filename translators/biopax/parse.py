import os
import sys
from typing import List, Tuple, Union, Any
import networkx as nx
from networkx import DiGraph, MultiDiGraph
from tqdm import tqdm
import pybiopax
import pybiopax.biopax as pybp
from translators.biopax.vocabs import *

# Parsing BioPAX to networkx graph, also supporting BioRECIPE format translation 

class Biopax: 

    def __init__(self): 
        self.CONTROL_VOCABS = CONTROLTYPE_VOCABULARY
        self.CONTROL2SIGN = CONTROLTYPE2SIGN
        self.PRIME_DB = PRIME_DB

        self.temp_entity_dict = {
                        'name': None, 
                        'type': None, 
                        'subtype': None, 
                        'database': None, 
                        'ID': None,
                        'compartment': None,
                        'compartment ID': None}
        
        self.temp_interaction_dict = {
            # Required information
            'src': None,
            'tgt': None,
            # Optional info: attributes 
            'sign': None,
            'mechanism': None,
            'site': None,
            'connection type': None,
            # Provenance properties
            'source': None,
            'statements': None,
            'paper ids': None
        }


        # Used for store temporary value during parsing
        self.__buffer_uid = None # Return additional nodes uid for merging entity list in genetic interactions
        self.__buffer_dict = None 

    def biopax2network(self, input_file=None, input_str=None, multi_xrefs=True):

        model = None
        network = DiGraph()

        if isinstance(input_file, str):
            basename = os.path.basename(input_file)
            name, ext = os.path.splitext(basename)

            if ext not in ['.owl', '.xml']: 
                raise ValueError(f"Unsupported file format: {ext}.")
            
            else: 
                model = pybiopax.model_from_owl_file(input_file)
                
            
        elif isinstance(input_str, str):
            model = pybiopax.model_from_owl_str(input_str)
            
        # Parse entity and relations
        entities, relations = self._parse_graph(model, multi_xrefs)
        network.add_nodes_from(entities)
        network.add_edges_from(relations)

        return network, entities, relations
            
    def biopax2tabular(self, input_file=None, input_str=None, multi_xrefs=False):
        """
        Convert BioPAX file to tabular output

        Parameters
        ----------
        input_file: str
            Path of the input BioPAX file (.owl or .xml)
        input_str: str
            String of the input BioPAX content used for API response data
        return_prime: bool
            Whether to prioritize returning xref from PRIME_DB, default True
        xid: bool
            Whether to include multiple xrefs in the output, default False
            
        Returns
        -------
        entities: list of tuples 
            (uid, {entity attributes})
        relations: list of tuples
            (source uid, target uid, {relation attributes})
        """
        if isinstance(input_file, str):
            basename = os.path.basename(input_file)
            name, ext = os.path.splitext(basename)

            if ext not in ['.owl', '.xml']: 
                raise ValueError(f"Unsupported file format: {ext}.")
            
            else: 
                model = pybiopax.model_from_owl_file(input_file)
                
            
        elif isinstance(input_str, str):
            model = pybiopax.model_from_owl_str(input_str)

        
        return self._parse_graph(model, multi_xrefs)
        
    def _parse_graph(self, model, multi_xrefs=False): 
        """
        Parse BioPAX model and return the entities list and relations list for adding nodes and edges
        
        Parameters
        ----------

        model: pybiopax model object

        Returns
        -------
        entities: list of tuples 
            (uid, {entity attributes})
        relations: list of tuples 
            (source uid, target uid, {relation attributes})
        """
        entities = {}; relations = []
        pbar = tqdm(model.objects.items(), desc="Parsing BioPAX model objects")
        for term, obj in pbar:
            if isinstance(obj, (pybp.PhysicalEntity, pybp.Gene, pybp.Pathway)):
                entity_dict = self.parse_entity(obj, multi_xrefs)
                uid = obj.uid
                entities[uid] = entity_dict

            if isinstance(obj, pybp.Interaction):
                rel_list = self.parse_interaction(obj)
                # Check if we created a new node for genetic interaction
                if isinstance(obj, pybp.GeneticInteraction):
                    uid = self.__buffer_uid
                    entity_dict = self.__buffer_dict
                    entities[uid] = entity_dict

                relations += rel_list

        entities = [(uid, x) for uid, x in entities.items()]
        relations = [(x['src'], 
                      x['tgt'], 
                      {k:v for k, v in x.items() if k not in ['src', 'tgt']})
                      for x in relations]
        
        return entities, relations
        
    def parse_entity(self, obj: Union[pybp.PhysicalEntity, pybp.Gene, pybp.Pathway], multi_xrefs=False) -> dict:

        # Template
        element_dict = self.temp_entity_dict.copy()
        # Parse
        element_dict['name'] = obj.standard_name or obj.display_name or obj.term
        element_dict['type'] = BPTYPE2BIORECIPE.get(type(obj).__name__, '')
        xref_db, xref_ids = self._parse_entity_xref(obj, multi_xrefs)
        element_dict['database'] = xref_db; element_dict['ID'] = xref_ids

        if not isinstance(obj, (pybp.Pathway, pybp.Gene)):
            compartment = obj.cellular_location if obj.cellular_location else None
            element_dict['compartment'] = compartment.term[0] if compartment else None
        return element_dict

    def parse_interaction(self, obj: pybp.Interaction) -> List[Any]:

        # Template 
        interaction_dict = self.temp_interaction_dict.copy()
        interacts_list = []

        provenance_attr = self._parse_provenance(obj)
        interaction_dict.update(provenance_attr)
        
        if isinstance(obj, pybp.Control): 

            srcs = obj.controller
            tgts = obj.controlled
            interaction_dict['src'] = srcs[0].uid if srcs else None

            # TODO: translate it with a binary abstraction for now
            # The controlled entity is either an interaction (e.g., BiochemicalReaction) or a pathway
            if isinstance(tgts, pybp.Pathway):
                tgts = [tgts] 
            else:
                # tgts = [x for x in tgts.right if not isinstance(x, pybp.SmallMolecule)]
                if isinstance(tgts, pybp.BiochemicalReaction):
                    tgts = [x for x in tgts.right]
                    mechanism = obj.control_type.lower() if obj.control_type else None
                    interaction_dict['mechanism'] = mechanism 
                    sign = self.CONTROL2SIGN.get(mechanism, None)
                    interaction_dict['sign'] = sign
                elif isinstance(tgts, pybp.TemplateReaction):
                    tgts = [x for x in tgts.product]
                    mechanism = obj.control_type.lower() if obj.control_type else None
                    interaction_dict['mechanism'] = mechanism
                    sign = self.CONTROL2SIGN.get(mechanism, None)
                    interaction_dict['sign'] = sign
                # TODO: add more interaction type here
                else:
                    return []


            for tgt in tgts:
                interact_i = interaction_dict.copy()
                interact_i['tgt'] = tgt.uid
                interacts_list.append(interact_i)
        # TODO: current add placeholder for other interaction types 
        elif isinstance(obj, pybp.Conversion):
            pass

        elif isinstance(obj, pybp.GeneticInteraction):
            src_list = obj.participant if obj.participant else None
            tgt = getattr(obj, 'phenotype', None)
            group_dict = self._merge_entity_list(src_list)
            self.__buffer_uid = obj.display_name
            self.__buffer_dict = {k: ','.join(v) for k, v in group_dict.items()}
            interaction_dict['src'] = self.__buffer_uid
            interaction_dict['sign'] = None
            interaction_dict['mechanism'] = None
            interaction_dict['site'] = None
            interaction_dict['connection type'] = 'i'
            if src_list and tgt: 
                interaction_dict['src'] = self.__buffer_uid
                interaction_dict['tgt'] = tgt.uid
                interacts_list += [interaction_dict]

        # Molecular interaction is undirected, mainly serving for ppi 
        elif isinstance(obj, pybp.MolecularInteraction):
            pass

        # template reaction
        # mainly serving for DNA->RNA(transcription), RNA->protein(translation) 
        elif isinstance(obj, pybp.TemplateReaction): 
            pass
            
        else: 
            pass
        
        return interacts_list
    
    def _parse_provenance(self, obj: pybp.Interaction): 
        # TODO: parse provenance info for interactions
        source = obj.data_source[0].display_name if obj.data_source else None
        statement = obj.evidence[0].evidence_code.term[0] if obj.evidence else None
        paper_ids = f'{obj.xref[0].db}:{obj.xref[0].id}' if obj.xref else None
        return {
            'source': source,
            'statements': statement,
            'paper ids': paper_ids
        }

    def _parse_entity_xref(self, obj: Union[pybp.PhysicalEntity, pybp.Gene], multi_xrefs=True):
        ele_ref = dict() 

        xrefs = obj.xref if obj.xref else None
        if not xrefs:
            return None, None
        
        # xrefs = [x for x in list(xrefs) if isinstance(x, pybp.UnificationXref)]
        xrefs = list(xrefs)

        for xref in xrefs: 
            if str(xref.db).strip().lower() in self.PRIME_DB:
                if xref.db not in ele_ref:
                    ele_ref[xref.db] = []
                ele_ref[xref.db].append(xref.id) 

        # Passive return the first xref if no prime db
        if len(ele_ref) == 0: 
            xref = xrefs[0]
            return xref.db, xref.id
        
        # Sort the database include the most id, return the db include the most xrefs 
        ele_ref = {k: list(set(v)) for k, v in ele_ref.items()}
        db = max(ele_ref, key=lambda k: len(ele_ref[k]))
        if multi_xrefs: 
            entity_db = db
            entity_ids = ','.join(ele_ref[db])
        else: 
            entity_db = db
            entity_ids = ele_ref[db][0]
        return entity_db, entity_ids
                

    # TODO: currently we only merge entity lists for genes
    def _merge_entity_list(self, entity_list: List[pybiopax.biopax.base.Gene]):

        group_dict = {k: [] for k in self.temp_entity_dict.keys()}
        for entity_obj in entity_list: 
            element_dict = self.parse_entity(entity_obj)
            for k, v in element_dict.items():
                if v is not None:
                    group_dict[k].append(v)
                else:
                    group_dict[k].append('None')

        return group_dict
            

def sample_test(): 
    biopax_parser = Biopax()
    test_dir = '../../examples/biopax'

    # If you want to test the files not in example folder, please download them from 
    # https://github.com/BioPAX/specification/tree/master/Level3/examples
    # # ControlInteraction test
    # filename = 'biopax3-phosphorylation-reaction.owl'

    # Conversion test
    # ...

    # GeneticInteraction test
    # filename = 'biopax3-genetic-interaction.owl'

    # MolecularInteraction (PPI) test
    # ...

    # TemplateReaction test
    # ...

    # Pathway Commons test
    # filename = 'Transcriptional_acti.xml'

    # Pathway Commons - KEGG test
    filename = 'Vitamin_B6_metabolis.xml'

    # Pathway Commons - Reactome test
    # filename = 'R-HSA-70171_level3.owl'
    # filename = 'HCMV_Early_Events.xml'

    # Pathway Commons - PID test 
    filename = 'IL27-mediated_signal.xml'
    g, ents, rels = biopax_parser.biopax2network(os.path.join(test_dir, filename))
    print(g.nodes(data=True))
    print(g.edges(data=True))
            

if __name__ == "__main__":
    sample_test()