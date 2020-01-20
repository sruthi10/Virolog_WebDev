import pandas as pd
import re


def get_csv_data(filename):
    df = pd.read_csv(filename)
    return df


def get_mapping(filename, pvalue):
    df = get_csv_data(filename)
    df = df.drop(df[df.probability_of_presequence < pvalue].index)
    cleavagecountmapping = {}
    for k, v in df.groupby(['cleavage_site']).size().to_dict().iteritems():
        numeric_key = re.match(r'[0-9]+', k.strip())
        if numeric_key:
            cleavagecountmapping[int(numeric_key.group(0))] = v
    return cleavagecountmapping


def format_values(cleavage_mapping_virus):
    cleavage_labels = []
    cleavage_site_values = []
    for key, value in cleavage_mapping_virus.iteritems():
        if key % 10 == 0:
            cleavage_labels.append(key)
        else:
            cleavage_labels.append('')
        cleavage_site_values.append(value)

    return cleavage_labels, cleavage_site_values
