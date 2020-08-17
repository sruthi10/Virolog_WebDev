"""
Viral Taxonomy Controller

Functions that fetch and manipulate data necessary for the Viral Taxonomy page go here.

The following functions are available:
    * get_db_data - function required to interact with db
    * getTaxonomyData - get viral tax distribution data
    * getFilteredTaxonomyData - get filtered viral tax data based on list
    * format_taxonomy - helper function to separate labels and data
    * format_string - helper function to make sure DNA labels are correctly formatted
"""

import pandas as pd
import pymysql
import pymysql.cursors
import sys # only need to printing to console


def get_db_data(query):
    """Connect to DB and execute query

    Parameters
    ----------
    query : string
        query to be executed

    Returns
    -------
    DataFrame
        DF of rows that represent result of query
    """
    connection = pymysql.connect(host='127.0.0.1',
                                 user='root',
                                 password='root',
                                 db='viralanalysisdb',
                                 cursorclass=pymysql.cursors.DictCursor)
    df = pd.read_sql(query, connection)
    return df 


def getTaxonomyDistribution():
    """Get the virus taxonomy distribution - the count for each group in the taxonomy data.

    Returns
    -------
    dict
        a dictionary with label = group, data = count(group)
    """
    df = get_db_data(
        'select `group`, COUNT(`group`) as taxocount from gene_taxonomy group by `group`')
    taxonomy_distrubution = {}
    for row in df.itertuples():
        taxonomy_key = format_string(row[1].strip())
        taxonomy_distrubution[taxonomy_key] = int(row[2])
    return taxonomy_distrubution

def getFilteredTaxonomyData(args, filteredList = '("")'):
    """Get the filtered virus taxonomy data where group isn't in filteredList

    Parameters
    ----------
    args : dict
        a dictionary containing args from datatables required to sort/ filter data
    filteredList : string
        list in string format representing labels to not include in return

    Returns
    -------
    dict
        a dictionary with the filtered viral data formatted as needed to work with datatables
    """
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

    Parameters
    ----------
    virus_taxonomy_distribution : dict
        dictionary of virus taxonomy distribution

    Returns
    -------
    list, list 
        labels and values formatted in two different lists
    """
    labels = []
    values = []
    for key in virus_taxonomy_distribution:
        labels.append(key)
        values.append(virus_taxonomy_distribution[key])

    return labels, values

def format_string(group):
    """Return the string formated as described: capitalize first letter of label unless it's a DNA or RNA label

    Parameters
    ----------
    group : string
        string that requires formatting

    Returns
    -------
    string 
        group in the proper formatting
    """
    new_group = group[0].upper() + group[1:]
    if "DsDNA" in new_group or "DsRNA" in new_group or "SsDNA" in new_group or "SsRNA" in new_group:
        new_group = group
    return new_group


if __name__ == '__main__':
    print(getTaxonomyDistribution())
