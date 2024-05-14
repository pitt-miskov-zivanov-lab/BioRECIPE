import argparse
import pandas as pd
import sys
import json
import re
from collections import defaultdict

try:
    import indra
    import indra.statements
except:
    print('indra import failed')

# Define column names for DySE format
# TODO: import interactions object from class based on interactions.py
_COLNAMES = [
    # Provenance attributes
    'Source', 'Reader', 'Evidence', 'Evidence Index', 'Notes',
    # Element variable and attributes
    'Element Variable',
    'Element Name', 'Element Text', 'Element Database', 'Element ID', 'Element Type',
    'Element Agent', 'Element Patient',
    'Element ValueJudgment', 'Element Scope',
    'Element Level', 'Element Change', 'Element Degree',
    'Element Location', 'Element Timing',
    # Interaction function and attributes
    'Interaction Function', 
    'Interaction Name', 'Interaction Text', 'Interaction ID', 'Interaction Type', 
    'Interaction Degree',
    'Interaction Location', 'Interaction Timing',
    # Regulator variable and attributes
    'Regulator Variable',
    'Regulator Name', 'Regulator Text', 'Regulator Database', 'Regulator ID', 'Regulator Type',
    'Regulator Agent', 'Regulator Patient',
    'Regulator ValueJudgment', 'Regulator Scope',
    'Regulator Level', 'Regulator Change', 'Regulator Degree',
    'Regulator Location', 'Regulator Timing',
    # Scoring metrics
    'Reader Count', 'Source Count', 'Evidence Count',
    'Total Score', 'Kind Score', 'Match Level', 'Epistemic Value', 'Belief'
    ]

def convert_indra_statements(statements, belief_threshold=0, ontology='WM') -> pd.DataFrame:
    """Process INDRA statements and convert to tabular format
    """

    global _COLNAMES

    final = pd.DataFrame(columns=_COLNAMES)

    # TODO: utilize dataframes rather than looping?
    for statement in statements:
        if (type(statement) is indra.statements.Influence
            and statement.belief > belief_threshold):

            thisrow = dict()

            # Cause attributes
            thisrow['Regulator Text'] = str(
                    getattr(getattr(statement.subj, 'concept', ''), 'db_refs', {}).get('TEXT', '')
                    )
            ontology_name = getattr(getattr(statement.subj, 'concept',''), 'db_refs', {}).get(ontology, '')
            if type(ontology_name) is list:
                # list of ontology terms sorted by grounding value, get first
                ontology_name = ontology_name[0][0]
            thisrow['Regulator Name'] = str(ontology_name)
            thisrow['Regulator Agent'] = write_out(
                [x.annotations.get('agent','') for x in statement.subj.evidence]
                )
            thisrow['Regulator Patient'] = write_out(
                [x.annotations.get('patient','') for x in statement.subj.evidence]
                )
            # thisrow['Regulator Level'] = 
            thisrow['Regulator Change'] = str(
                    getattr(getattr(statement.subj, 'delta', ''), 'polarity', '')
                    )
            thisrow['Regulator Degree'] = write_out(
                    getattr(getattr(statement.subj, 'delta', ''), 'adjectives', '')
                    )
            # thisrow['Regulator Scope'] = 
            thisrow['Regulator Location'] = str(
                    getattr(getattr(getattr(statement.subj, 'context', ''), 'geo_location', ''), 'name', '')
                    )
            thisrow['Regulator Timing'] = str(
                    getattr(getattr(getattr(statement.subj, 'context', ''), 'time', ''), 'text', '')
                    )
                    
            # Effect attributes
            thisrow['Element Text'] = str(
                    getattr(getattr(statement.obj, 'concept', ''), 'db_refs', {}).get('TEXT', '')
                    )
            ontology_name = getattr(getattr(statement.obj, 'concept',''), 'db_refs', {}).get(ontology, '')
            if type(ontology_name) is list:
                # list of ontology terms sorted by grounding value, get first
                ontology_name = ontology_name[0][0]
            thisrow['Element Name'] = str(ontology_name)
            thisrow['Element Agent'] = write_out(
                [x.annotations.get('agent','') for x in statement.obj.evidence]
                )
            thisrow['Element Patient'] = write_out(
                [x.annotations.get('patient','') for x in statement.obj.evidence]
                )
            # thisrow['Element Level'] = 
            thisrow['Element Change'] = str(
                    getattr(getattr(statement.obj, 'delta', ''), 'polarity', '')
                    )
            thisrow['Element Degree'] =  write_out(
                    getattr(getattr(statement.obj, 'delta', ''), 'adjectives', '')
                    )
            # thisrow['Element Scope'] = 
            thisrow['Element Location'] = str(
                    getattr(getattr(getattr(statement.obj, 'context', ''), 'geo_location', ''), 'name', '')
                    )
            thisrow['Element Timing'] = str(
                    getattr(getattr(getattr(statement.obj, 'context', ''), 'time', ''), 'text', '')
                    )
            
            thisrow['Interaction Text'] = write_out(
                    [x.annotations.get('Relation', '') for x in statement.evidence]
                    )
            # thisrow['Interaction Type'] = 
            # thisrow['Interaction ID'] = 
            # thisrow['Interaction Degree'] = 
            # thisrow['Interaction Location'] = 
            # thisrow['Interaction Timing'] = 

            # get source documents
            thisrow['Source'] = write_out([x.pmid for x in statement.evidence])
            thisrow['Reader'] = write_out([x.source_api for x in statement.evidence])
            # TODO: reader formats for provenance are not standardized (don't always include the @id tag),
            # so just converting to a string, but could use the code below to access the sentence id using @id
            # thisrow['Evidence Index'] = write_out(
            #         [y['sentence']['@id'] for x in statement.evidence for y in x.annotations.get('provenance','')])
            # thisrow['Evidence Index'] = write_out(
            #         [str(y['sentence']) for x in statement.evidence for y in x.annotations.get('provenance','')])
            thisrow['Evidence'] = write_out([x.text for x in statement.evidence])
            thisrow['Belief'] = str(statement.belief)

            final = final.append(thisrow, ignore_index=True)
        
    final = final.fillna('')      

    return final

