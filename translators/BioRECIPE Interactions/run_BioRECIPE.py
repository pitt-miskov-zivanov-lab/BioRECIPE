from util import BioRECIPE, get_model, model_to_dict
import pandas as pd
import warnings
import re
import argparse
import logging

def cmu_to_biorecipe(input_df):
    """This is a function for translating CMU input format to BioRECIPE reading output format

    :param input_df:
    :return:
    """
    recipe_format = BioRECIPE()
    cmu = recipe_format.get_format("cmu")
    biorecipe = recipe_format.get_format("biorecipe")

    output_df_biorecipe = pd.DataFrame(columns=recipe_format.biorecipe_cols)
    for i in range(len(input_df)):
        for col in recipe_format.default_cols:
            biorecipe_col = biorecipe[col]
            cmu_col = cmu[col]
            if col == "regulator_name":
                if input_df.isnull().loc[i, cmu["NegReg_Name"]]:
                    output_df_biorecipe.loc[i, biorecipe_col] = input_df.loc[i, cmu["PosReg_Name"]]
                    output_df_biorecipe.loc[i, biorecipe["regulator_id"]] = input_df.loc[i, cmu["PosReg_ID"]]
                    output_df_biorecipe.loc[i, biorecipe["regulator_compartment"]] = input_df.loc[
                        i, cmu["PosReg_Location"]]
                    output_df_biorecipe.loc[i, biorecipe["regulator_compartment_id"]] = input_df.loc[
                        i, cmu["PosReg_Location_ID"]]
                    output_df_biorecipe.loc[i, biorecipe["sign"]] = "positive"

                else:
                    output_df_biorecipe.loc[i, biorecipe_col] = input_df.loc[i, cmu["NegReg_Name"]]
                    output_df_biorecipe.loc[i, biorecipe["regulator_id"]] = input_df.loc[i, cmu["NegReg_ID"]]
                    output_df_biorecipe.loc[i, biorecipe["regulator_compartment"]] = input_df.loc[
                        i, cmu["NegReg_Location"]]
                    output_df_biorecipe.loc[i, biorecipe["regulator_compartment_id"]] = input_df.loc[
                        i, cmu["NegReg_Location_ID"]]
                    output_df_biorecipe.loc[i, biorecipe["sign"]] = "negative"
            elif cmu_col and biorecipe_col:
                output_df_biorecipe.loc[i, biorecipe_col] = input_df.loc[i, cmu_col]
            else:
                pass
    df = pd.DataFrame(output_df_biorecipe, columns=recipe_format.biorecipe_cols)
    return df

def get_element(reg_rule: str, layer=0):
    """Convert a regulation rule to a regulator list
    """
    if reg_rule:
        regulator_list = []

        if '+' not in reg_rule:
            reg_list = split_comma_out_parentheses(reg_rule)
        else:
            if ',' in reg_rule:
                raise ValueError(
                'Found mixed commas and plus sign in regulation function'
                )
            elif reg_rule[-1] == '+':
                raise ValueError(
                'Regulation rule is not correct'
                )
            else:
                reg_list = reg_rule.split('+')

        for reg_element in reg_list:
            if reg_element[0] == '{' and reg_element[-1] == '}':
                assert(layer == 0)
                if '*' in reg_element:
                    weight, name = reg_element[1:-1].split('*')
                    regulator_list = regulator_list + get_element(name, 1)
                else:
                    regulator_list = regulator_list + get_element(reg_element, 1)

            elif reg_element[0] == '{' and reg_element[-1] == ']':
                # This is a necessary pair
                # check the point between {} and []
                parentheses = 0
                cutpoint = 0
                for index, char in enumerate(reg_element):
                    if char == '{':
                        parentheses +=1
                    elif char =='}':
                        parentheses -=1

                    if parentheses == 0:
                        cutpoint = index
                        break

                necessary_element = reg_element[1: cutpoint]
                enhence_element = reg_element[cutpoint+2:-1]
                if '*' in necessary_element:
                    weight, name = necessary_element.split('*')
                    regulator_list = regulator_list + get_element(name, 1)
                else:
                    regulator_list = regulator_list + get_element(necessary_element, 1)

                if '*' in necessary_element:
                    weight, name = necessary_element.split('*')
                    regulator_list = regulator_list + get_element(name, 1)
                else:
                    regulator_list = regulator_list + get_element(necessary_element, 1)

            elif reg_element[0] == '(' and reg_element[-1] == ')':
                list = [element for ele_list in split_comma_out_parentheses(reg_element[1:-1])
                        for element in get_element(ele_list, 1)]
                regulator_list += list
            else:

                assert(',' not in reg_element)

                if reg_element[-1] == '^':
                    regulator_list.append(reg_element[0:-1])
                elif '&' in reg_element:
                    regulator_list.append(reg_element[1:-1])
                elif '*' in reg_element:
                    multiply_reg_list = reg_element.split('*')
                    for reg_ in multiply_reg_list:
                        if not re.search(r'[a-zA-Z0-9\ !]]+', reg_):
                            pass
                        else:
                            regulator_list.append(reg_)
                elif reg_element[0] == '!':
                    if '~' in reg_element[1:]:
                        delay, reg_delay = reg_element[1:].split('~')
                        regulator_list.append(reg_delay)
                    else:
                        regulator_list.append(reg_element[1:])

                elif '=' in reg_element:
                    name, target_state = reg_element.split('=')
                    regulator_list.append(target_state)
                elif '~' in reg_element:
                    delay, state = reg_element.split('~')
                    regulator_list.append(state)

                else:
                    regulator_list.append(reg_element)

        return regulator_list

