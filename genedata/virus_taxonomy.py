import pandas as pd
import pymysql
import pymysql.cursors


def get_db_data(query):
    connection = pymysql.connect(host='127.0.0.1',
                                 user='root',
                                 password='password',
                                 db='viralanalysisdb',
                                 cursorclass=pymysql.cursors.DictCursor)
    df = pd.read_sql(query, connection)
    return df


def getTaxonomyDistribution():
    """Get the virus taxonomy distribution.

    Accesses the database to retrieve the gene_taxonomy data and returns the
    virus type distribution.

    :return: Dictionary of virustype:count
    """
    df = get_db_data(
        'select `group`, COUNT(`group`) as taxocount from gene_taxonomy group by `group`')
    taxonomy_distrubution = {}
    for row in df.itertuples():
        taxonomy_key = row[1].strip()
        taxonomy_distrubution[taxonomy_key] = int(row[2])
    return taxonomy_distrubution

def getTaxonomyData(filteredList = '("")'):
    """Get specific taxonomy data for each virus"""
    df = get_db_data(
        'select `sequence_id`, `domain`, `group` from gene_taxonomy where `group` not in {} limit 20'.format(filteredList))
    tax_data = []
    for row in df.itertuples():
        tax_key = getattr(row, 'sequence_id')
        tax_domain = getattr(row, 'domain')
        tax_group = getattr(row, 'group')
        tax_data.append( [tax_key, tax_domain, tax_group] )
    return tax_data
		
def format_taxonomy(virus_taxonomy_distribution):
    """Return the formatted values to be sent to charting library in json format.

    :param virus_taxonomy_distribution: dictionary of virus taxonomy distribution
    :return: Two lists: labels and values
    """
    labels = []
    values = []
    for key in virus_taxonomy_distribution:
        labels.append(key)
        values.append(virus_taxonomy_distribution[key])

    return labels, values


if __name__ == '__main__':
    print(getTaxonomyDistribution())
