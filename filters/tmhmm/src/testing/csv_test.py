#!/usr/bin/python
import subprocess
import os
import sys
import csv

outputfile = open("testOut.txt", 'ab')
filename = "test.fasta"
out = subprocess.check_output(["tmhmm", filename])
outputfile.write(out)
outputfile.close()

# convert to csv
txt_file = r"testOut.txt"
csv_file = r"testOut.csv"
with open(txt_file, "r") as in_text:
    lines = in_text.readlines()
    with open(csv_file, "w") as out_pre:
        out_csv = csv.writer(out_pre, quoting=csv.QUOTE_ALL)
        out_csv.writerow(['name', 'length', 'exp number of AAs in TMHs', 'exp number of AAs in TMHs in the first 60 AAs', 'predicted number of TMH', 'topology'])
        for line in lines:
            name = line.split("\t")[0]
            length = line.split("\t")[1].split("=")[1]
            expAA = line.split("\t")[2].split("=")[1]
            exp60 = line.split("\t")[3].split("=")[1]
            pred = line.split("\t")[4].split("=")[1]
            top = line.split("\t")[5].split("=")[1].split("\n")[0]
            out_csv.writerow([name, length, expAA, exp60, pred, top])

