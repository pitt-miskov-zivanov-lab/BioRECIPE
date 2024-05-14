# TODO: remove this file if framework is released

import pandas as pd
import logging
import re
import networkx as nx
import warnings

biorecipe_reading_col = ['Regulator Name', 'Regulator Type', 'Regulator Subtype',
						 'Regulator HGNC Symbol', 'Regulator Database', 'Regulator ID',
						 'Regulator Compartment', 'Regulator Compartment ID',
						 'Regulated Name', 'Regulated Type', 'Regulated Subtype',
						 'Regulated HGNC Symbol', 'Regulated Database', 'Regulated ID',
						 'Regulated Compartment', 'Regulated Compartment ID',
						 'Sign', 'Connection Type', 'Mechanism', 'Site',
						 'Cell Line', 'Cell Type', 'Tissue Type', 'Organism',
						 'Score', 'Source', 'Statements', 'Paper IDs', 'Database Source', 'Database ID']

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

def sub_comma_in_entity(df: pd.DataFrame, col_name: str):
    """

    Parameters
    ----------
    df: pd.DataFrame
    col_name: str

    Returns
    -------
    df
    """
    df = df.fillna('nan')
    entity_attribute_col = ['Name', 'ID', 'Type']
    entity, attribute = col_name.split(' ')
    entity_attribute_col.remove(attribute)
    df = df.astype(str)
    for row in range(len(df)):
        value = df.loc[row, col_name]
        # operate on this column
        if ',' in value:
            value_list = value.split(',')
            value_list = [value_i.strip() for value_i in value_list]
            df.loc[row, col_name] = '_'.join(value_list)
            # operate on the other columns
            for col in entity_attribute_col:
                if ',' in value:
                    value_attr_1 = df.loc[row, f'{entity} {col}']
                    value_attr_1_list = value_attr_1.split(',')
                    value_attr_1_list = [value_i.strip() for value_i in value_attr_1_list]
                    df.loc[row, f'{entity} {col}'] = '_'.join(value_attr_1_list)
                else:
                    pass
        else:
            pass

    return df

def change_name_by_type(reading_df:pd.DataFrame, entity: str) -> pd.DataFrame:
    """This function will make entities name display their type when entity name are the same

    Parameters
    ----------
    reading_df: pd.DataFrame
    entity: str

    Returns
    -------
    reading_df
    """
    type_dict = {'protein': 'pt', 'gene':'gene', 'chemical': 'ch', 'RNA': 'rna', \
                 'protein family|protein complex':'pf', 'family':'pf', 'complex':'pf', \
                 'protein family': 'pf', 'biological process': 'bp'}
    type_ = list(type_dict.keys())
    for name_, df in reading_df.groupby(by=f'{entity} Name'):
        index_list = list(df.index)
        for row in index_list:
            entity_type = reading_df.loc[row, f'{entity} Type'].lower()

            if '_' in entity_type:
                type_multiple = entity_type.split('_')
                if all(type_i in type_ for type_i in type_multiple):
                    type_sym = [type_dict[type_i] for type_i in type_multiple]
                    type_add = '_'.join(type_sym)
                    reading_df.loc[row, f'{entity} Name'] = reading_df.loc[row, f'{entity} Name'] + '_' + type_add
                else:
                    warnings.warn(
                        f'cannot process row {row}, entity types are not included in BioRECIPE.'
                    )
                    reading_df.drop(row)

            else:
                if entity_type in type_:
                    reading_df.loc[row, f'{entity} Name'] = reading_df.loc[row, f'{entity} Name'] + '_' + type_dict[entity_type]
                else:
                    warnings.warn(
                        f'cannot process row {row}, entity types are not included in BioRECIPE.'
                    )
                    reading_df.drop(row)
    return reading_df

