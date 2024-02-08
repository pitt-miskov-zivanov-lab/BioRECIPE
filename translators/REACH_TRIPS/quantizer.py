"""Convert real values to discrete using quantization methods"""
import logging
import pandas as pd
import numpy as np


def read_data_column(input_filename, sheet_name=0, data_column=0, header=0):
    """Read a column of input data from Excel
    """

    input_data = pd.read_excel(input_filename, sheet_name=sheet_name, header=header)

    if type(data_column) is int:
        # get name of column from its index
        data_column = input_data.columns[data_column]
    
    input_data_series = input_data[data_column]

    return input_data_series


def get_thresholds(data_min, data_max, levels=3, distribution='uniform'):
    """Calculate threshold values given min/max and optionally number of levels
    """

    # TODO: different distributions other than uniform

    if distribution == 'uniform':
        bin_width = (float(data_max) - float(data_min))/float(levels)
        thresholds = [bin_width*idx for idx in range(levels)] + [data_max]
    else:
        raise ValueError(f'Unrecognized distribution: {distribution}')

    return thresholds


def quantize_data(data: pd.DataFrame, thresholds=None, levels=None, columns=None):
    """Quantize values in a DataFrame, using dicts of thresholds or levels if specified

    Inputs:
        thresholds: dict of lists, keys must be data.columns or columns
        levels: dict of ints, keys must be data.columns or columns
        columns: subset of data.columns to quantize
    """

    # prepare dicts for passing to quantize_data_series
    if thresholds is None:
        thresholds = {col : None for col in data.columns}
    
    if levels is None:
        levels = {col : None for col in data.columns}
    
    if columns is None:
        columns = data.columns

    # TODO: preserve msqe and add error_method as input
    data_quant = data.apply(
            lambda col: 
            quantize_data_series(col, thresholds[col.name], levels[col.name])[0]
            if col.name in columns else col
            )
    
    return data_quant


def quantize_data_series(data_series: pd.Series, thresholds=None, levels=None, error_method='difference'):
    """Quantize values in a data series, using the specified number of levels or a list of thresholds

    Inputs:
        thresholds: list, should include the min and max data values so length hould be num levels + 1
        levels: int, number of discrete levels desired from quantization
    """


    # TODO: support thresholds as percent of max
    # TODO: other quantization methods/thresholds

    if levels is not None and thresholds is not None:
        # the number of thresholds should be one less than the number of levels
        if len(thresholds) > (int(levels)+1):
            logging.warning('Too many thresholds for the number of levels, thresholds will take precedence')
        elif len(thresholds) < (int(levels)+1):
            logging.warning('Not enough thresholds for the number of levels, thresholds will take precedence')

    if levels is None:
        # default to 3 levels
        levels = 3
    elif levels < 2:
        raise ValueError('Need at least 2 levels')
    
    if thresholds is None:
        # default to uniform quantization using the range of values in the data
        thresholds = get_thresholds(data_series.min(), data_series.max(), levels)
    
    data_quantized = data_series.apply(quantize_by_threshold, thresholds=thresholds, error_method=error_method)

    data_quantized = data_quantized.apply(pd.Series)

    return data_quantized


def quantize_by_threshold(data_value, thresholds, error_method='difference'):
    """Quantize by comparing a value to specified thresholds, return discrete level and quantization error
    """
    
    # get equivalent data values of the quantization levels
    # as the midpoint between threshold levels
    # to calculate quantization error
    quant_values = [(thresholds[idx+1] - thresholds[idx])/2 for idx in range(len(thresholds)-1)]

    # will compare to each threshold to see if data value is < threshold
    data_level = -1

    for idx,this_threshold in enumerate(thresholds[1:]):
        if data_value <= this_threshold:
            data_level = idx
            quantization_error = get_quantization_error(data_value, quant_values[idx], error_method)
            break
    
    if data_level == -1:
        raise ValueError(f'Data value out of range: {data_value}')

    return data_level, quantization_error


def get_quantization_error(data_value, quantization_level, method='difference'):
    
    # TODO: other quantization error calculations
    
    if method == 'difference':
        quantization_error = quantization_level - data_value
    else:
        raise ValueError(f'Unrecognized quantization method: {method}')
    
    return quantization_error


def get_msqe(quantization_error):

    # note that numpy square is faster than x*x, x**2 or pow(x,2) with lists
    msqe = np.square(np.array(quantization_error)).mean()

    return msqe


def format_data_for_input(data_quantized, repeats=1):
    """Set the time scale of quantized data and convert to simulation toggle notation
    """

    # repeat numbers in input sequence to scale simulation length
    data_scaled = np.repeat(list(data_quantized), repeats)

    # create a comma-separated string of values starting with the initial value
    # using toggle (bracket) notation
    # the first value is assumed to be at step 0 (the initial value)
    # so there is no bracket notation
    input_sequence_list = [str(int(data_scaled[0]))]
    # adding 1 to the idx when adding steps to the input string,
    # because of the enumerate index and starting from the second value in data_scaled
    # only including values that change from the previous value (data_scaled[idx] != data_scaled[idx-1])
    input_sequence_list += [
            f'{int(data_value)}[{idx+1}]' 
            for idx,data_value in enumerate(data_scaled[1:])
            if data_scaled[idx] != data_scaled[idx-1]
            ]
    
    input_sequence = ','.join(input_sequence_list)

    return input_sequence
