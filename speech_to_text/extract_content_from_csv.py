"""
This file allows you to extract , just the content alone from CSV file.
Today we get both content and confidence. If we need content alone
only way to todo it is open in excel and copy content column. This script
is to automate that process!
Make sure you execute this from within mlenv virtualenv
source mlenv/bin/activate
Invoke 
python3 ./extract_content_from_csv.py -i ~/Downloads/DS350697.csv
"""
import pandas as pd
import os
import sys, getopt

def load_csv(file_name):
    df = pd.read_csv(file_name, 
                  sep=',', 
                  names=["content", "confidence"])
    return df

if __name__ == "__main__":
    inputfile = ''
    
    try:
      opts, args = getopt.getopt(sys.argv[1:],"hi:",["ifile="])
    except getopt.GetoptError:
      print('extract_content_from_csv.py -i <inputfile>')
      sys.exit(2)
    for opt, arg in opts:
      if opt == '-h':
         print('extract_content_from_csv.py -i <inputfile>')
         sys.exit()
      elif opt in ("-i", "--ifile"):
         inputfile = arg

    df = load_csv(inputfile)
    print(df["content"])