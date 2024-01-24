# TODO: remove this file if framework is released

import pandas as pd
import logging
import re
import networkx as nx

# define regex for valid characters in variable names
_VALID_CHARS = r'a-zA-Z0-9\_'

# valid element types
_VALID_TYPES = [
    'protein', 'protein family', 'protein complex',
    'rna', 'mrna', 'gene', 'chemical', 'biological process'
    ]

_VAR_COL = 'Variable'
_IDX_COL = '#'

def get_model(model_file: str) -> pd.DataFrame:
    """Load model into a DataFrame and standardize column names
    """

    global _VALID_CHARS
    global _VAR_COL
    global _IDX_COL

    index_col_name = _IDX_COL
    var_col_name = _VAR_COL
    pos_reg_col_name = 'Positive Regulation Rule'
    pos_list_col_name = 'Positive List'
    neg_reg_col_name = 'Negative Regulation Rule'
    neg_list_col_name = 'Negative List'
    reg_list_col_name = 'Regulators'
    element_name_col_name = 'Element Name'
    ids_col_name = 'Element IDs'
    type_col_name = 'Element Type'

    # Load the input file containing elements and regulators
    model_sheets = pd.ExcelFile(model_file)
    # get the model from the first sheet, will check the other sheets for truth tables later
    model = model_sheets.parse(0,na_values='NaN',keep_default_na=False,index_col=None)

    # check model format
    if 'element attributes' in [x.lower() for x in model.columns]:
        # drop two header rows and set column names to third row
        model = model.rename(columns=model.iloc[1]).drop([0,1]).set_index(index_col_name)

    # get other sheets
    # TODO: parse truth tables here? or just return other sheets separately?
    if len(model_sheets.sheet_names) > 1:
        df_other_sheets = {sheet : model_sheets.parse(sheet,na_values='NaN',keep_default_na=False) \
            for sheet in model_sheets.sheet_names[1:]}
    else:
        df_other_sheets = ''

    # format model columns
    input_col_X = [
            x.strip() for x in model.columns
            if ('variable' in x.lower())
            ]
    input_col_A = [
            x.strip() for x in model.columns
            if ('positive regulation rule' in x.lower())
            ]
    input_col_I = [
            x.strip() for x in model.columns
            if ('negative regulation rule' in x.lower())
            ]
    input_col_initial = [
            x.strip() for x in model.columns
            if ('state list' in x.lower())
            ]

    input_col_name = [
            x.strip() for x in model.columns
            if ('element name' in x.lower())
            ]
    input_col_ids = [
            x.strip() for x in model.columns
            if ('element ids' in x.lower())
            ]
    input_col_type = [
            x.strip() for x in model.columns
            if ('element type' in x.lower())
            ]

    # check for all required columns or duplicate colummns
    if (len(input_col_X) == 0
            or len(input_col_A) == 0
            or len(input_col_I) == 0
            or len(input_col_initial) == 0
            ):
        raise ValueError(
                'Missing one or more required columns in input file: '
                'Variable, Positive Regulation Rule, Negative Regulation Rule, State List'
                )
    elif (len(input_col_X) > 1
            or len(input_col_A) > 1
            or len(input_col_I) > 1
            ):
        raise ValueError('Duplicate column of: Variable, Positive Regulation Rule, Negative Regulation Rule')

    if (len(input_col_name) == 0
            or len(input_col_ids) == 0
            or len(input_col_type) == 0
            ):
        raise ValueError(
                'Missing one or more required column names: '
                'Element Name, Element IDs, Element Type'
                )
    elif (len(input_col_name) > 1
            or len(input_col_ids) > 1
            or len(input_col_type) > 1
            ):
        raise ValueError(
                'Duplicate column of: '
                'Element Name, Element IDs, Element Type'
                )

    # TODO: check for other columns here as they are needed

    # processing
    # use # column or index to preserve order of elements in the model
    if index_col_name in model.columns:
        model.set_index(index_col_name,inplace=True)

    # remove rows with missing or marked indices
    model = drop_x_indices(model)

    model = model.reset_index()
    # standardize column names
    model = model.rename(
        index=str,
        columns={
            'index': index_col_name,
            input_col_X[0]: var_col_name,
            input_col_A[0]: pos_reg_col_name,
            input_col_I[0]: neg_reg_col_name,
            input_col_name[0]: element_name_col_name,
            input_col_ids[0]: ids_col_name,
            input_col_type[0]: type_col_name
        })

    # format invalid variable names
    model = format_variable_names(model)

    # standardize element types
    model['Element Type'] = model['Element Type'].apply(get_type)

    # set variable name as the index
    model.set_index(var_col_name,inplace=True)

    # check for empty indices
    if '' in model.index:
        raise ValueError('Missing variable names')
        # model = model.drop([''])

    # parse regulation functions into lists of regulators
    model[pos_list_col_name] = model[pos_reg_col_name].apply(
            lambda x: [y.strip() for y in re.findall('['+_VALID_CHARS+']+',x)]
            )
    model[neg_list_col_name] = model[neg_reg_col_name].apply(
            lambda x: [y.strip() for y in re.findall('['+_VALID_CHARS+']+',x)]
            )
    model[reg_list_col_name] = model.apply(
            lambda x:
            set(list(x[pos_list_col_name]) + list(x[neg_list_col_name])),
            axis=1
            )

    model.fillna('',inplace=True)

    return model

