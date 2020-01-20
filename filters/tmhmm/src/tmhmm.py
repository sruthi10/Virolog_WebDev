#!/usr/bin/python
import os
import subprocess
import itertools
from Bio import SeqIO
import csv

inputName = "test.fasta"
outputName = "testOut"
textName = outputName + ".txt"
csvName = outputName + ".csv"
inputFile = open(inputName)
i = 0 # file count

def main():
    # clear out old contents of csv file and write heading
    out_pre = open(csvName, "w")
    out_csv = csv.writer(out_pre, quoting=csv.QUOTE_ALL)
    out_csv.writerow(['Sequence ID', 'length', 'exp number of AAs in TMHs', 'exp number of AAs in TMHs in the first 60 AAs', 'predicted number of TMH', 'topology'])
    out_pre.close()
    # split file into manageable pieces for TMHMM
    record_iter = SeqIO.parse(inputFile,"fasta")
    for i, batch in enumerate(batch_iterator(record_iter, 5000)):
        filename = "group_%i.fasta" % (i + 1)
        with open(filename, "w") as handle:
            count = SeqIO.write(batch, handle, "fasta")
        print("Wrote %i records to %s" % (count, filename))
    # call TMHMM on each file created
    for x in range(0,i+1):
        filename = "group_%i.fasta" % (x + 1)
        print(filename + " being processed")
        tmhmm_call(filename) # calls TMHMM filter
        parseToCSV() # adds results to CSV file
        print(filename + " processed")
        os.remove(filename) # remove group file once not needed
        print("Generating plots for " + filename)
        generatePlots()
        print("Finished making plots for " + filename)
    open(textName, "w").close() # delete contents of text output
    os.remove(textName) # no longer need output text file since have CSV file
    inputFile.close()

def generatePlots():
    cwd = os.getcwd()
    # look through current working directory for directories beginning with TMHMM
    for root, dirs, files in os.walk(cwd):
        for dir in dirs:
            if dir.startswith("TMHMM"):
                path = os.path.join(root, dir)
                for file in os.listdir(path): # search through all files in TMHMM directory
                    if file.endswith(".gnuplot"): # execute files ending with .gnuplot
                        print(os.path.join(path, file))
                        file_path = os.path.join(path, file)
                        subprocess.check_output(["gnuplot", file_path]) # gets eps file, which will be converted to jpg
                        file_split = file.split("gnuplot") # get YP code corresponding to eps file just made
                        source = file_split[0] + "eps" # source is <YPcode>.eps, without the <>
                        source = os.path.join(path, source)
                        dest = file_split[0] + "jpg" # dest is <YPcode>.jpg, without the <>
                        dest_dir = os.path.join(cwd, "plots") # result saved in plots directory
                        dest = os.path.join(dest_dir, dest)
                        subprocess.check_output(["convert", "-density", "150", source, dest]) # converts eps to jpg and stores in plots directory
                        os.remove(file_path) # remove gnuplot script once done
                        os.remove(source) # remove eps file once done
                        os.remove(file_path.split("gnuplot")[0] + "plp") # remove plp data once done
                os.rmdir(dir)

def parseToCSV():
    with open(textName, "r") as in_text:
        lines = in_text.readlines()
        with open(csvName, "a") as out_pre:
            out_csv = csv.writer(out_pre, quoting=csv.QUOTE_ALL)
            # out_csv.writerow(['name', 'length', 'exp number of AAs in TMHs', 'exp number of AAs in TMHs in the first 60 AAs', 'predicted number of TMH', 'topology'])
            x = 0
            while x < len(lines):
                # print lines[x]
                name = lines[x].split()[1].strip()
                length = lines[x].split()[3].strip()
		x = x+1
                # print lines[x]
                pred = lines[x].split()[6].strip()
                x = x+1
                # print lines[x]
                expAA = lines[x].split()[8].strip()
                x = x+1
                # print lines[x]
                exp60 = lines[x].split()[7].strip()
                x = x+2
                top = ""
                while x < len(lines) and lines[x].split()[0] != "#": # else beginning of next sequence
                    topSplit = lines[x].split()
                    if topSplit[2][0] == 'o': # is outside cell
                        top = top + "o"
                    if topSplit[2][0] == 'T': # is TM helix
                        top = top + topSplit[3] + "-" + topSplit[4]
                    if topSplit[2][0] == 'i': # is inside cell
                        top = top + "i"
                    # print(lines[x].split())
                    x = x+1
                out_csv.writerow([name, length, expAA, exp60, pred, top])

def tmhmm_call(filename):
    out = subprocess.check_output(["tmhmm", filename])
    outputFile = open(textName, "w")
    outputFile.write(out)
    outputFile.close()
        
def batch_iterator(iterator, batch_size):
    # Returns lists of length batch_size.
    entry = True  # Make sure we loop once
    while entry:
        batch = []
        while len(batch) < batch_size:
            try:
                entry = iterator.next()
            except StopIteration:
                entry = None
            if entry is None:
                # End of file
                break
            batch.append(entry)
        if batch:
            yield batch
            
if __name__ == "__main__":main()
