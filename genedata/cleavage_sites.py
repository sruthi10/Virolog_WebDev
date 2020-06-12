"""
Cleavage Sites Controller

Functions that fetch and manipulate data necessary for the Cleavage Sites page go here.

The following functions are available:
    * get_csv_data - function required to fetch data from csv file
    * get_mapping - return dictionary or labels and values
    * format_values - filter based on min and max P-values
"""
import pandas as pd
import re


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


def get_mapping(filename, pvalue):
    """Map data in CSV file so cleavage site is mapped to a count

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
    df = df.drop(df[df.probability_of_presequence < pvalue].index)
    cleavagecountmapping = {}
    for k, v in df.groupby(['cleavage_site']).size().to_dict().items():
        numeric_key = re.match(r'[0-9]+', k.strip())
        if numeric_key:
            cleavagecountmapping[int(numeric_key.group(0))] = v
            return cleavagecountmapping


        def format_values(cleavage_mapping_virus):
            """Format mapping to separate mapping into labels and values

    Parameters
    ----------
    cleavage_mapping_virus : dict
        mapping of cleavage site to a count

    Returns
    -------
    list, list
        labels and values for the cleavage sites and counts after being formatted
    """
            cleavage_labels = []
            cleavage_site_values = []
            for key, value in cleavage_mapping_virus.items():
                if key % 10 == 0:
                    cleavage_labels.append(key)
                    else:
                        cleavage_labels.append('')
                        cleavage_site_values.append(value)

                        return cleavage_labels, cleavage_site_values
