import pandas as pd
from collections import OrderedDict


def get_csv_data(filename):
    df = pd.read_csv(filename)
    return df


def get_mapping(filename):
    df = get_csv_data(filename)
    mapping = df.groupby(['probability_of_presequence']).size().to_dict()
    del mapping[0]
    orderedMapping = OrderedDict(sorted(mapping.items()))
    return orderedMapping


def format_values(mapping, pvalueMin, pvalueMax):
    probability_labels = []
    probability_values = []
    for key, value in mapping.items():
        if key >= pvalueMin and key <= pvalueMax:
            probability_labels.append(key)
            probability_values.append(value)

    return probability_labels, probability_values


def normalize(probability_values):
    targetvalues = []
    for value in probability_values:
        temp = (1 - 0.9) * value + (0.9 * 1000)
        targetvalues.append(temp)
    return targetvalues