def drop_x_indices(model: pd.DataFrame) -> pd.DataFrame:
    """Drop rows with missing or X indices
    """

    if 'X' in model.index or 'x' in model.index:
        logging.info('Dropping %s rows with X indices' % str(len(model.loc[['X']])))
        model.drop(['X'],axis=0,inplace=True)
    if '' in model.index:
        logging.info('Dropping %s rows missing indices' % str(len(model.loc[['']])))
        model.drop([''],axis=0,inplace=True)

    return model

def format_variable_names(model: pd.DataFrame) -> pd.DataFrame:
    """Format model variable names to make compatible with model checking
    """

    global _VALID_CHARS
    global _VAR_COL

    # remove whitespace in variable names
    model[_VAR_COL] = model[_VAR_COL].str.strip()

    # collect invalid element names in a list so they can be removed everywhere in the model
    # find invalid characters in element names and names starting with numbers
    invalid_names = [
        x for x in model[_VAR_COL]
        if re.search(r'(^[0-9]+)',x.strip()) or re.search(r'([^'+_VALID_CHARS+']+)',x.strip())
        ]

    if len(invalid_names) > 0:
        logging.info('Formatting variable names: ')

    # remove invalid characters at the start of the variable name
    replace_names = [re.sub(r'^[^'+_VALID_CHARS+']+','',x) for x in invalid_names]
    # replace invalid characters elsewhere in variable names
    replace_names = [re.sub(r'[^'+_VALID_CHARS+']+','_',x) for x in replace_names]

    # add ELE_ at the beginning of names starting with numbers
    replace_names = [re.sub(r'(^[0-9]+)','ELE_\\1',x) for x in replace_names]

    name_pairs = zip(invalid_names,replace_names)

    for (invalid_name,replace_name) in name_pairs:
        logging.info('%s -> %s' % (invalid_name,replace_name))
        model.replace(re.escape(invalid_name),re.escape(replace_name),regex=True,inplace=True)

    return model

def get_type(input_type):
    """Standardize element types
    """

    global _VALID_TYPES

    if input_type.lower() in _VALID_TYPES:
        return input_type
    elif input_type.lower().startswith('protein'):
        return 'protein'
    elif input_type.lower().startswith('chemical'):
        return 'chemical'
    elif input_type.lower().startswith('biological'):
        return 'biological'
    else:
        return 'other'

def model_to_dict(model: pd.DataFrame):
    """Convert model table to a dictionary
    """

    # convert dataframe to dict with variable name as the index
    model_dict = model.to_dict(orient='index')

    return model_dict

def model_to_edges(model : pd.DataFrame) -> pd.DataFrame:
    """Convert the model into a dataframe of edges in the format
        element-regulator-interaction
    """

    # convert to dict for faster iteration
    model_dict = model_to_dict(model)

    edges_dict = dict()

    # create entries in edges_dict for each regulator-regulated pair in the model
    # using the model dict positive and negative regulator lists
    for key,item in model_dict.items():

        # re-parsing here to handle ! (not) notation
        # TODO: also handle AND, highest state, etc.
        pos_list = [x.strip() for x in re.findall(r'[a-zA-Z0-9\_!=]+',item.get('Positive Regulation Rule',''))]
        neg_list = [x.strip() for x in re.findall(r'[a-zA-Z0-9\_!=]+',item.get('Negative Regulation Rule',''))]

        # TODO: preserve element/regulator names and attributes
        pos_dict = {
            key+'pos'+str(i) : {'element':key, 'regulator':pos, 'interaction':'increases'}
            if pos[0]!='!' else {'element':key, 'regulator':pos[1:], 'interaction':'NOT increases'}
            for i,pos in enumerate(pos_list)
            }
        neg_dict = {
            key+'neg'+str(i) : {'element':key, 'regulator':neg, 'interaction':'decreases'}
            if neg[0]!='!' else {'element':key, 'regulator':neg[1:], 'interaction':'NOT decreases'}
            for i,neg in enumerate(neg_list)
            }
        edges_dict.update(pos_dict)
        edges_dict.update(neg_dict)

    edges_df = pd.DataFrame.from_dict(edges_dict,orient='index')

    return edges_df

def model_to_networkx(model: pd.DataFrame) -> nx.DiGraph():
    """Convert model to a networkx graph
    """

    edges = model_to_edges(model)
    # In networkx 2.0 from_pandas_dataframe has been removed.
    graph = nx.from_pandas_edgelist(edges,
        source='regulator',target='element',edge_attr='interaction',
        create_using=nx.DiGraph())

    return graph