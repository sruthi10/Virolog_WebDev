from Bio import Entrez
import csv
import time


Entrez.email = "dgs160230@utdallas.edu"
fname = 'data/gene_identifiers.txt'


class Protein:
    def __init__(self):
        self.id = ''
        self.key = ''
        self.ref = ''
        self.taxonomy = []


def fetch_gene_info(geneids):
    ids = ','.join(geneid.strip() for geneid in geneids)
    handle = Entrez.efetch(db="protein", id=ids, retmode="xml")
    proteinInfoObjects = Entrez.read(handle)
    proteinList = []
    for info in proteinInfoObjects:
        proteinobject = Protein()
        proteinobject.id = info['GBSeq_accession-version']
        proteinobject.taxonomy = info['GBSeq_taxonomy'].split(';')
        proteinList.append(proteinobject)
    return proteinList


def create_taxonomy_mapping():
    start = time.time()
    with open(fname) as f:
        genes = f.readlines()

    genespercall = 1000
    numberOfGenes = len(genes)
    numberOfcalls = (numberOfGenes / genespercall) + 1

    print('number of calls to be made = {0}'.format(numberOfcalls))
    proteinList = []
    for i in range(0, numberOfcalls):
        geneidstart = genespercall * i
        geneidend = genespercall * (i + 1)
        geneids = genes[geneidstart:geneidend]
        proteinList.extend(fetch_gene_info(geneids))
        if i % 20 == 0:
            end = time.time()
            timeelapsed = end - start
            print('Call number: {0}. Time Elapsed: {1}'.format(i, timeelapsed))

    with open('outputdata/gene_taxonomy.csv', 'wb') as csv_file:
        writer = csv.writer(csv_file)
        for pro in proteinList:
            taxonomy = ','.join(pro.taxonomy)
            writer.writerow([pro.id, taxonomy])


if __name__ == '__main__':
    create_taxonomy_mapping()
