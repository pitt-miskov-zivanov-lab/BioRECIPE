from within_biorecipe.biorecipe_std import BioRECIPE, get_model, get_reading
import pandas as pd
import numpy as np
import networkx as nx
import warnings
import re
import argparse

def get_element(reg_rule: str, layer=0):

    """
    Convert a regulation rule to a regulator list
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

                if '*' in enhence_element:
                    weight, name = necessary_element.split('*')
                    regulator_list = regulator_list + get_element(name, 1)
                else:
                    regulator_list = regulator_list + get_element(enhence_element, 1)

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
                        if re.search(r'^[0-9]', reg_):
                            pass
                        elif re.search(r'[a-zA-Z0-9\_!]+', reg_) is None:
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

def model_to_interactions(model : pd.DataFrame) -> pd.DataFrame:

    """
    Convert the model dataframe into a dataframe of edges in the format
    element-regulator-interaction
    """

    # convert to dict for iteration
    model_dict = model.to_dict(orient='index')

    biorecipe_col = BioRECIPE().biorecipe_int_cols
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
            if type(item.get(index)) == str:
                model_item_dict[index] = item.get(index).strip() if item.get(index) is not None else ''
            else:
                model_item_dict[index] = str(item.get(index)).strip()
            pos_reg_rule = item.get('Positive Regulation Rule')
            neg_reg_rule = item.get('Negative Regulation Rule')
            pos_reg_list = '' if pos_reg_rule == '' else ','.join(list(set(get_element(pos_reg_rule, 0))))
            neg_reg_list = '' if neg_reg_rule == '' else ','.join(list(set(get_element(neg_reg_rule, 0))))

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
    return interaction_bio_df[biorecipe_col]

def interactions_to_model(interaction_df : pd.DataFrame) -> pd.DataFrame:

    """
    Convert a interaction dataFrame to model dataframe
    """

    model_cols = BioRECIPE().biorecipe_mdl_cols

    attrb_cols = ['Element Name', 'Element Type', 'Element Database', 'Element Subtype','Element HGNC Symbol','Element IDs','Compartment', 'Compartment ID', 'Cell Line', 'Cell Type', 'Tissue Type', 'Organism']

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

    ele_dict, pos_reg_list, output_ele_df = {}, str(), pd.DataFrame(columns=model_cols)
    category_stack = []

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
                j+=1

            # append papers ids, source, and score
            paper_id = str(element_df.loc[row, 'Paper IDs'])
            source = str(element_df.loc[row, 'Source'])
            score = str(element_df.loc[row, 'Score'])

            # check if adjecent rows are from same paper id, source, or score
            if row != 0:
                paper_id_list = paper_id_list + ',' + paper_id if paper_id != 'nan' else paper_id_list + ','
                source_list = source_list + ',' + source if source != 'nan' else source_list + ','
                score_list = score_list + ',' + score if score != 'nan' else score_list + ','
            else:
                paper_id_list = paper_id if paper_id != 'nan' else np.nan
                source_list = source if source != 'nan' else np.nan
                score_list = score if score != 'nan' else np.nan

        # copy regulated element attributions
        element_attribution = element_df.loc[0, bio_attrb]
        for i in range(len(attrb_cols)):
            output_ele_df.loc[k,attrb_cols[i]] = element_attribution[bio_attrb[i]]

        output_ele_df.loc[k, '#'] = str(int(k+1))

        # paste the list parsed above
        output_ele_df.loc[k, 'Variable'] = element_name
        output_ele_df.loc[k, 'Positive Regulator List'] = pos_reg_list
        output_ele_df.loc[k, 'Negative Regulator List'] = neg_reg_list
        output_ele_df.loc[k, 'Positive Connection Type List'] = pos_connection if (pos_connection != len(pos_connection) * ',') else np.nan
        output_ele_df.loc[k, 'Negative Connection Type List'] = neg_connection if (neg_connection != len(neg_connection) * ',') else np.nan
        output_ele_df.loc[k, 'Positive Mechanism List'] = pos_mech if (pos_mech != len(pos_mech) * ',') else np.nan
        output_ele_df.loc[k, 'Negative Mechanism List'] = neg_mech if (neg_mech != len(neg_mech) * ',') else np.nan
        output_ele_df.loc[k, 'Positive Site List'] = pos_site if (pos_site != len(pos_site) * ',') else np.nan
        output_ele_df.loc[k, 'Negative Site List'] = neg_site if (neg_site != len(neg_site) * ',') else np.nan
        output_ele_df.loc[k, 'Paper IDs List'] = paper_id_list if (paper_id_list != len(paper_id_list) * ',') else np.nan
        output_ele_df.loc[k, 'Source List'] = source_list if (source_list != len(source_list) * ',') else np.nan
        output_ele_df.loc[k, 'Score List'] = score_list if (score_list != len(score_list) * ',') else np.nan

        #FIXME later: for now assume 'Positive Regulation Rule' is always ORing all elements in 'Positive Regulator List'
        output_ele_df.loc[k, 'Positive Regulation Rule'] = pos_reg_list
        output_ele_df.loc[k, 'Negative Regulation Rule'] = neg_reg_list

        k+=1

    category_add = list(set(category_reg) - set(element_name_list))
    # Append the regulators that are never regulated in interactions file
    for element in category_add:
        element_df = interaction_df.loc[interaction_df['Regulator Name'] == element].reset_index(drop=True)

        # get attributes
        ele_ids = set(element_df['Regulator ID'].astype("string").to_list())
        ele_type = set(element_df['Regulator Type'].astype("string").to_list())
        ele_subtype = set(element_df['Regulator Subtype'].astype("string").to_list())
        ele_db = set(element_df['Regulator Database'].astype("string").to_list())

        # append attributes with different names but same element
        name_list = set(element_df['Regulator Name'].to_list())

        for name in name_list:
            output_ele_df.loc[k, '#'] = str(int(k+1))
            output_ele_df.loc[k, 'Element Name'] = name
            output_ele_df.loc[k, 'Variable'] = name
            # Put them to the model
            output_ele_df.loc[k, 'Element IDs'] = ','.join([i for i in list(ele_ids) if not pd.isna(i)])
            output_ele_df.loc[k, 'Element Type'] = ','.join([i for i in list(ele_type) if not pd.isna(i)])
            output_ele_df.loc[k, 'Element Subtype'] = ','.join([i for i in list(ele_subtype) if not pd.isna(i)])
            output_ele_df.loc[k, 'Element Database'] = ','.join([i for i in list(ele_db) if not pd.isna(i)])
            k+=1

    output_ele_df.fillna('',inplace=True)
    # build BioRECIPE up
    return output_ele_df

def model_to_edges_set(model : pd.DataFrame) -> set:

    """
    Convert the model into a set of edges in the format
    regulator-regulated-interaction with +/- for interaction
    """

    model_dict = model.to_dict(orient='index')

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

def get_interactions_from_model(model_file, interactions_file):

    """
    Convert the model spreadsheet .xlsx into interaction spreadsheet .xlsx
    """

    model = get_model(model_file)
    interaction_df = model_to_interactions(model)
    interaction_df.to_excel(interactions_file, index=False)
    return

def get_model_from_interactions(interaction_file, model_file):

    """
    Convert the interaction spreadsheet .xlsx into model spreadsheet .xlsx
    """

    # load and preprocess the interactions to DataFrame
    interaction_df = get_reading(interaction_file)
    model_df = interactions_to_model(interaction_df)
    model_df.to_excel(model_file, index=False)
    return

def get_biorecipeI_from_reach_tab(reach_tab_file, interactions_file):

    """
    This is a function to translate REACH tabular format to BioRECIPE interaction format

    Parameters
	----------
    reach_tab_file:
        REACH tabular format file (.csv) containing reading machine's output

    Returns
	-------
    interactions_file:
        BioRECIPE interaction file
    """

    input_df = pd.read_csv(reach_tab_file, sep='\t')
    recipe_format = BioRECIPE()
    reach_tab = recipe_format.get_format("reach_tab")
    biorecipe = recipe_format.get_format("biorecipe")

    output_df_biorecipe = pd.DataFrame(columns=recipe_format.biorecipe_int_cols)
    for i in range(len(input_df)):
        for col in recipe_format.default_cols:
            biorecipe_col = biorecipe[col]
            reach_tab_col = reach_tab[col]
            if col == "regulator_name":
                if input_df.isnull().loc[i, reach_tab["NegReg_Name"]]:
                    output_df_biorecipe.loc[i, biorecipe_col] = input_df.loc[i, reach_tab["PosReg_Name"]]
                    output_df_biorecipe.loc[i, biorecipe["regulator_id"]] = input_df.loc[i, reach_tab["PosReg_ID"]]
                    output_df_biorecipe.loc[i, biorecipe["regulator_compartment"]] = input_df.loc[
                        i, reach_tab["PosReg_Location"]]
                    output_df_biorecipe.loc[i, biorecipe["regulator_compartment_id"]] = input_df.loc[
                        i, reach_tab["PosReg_Location_ID"]]
                    output_df_biorecipe.loc[i, biorecipe["sign"]] = "positive"

                else:
                    output_df_biorecipe.loc[i, biorecipe_col] = input_df.loc[i, reach_tab["NegReg_Name"]]
                    output_df_biorecipe.loc[i, biorecipe["regulator_id"]] = input_df.loc[i, reach_tab["NegReg_ID"]]
                    output_df_biorecipe.loc[i, biorecipe["regulator_compartment"]] = input_df.loc[
                        i, reach_tab["NegReg_Location"]]
                    output_df_biorecipe.loc[i, biorecipe["regulator_compartment_id"]] = input_df.loc[
                        i, reach_tab["NegReg_Location_ID"]]
                    output_df_biorecipe.loc[i, biorecipe["sign"]] = "negative"
            elif reach_tab_col and biorecipe_col:
                output_df_biorecipe.loc[i, biorecipe_col] = input_df.loc[i, reach_tab_col]
            else:
                pass
    df = pd.DataFrame(output_df_biorecipe, columns=recipe_format.biorecipe_int_cols)
    df.to_excel(interactions_file, index=False)
    return

def main():
    parser = argparse.ArgumentParser(
        description='Prceess model/interactions list and convert among formats.',
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument('--input_file', type=str, help='Input file path')
    parser.add_argument('--output_file', type=str, help='Output file path')

    parser.add_argument('--input_format', '-i', type=str, choices=["interactions", "model", "reach_tab"],
    default='interactions',
    help='Input file format \n'
        '\t interactions (default): BioRECIPE interactions file \n'
        '\t model: BioRECIPE model file\n'
        '\t reach_tab: reach_tab spreadsheet\n')

    args = parser.parse_args()

    if args.input_format == 'interactions':
        get_model_from_interactions(args.input_file, args.output_file)

    elif args.input_format == 'model':
        get_interactions_from_model(args.input_file, args.output_file)

    elif args.input_format == 'reach_tab':
        get_biorecipeI_from_reach_tab(args.input_file, args.output_file)

if __name__ == '__main__':
    main()