def convert_bbn_jsonld(input_file) -> pd.DataFrame:
    """Process BBN's World Modelers json-ld format 
    """

    global _COLNAMES

    source_types = ['has_cause', 'has_catalyst', 'has_mitigating_factor',
                    'has_precondition', 'has_preventative', 'has_before',
                    'giver', 'agent', 'attacker', 'origin', 'instrument',
                    'left_arg', 'left_argument']
    target_types = ['has_effect', 'has_after',
                    'target', 'victim', 'recipient', 'audience',
                    'entity', 'person', 'thing',
                    'right_arg', 'right_argument']

    final = pd.DataFrame(columns=_COLNAMES)

    with open(input_file) as json_file:
        reading = json.load(json_file)

    # get document titles/IDs
    docs = dict()
    for this_doc in reading['documents']:
        if 'title' in this_doc.keys():
            title = this_doc['title']
        else:
            title = this_doc['@id']

        docs[this_doc['@id']] = title

    # format extractions into a dict with IDs for keys
    extractions = dict()
    for this_extraction in reading['extractions']:
        # print(this_extraction.keys())
        type_ = this_extraction['@type']
        # TODO: not sure if event and entity types are needed anymore
        if type_ in ['Event','Entity', 'Extraction']:
            canonical_name = this_extraction.get('canonicalName','')

            # TODO: preserve several top grounding terms
            grounding = max([[g['value'],g['ontologyConcept']] 
                for g in this_extraction.get('grounding',[])], default=[''])[-1]

            text = []
            document = []
            sentence = []
            if 'mentions' in this_extraction.keys():
                text += [x['text'] for x in this_extraction['mentions']]
                document += [x['provenance']['document']['@id'] for x in this_extraction['mentions']]
            
            if 'text' in this_extraction.keys():
                text += [this_extraction['text']]
            
            if 'provenance' in this_extraction.keys():
                #TODO: may be more than one provenance but currently assumes one
                if isinstance(this_extraction['provenance'], dict):
                    document += this_extraction['provenance']['document']['@id']
                elif isinstance(this_extraction['provenance'], list):
                    document += [x['document']['@id'] for x in this_extraction['provenance']]



                # # Code below is a hack to get document text but isn't aligned properly with the sentences
                # text_indices = [x['documentCharPositions'] 
                #     for x in this_extraction['provenance']]
                # sentence += [docs[s]['text'][text_indices[i]['start']:text_indices[i]['end']] 
                #     for i,s in enumerate(document_ids)]
            
            ext_type = this_extraction.get('type','')

            labels = this_extraction.get('labels','')

            if 'trigger' in this_extraction.keys():
                trigger = this_extraction['trigger']['text']
            else:
                trigger = ''
            
            # arguments include place, time for non-relations; causes/effects for relations
            location = []
            time = []
            sources = []
            targets = []
            for arg in this_extraction.get('arguments',[]):
                arg_type = arg['type'].lower()
                # TODO: no arguments have more than one id in value?
                arg_val = [arg['value']['@id']]
                if arg_type in ['place', 'destination', 'origin']:
                    location += arg_val
                elif arg_type in ['time']:
                    time += arg_val
                elif arg_type in source_types:
                    sources += arg_val #[x['@id'] for x in arg.get('value',[])]
                elif arg_type in target_types:
                    targets += arg_val
                elif arg_type in ['group','member']:
                    # TODO: use group, member, left/right argument relations between entities?
                    pass
                else:
                    print('Unrecognized argument type: ' + str(arg_type))

            change = []
            level = []
            polarity = []
            modality = []
            genericity = []
            for state in this_extraction.get('states',[]):
                state_type = state['type'].lower()
                # FIXME: states can be attached to different words, spatial increase, value increase etc.
                # states have type, text, (provenance), (modifiers)
                if state_type in ['inc','dec']:
                    change += [state['type']]
                elif state_type in ['quant']:
                    level += [state['text']]
                elif state_type in ['polarity']:
                    polarity += [state['text']]
                elif state_type in ['modality']:
                    modality += [state['text']]
                elif state_type in ['genericity']:
                    genericity += [state['text']]
                else:
                    print('Unrecognized state type: ' + str(state))
            
            # TODO: keep degree attached to state?
            degree = [y.get('text') for x in this_extraction.get('states',[]) 
                for y in x.get('modifiers',[])]

            extractions[this_extraction['@id']] = {
                'canonicalName' : canonical_name, 
                'grounding' : grounding,
                'text' : text, 
                'document' : document,
                'sentence' : sentence,
                'type' : ext_type,
                'labels' : labels,
                'trigger' : trigger,
                'sources' : sources,
                'targets' : targets,
                'change' : change, 
                'level' : level,
                'degree' : degree,
                'polarity' : polarity,
                'modality' : modality,
                'genericity' : genericity,
                'location' : location,
                'time' : time
                }
        else:
            print('Unrecognized type: ' + str(type_))
            
    # get relations from json file and write to final
    for id_, this_extraction in extractions.items():
        type_ = this_extraction['type']
        if re.search('-Effect',type_):
            thisrow = dict()

            # Cause attributes
            # TODO: deal with multiple causes
            if len(this_extraction.get('sources',[])) > 1:
                print('Warning: more than one source')
            
            # index the source object from this_extraction ID
            source = extractions[this_extraction['sources'][0]]

            # TODO: use canonical name for something?
            # TODO: use modality?
            thisrow['Regulator Text'] = write_out(source['text'])
            thisrow['Regulator Name'] = source['grounding']
            thisrow['Regulator Agent'] = write_out(source['sources'])
            thisrow['Regulator Patient'] = write_out(source['targets'])
            thisrow['Regulator Level'] = write_out(source['level'])
            thisrow['Regulator Change'] = write_out(source['change'])
            thisrow['Regulator Degree'] = write_out(source['degree'])
            thisrow['Regulator Scope'] = write_out(source['genericity'])
            thisrow['Regulator Location'] = write_out(source['location'])
            thisrow['Regulator Timing'] = write_out(source['time'])
                    
            # Effect attributes
            # TODO: deal with multiple effects, nested effects
            if len(this_extraction.get('targets',[])) > 1:
                print('Warning: more than one target')

            # index the target object from this_extraction ID
            target = extractions[this_extraction['targets'][0]]
            
            thisrow['Element Text'] = write_out(target['text'])
            thisrow['Element Name'] = target['grounding']
            thisrow['Element Agent'] = write_out(source['sources'])
            thisrow['Element Patient'] = write_out(source['targets'])
            thisrow['Element Level'] = write_out(target['level'])
            thisrow['Element Change'] = write_out(target['change'])
            thisrow['Element Degree'] = write_out(target['degree'])
            thisrow['Element Scope'] = write_out(target['genericity'])
            thisrow['Element Location'] = write_out(target['location'])
            thisrow['Element Timing'] = write_out(target['time'])
            
            # TODO: use trigger or text?
            thisrow['Interaction Text'] = write_out([this_extraction['trigger']] + this_extraction['text'])
            thisrow['Interaction ID'] = type_
            thisrow['Interaction Degree'] = write_out(this_extraction['degree'])
            thisrow['Interaction Location'] = write_out(this_extraction['location'])
            thisrow['Interaction Timing'] = write_out(this_extraction['time'])
            
            for key in ['change', 'level', 'polarity', 'genericity', 'modality']:
                if len(this_extraction[key]) > 0:
                    print('Warning: interaction has attribute ' + key)

            # get source documents
            thisrow['Source'] = write_out([docs[x] for x in this_extraction['document']])
            thisrow['Reader'] = 'BBN'
            thisrow['Evidence'] = write_out(this_extraction['text'])

            final = final.append(thisrow,ignore_index=True)
        
    final = final.fillna('')      

    return final


