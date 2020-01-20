from Bio import SeqIO

import sys

ISG_FILE = "ISG.txt"

def main():
    """
    Usage: python main <viral_protein_file>
    """

    viral_protein_file = sys.argv[1]
    
    for record in SeqIO.parse(viral_protein_file, "fasta"):
        print(record.annotations, record.description, record.features,
              record.format, record.id)

def get_ISG_proteins():
    proteins = []

    with open(ISG_FILE) as fil:
        for line in fil:
            proteins.append(line.strip())

    return proteins

if __name__ == "__main__":
    main()
