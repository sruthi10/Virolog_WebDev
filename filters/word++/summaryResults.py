import csv
import datetime
import os
import math
import sys
import pandas as pd
import numpy as np


QUERY_FILE = sys.argv[1] #QUERY_FILE = results_TFIDF.csv"
OUTPUT_FILE = os.path.splitext(QUERY_FILE)[0] + "resultsSummary.csv"
print("outputfile", OUTPUT_FILE)
def main():
    df = pd.read_csv(QUERY_FILE)
    #print(df)
    print("Number of Rows:",df['Symbol'].count())
    print("Unique Entries-Symbols:",df['Symbol'].unique().count())
    df = df.groupby('Symbol')['Count'].sum()
          
    df.to_csv(OUTPUT_FILE,header=True)
    print("done")
if __name__ == '__main__':
    main()
    