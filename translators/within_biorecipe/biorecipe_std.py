from collections import OrderedDict
from dataclasses import dataclass, asdict
from typing import Optional
import pandas as pd
import warnings
import re
import argparse
import logging


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

# define regex for valid characters in variable names
_VALID_CHARS = r'a-zA-Z0-9\_'

# valid element types
_VALID_TYPES = [
    'protein', 'protein family', 'protein complex',
    'rna', 'mrna', 'gene', 'chemical', 'biological process'
    ]

_VAR_COL = 'Variable'
_IDX_COL = '#'

@dataclass
class ReadingOutput:
    # Required columns for a minimal form of reading output
    # NOTE: this is only for columns matching, values should be updated if needed
    regulator_name: Optional[str] = None
    regulator_type: Optional[str] = None
    regulator_id: Optional[str] = None
    regulator_subtype: Optional[str] = None
    regulator_hgnc_symbol: Optional[str] = None
    regulator_database: Optional[str] = None
    regulator_compartment: Optional[str] = None
    regulator_compartment_id: Optional[str] = None
    regulator_full_id: Optional[str] = None
    regulator_cell_type: Optional[str] = None
    regulator_cell_line: Optional[str] = None
    regulator_variable_name: Optional[str] = None

    regulated_name: Optional[str] = None
    regulated_type: Optional[str] = None
    regulated_id: Optional[str] = None
    regulated_subtype: Optional[str] = None
    regulated_hgnc_symbol: Optional[str] = None
    regulated_hgnc_id: Optional[str] = None
    regulated_database: Optional[str] = None
    regulated_compartment: Optional[str] = None
    regulated_compartment_id: Optional[str] = None
    regulated_full_id: Optional[str] = None
    regulated_cell_type: Optional[str] = None
    regulated_cell_line: Optional[str] = None
    regulated_variable_name: Optional[str] = None

    sign: Optional[str] = None
    connection_type: Optional[str] = None
    mechanism: Optional[str] = None
    site: Optional[str] = None

    cell_line: Optional[str] = None
    cell_type: Optional[str] = None
    tissue_type: Optional[str] = None
    organism: Optional[str] = None

    score: Optional[str] = None
    source: Optional[str] = None
    statements: Optional[str] = None
    paper_ids: Optional[str] = None
    #Optional columns
    PosReg_Name: Optional[str] = None # PosReg_name is the abbrivation of Positive Regulator Name
    PosReg_Type: Optional[str] = None
    PosReg_Connection_Type: Optional[str] = None
    PosReg_Mechanism: Optional[str] = None
    PosReg_ID: Optional[str] = None
    PosReg_Location: Optional[str] = None
    PosReg_Location_ID: Optional[str] = None
    NegReg_Name: Optional[str] = None
    NegReg_Type: Optional[str] = None
    NegReg_Connection_Type: Optional[str] = None
    NegReg_Mechanism: Optional[str] = None
    NegReg_ID: Optional[str] = None
    NegReg_Location: Optional[str] = None
    NegReg_Location_ID: Optional[str] = None
    # clarinet special columns
    kindscore: Optional[str] = None
    matchlevel: Optional[str] = None
    epistemicvalue: Optional[str] = None
    file_numbers: Optional[str] = None
    number:Optional[str] = None
    database_source: Optional[str] = None
    database_id: Optional[str] = None