def preprocess_reading(reading_df: pd.DataFrame) -> pd.DataFrame:
    """
    This is a function to normalize the entity name, the entities that are different but have same entity name
    will be renamed
    Renaming are following the rule below:
        1. Entities have different IDs are different
        2. Entities have same ID and same type but different names, their names should be renamed as the identical
        3. Entities have same name but different type, the element name should be distinguished
    Returns
    reading_output
    -------

    """

    # check if there are multiple entities in a single row
    for entity in ['Regulator', 'Regulated']:
        # check if there are multiple entities in a single row
        name_empty, id_empty, type_empty = reading_df[f'{entity} Name'].empty, reading_df[f'{entity} ID'].empty, reading_df[f'{entity} Type'].empty
        if name_empty:
            raise ValueError(
                'Column of element name cannot be empty.'
            )
        else:
            if not id_empty and not type_empty:
                # first, check all the entities that consist of multiple entities
                reading_df = sub_comma_in_entity(reading_df, f'{entity} Name')
                # groupby the element id and get their attributes by index
                reading_df[f'{entity} Name'] = reading_df[f'{entity} Name'].str.lower()
                # follow rule 3 to make name report their type
                reading_df = change_name_by_type(reading_df, entity)
                reading_df = reading_df.reset_index()
                # make entity unique
                reading_df = check_id_type_and_change_name(reading_df, entity)


            elif not id_empty and type_empty:
                warnings.warn(
                    f'{entity} type column is empty. entity names is only sort by IDs.'
                )
                reading_df = sub_comma_in_entity(reading_df, f'{entity} Name')
                reading_df[f'{entity} Name'] = reading_df[f'{entity} Name'].str.lower()
                # sort by id only
                reading_df = check_and_change_name(reading_df, entity, f'{entity} ID')
            elif id_empty and not type_empty:
                warnings.warn(
                    f'{entity} type column is empty. entity names will be sort by type only'
                )
                reading_df = check_and_change_name(reading_df, entity, f'{entity} type')
            else:
                warnings.warn(
                    f'type and ID columns are empty'
                )
                pass

    return reading_df

def check_id_type_and_change_name(reading_df: pd.DataFrame, entity: str) -> pd.DataFrame:
    """ This function make sure all the element name are unique based on their attributes ID and type

    Parameters
    ----------
    reading_df: pd.Dataframe
    entity: regulator or regulated
    Returns
    -------
    reading_df
    """
    for id_, df in reading_df.groupby(by=f'{entity} ID'):
        # get all types and name under controlled by the same ID
        Type_list = list(set(df[f'{entity} Type'].to_numpy()))
        name_list = list(set(df[f'{entity} Name'].to_numpy()))
        # add names to make every entity take a unique name
        if len(name_list) < len(Type_list):
            add_name_len = len(Type_list) - len(name_list)
            # FIXME: This could also be named in different ways
            for i in range(add_name_len): name_list.append(f'{name_list[-1]}_{i}')
        else:
            pass

        # assign the entities have same type with the same name
        counter = 0 # count how many types are processed
        for Type in Type_list:
            sub_df = df[df[f'{entity} Type'] == Type]
            sub_df_index = list(sub_df.index)
            for i in range(len(sub_df)):
                reading_df.loc[sub_df_index[i], f'{entity} Name'] = name_list[counter]
            counter+=1

    return reading_df

def check_and_change_name(reading_df: pd.DataFrame, entity: str, sort_by_attrb: str) -> pd.DataFrame:
    """ This function make sure all the element name are unique based on their attributes ID or type

    Parameters
    ----------
    reading_df: pd.Dataframe
    entity: regulator or regulated
    Returns
    -------
    reading_df
    """
    reading_output_df = reading_df.copy()
    # make all the names different
    for name, df in reading_df.groupby(by=f'{entity} name'):
        same_name_index = df.index
        for i in range(len(same_name_index)):
            if i == 0:
                pass
            else:
                reading_output_df.loc[same_name_index[i], f'{entity} name'] = reading_output_df.loc[same_name_index[i], f'{entity} name'] + f'_{i}'

    # compare the names by category attribute
    for id_, df in reading_df.groupby(by=f'{entity} {sort_by_attrb}'):
        std_index = list(df.index)[0]
        for row in range(len(df)):
            reading_output_df.loc[row, f'{entity} {sort_by_attrb}'] = df.loc[std_index, f'{entity} {sort_by_attrb}']
    return reading_output_df

