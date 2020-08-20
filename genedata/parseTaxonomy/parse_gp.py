"""
Parser for GenePept Files

This file parses a GenPept file and extracts the desired features to create a usable CSV file.

The extracted features are described below:
    * Accession - protein accession ID for the protein
    * Description - also known as definition, the name of the protein
    * Length - length of protein
    * Topology - the descriptor for the protein orientation
    ** Data_File_Division - this is not included anymore
    * Last_Update_Date - date for when the protein's info was last updated
    * dbSource - database source where protein info comes from
    * Source - origin of the protein, typically same as organism
    * Organism - organism the protein is from
    * Taxonomy_ID - taxonomy id that can be used to find taxonomy info from the taxonomy CSV table
    * Feature.Source - source feature of the protein containing info on sources for the protein such as db refs, organism, and further notes

For more information, go to:
https://www.ncbi.nlm.nih.gov/protein/YP_008320337.1
^^ This links to a specific gene but gives idea of where the GenPept file comes from.
"""

from Bio import SeqIO
from urllib.parse import urlencode
from urllib.parse import unquote_plus

fr = open('24_genes_genpeptfiles.gp')
fw = open('proteinMetadata.csv', 'w+')
fw.write("Accession, Description, Length, Topology, Last_Update_Date, dbSource, Source, Organism, Taxonomy_ID, Feature.Source")
recs = list(SeqIO.parse(fr,'genbank'))

# loop through records and print info for each rec on each line
for record in recs:
    # remove Viruses from beginning of taxonomy
    record.annotations['taxonomy'].pop(0)
    
    # find location of '[' in description to parse out protein/ gene name
    char_loc = record.description.find(' [')
    fw.write("\n%s, %s, %s, %s, %s, %s, %s, %s, " 
        % (record.id, record.description[:char_loc], len(record.seq), # TODO: described above
            record.annotations['topology'],
            record.annotations['date'],
            record.annotations['db_source'], record.annotations['source'],
            record.annotations['organism']))
    
    # find the source feat
    for feat in record.features:
        if feat.type == "source":
            refs = ' '.join(record.features[0].qualifiers.get("db_xref"))
            refs = refs[refs.find('taxon')+6:]
            space_loc = refs.find(' ')
            
            # first print taxonomy id
            if space_loc == -1: # no space in string
                fw.write("%s, " % (refs))
            else: # space in string, so remove everything afterwards
                fw.write("%s, " % (refs[:space_loc]))
            
            # second print source feature
            fw.write("%s" % (unquote_plus(urlencode(record.features[0].qualifiers)).replace(',','')))
            break
fw.close()



# TEST code below that is not important to function of extracting data
first = recs[7]

# TEST: extract taxonomy ID from source feature
for feat in first.features:
    if feat.type == "source":
        refs = ' '.join(first.features[0].qualifiers.get("db_xref"))
        refs = refs[refs.find('taxon')+6:]
        space_loc = refs.find(' ')
        if space_loc == -1: # no space in string
            print(refs)
        else: # space in string, so remove everything afterwards
            print(refs[:space_loc])
        break

# TEST: encode and decode source feature
encodedStr = urlencode(first.features[0].qualifiers)
print(first.features[0].qualifiers)
print(urlencode(first.features[0].qualifiers))
print(unquote_plus(encodedStr).replace(',',''))

