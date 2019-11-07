import sys
from google.cloud import storage

def get_storage_client():
    return storage.Client()

def list_blobs(bucket_name):
    """Lists all the blobs in the bucket."""
    # Note: Client.list_blobs requires at least package version 1.17.0.
    blobs = get_storage_client().list_blobs(bucket_name)

    for blob in blobs:
        print(blob.name)

def remove_object_from_bucket(bucket_name, blob_name):
    pass

def upload_object_to_bucket(bucket_name, destination_blob_name, source_file_name):
    bucket = get_storage_client().get_bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    blob.upload_from_filename(source_file_name)

    print('File {} uploaded to {}.'.format(
        source_file_name,
        destination_blob_name))

if __name__ == "__main__":
    try:
        bucket_name = str(sys.argv[1])
        if bucket_name:
            list_blobs(bucket_name)
    except: 
        print("list_bucket.py <<bucket_name>>")
    
    