def convert_eidos_jsonld(input_file) -> pd.DataFrame:
    """Process a json-ld file created using eidos
    """

    global _COLNAMES
    source_types = ['source']
    target_types = ['destination']
    correlation_types = ['argument']

    final = pd.DataFrame(columns=_COLNAMES)

    with open(input_file) as json_file:
        reading = json.load(json_file)

    # get document titles/IDs
    docs = dict()
    for this_doc in reading['documents']:
        if 'title' in this_doc.keys():
            title = this_doc['title']
        else:
            title = this_doc['@id']

        docs[this_doc['@id']] = title

    # format extractions into a dict with IDs for keys
    extractions = dict()
    for this_extraction in reading['extractions']:
        type_ = this_extraction['type']
        # print(this_extraction.keys())
        if type_ in ['concept','relation']:
            canonical_name = this_extraction.get('canonicalName','')

            # use top grounding value term from UN/FAO/WDI groundings
            grounding = [max([[g['value'],g['ontologyConcept']] 
                for g in gs.get('values',[])], default=[''])[-1] 
                for gs in this_extraction.get('groundings',[])]
            # TODO: split to make more readable?
            # grounding_values = [gs['values'] for gs in this_extraction.get('groundings',[])]
            # grounding = [max([[g['value'],g['ontologyConcept']], default=[''])[-1]
            #     for g in grounding_values]

            text = this_extraction.get('text','')
            source = [x['document']['@id'] for x in this_extraction.get('provenance',[])]
            sentence = [x['sentence']['@id'] for x in this_extraction.get('provenance',[])]

            ext_type = type_
            subtype = this_extraction.get('subtype','')

            labels = this_extraction.get('labels','')

            if 'trigger' in this_extraction.keys():
                trigger = this_extraction['trigger']['text']
            else:
                trigger = ''

            # TODO: check whether these assignments are still needed, since sources and destinations are now contained in arguments section
            sources = [x['@id'] for x in this_extraction.get('sources',[])]
            targets = [x['@id'] for x in this_extraction.get('destinations',[])]

            location = []
            time = []
            correlations = []
            for arg in this_extraction.get('arguments',[]):
                arg_type = arg['type'].lower()
                arg_val = [arg['value']['@id']]
                if arg_type in ['place', 'origin']:
                    # TODO: remove this check since location now contained in the state section; Also removed destination from location options
                    print("Hey this location check should be deprecated----------------------------------------------------------")
                    location += arg_val
                elif arg_type in ['time']:
                    # TODO: remove this check since time now contained in the state section
                    print("Hey this time check should be deprecated----------------------------------------------------------")
                    time += arg_val
                elif arg_type in source_types:
                    sources += arg_val #[x['@id'] for x in arg.get('value',[])]
                elif arg_type in target_types:
                    targets += arg_val
                elif arg_type in correlation_types:
                    correlations += arg_val
                elif arg_type in ['group','member','left_argument','right_argument','left_arg','right_arg']:
                    # TODO: use group, member, left/right argument relations between entities?
                    pass
                else:
                    print('Unrecognized argument type: ' + str(arg_type))

            change = []
            level = []
            polarity = []
            modality = []
            genericity = []
            for state in this_extraction.get('states',[]):
                state_type = state['type'].lower()
                # FIXME: states can be attached to different words, spatial increase, value increase etc.
                # states have type, text, (provenance), (modifiers)
                if state_type in ['inc','dec']:
                    change += [state['type']]
                elif state_type in ['quant']:
                    level += [state['text']]
                elif state_type in ['timex']:
                    time += [state['text']]
                elif state_type in ['locationexp']:
                    location += [state['text']]
                elif state_type in ['polarity']:
                    polarity += [state['text']]
                elif state_type in ['modality']:
                    modality += [state['text']]
                elif state_type in ['genericity']:
                    genericity += [state['text']]
                else:
                    print('Unrecognized state type: ' + str(state_type))
            
            # TODO: keep degree modifiers attached to state?
            degree = [y.get('text') for x in this_extraction.get('states',[]) 
                for y in x.get('modifiers',[])]

            extractions[this_extraction['@id']] = {
                'canonicalName' : canonical_name, 
                'grounding' : grounding,
                'text' : text, 
                'source' : source,
                'sentence' : sentence,
                'type' : ext_type,
                'subtype' : subtype,
                'labels' : labels,
                'trigger' : trigger,
                'sources' : sources,
                'targets' : targets,
                'correlations' : correlations,
                'change' : change, 
                'level' : level,
                'degree' : degree,
                'polarity' : polarity,
                'modality' : modality,
                'genericity' : genericity,
                'location' : location,
                'time' : time
                }
        else:
            print('Unrecognized type: ' + str(type_))
            
    for id_, this_extraction in extractions.items():
        type_ = this_extraction['type']
        subtype = this_extraction['subtype']
        #print('The type is: %s and the subtype is: %s'% (type_, subtype))
        if type_ in ['relation'] and subtype in ['causation']:
            thisrow = dict()

            # Cause attributes
            # TODO: deal with multiple causes
            if len(this_extraction.get('sources',[])) > 1:
                print('Warning: more than one source')
            
            source = extractions[this_extraction['sources'][0]]

            # TODO: use canonical name for something?
            thisrow['Regulator Text'] = source['text']
            thisrow['Regulator Name'] = write_out(source['grounding'])
            thisrow['Regulator Level'] = write_out(source['level'])
            thisrow['Regulator Change'] = write_out(source['change'])
            thisrow['Regulator Degree'] = write_out(source['degree'])
            thisrow['Regulator Scope'] = write_out(source['genericity'])
            thisrow['Regulator Location'] = write_out(source['location'])
            thisrow['Regulator Timing'] = write_out(source['time'])
                    
            # Effect attributes
            # TODO: deal with multiple effects, nested effects
            if len(this_extraction.get('targets',[])) > 1:
                print('Warning: more than one target')

            # index the target object from this_extraction ID
            target = extractions[this_extraction['targets'][0]]
            
            thisrow['Element Text'] = target['text']
            thisrow['Element Name'] = write_out(target['grounding'])
            thisrow['Element Level'] = write_out(target['level'])
            thisrow['Element Change'] = write_out(target['change'])
            thisrow['Element Degree'] = write_out(target['degree'])
            thisrow['Element Scope'] = write_out(target['genericity'])
            thisrow['Element Location'] = write_out(target['location'])
            thisrow['Element Timing'] = write_out(target['time'])
            
            thisrow['Interaction Text'] = this_extraction['trigger']
            thisrow['Interaction ID'] = type_ 
            thisrow['Interaction Degree'] = write_out(this_extraction['degree'])
            thisrow['Interaction Location'] = write_out(this_extraction['location'])
            thisrow['Interaction Timing'] = write_out(this_extraction['time'])
            
            for key in ['change', 'level', 'polarity', 'genericity', 'modality']:
                if len(this_extraction[key]) > 0:
                    print('Warning: interaction has attribute ' + key)

            # get source documents
            thisrow['Source'] = write_out([docs[x] for x in this_extraction['source']])
            thisrow['Reader'] = 'eidos'
            thisrow['Sentence ID'] = write_out(this_extraction['sentence'])
            thisrow['Evidence'] = this_extraction['text']

            final = final.append(thisrow,ignore_index=True)
    
    final = final.fillna('')      

    return final


