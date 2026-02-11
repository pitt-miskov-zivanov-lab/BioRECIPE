import os 
import sys 
import pandas as pd
from typing import Union, Any, List 
from argparse import ArgumentParser
from translators.biopax.parse import Biopax
from translators.within_biorecipe.biorecipe_std import (
    biorecipe_int_cols, biorecipe_mdl_cols, format_variable_names,
    INTERACTION_ATTR, CONTEXT_ATTR, PROVENANCE_ATTR
)


INTERACTION_COLS = INTERACTION_ATTR + CONTEXT_ATTR + PROVENANCE_ATTR
bp = Biopax() 

ele_cols = {
    'name': 'Element Name',
    'type': 'Element Type',
    'subtype': 'Element Subtype',
    'database': 'Element Database',
    'ID': 'Element IDs',
    'compartment': 'Compartment',
    'compartment ID': 'Compartment ID'
}

def biopax_to_biorecipeI(df:pd.DataFrame=None, 
                         input_file:str=None, 
                         input_str:str=None,
                         output_file: str=None) -> Union[pd.DataFrame, None]: 
    
    if input_file: 
        entities, relations = bp.biopax2tabular(input_file=input_file)
    elif input_str:
        entities, relations = bp.biopax2tabular(input_str=input_str)
    entities = {uid: attr for uid, attr in entities}
    # Conver to DataFrame
    df = pd.DataFrame(columns=biorecipe_int_cols)
    for idx, (src, tgt, interact) in enumerate(relations): 
        src_attr = entities[src]
        tgt_attr = entities[tgt]
        for k, v in src_attr.items():
            df.loc[idx, f'Regulator {k.capitalize() if "ID" not in k else k}'] = v if k != None else ''
        
        for k, v in tgt_attr.items():
            df.loc[idx, f'Regulated {k.capitalize() if "ID" not in k else k}'] = v if k != None else ''

        for key in INTERACTION_COLS:
            df.loc[idx, key] = interact.get(key.lower(), '')

        # TODO: add provenance info
    if output_file: 
        df.to_excel(output_file, index=False)

    else:
        return df

def biopax_to_biorecipeM(input_file: str=None, 
                         input_str: str=None,
                         output_file: str=None) -> Union[pd.DataFrame, None]:
    
    if input_file:
        entities, relations = bp.biopax2tabular(input_file=input_file, multi_xrefs=True)
    elif input_str:
        entities, relations = bp.biopax2tabular(input_str=input_str, multi_xrefs=True)
    df = pd.DataFrame(columns=biorecipe_mdl_cols)

    for idx, element in enumerate(entities):
        uid, attr = element 
        df.loc[idx, '#'] = idx
        df.loc[idx, 'Variable'] = uid
        for k, v in attr.items():
            df.loc[idx, ele_cols[k]] = v if v != None else ''

    var_list = df['Variable'].tolist()
    # initialize regulator list columns
    df['Positive Regulator List'] = [[] for _ in range(len(df))]
    df['Negative Regulator List'] = [[] for _ in range(len(df))]
    df['Positive Connection Type List'] = [[] for _ in range(len(df))]
    df['Negative Connection Type List'] = [[] for _ in range(len(df))]
    for idx, (src, tgt, interact) in enumerate(relations): 
        sign = interact.get('sign', '')
        if sign == None:
            continue
        cnx_type = interact.get('connection type', 'i')
        if cnx_type == None:
            cnx_type = 'i'
        df.at[var_list.index(tgt), f'{sign.capitalize()} Regulator List'].append(src)
        df.at[var_list.index(tgt), f'{sign.capitalize()} Connection Type List'].append(cnx_type)

    df['Positive Regulator List'] = df['Positive Regulator List'].apply(lambda x: ','.join(x) if len(x) > 0 else '')
    df['Negative Regulator List'] = df['Negative Regulator List'].apply(lambda x: ','.join(x) if len(x) > 0 else '')
    df['Positive Connection Type List'] = df['Positive Connection Type List'].apply(lambda x: ','.join(x) if len(x) > 0 else '')
    df['Negative Connection Type List'] = df['Negative Connection Type List'].apply(lambda x: ','.join(x) if len(x) > 0 else '')

    df = format_variable_names(df)
    if output_file:
        df.to_excel(output_file, index=False)

    return df



def biorecipeI_to_biopax(df, entity_list, relation_list):
    pass

def biorecipeM_to_biopax(df, entity_list, relation_list):
    pass


def main():
    args = ArgumentParser()
    args.add_argument('--input_file', type=str, required=True, 
                      help='Path to the input Biopax file (.owl/.xml or .xlsx)')
    args.add_argument('--output_file', type=str, required=True,
                        help='Path to the output Biorecipe file (.xlsx or .owl/.xml)')
    args.add_argument('--biorecipe_type', type=str, choices=['interaction', 'model'], required=True,
                      help='Type of BioRECIPE to convert to: interaction list or model.')
    
    args = args.parse_args()

    iname, iext = os.path.splitext(args.input_file)
    oname, oext = os.path.splitext(args.output_file)

    assert iext != oext, "Input and output file formats must be different."
    io_exts = set([iext, oext])
    assert io_exts == set(['.xml', '.xlsx']) or io_exts == set(['.owl', '.xlsx']), \
        "Input must be .owl/.xml and output must be .xlsx, or vice versa."
    
    if iext in ['.owl', '.xml'] and args.biorecipe_type == 'interaction':
        biopax_to_biorecipeI(input_file=args.input_file, output_file=args.output_file)
    
    if iext in ['.owl', '.xml'] and args.biorecipe_type == 'model':
        biopax_to_biorecipeM(input_file=args.input_file, output_file=args.output_file)

    if iext == '.xlsx' and args.biorecipe_type == 'interaction':
        biorecipeI_to_biopax(args.input_file, args.output_file)

    if iext == '.xlsx' and args.biorecipe_type == 'model':
        biorecipeM_to_biopax(args.input_file, args.output_file)


if __name__ == '__main__':
    main()