class BioRECIPE:
    __FORMAT = {}
    # this is for BioRECIPE reading output
    BIORECIPE = OrderedDict([("regulator_name","Regulator Name"),
                                     ("regulator_type","Regulator Type"),
                                     ("regulator_subtype","Regulator Subtype"),
                                     ("regulator_hgnc_symbol","Regulator HGNC Symbol"),
                                     ("regulator_database","Regulator Database"),
                                     ("regulator_id","Regulator ID"),
                                     ("regulator_compartment","Regulator Compartment"),
                                     ("regulator_compartment_id","Regulator Compartment ID"),
                                     ("regulated_name","Regulated Name"),
                                     ("regulated_type","Regulated Type"),
                                     ("regulated_subtype","Regulated Subtype"),
                                     ("regulated_hgnc_symbol","Regulated HGNC Symbol"),
                                     ("regulated_database","Regulated Database"),
                                     ("regulated_id","Regulated ID"),
                                     ("regulated_compartment","Regulated Compartment"),
                                     ("regulated_compartment_id","Regulated Compartment ID"),
                                     ("sign","Sign"),
                                     ("connection_type","Connection Type"),
                                     ("mechanism", "Mechanism"),
                                     ("site", "Site"),
                                     ("cell_line", "Cell Line"),
                                     ("cell_type", "Cell Type"),
                                     ("tissue_type","Tissue Type"),
                                     ("organism","Organism"),
                                     ("score","Score"),
                                     ("source","Source"),
                                     ("statements","Statements"),
                                     ("paper_ids","Paper IDs")
                                     ])
    __BIORECIPE_DATA = ReadingOutput(**BIORECIPE)
    __BIORECIPE_DICT = asdict(__BIORECIPE_DATA)

    reach_tab = OrderedDict([("regulated_name", "Element Name"),
                       ("regulated_type", "Element Type"),
                       ("regulated_database", "Database Name"),
                       ("regulated_id", "Element Identifier"),
                       ("regulated_compartment", "Location"),
                       ("regulated_compartment_id", "Location Identifier"),
                       ("cell_line", "Cell Line"),
                       ("cell_type", "Cell Type"),
                       ("organism", "Organism"),
                       ("paper_ids", "Paper ID"),
                       ("PosReg_Name", "PosReg Name"),
                       ("PosReg_Type", "PosReg Type"),
                       ("PosReg_ID", "PosReg ID"),
                       ("PosReg_Location", "PosReg Location"),
                       ("PosReg_Location_ID", "PosReg Location ID"),
                       ("NegReg_Name", "NegReg Name"),
                       ("NegReg_Type", "NegReg Type"),
                       ("NegReg_ID", "NegReg ID"),
                       ("NegReg_Location", "NegReg Location"),
                       ("NegReg_Location_ID", "NegReg Location ID"),
                       ("connection_type", "Interaction  Direct (D) or Indirect (I)"),
                       ("mechanism", "Mechanism Type for Direct"),
                       ("statements", "Evidence")
                       ])
    __reach_tab_DATA = ReadingOutput(**reach_tab)
    __reach_tab_DICT = asdict(__reach_tab_DATA)

    def __init__(self):
        # by default, we register BioRECIPE, FLUTE, VIOLIN reading formats automatically
        self.register_format("biorecipe", self.__BIORECIPE_DICT)
        self.register_format("reach_tab", self.__reach_tab_DICT)

        # What's more, we register full base dateclass to check the same columns in both formats
        self.default_cols = list(self.__BIORECIPE_DICT.keys())

        # Finally, we create BioRECIPE, reach_tab, FLUTE, VIOLIN, and CLARINET table headers to contain the data
        self.biorecipe_cols = list(self.BIORECIPE.values())
        self.reach_tab_cols = list(self.reach_tab.values())

    @classmethod
    def get_cols(cls, format_name):
        cols = list(cls.get_format(format_name).values())
        # return list([col for ])
        return list(filter(lambda col: col is not None, cols))

    @classmethod
    def get_format(cls, format_name):
        """Return the instance of a registered format"""
        format = cls.__FORMAT.get(format_name, None)
        return format

    @classmethod
    def register_format(cls, format_name, obj):
        """Register a format providing the format name and the instance"""
        cls.__FORMAT[format_name] = obj

def drop_x_indices(model: pd.DataFrame) -> pd.DataFrame:

    """
    Drop rows with missing or X indices
    """

    if 'X' in model.index or 'x' in model.index:
        logging.info('Dropping %s rows with X indices' % str(len(model.loc[['X']])))
        model.drop(['X'],axis=0,inplace=True)
    if '' in model.index:
        logging.info('Dropping %s rows missing indices' % str(len(model.loc[['']])))
        model.drop([''],axis=0,inplace=True)

    return model

def get_model(model_file: str) -> pd.DataFrame:

    """
    Load model into a DataFrame and standardize column names
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

def format_variable_names(model: pd.DataFrame) -> pd.DataFrame:

    """
    Format model variable names to make compatible with model checking
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

    """
    Standardize element types
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