def interactions_to_model(interaction_df: pd.DataFrame) -> pd.DataFrame:
    """
    """
    model_cols = ['#', 'Element Name', 'Element Type', 'Element Subtype',
       'Element HGNC Symbol', 'Element Database', 'Element IDs', 'Compartment',
       'Compartment ID', 'Cell Line', 'Cell Type', 'Tissue Type', 'Organism',
       'Positive Regulator List', 'Positive Connection Type List',
       'Positive Mechanism List', 'Positive Site List',
       'Negative Regulator List', 'Negative Connection Type List',
       'Negative Mechanism List', 'Negative Site List', 'Score List',
       'Source List', 'Statements List', 'Paper IDs List',
       'Positive Regulation Rule', 'Negative Regulation Rule', 'Variable',
       'Value Type', 'Levels', 'State List 0', 'State List 1', 'Const OFF',
       'Const ON', 'Increment', 'Spontaneous', 'Balancing', 'Delay',
       'Update Group', 'Update Rate', 'Update Rank']

    attrb_cols = ['Element Name', 'Element Type', 'Element Database', 'Element Subtype','Element HGNC Symbol','Element IDs','Compartment'
             'Compartment ID', 'Cell Line', 'Cell Type', 'Tissue Type', 'Organism']

    bio_attrb = ['Regulated Name',
            'Regulated Type',
            'Regulated Database',
            'Regulated Subtype',
            'Regulated HGNC Symbol',
            'Regulated ID',
            'Regulated Compartment',
            'Regulated Compartment ID',
            'Cell Line',
            'Cell Type',
            'Tissue Type',
            'Organism']

    ele_dict, pos_reg_list,output_df, output_ele_df = {}, str(), pd.DataFrame(columns=model_cols), pd.DataFrame(columns=attrb_cols)
    category_stack = []

    # preprocess the spreadsheet
    interaction_df = preprocess_reading(interaction_df)
    ######clean up the name of regulator and element
    # Get all unique elements to index
    category = set(interaction_df['Regulated Name'].str.lower())
    category = [str(ele) for ele in category]
    if 'nan' in category:
        category.remove('nan')
    else:
        pass

    # Get the set in which elements are regulators but not regulated
    category_reg = set(interaction_df['Regulator Name'])
    category_reg = [ele for ele in category_reg]

    if 'nan' in category_reg:
        category_reg.remove('nan')
    else:
        pass

    k = 0; element_name_list = []
    for element in category:
        # Find the sub-dataframe of every unique element
        element_df = interaction_df.loc[interaction_df['Regulated Name'].str.lower() == element].reset_index(drop=True)
        element_name = element_df.loc[0, 'Regulated Name']
        element_name_list.append(element_name)
        # initialize the variables
        i, j = 0, 0
        pos_reg_list, neg_reg_list, paper_id_list, source_list, score_list = str(), str(), str(), str(), str()
        pos_connection, neg_connection = str(), str()
        pos_mech, neg_mech = str(), str()
        pos_site, neg_site = str(), str()
        pos_reg_stack, neg_reg_stack = [], []

        # get all the positive and negative regulator list for the unique element
        for row in range(len(element_df)):
            # get and clean up the name again to put them in positive/negative regulator list
            reg_name = element_df.loc[row, 'Regulator Name'].strip()
            #reg_name = reg_name.replace('*', '-')
            #reg_name = reg_name.replace('+', '')
            #reg_name = reg_name.replace(',', '_')
            # connection Type
            connection_type = element_df.loc[row, 'Connection Type']
            mech = element_df.loc[row, 'Mechanism']
            site = element_df.loc[row, 'Site']

            # append positive regulators
            if element_df.loc[row, 'Sign'].lower() in ['positive', 'positive', 'not positive']:
                if i != 0:
                    if reg_name.lower() not in pos_reg_stack:
                        pos_reg_list = pos_reg_list + f',{reg_name}'
                        pos_reg_stack.append(reg_name.lower())
                    else:
                        pass
                else:
                    pos_reg_list = reg_name
                    pos_reg_stack.append(reg_name.lower()) # store the last reg and compare with next reg to avoid repeat.

                # FIXME: Pos_connection, Pos_mech, Pos_site need to be discuss for repeating
                pos_connection = pos_connection + f',{connection_type}' if i != 0 else f'{connection_type}'
                #pos_mech = pos_mech + f',{mech}' if i != 0 else f'{mech}'
                #pos_site = pos_site + f',{site}' if i != 0 else f'{site}'

                i+=1
            # append negative regulators
            else:
                if j != 0:
                    if reg_name.lower() not in neg_reg_stack:
                        neg_reg_list = neg_reg_list + f',{reg_name}'
                        neg_reg_stack.append(reg_name.lower())
                    else:
                        pass
                else:
                    neg_reg_list = reg_name
                    neg_reg_stack.append(reg_name.lower()) # store the last reg and compare with next reg to avoid repeat.

                # FIXME: Pos_connection, Pos_mech, Pos_site need to be discuss for repeating
                neg_connection = neg_connection + f',{connection_type}' if j != 0 else f'{connection_type}'
                #neg_mech = neg_mech + f',{mech}' if j != 0 else f'{mech}'
                #neg_site = neg_site + f',{site}' if j != 0 else f'{site}'
                j+=1


            # append papers ids, source, and score
            paper_id = str(element_df.loc[row, 'Paper IDs'])
            source = str(element_df.loc[row, 'Source'])
            score = str(element_df.loc[row, 'Score'])

            # check if adjecent rows are from same paper id, sousrce, or score
            if row != 0:
                paper_id_list = paper_id_list + ',' + paper_id if paper_id != 'nan' else paper_id_list + ','
                source_list = source_list + ',' + source if source != 'nan' else source_list + ','
                score_list = score_list + ',' + score if score != 'nan' else score_list + ','
            else:
                paper_id_list = paper_id if paper_id != 'nan' else ''
                source_list = source if source != 'nan' else ''
                score_list = score if score != 'nan' else ''



        # copy regulated element attributions
        element_attribution = element_df.loc[0, bio_attrb]
        for i in range(len(attrb_cols)):
            output_ele_df.loc[k,attrb_cols[i]] = element_attribution[bio_attrb[i]]

        # paste the list parsed above
        output_ele_df.loc[k, 'Variable'] = element_name
        output_ele_df.loc[k, 'Positive Regulator List'] = pos_reg_list
        output_ele_df.loc[k, 'Negative Regulator List'] = neg_reg_list
        output_ele_df.loc[k, 'Positive Connection Type List'] = pos_connection
        output_ele_df.loc[k, 'Negative Connection Type List'] = neg_connection
        output_ele_df.loc[k, 'Positive Mechanism List'] = pos_mech
        output_ele_df.loc[k, 'Negative Mechanism List'] = neg_mech
        output_ele_df.loc[k, 'Positive Site List'] = pos_site
        output_ele_df.loc[k, 'Negative Site List'] = neg_site
        output_ele_df.loc[k, 'Paper IDs List'] = paper_id_list
        output_ele_df.loc[k, 'Source List'] = source_list
        output_ele_df.loc[k, 'Score List'] = score_list
        k+=1

    category_add = list(set(category_reg) - set(element_name_list))
    # Append the regulators that are never regulated in interactions file
    for element in category_add:
        element_df = interaction_df.loc[interaction_df['Regulator Name'] == element].reset_index(drop=True)

        # get attributes
        ele_ids = set(element_df['Regulator ID'].astype(str).to_list())
        ele_type = set(element_df['Regulator Type'].astype(str).to_list())
        ele_subtype = set(element_df['Regulator Subtype'].astype(str).to_list())
        ele_db = set(element_df['Regulator Database'].astype(str).to_list())

        # append attributes with different names but same elemnt
        name_list = set(element_df['Regulator Name'].to_list())

        for name in name_list:
            output_ele_df.loc[k, 'Element Name'] = name
            output_ele_df.loc[k, 'Variable'] = name
            # Put them to the model
            output_ele_df.loc[k, 'Element IDs'] = ','.join(list(ele_ids))
            output_ele_df.loc[k, 'Element Type'] = ','.join(list(ele_type))
            output_ele_df.loc[k, 'Element Subtype'] = ','.join(list(ele_subtype))
            output_ele_df.loc[k, 'Element Database'] = ','.join(list(ele_db))
            k+=1

    other_cols = list(set(model_cols) - set(output_ele_df.columns))
    # build BioRECIPE up
    model_bio_df = pd.concat([output_ele_df, pd.DataFrame(columns=other_cols)], axis = 1)

    # set variable name as the index
    model_bio_df = model_bio_df[model_cols]
    model_bio_df.set_index('Variable',inplace=True)

    return model_bio_df


