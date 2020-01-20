#!/usr/bin/python

# Mitochondira localization of Viral Protein sequences with help of MitoFates
# Python 3  and Biopython 1.7
# Read Setup-Steps.txt
import csv
from multiprocessing.pool import Pool
import os
import os.path
from subprocess import Popen, PIPE
from tempfile import NamedTemporaryFile


from Bio import SeqIO

INPUT_DIR = "input"
OUTPUT_DIR = "output"
ORGANISM = "metazoa"


def main():
    """
    Runs mitofates on all files in INPUT_DIR and sends output to OUTPUT_DIR.
    N mitofates jobs are run in parallel where N is the number of CPU cores on
    your system.
    """
    files = os.listdir(INPUT_DIR)
    pool = Pool()
    pool.map(process_input, files)
    
        
def process_input(in_file):
    """
    Calls mitofates on a single file and sends output to OUTPUT_DIR.
    """
    in_file = os.path.join(INPUT_DIR, in_file)
    base_name = os.path.basename(in_file)
    out_file = os.path.join(OUTPUT_DIR, base_name + '.out')

    record_iter = SeqIO.parse(in_file, "fasta")
    for batch in batch_iterator(record_iter, 2000):
        with NamedTemporaryFile('w') as handle:
            count = SeqIO.write(batch, handle, "fasta")
            handle.flush()
            part = handle.name
            print(f"Wrote {count} records to {part}")

            print(f"{part} being processed")
            mito_fates_call(part, out_file)
            print(f"{part} processed")
                
    process_output(out_file)
    to_csv(out_file, os.path.join(OUTPUT_DIR, base_name + '.csv'))


def process_output(output):
    # process the output to remove header produced from each mitofates call
    with open(output) as fil:
        lines = fil.readlines()

    header = lines[0]
    header_written = False

    with open(output, "w") as fil:
        for line in lines:
            if line == header:
                if not header_written:
                    fil.write(line)
                    header_written = True
            else:
                fil.write(line)


def to_csv(in_file, out_file):
    # convert mitofates output into CSV
    with open(in_file, 'r') as in_text:
        in_reader = csv.reader(in_text, delimiter='\t')
        with open(out_file, 'a') as out_csv:
            out_writer = csv.writer(out_csv, quoting=csv.QUOTE_ALL)
            for row in in_reader:
                i = 0
                out_writer.writerow(row)


def mito_fates_call(in_file, out_file):
    # MitoFates call with 2000 sequences fasta  at a time
    # Args: Input FileName
    # Results append to out.txt
    # Call to Mitofates perl script
    args = ['perl', 'MitoFates/MitoFates.pl', in_file, ORGANISM]
    output, _ = Popen(args, stdout=PIPE, stderr=PIPE).communicate()

    with open(out_file, 'ab') as fil:
        fil.write(output)


def batch_iterator(iterator, batch_size):
    # Returns lists of length batch_size.
    entry = True  # Make sure we loop once
    while entry:
        batch = []
        while len(batch) < batch_size:
            try:
                entry = next(iterator)
            except StopIteration:
                entry = None
            if entry is None:
                # End of file
                break
            batch.append(entry)
        if batch:
            yield batch


if __name__ == "__main__":
    main()