def convert_sofia(input_file,score_threshold=0) -> pd.DataFrame:
    """Convert automated reading output from SOFIA reader 
    """

    global _COLNAMES
    
    final = pd.DataFrame(columns=_COLNAMES+['Score'])

    reading = pd.ExcelFile(input_file)

    # get relations
    relations = reading.parse(
            'Causal',
            na_values='NaN',
            keep_default_na=False,
            index_col=None
            )
    relations = relations.rename(
            index=str,
            columns={
                    'Relation' : 'text',
                    'Relation_Type' : 'type',
                    'Source_File' : 'source',
                    'Sentence' : 'evidence',
                    'Score' : 'score'
                    }
            )
    # get events 
    events = reading.parse(
            'Events',
            na_values='NaN',
            keep_default_na=False,
            index_col='Event Index'
            )
    events = events.rename(
            index=str,
            columns={
                    'Relation' : 'text',
                    'Event_Type' : 'type',
                    'Agent' : 'agent',
                    'Agent Index' : 'agent_id',
                    'Patient' : 'patient',
                    'Patient Index' : 'patient_id',
                    'Location' : 'location',
                    'Time' : 'timing'
                    }
            )
    events_dict = events.to_dict(orient='index')
    # get entities
    entities = reading.parse(
            'Entities',
            na_values='NaN',
            keep_default_na=False,
            index_col='Entity Index'
            )
    entities = entities.rename(index=str,
            columns={
                    'Entity' : 'text',
                    'Entity_Type' : 'type',
                    'Qualifier' : 'degree'
                    }
            )
    entities_dict = entities.to_dict(orient='index')

    # iterate through relations to link agents/patients and format columns
    # TODO: speed up with dataframe apply
    relations_dict = relations.to_dict(orient='index')
    for key, row in relations_dict.items():
        thisrow = dict()
        
        cause_ids = [x.strip() for x in row['Cause Index'].split(',')]
        # check for comma-separated entries in cause 
        # TODO: look for AND relationships
        for cause_id in cause_ids:
            if float(row['score']) >= score_threshold:

                if cause_id != '':
                    if cause_id in events_dict:
                        cause = events_dict[cause_id]
                    else:
                        cause = entities_dict.get(cause_id,'') 
                else:
                    cause = ''

                if cause != '':
                    # get cause and effect attributes
                    thisrow['Regulator Text'] = cause['text']
                    thisrow['Regulator Name'] = cause['type']
                    # TODO: Type
                    # for agent and patient, looking for entity type, 
                    # falling back on text
                    cause_agent_entity = entities_dict.get(
                            cause.get('agent_id', ''), defaultdict()
                            )
                    thisrow['Regulator Agent'] = cause_agent_entity.get(
                            'type',
                            cause.get('agent', '')
                            )
                    cause_patient_entity = entities_dict.get(
                            cause.get('patient_id', ''), defaultdict()
                            )
                    thisrow['Regulator Patient'] = cause_patient_entity.get(
                            'type', 
                            cause.get('patient', '')
                            )
                    # TODO: detect nested events, use evan's parsing method
                    thisrow['Regulator Location'] = cause.get('location','')
                    thisrow['Regulator Timing'] = cause.get('timing','')
                    thisrow['Regulator Degree'] = cause.get('degree','')

                    thisrow['Interaction Text'] = row['text']
                    thisrow['Interaction ID'] = row['type']

                    thisrow['Source'] = row['source'] 
                    thisrow['Reader'] = 'SOFIA'
                    thisrow['Evidence'] = row['evidence']

                    thisrow['Score'] = row['score']

                    effect_ids = [x.strip() for x in row['Effect Index'].split(',')]
                    # check for comma-separated entries in effect and add a row for each
                    for effect_id in effect_ids:
                        if effect_id != '':
                            if effect_id in events_dict:
                                effect = events_dict[effect_id] 
                            else:
                                effect = entities_dict.get(effect_id,'')
                        else:
                            effect = '' 

                        if effect != '':
                            thisrow['Element Text'] = effect['text']
                            thisrow['Element Name'] = effect['type']
                            # TODO: Type
                            # for agent and patient, looking for entity type, 
                            # falling back on text
                            effect_agent_entity = effect.get(
                                    effect.get('agent_id',''), defaultdict()
                                    )
                            thisrow['Element Agent'] = effect_agent_entity.get(
                                    'type', 
                                    effect.get('agent', ''),
                                    )
                            effect_patient_entity = effect.get(
                                    effect.get('patient_id',''), defaultdict()
                                    )
                            thisrow['Element Patient'] = effect_patient_entity.get(
                                    'type', 
                                    effect.get('patient', '')
                                    )
                            thisrow['Element Location'] = effect.get('location','')
                            thisrow['Element Timing'] = effect.get('timing','')
                            thisrow['Element Degree'] = effect.get('degree','')

                            final = final.append(thisrow,ignore_index=True)

    final['Score'] = pd.to_numeric(final['Score'])
    # # filter by score threshold
    # final = final[final['Score'] > score_threshold]

    final = final.fillna('')      

    return final


