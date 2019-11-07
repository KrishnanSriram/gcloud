"""
This file will help extract key information like get 'certainity %'. If we can work more,
we should be able to identify words that have low percentage, do a SD on transcribed text,
so on and so forth
Make sure you execute this from within mlenv virtualenv
source mlenv/bin/activate
Invoke 
python3 ml_analyze_reponse.py -i ~/Downloads/DS350697.csv
"""
import pandas as pd
import os
import sys, getopt

def load_csv(file_name):
    df = pd.read_csv(file_name, 
                  sep=',', 
                  names=["content", "confidence"])
    return df.fillna(0)

def get_confidence_stats(df):
    max = df["confidence"].max()
    min = df["confidence"].min()
    mean = df["confidence"].mean()
    sd = df["confidence"].std()
    print("Confidence\nMax : {0}, Min: {1}, Avg: {2}".format(max, min, mean))
    print("Std. Deviation: {0}".format(sd))
    return [max, min, mean]

def get_min_confidence_content(df, min_confidence):
    return df[df["confidence"]==min_confidence]

if __name__ == "__main__":
    inputfile = ''
    
    try:
      opts, args = getopt.getopt(sys.argv[1:],"hi:",["ifile="])
    except getopt.GetoptError:
      print('ml_analyze_transcribe_csv.py -i <inputfile>')
      sys.exit(2)
    for opt, arg in opts:
      if opt == '-h':
         print('ml_analyze_transcribe_csv.py -i <inputfile>')
         sys.exit()
      elif opt in ("-i", "--ifile"):
         inputfile = arg

    df = load_csv(inputfile)
    confidence = get_confidence_stats(df)
    df_min = get_min_confidence_content(df, confidence[1])
    print("There are {0} items with min confidence".format(df_min.size))