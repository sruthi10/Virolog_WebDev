#!/usr/bin/python
# This file cleans up the tmhmm_mitofates combined filtered results by getting rid of unnecessary spaces and removing sequence/ accession id from the name column. The results now look much nicer!
import csv

inputName = "tmhmm_mitofates_viralResults.csv"
outputName = "tmhmm_mitofates_cleanResults.csv"

def main():
    with open(inputName, "r") as in_file:
        lines = csv.reader(in_file)
        with open(outputName, "wb") as out_pre:
            out_csv = csv.writer(out_pre)
            for row in lines:
                seqID = row[0].strip()
                length = row[1].strip()
                expAA = row[2].strip()
                expAA60 = row[3].strip()
                predNumTMH = row[4].strip()
                topology = row[5].strip()
                name = ""
                if seqID == "Sequence ID":
                    name = row[6].strip()
                else:
                    start = row[6].find(" ", 1)+1 # name starts after second space of row[6]
                    name = row[6][start:].strip()
                prob = row[7].strip()
                prediction = row[8].strip()
                cleavage = row[9].strip()
                netCharge = row[10].strip()
                posTOM20 = row[11].strip()
                posAAH = row[12].strip()
                BHHPPP = row[13].strip()
                BPHBHH = row[14].strip()
                HBHHBb = row[15].strip()
                HBHHbB = row[16].strip()
                HHBHHB = row[17].strip()
                HHBPHB = row[18].strip()
                HHBPHH = row[19].strip()
                HHBPHP = row[20].strip()
                HHHBBH = row[21].strip()
                HHHBPH = row[22].strip()
                HHHHBB = row[23].strip()
                HHPBHH = row[24].strip()
                HPBHHP = row[25].strip()
                PHHBPH = row[26].strip()
                out_csv.writerow([seqID, name, length, expAA, expAA60, predNumTMH, topology, prob, prediction, cleavage, netCharge, posTOM20, posAAH, BHHPPP, BPHBHH, HBHHBb, HBHHbB, HHBHHB, HHBPHB, HHBPHH, HHBPHP, HHHBBH, HHHBPH, HHHHBB, HHPBHH, HPBHHP, PHHBPH]) # write header

if __name__ == "__main__":main()