def write_out(value_) -> str:
    """Process values to write to a cell in tabular output 
    """

    if type(value_) is list:
        write_out_value = ';'.join([str(x) for x in value_ if x!='' and x is not None])
    else:
        write_out_value = value_

    return write_out_value


def main():

    # Parse command line arguments
    parser = argparse.ArgumentParser(
        description='Translate automated reading output into standard format (for DySE model assembly or extension).',
        formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('input_file', type=str, 
                        help='automated reading output to convert to standard format')
    parser.add_argument('output_file', type=str,
                        help='path and name of output file to save converted reading')
    parser.add_argument('input_format', type=str, choices=['text','sofia','eidos','bbn'],
                        help='format of automated reading \n' 
                        'text: plain text, translate using eidos and indra \n' 
                        'sofia: tabular output from SOFIA reader \n' 
                        'eidos: json output from the eidos parser \n' 
                        'bbn: json-ld output from BBN\'s reader' 
                        )
 
    args = parser.parse_args()

    if args.input_format == 'text':
        # FIXME: fix import of indra/eidos
        if 'indra.sources.eidos' in sys.modules:
            final = convert_text(args.input_file)
        else:
            raise ValueError('Text conversion failed, INDRA Eidos parser is not available')
    elif args.input_format == 'eidos':
        final = convert_eidos_jsonld(args.input_file)
    elif args.input_format == 'sofia':
        final = convert_sofia(args.input_file)
    elif args.input_format == 'bbn':
        final = convert_bbn_jsonld(args.input_file)
    else:
        raise InputError('Unrecognized input format')

    final.to_excel(args.output_file, index=False)

if __name__ == '__main__':
    main()