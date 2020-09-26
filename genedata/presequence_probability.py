"""
Presequence Probability Controller

Functions that fetch and manipulate data necessary for the Presequence Probability page go here.

The following functions are available:
    * get_csv_data - function required to fetch data from csv file
    * get_mapping - return dictionary or labels and values
    * format_values - filter based on min and max P-values
"""

import pandas as pd
from collections import OrderedDict


def get_csv_data(filename):
    """Retrieve data from CSV file

    Parameters
    ----------
    filename : string
        file name of the CSV file to read

    Returns
    -------
    DataFrame
        DF of rows that represent data read from file
    """
    df = pd.read_csv(filename)
    return df


def get_mapping(filename,val):
    """Map data in CSV file so probability maps to num of presequences that have that probability (EX: 0.75 -> 10 indicates 10 presequences have probability of 0.75)

    Parameters
    ----------
    filename : string
        file name of the CSV file to read

    Returns
    -------
    OrderedDict
        Dict that represent the resulting mapping
    """
    df = get_csv_data(filename)
    #to round the input have only 2 decimal values
    df['probability_of_presequence'] = df['probability_of_presequence'].round(2)
    mapping = df.groupby(['probability_of_presequence']).size().to_dict()
    #del mapping[0] # this delete all 0.0 probabilities (removed to even get the count how many have 0 probability)
    orderedMapping = OrderedDict(sorted(mapping.items()))
    return orderedMapping


def format_values(mapping, pvalueMin, pvalueMax):
    """Filter mapping based on min and max P-values

    Parameters
    ----------
    mapping : OrderedDict`
        ordered dictionary of probabilities and their size
    pvalueMin : float
        min P-value to include
    pvalueMax : float
        max P-value to include

    Returns
    -------
    list, list
        labels and values for the probabilities after being filtered
    """
    probability_labels = []
    probability_values = []
    for key, value in mapping.items():
        if key >= pvalueMin and key <= pvalueMax:
            probability_labels.append(key)
            probability_values.append(value)
    # debug statements
    print("la")
    print(probability_labels)
    print(probability_values)

    return probability_labels, probability_values
