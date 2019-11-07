"""
This file will initiate transcribe process for a WAV file
We use Google cloud. Its imperative to set GOOGLE_APPLICATION_CREDENTIALS environment variable to execute
We should execute this file from gcloud virtual env
source gcloud/bin/activate
Invoke 
python3 ./start_convert.py -i DS350697.wav -o ~/Downloads/DS350697.csv -b grangelegal
"""
import sys
import getopt
import io
import os
import csv

# Imports the Google Cloud client library
from google.cloud import speech
from google.cloud.speech import enums
from google.cloud.speech import types

# this can be used for files that are smaller and local
def audio_content_from_file(file_name):
    with io.open(file_name, 'rb') as audio_file:
        content = audio_file.read()
        audio = types.RecognitionAudio(content=content)
    return audio

def config_for_recognition():
    # Sample rate in Hertz of the audio data sent
    sample_rate_hertz = 16000
    # The language of the supplied audio
    language_code = "en-US"
    # Encoding of audio data sent. This sample sets this explicitly.
    # This field is optional for FLAC and WAV audio formats.
    encoding = enums.RecognitionConfig.AudioEncoding.LINEAR16
    config = {
        "sample_rate_hertz": sample_rate_hertz,
        "language_code": language_code,
        "encoding": encoding,
    }
    return config

def print_transcribe_result(response):
    for result in response.results:
        print('Transcript: {}'.format(result.alternatives[0].transcript))

def convert_speech_to_text(file_name, bucket):    
    # Instantiates a client
    client = speech.SpeechClient()
    # Loads the audio into memory
    # audio = {"uri": "gs://grangelegal/DS340758.wav"}
    audio = {"uri": "gs://{0}/{1}".format(bucket, file_name)}
    config = config_for_recognition()
    rows = []
    # Detects speech in the audio file
    try:
        operation = client.long_running_recognize(config, audio)
        print("Waiting for operation to complete...")
        op_result = operation.result()
        for result in op_result.results:
            for alternative in result.alternatives:
                row = [alternative.transcript, alternative.confidence]
                rows.append(row)
                # print("{0}, {1}".format(alternative.transcript, alternative.confidence))
    except Exception as e:
        print("ERROR: Google transcribe failed with error")
        print(e)
        sys.exit(2)

    return rows

def save_contents_to_csv(file_name, rows):
    print('Writing following content to file')
    print(rows)
    with open(file_name, 'w+') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(rows)
    csvfile.close()
    print('COMPLETED writing to FILE')

if __name__ == "__main__":
    inputfile = ''
    outputfile = ''
    bucket = ''
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hi:o:b:", [
                                   "ifile=", "ofile=", "bucket="])
    except getopt.GetoptError:
        print('start_convert.py -i <inputfile> -o <outputfile> -b <bucket>')
        sys.exit(2)
    except:
        print('start_convert.py -i <inputfile> -o <outputfile> -b <bucket>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print(
                'start_convert.py -i <inputfile> -o <outputfile> -b <bucket>')
            sys.exit()
        elif opt in ("-i", "--ifile"):
            inputfile = arg
        elif opt in ("-o", "--ofile"):
            outputfile = arg
        elif opt in ("-b", "--bucket"):
            bucket = arg
    #TODO: Check to see if file exists
    #TODO: Check to see if it is a WAV file
    print("Start transcribe {0} from bucket {1}".format(inputfile, bucket))
    rows = convert_speech_to_text(inputfile, bucket)
    save_contents_to_csv(outputfile, rows)