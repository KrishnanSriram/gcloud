import sys
import getopt
from google.cloud import storage


def get_storage_client():
    return storage.Client()


def upload_object_to_bucket(bucket_name, source_file_name, blob_name):
    bucket = get_storage_client().get_bucket(bucket_name)
    blob = bucket.blob(blob_name)

    blob.upload_from_filename(source_file_name)

    print('DONE: File {} uploaded to {}.'.format(
        source_file_name,
        blob_name))


if __name__ == "__main__":
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hb:f:n:", [
                                   "bucket_name=", "source_file=", "blob_name="])
    except getopt.GetoptError:
        print('upload_blob_bucket.py -b <bucket_name> -f <source_file> -n <blob_name>')
        sys.exit(2)
    except:
        print('upload_blob_bucket.py -b <bucket_name> -f <source_file> -n <blob_name>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print(
                'upload_blob_bucket.py -b <bucket_name> -f <source_file> -n <blob_name>')
            sys.exit()
        elif opt in ("-b", "--bucket_name"):
            bucket_name = arg
        elif opt in ("-f", "--source_file"):
            source_file = arg
        elif opt in ("-n", "--blob_name"):
            blob_name = arg
    print('Bucket: {0}, source file: {1} BLOB name: {2}'.format(
        bucket_name, source_file, blob_name))
    
    # invoke upload function
    print("Uploading file {0} to {1} .....".format(source_file, bucket_name))
    upload_object_to_bucket(bucket_name, source_file, blob_name)
