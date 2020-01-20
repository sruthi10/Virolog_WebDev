import csv
import datetime
import os
import math
import sys

#analyze.py genelist.csv
from collections import defaultdict

import ahocorasick
from bs4 import BeautifulSoup as bs

#DIRECTORY = 'webpages/plosgenetics/article/'
DIRECTORY = sys.argv[1]
QUERY_FILE = sys.argv[2] #QUERY_FILE = '../../parsedViralOrtholog.csv'
OUTPUT_FILE_TFIDF = os.path.splitext(QUERY_FILE)[0] + "results_TFIDF.csv"
OUTPUT_FILE = os.path.splitext(QUERY_FILE)[0] + "resultsSummary.csv"
print("outputfile", OUTPUT_FILE)
def main():
    genes = {}
    
    A = ahocorasick.Automaton()
    with open(QUERY_FILE) as fil:
        reader = csv.reader(fil)
        next(reader) # skip header
        for row in reader:
            query_id, symbol = row[0], row[1]
            genes[query_id] = row[1:]
            
            A.add_word(symbol, query_id)

    A.make_automaton()
    n_occurences = defaultdict(int) # holds term, document counts
    doc_occur = defaultdict(int) # holds number of docs a term appears in
    
    n_docs = 0
    for item in os.listdir(DIRECTORY):
        full_path = os.path.join(DIRECTORY, item)
        if not os.path.isfile(full_path):
            continue

        n_docs += 1
        counted = set()
        
        with open(full_path) as fil:
            for _, match in A.iter(fil.read()):
                n_occurences[match, full_path] += 1
                if match not in counted:
                    counted.add(match)
                    doc_occur[match] += 1
    tf_idf = {}

    
    for item in os.listdir(DIRECTORY):
        full_path = os.path.join(DIRECTORY, item)
        if not os.path.isfile(full_path):
            continue

        for query_id in genes:
            if n_occurences[query_id, full_path] != 0:

                score = n_occurences[query_id, full_path] * math.log(n_docs/doc_occur[query_id])
                tf_idf[query_id, full_path] = score
    writer = csv.writer(open(OUTPUT_FILE_TFIDF,"w+"))
    print('ID\t Symbol\tDocument\tTf-idf score\tCount')
    for key, score in sorted(tf_idf.items(), key = lambda x: x[0][0]):
        query_id, full_path = key 
        print(f'{query_id}\t{genes[query_id][0]}\t{full_path}\t{score}\t{n_occurences[query_id,full_path]}')
        writer.writerow([query_id,genes[query_id][0],full_path,score,n_occurences[query_id,full_path]])
    #summaryresults(OUTPUT_FILE_TFIDF)   

def summaryresults(filename):
    df = pd.read_csv(filename)
    df.groupby(['ID','Symbol'])['Count'].first()\
          .reset_index().groupby(['ID'])['Count'].sum()
    df.to_csv(OUTPUT_FILE)
def get_publication_date(filename):
    """
    Gets publication date of a PLOS article
    Args:
    filename: name of the file containing the article
    Returns:
    A datetime object (year, month, day) of the publication date
    """
    with open(filename) as fil:
        soup = bs(fil.read(), "html.parser")
        meta_tags = soup.find_all("meta")
        meta_tags = filter(lambda x: x.get("name")  == "citation_date", meta_tags)
        tag = next(meta_tags) #Tag which contains the publication date
        date = datetime.datetime.strptime(tag.get("content"), "%b %d, %Y")

        if date is None:
            raise ValueError(f"Article {filename} does not contain date tag")

        return date
        
if __name__ == '__main__':
    main()
    
