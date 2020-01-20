#!/usr/bin/python
import os
import csv
import glob
from itertools import islice

dirName1 = "tmhmm"
dirName2 = "localization"
compare = "viral"
resultsName = dirName1 + "_" + dirName2 + "_" + compare + "Results.csv"
resultsJustNames = dirName1 + "_" + dirName2 + "_" + compare + "ShortResults.csv"
cwd = os.getcwd()

def main():
    # traverse through localization directory and tmhmm directory looing for csv result files for comparison
    dir1 = os.getcwd()
    dir2 = os.getcwd()
    print(dir1 + "\n" + dir2)
    for root, dirs, files in os.walk(cwd):
        for dir in dirs:
            if dir.startswith(dirName1):
                dir1 = os.path.join(root, dir)
            if dir.startswith(dirName2):
                dir2 = os.path.join(root, dir)
    print(dir1 + "\n" + dir2 + "\n")
    # loop through both directories finding files containing value of compare var and "csv" in name
    for file1 in glob.glob(dir1 + "/src/*" + compare + "*.csv"):
        for file2 in glob.glob(dir2 + "/*" + compare + "*.csv"):
            # compare the two files for same YP code names
            compareFiles(file1, file2)

def compareFiles(file1, file2):
    print(file1 + " " + file2)
    with open(file1, 'rb') as tmhmm: # tmhmm
        tmhmmReader = csv.reader(tmhmm)
        tmhmm_names = dict((r[0], i) for i, r in enumerate(tmhmmReader)) # map tmhmm codes to indices
    with open(file1, 'rb') as tmhmm: # reopen to be used to find rows
        tmhmmReader = csv.reader(tmhmm)
        with open(file2, 'rb') as mitofates: # mitofates
            with open(resultsName, 'wb') as results: # full results
                with open(resultsJustNames, 'wb') as results_just_names: # column of only matching names
                    mitofatesReader = csv.reader(mitofates)
                    writer = csv.writer(results)
                    writer2 = csv.writer(results_just_names)
                    tmhmmRow = list(tmhmmReader)

                    writer.writerow(tmhmmRow[0] + next(mitofatesReader, []))
                    writer2.writerow(["code_name"])

                    for row in mitofatesReader: # loop through mitofates rows
                        split_name = row[0].strip().split(" ")[0] # get code name
                        index = tmhmm_names.get(split_name) # index of name in tmhmm map
                        if index is not None: # write results if match
                            writer.writerow(tmhmmRow[index] + row)
                            writer2.writerow([split_name])

if __name__ == "__main__":main()
