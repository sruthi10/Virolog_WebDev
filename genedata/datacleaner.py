import pandas as pd
import csv


def get_data(filename):
    path = 'csvdata/' + filename + '.csv'
    df = pd.read_csv(path)
    return df


def clean_cleavage_data():
    filename = r'mitofatesResults_Mouse.MitoCarta2.0'
    df = get_data(filename)
    cleanDataList = []

    for index, row in df.iterrows():
        if ',' in str(row['Cleavage_site']):
            cleavage_site_values = str(row['Cleavage_site']).split(',')
            for val in cleavage_site_values:
                newrow = row.copy()
                newrow['Cleavage_site'] = str(val)
                cleanDataList.append(newrow)
        else:
            cleanDataList.append(row)

    newDataFrame = pd.DataFrame(cleanDataList, columns=df.columns)
    newDataFrame.to_csv('outputdata/' + file + '-cleaned.csv', sep=',')


def clean_taxonomy_data():
    """Clean the taxonomy data kept in csvdata folder and output new file.

    Removes trailing whitespace, generates a well-formed csv
    from the raw csv file. Writes the csv file to the output
    data directory. After generating the csv file, open this
    file in Excel, save as CSV to add null columns for all
    the rows.

    Args:

    Returns:
        None

    """
    filename = r'gene_taxonomy'
    df = get_data(filename)
    csvrows = []
    for index, row in df.iterrows():
        newrow = [row[0]]
        newrow.extend(x.strip() for x in row[1].replace('"', '').split(','))
        csvrows.append(newrow)
    with open('outputdata/gene_taxonomy.csv', 'wb') as csvfile:
        writer = csv.writer(csvfile, delimiter=',')
        for newrow in csvrows:
            writer.writerow(newrow)


if __name__ == '__main__':
    clean_taxonomy_data()