def model_to_interactions(model : pd.DataFrame) -> pd.DataFrame:
    """Convert the model into a dataframe of edges in the format
        element-regulator-interaction
    """
    # check if the regulator and regulation columns are empty or not
    for sign in ['Positive', 'Negative']:
        if model[f'{sign} Regulator List'].empty and model[f'{sign} Regulation Rule'].empty:
            raise ValueError(
                "The regulation rule and list columns are both empty, please fill at least one column out"
            )
        elif not model[f'{sign} Regulator List'].empty and model[f'{sign} Regulation Rule'].empty:
            regulator, regulation = True, False
        elif model[f'{sign} Regulator List'].empty and not model[f'{sign} Regulation Rule'].empty:
            regulator, regulation = False, True
        else:
            regulator, regulation = True, True

    # convert to dict for iteration
    model_dict = model_to_dict(model)
    biorecipe_col = ["Regulator Name","Regulator Type","Regulator Subtype","Regulator HGNC Symbol","Regulator Database","Regulator ID","Regulator Compartment","Regulator Compartment ID"
    ,"Regulated Name","Regulated Type","Regulated Subtype","Regulated HGNC Symbol","Regulated Database","Regulated ID","Regulated Compartment","Regulated Compartment ID","Sign","Connection Type"
    ,"Mechanism", "Site", "Cell Line", "Cell Type","Tissue Type","Organism","Score","Source","Statements","Paper IDs"]
    interactions_dict, model_item_dict, i = dict(), dict(), 0

    model_col_index = ['Element Name',
    'Element Type',
    'Element Subtype',
    'Element IDs',
    'Cell Line',
    'Cell Type',
    'Organism',
    'Compartment',
    'Compartment ID',
    'Tissue Type'] # model intersect-column names
    interaction_col_index = ['Regulated Name',
    'Regulated Type',
    'Regulated Subtype',
    'Regulated ID',
    'Cell Line',
    'Cell Type',
    'Organism',
    'Regulated Compartment',
    'Regulated Compartment ID',
    'Tissue Type'] # interaction intersect-column names

    for key,item in model_dict.items():
        for index in model_col_index:
            model_item_dict[index] = item.get(index).strip() if item.get(index) is not None else ''
        if regulator:
            pos_reg_list = str(item.get('Positive Regulator List',''))
            neg_reg_list = str(item.get('Negative Regulator List',''))
        else:
            pos_reg_list = ','.join(list(set(get_element(str(item.get('Positive Regulation Rule')), 0))))
            neg_reg_list = ','.join(list(set(get_element(str(item.get('Negative Regulation Rule')), 0))))
        '''
        if pos_reg_list is None and neg_reg_list is None:
            pos_reg_list = str(item.get('Positive Regulation List',''))
            neg_reg_list = str(item.get('Negative Regulation List',''))
        '''
        pos_dict, neg_dict = dict(), dict()
        if pos_reg_list != 'nan':
            pos_list = [x.strip() for x in re.findall(r'[a-zA-Z0-9\_!=]+',pos_reg_list)]
            k = i
            pos_dict = {i: dict for pos in pos_list}
            for pos in pos_list:
                dict_ = dict()
                dict_ = {interc_index: model_item_dict[model_index] for interc_index, model_index in zip(interaction_col_index, model_col_index) }
                if pos[0] != '!':
                    dict_['Sign'] = 'Positive'
                    dict_['Regulator Name'] = pos
                else:
                    dict_['Sign'] = 'NOT Positive'
                    dict_['Regulator Name'] = pos[1:]
                pos_dict[k] = dict_
                k+=1
            i+= len(pos_list)
        else:
            pass

        if neg_reg_list != 'nan':
            neg_list = [x.strip() for x in re.findall(r'[a-zA-Z0-9\_!=]+',neg_reg_list)]
            j = i
            for neg in neg_list:
                dict_ = dict()
                dict_ = {interc_index: model_item_dict[model_index] for interc_index, model_index in zip(interaction_col_index, model_col_index) }
                if neg[0] != '!':
                    dict_['Sign'] = 'Negative'
                    dict_['Regulator Name'] = neg
                else:
                    dict_['Sign'] = 'NOT Negative'
                    dict_['Regulator Name'] = neg[1:]
                neg_dict[j] = dict_
                j+=1
            i+=len(neg_list)
        else:
            pass

        interactions_dict.update(pos_dict)
        interactions_dict.update(neg_dict)

    interaction_df = pd.DataFrame.from_dict(interactions_dict, orient='index')
    other_cols = list(set(biorecipe_col) - set(interaction_df.columns))
    # build BioRECIPE up
    interaction_bio_df = pd.concat([interaction_df, pd.DataFrame(columns=other_cols)], axis=1)
    # reorder the columns
    return interaction_bio_df[biorecipe_col]
