"""
Parser for XML File containing Taxonomy Information for a Protein

This file parses a Taxonomy XML file and extracts the desired features to create a usable CSV file.

The extracted features are described below:
    * Taxonomy_ID - taxonomy id that can be used to find protein info from the protein CSV table
    * Pub_Date - the date when the taxonomy info was published
    * Features Superkingdom -> Species - taxonomy info
    * NoRank - indicates if the species is an unclassified species (which probably means it isn't well-studied yet)
"""

import xml.etree.ElementTree as ET

root = ET.parse('Entire_taxonomy_result.xml').getroot()
fw = open('taxonomy.csv', 'w+')
fw.write("Taxonomy_ID, Pub_Date, Superkingdom, Realm, Kingdom, Phylum, Class, Order, Family, Genus, Species, Subspecies, NoRank")

# loop through each Taxonomy record and create CSV line containing relevant info
for child in root:
    # extract taxonomy ID and pub date
    taxId = child.find('TaxId').text
    pubDate = child.find("PubDate").text
    pubDate = pubDate[:pubDate.find(' ')]
    
    # skip this taxon if no lineage or if not a no rank or species
    lineage = child.find('LineageEx')
    if lineage is None:
        continue
    if child.find('Rank').text != "species" and child.find('Rank').text != "no rank":
        continue
    
    # setup vars to extract taxonomy info
    i = 0
    prev = ""
    singleDict = {}
    
    # loop through taxonomy info and extract classifications
    for taxon in lineage:
        sciName = taxon.find('ScientificName').text
        rank = taxon.find("Rank").text
        if rank == "no rank" and prev == "superkingdom":
            rank = "realm"
        if rank == "no rank" and prev == "realm":
            rank = "kingdom"
        if "sub" in rank:
            continue
        singleDict[rank] = sciName
        prev = rank
    
    # set species/ subspecies info and indicate if no rank
    if prev != "genus" and prev != "species" and prev != "no rank":
        continue
    if child.find('Rank').text == "species":
        singleDict["species"] = child.find('ScientificName').text
        singleDict["noRank"] = "false"
    if child.find('Rank').text == "no rank":
        if prev == "genus":
            singleDict["species"] = child.find('ScientificName').text
        else:
            singleDict["subspecies"] = child.find('ScientificName').text
        singleDict["noRank"] = "true"
    
    # put None when info not available for a classification
    if "superkingdom" not in singleDict:
        singleDict["superkingdom"] = "None"
    if "realm" not in singleDict:
        singleDict["realm"] = "None"
    if "kingdom" not in singleDict:
        singleDict["kingdom"] = "None"
    if "phylum" not in singleDict:
        singleDict["phylum"] = "None"
    if "class" not in singleDict:
        singleDict["class"] = "None"
    if "order" not in singleDict:
        singleDict["order"] = "None"
    if "family" not in singleDict:
        singleDict["family"] = "None"
    if "genus" not in singleDict:
        singleDict["genus"] = "None"
    if "species" not in singleDict:
        singleDict["species"] = "None"
    if "subspecies" not in singleDict:
        singleDict["subspecies"] = "None"
    if "noRank" not in singleDict:
        print("%s has no noRank info - fix" % (taxId))
        singleDict["noRank"] = "true"
    
    # print info to CSV file
    fw.write("\n%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s"
             % (taxId, pubDate, singleDict["superkingdom"],
               singleDict["realm"], singleDict["kingdom"],
               singleDict["phylum"], singleDict["class"],
               singleDict["order"], singleDict["family"],
               singleDict["genus"], singleDict["species"],
               singleDict["subspecies"], singleDict["noRank"]))

fw.close()