def split_comma_out_parentheses(reg_rule:str):
    """
    split the comma outside of parentheses
    """
    reg_list = list()
    parentheses = 0
    start = 0
    for index, char in enumerate(reg_rule):
        if index == len(reg_rule) - 1:
            reg_list.append(reg_rule[start:index+1])
        elif char == '(' or char == '{' or char == '[':
            parentheses += 1
        elif char == ')' or char == '}' or char == ']':
            parentheses -= 1
        elif (char == ',' and parentheses == 0):
            reg_list.append(reg_rule[start:index])
            start = index+1
    return reg_list

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
def model_to_interactions(model : pd.DataFrame) -> pd.DataFrame:
    """Convert the model into a dataframe of edges in the format
        element-regulator-interaction
    """

    '''
    # check if the regulator and regulation columns are empty or not
    for sign in ['Positive', 'Negative']:
        print(model[f'{sign} Regulator List'].empty)
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
    '''
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
    #print(model_dict)
    for key,item in model_dict.items():
        for index in model_col_index:
            model_item_dict[index] = item.get(index).strip() if item.get(index) is not None else ''
            pos_reg_list = ','.join(item.get('Positive List',''))
            neg_reg_list = ','.join(item.get('Negative List',''))
        '''
        if pos_reg_list is None and neg_reg_list is None:
            pos_reg_list = str(item.get('Positive Regulation List',''))
            neg_reg_list = str(item.get('Negative Regulation List',''))
        '''
        pos_dict, neg_dict = dict(), dict()
        if pos_reg_list != 'nan' or pos_reg_list != '':
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

        if neg_reg_list != 'nan' or neg_reg_list != '':
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
    interaction_bio_df
    return interaction_bio_df[biorecipe_col]


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

        # append attributes with different names but same element
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

    return model_bio_df[model_cols]


def model_to_edges_set(model : pd.DataFrame) -> set:
    """Convert the model into a set of edges in the format
        regulator-regulated-interaction with +/- for interaction
    """

    model_dict = model_to_dict(model)

    edges_set = set()

    # create entries in edges_dict for each regulator-regulated pair in the model
    # using the model dict positive and negative regulator lists
    for key,item in model_dict.items():

        # re-parsing here to handle ! (not) notation
        # TODO: also handle AND, highest state, etc.
        pos_list = re.findall(r'[a-zA-Z0-9\_!]+',item.get('Positive',''))
        neg_list = re.findall(r'[a-zA-Z0-9\_!]+',item.get('Negative',''))

        for i,pos in enumerate(pos_list):
            if pos[0]!='!':
                edges_set.add((pos, key, '+'))
            else:
                # NOT increases
                edges_set.add((pos[1:], key, '-'))

        for i,neg in enumerate(neg_list):
            if neg[0]!='!':
                edges_set.add((neg, key, '-'))
            else:
                # NOT decreases
                edges_set.add((neg[1:], key, '+'))

    return edges_set

def get_interactions(model_file: str) -> pd.DataFrame:
    df_interactions = pd.read_excel(model_file, index_col=None)
    return df_interactions

def main():
    parser = argparse.ArgumentParser(
        description='Prceess model/interactions list and convert among formats.',
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument('input_file', type=str, help='Input file path')
    parser.add_argument('output_file', type=str, help='Input file path')

    parser.add_argument('--input_format', '-i', type=str, choices=["interactions", "model", "cmu"],
    default='interactions',
    help='Input file format \n'
        '\t interactions (default): BioRECIPE interactions file \n'
        '\t model: BioRECIPE model file\n'
        '\t cmu: cmu spreadsheet\n')


    args = parser.parse_args()

    if args.input_format == 'interactions':
        interactions = get_interactions(args.input_file)
        model = interactions_to_model(interactions)
        model.to_excel(args.output_file, index=False)

    elif args.input_format == 'model':
        model = get_model(args.input_file)
        interactions = model_to_interactions(model)
        interactions.to_excel(args.output_file, index=False)

    elif args.input_format == 'cmu':
        cmu = pd.read_csv(args.input_file, sep='\t')
        interactions = cmu_to_biorecipe(cmu)
        interactions.to_excel(args.output_file, index=False)


if __name__ == '__main__':
    main()





















