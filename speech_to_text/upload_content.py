"""
This file is used to upload content to Google cloud storage bucket
We use Google cloud. Its imperative to set GOOGLE_APPLICATION_CREDENTIALS environment variable to execute
We should execute this file from gcloud virtual env
source gcloud/bin/activate
Invoke 
python3 ./upload_content.py -i ~/Downloads/DS350697.wav -b grangelegal
"""
import sys
import getopt
import io
import os
import csv

# Imports the Google Cloud client library
from google.cloud import storage

def upload_blob(bucket_name, source_file_name, destination_blob_name):
    """Uploads a file to the bucket."""
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    blob.upload_from_filename(source_file_name)

    print('File {} uploaded to {}.'.format(
        source_file_name,
        destination_blob_name))

if __name__ == "__main__":
    inputfile = ''
    bucket = ''
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hi:b:", [
                                   "ifile=", "bucket="])
    except getopt.GetoptError:
        print('upload_content.py -i <inputfile> -b <bucket_name>')
        sys.exit(2)
    except:
        print('upload_content.py -i <inputfile> -b <bucket_name>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print(
                'upload_content.py -i <inputfile> -b <bucket_name>')
            sys.exit()
        elif opt in ("-i", "--ifile"):
            inputfile = arg
        elif opt in ("-b", "--bucket"):
            bucket = arg

    head, tail = os.path.split(inputfile)
    print("Upload file {0} to bucket {1}".format(tail, bucket))
    upload_blob(bucket, inputfile, tail)