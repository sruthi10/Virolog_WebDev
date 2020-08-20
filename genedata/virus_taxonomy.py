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


def getTaxonomyDistribution():
    """Get the virus taxonomy distribution - the count for each Realm in the taxonomy data.

    Returns
    -------
    dict
        a dictionary with label = group, data = count(group)
    """
    df = get_db_data(
        'select `realm`, COUNT(`realm`) as taxocount from taxonomy group by `realm`')
    taxonomy_distrubution = {}
    for row in df.itertuples():
        taxonomy_key = format_string(row[1].strip())
        taxonomy_distrubution[taxonomy_key] = int(row[2])
    return taxonomy_distrubution

def getFamilyTaxonomyDistribution(realm):
    """Get the family virus taxonomy distribution - the count for each Family in the taxonomy data.

    Returns
    -------
    dict
        a dictionary with label = group, data = count(group)
    """
    print(realm)
    df = get_db_data(
        'select `realm`, `family`, COUNT(`family`) as taxocount from taxonomy where `realm` = "{}" group by `family` order by taxocount desc limit 5'.format(realm))
    taxonomy_distrubution = {}
    for row in df.itertuples():
        taxonomy_key = format_string(row[2].strip())
        taxonomy_distrubution[taxonomy_key] = int(row[3])
    print("FAMILY TAX: ")
    print(taxonomy_distrubution)
    return taxonomy_distrubution

def getFilteredTaxonomyData(args, filteredList = '("")'):
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
    df = get_db_data(
        'select m.`Accession`, m.`Description`, m.`Length`, m.`Organism`, t.`Realm`, t.`Family` from protein_metadata_small m, taxonomy t where m.`Taxonomy_ID` = t.`Taxonomy_ID` AND `Realm` not in {} AND `Family` not in {} AND (`Accession` LIKE "%{}%" OR `Description` LIKE "%{}%" OR `Organism` LIKE "%{}%") order by {} {} limit {} offset {}'.format(filteredList, filteredList, args["search[value]"], args["search[value]"], args["search[value]"], orderby, args["order[0][dir]"], args["length"], args["start"]))
    total_size = get_db_data(
        'select COUNT(`Accession`) as count from protein_metadata_small')
    filtered_size = get_db_data(
        'select COUNT(`Accession`) as count from protein_metadata_small m, taxonomy t where m.`Taxonomy_ID` = t.`Taxonomy_ID` AND `Realm` not in {} AND `Family` not in {} AND (`Accession` LIKE "%{}%" OR `Description` LIKE "%{}%" OR `Organism` LIKE "%{}%")'.format(filteredList, filteredList, args["search[value]"], args["search[value]"], args["search[value]"]))
    
    print(filtered_size['count'][0], file=sys.stderr)
    print(total_size['count'][0], file=sys.stderr)
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
