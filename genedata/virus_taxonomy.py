import pandas as pd
import pymysql
import pymysql.cursors
import sys # only need to printing to console


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
        taxonomy_key = format_string(row[1].strip())
        taxonomy_distrubution[taxonomy_key] = int(row[2])
    return taxonomy_distrubution

def getTaxonomyData(filteredList = '("")'):
    """Get specific taxonomy data for each virus"""
    df = get_db_data(
        'select `sequence_id`, `domain`, `group` from gene_taxonomy where `group` not in {} limit 50'.format(filteredList))
    tax_data = []
    for row in df.itertuples():
        tax_key = getattr(row, 'sequence_id')
        tax_domain = format_string(getattr(row, 'domain'))
        tax_group = format_string(getattr(row, 'group'))
        tax_data.append( [tax_key, tax_domain, tax_group] )
    return tax_data
		
def newGetTaxonomyData(args, filteredList = '("")'):
    """Get specific taxonomy data for each virus"""
    orderby = "`sequence_id`"
    if args["order[0][column]"] is '1':
        orderby = "`domain`"
    elif args["order[0][column]"] is '2':
        orderby = "`group`"
    df = get_db_data(
        'select `sequence_id`, `domain`, `group` from gene_taxonomy where `group` not in {} AND (`sequence_id` LIKE "%{}%" OR `domain` LIKE "%{}%" OR `group` LIKE "%{}%") order by {} {} limit {} offset {}'.format(filteredList, args["search[value]"], args["search[value]"], args["search[value]"], orderby, args["order[0][dir]"], args["length"], args["start"]))
    total_size = get_db_data(
        'select COUNT(`sequence_id`) as count from gene_taxonomy')
    filtered_size = get_db_data(
        'select COUNT(`sequence_id`) as count from gene_taxonomy where `group` not in {} AND (`sequence_id` LIKE "%{}%" OR `domain` LIKE "%{}%" OR `group` LIKE "%{}%")'.format(filteredList, args["search[value]"], args["search[value]"], args["search[value]"]))
    print(filtered_size['count'][0], file=sys.stderr)
    print(total_size['count'][0], file=sys.stderr)
    tax_data = []
    for row in df.itertuples():
        tax_key = getattr(row, 'sequence_id')
        tax_domain = format_string(getattr(row, 'domain'))
        tax_group = format_string(getattr(row, 'group'))
        tax_data.append( [tax_key, tax_domain, tax_group] )
    data = {
        "draw": args["draw"],
        "recordsTotal": int(total_size['count'][0]),
        "recordsFiltered": int(filtered_size['count'][0]),
        "data": tax_data
    }
    return data
    
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

def format_string(group):
    new_group = group[0].upper() + group[1:]
    if "DsDNA" in new_group or "DsRNA" in new_group or "SsDNA" in new_group or "SsRNA" in new_group:
        new_group = group
    return new_group


if __name__ == '__main__':
    print(getTaxonomyDistribution())
