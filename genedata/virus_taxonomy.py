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
                                 password='password', # on cloud server: pw = root
                                 db='viralanalysisdb',
                                 cursorclass=pymysql.cursors.DictCursor)
    df = pd.read_sql(query, connection)
    return df 

def getFamilies(realm):
    """Get the families within a given realm

    Returns
    -------
    list
        a list with families in realm
    """
    df = get_db_data(
        'select `family`, COUNT(`family`) from tax_metadata where `realm` = "{}" group by `family`'.format(realm))
    result = {}
    for row in df.itertuples():
        key = format_string(row[1].strip())
        result[key] = int(row[2])
    return format_taxonomy(result)

def getFamilyCount(family):
    """Get the number of occurrences of family in the db

    Returns
    -------
    int
        a count of proteins in the given family
    """
    df = get_db_data(
        'select COUNT(`family`) as taxocount from tax_metadata where `family` = "{}" group by `family`'.format(family))
    print(df.values[0][0])
    return df.values[0][0]

def getTaxonomyDistribution():
    """Get the virus taxonomy distribution - the count for each Realm in the taxonomy data.

    Returns
    -------
    dict
        a dictionary with label = Realm, data = count(Realm)
    """
    df = get_db_data(
        'select `realm`, COUNT(`realm`) as taxocount from tax_metadata group by `realm`')
    taxonomy_distrubution = {}
    for row in df.itertuples():
        taxonomy_key = format_string(row[1].strip())
        taxonomy_distrubution[taxonomy_key] = int(row[2])
    return taxonomy_distrubution

def getFamilyTaxonomyDistribution(realm, familyList = '("")'):
    """Get the family virus taxonomy distribution - the count for each Family in the taxonomy data.

    Returns
    -------
    dict
        a dictionary with label = family, data = count(family)
    """
    df = get_db_data(
        'select * from ((select `family`, COUNT(`family`) as taxocount from tax_metadata where `realm` = "{}" group by `family` order by taxocount desc limit 5) UNION (SELECT `family`, COUNT(`family`) as taxocount FROM tax_metadata where `family` in {} group by `family`)) as d where `family` is not null'.format(realm, familyList))
    taxonomy_distrubution = {}
    for row in df.itertuples():
        taxonomy_key = format_string(row[1].strip())
        taxonomy_distrubution[taxonomy_key] = int(row[2])
    return taxonomy_distrubution

def getFilteredTaxonomyData(args, filteredList = '("")', familyList = '("NA")'):
    """Get the filtered virus metadata and taxonomy data where Realm isn't in filteredList

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
    orderby = "`Accession`"
    if args["order[0][column]"] is '1':
        orderby = "`Description`"
    elif args["order[0][column]"] is '2':
        orderby = "`Length`"
    elif args["order[0][column]"] is '3':
        orderby = "`Organism`"
    elif args["order[0][column]"] is '4':
        orderby = "`Realm`"
    elif args["order[0][column]"] is '5':
        orderby = "`Family`"
    
    initialQuery = 'SELECT * FROM tax_metadata WHERE (`Accession` LIKE "%{}%" OR `Description` LIKE "%{}%" OR `Organism` LIKE "%{}%" OR `Realm` LIKE "%{}%" OR `Family` LIKE "%{}%") AND `Realm` not in {} AND `Family` not in {}'
    if familyList != '("NA")':
        initialQuery = initialQuery + ' AND `Family` in {} order by {} {} limit {} offset {}'
        initialQuery = initialQuery.format(args["search[value]"], args["search[value]"], args["search[value]"], args["search[value]"], args["search[value]"], filteredList, filteredList, familyList, orderby, args["order[0][dir]"], args["length"], args["start"])
    else:
        initialQuery = initialQuery + ' order by {} {} limit {} offset {}'
        initialQuery = initialQuery.format(args["search[value]"], args["search[value]"], args["search[value]"], args["search[value]"], args["search[value]"], filteredList, filteredList, orderby, args["order[0][dir]"], args["length"], args["start"])
    df = get_db_data(initialQuery)
    total_size = get_db_data(
        'select COUNT(`Accession`) as count from tax_metadata')
    
    countQuery = 'select COUNT(`Accession`) as count from tax_metadata WHERE (`Accession` LIKE "%{}%" OR `Description` LIKE "%{}%" OR `Organism` LIKE "%{}%" OR `Realm` LIKE "%{}%" OR `Family` LIKE "%{}%") AND `Realm` not in {} AND `Family` not in {}'
    if familyList != '("NA")':
        countQuery = countQuery + ' AND `Family` in {}'
        countQuery = countQuery.format(args["search[value]"], args["search[value]"], args["search[value]"], args["search[value]"], args["search[value]"], filteredList, filteredList, familyList)
    else:
        countQuery = countQuery.format(args["search[value]"], args["search[value]"], args["search[value]"], args["search[value]"], args["search[value]"], filteredList, filteredList)
    filtered_size = get_db_data(countQuery)
    print("*****QUERIES******")
    print(initialQuery)
    print(countQuery)

    tax_data = []
    for row in df.itertuples():
        tax_key = getattr(row, 'Accession')
        tax_name = format_string(getattr(row, 'Description'))
        tax_len = getattr(row, 'Length')
        tax_org = format_string(getattr(row, 'Organism'))
        tax_realm = format_string(getattr(row, 'Realm'))
        tax_fam = format_string(getattr(row, 'Family'))
        tax_data.append( [tax_key, tax_name, tax_len, tax_org, tax_realm, tax_fam] )
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
