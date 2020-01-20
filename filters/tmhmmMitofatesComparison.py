#!/usr/bin/python
import os
import csv
import glob
from itertools import islice

dirName1 = "tmhmm"
dirName2 = "mitofates"
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
    first = 1
    for file1 in glob.glob(dir1 + "/src/*" + compare + "*.csv"):
        for file2 in glob.glob(dir2 + "/*" + compare + "*.csv"):
            # compare the two files for same YP code names
            compareFiles(file1, file2, first)
            first = 0

def compareFiles(file1, file2, first):
    print(file1 + " " + file2)
    if first == 1:
        openAs = "wb"
    else:
        openAs = "ab"
    with open(file1, 'rb') as tmhmm: # reopen to be used to find rows
        with open(file2, 'rb') as mitofates: # mitofates
            with open(resultsName, openAs) as results: # full results
                with open(resultsJustNames, openAs) as results_just_names: # column of only matching names
                    tmhmmReader = csv.reader(tmhmm)
                    mitofatesReader = csv.reader(mitofates)
                    writer = csv.writer(results)
                    writer2 = csv.writer(results_just_names)
                    if first == 1: # write header if first time comparing
                        writer.writerow(next(tmhmmReader, []) + next(mitofatesReader, []))
                        writer2.writerow(["code_name"])

                    match = 0
                    for row in mitofatesReader: # loop through mitofates rows
                        for row2 in tmhmmReader: # loop through tmhmm rows
                            if row2[0] == "name":
                                break
                            split_name = row[0].strip().split(" ")[0] # get code name from mitofates file since formatted strangely
                            if split_name.strip() == row2[0].strip(): # write results if match
                                mfProb = float(row[1].strip())
                                tmNum = int(row2[4].strip())
                                if mfProb > 0.1 and tmNum > 0: # write results if significant mitochondria probability and significant number of TMHs
                                    #print("Match: " + split_name + " " + row[1] + " " + row2[4])
                                    match = match + 1
                                    writer.writerow(row2 + row)
                                    writer2.writerow([split_name])
                                break
                    print(match) # prints number of matches

if __name__ == "__main__":main()
