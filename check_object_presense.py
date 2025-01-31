"""
Check if an object exists in an S3 bucket using HTTP HEAD.

[command line parameter]
# Get command-line arguments (option)
target_CSV: manifest file name (full path or relative path) [option: default "centr.csv"]
target_bucket: target bucket to check the existance of the object listed on the manifest file 
                [option: default "centr-backup-november2024"]
target_region:  target region of the target_bucket
                [option: default "ap-southeast-2.wasabisys.com" (Sydney)]
# Python command example:
>python3 check_object_presense.py manifest.csv centr-backup-november2024

If the bucket region is not Sydney, and is Tokyo for example:
>python3 check_object_presense.py manifest.csv centr-backup-november2024 ap-northeast-1.wasabisys.com
"""

import sys
import csv
import boto3
from botocore.exceptions import ClientError

# define global variables
DEFAULT_REGION = 'us-east-1' #ALWAYS
default_target_region = 'ap-southeast-2'
default_target_bucket = "centr-backup-november2024"
default_target_CSV = "centr.csv"

# Get command-line arguments
target_CSV = sys.argv[1] if len(sys.argv) > 1 else default_target_CSV
target_bucket = sys.argv[2] if len(sys.argv) > 2 else default_target_bucket
target_region = sys.argv[3] if len(sys.argv) > 3 else default_target_region

def check_object_exists(bucket_name, object_key):
    """
    Check if an object exists in an S3 bucket using HTTP HEAD.
    
    :param bucket_name: Name of the S3 bucket
    :param object_key: Key of the object to check
    :return: HTTP status code from the HEAD request
    """

    # Use the following code to connect using Wasabi profile from .aws/credentials file
    # session = boto3.Session(profile_name="wasabi")
    session = boto3.Session(profile_name="centr")
    credentials = session.get_credentials()
    aws_access_key_id = credentials.access_key
    aws_secret_access_key = credentials.secret_key

    endpoint_url = 'https://s3.' + target_region + '.wasabisys.com'

    # print(target_region)
    # print(endpoint_url)
    #print(aws_access_key_id)
    #print(aws_secret_access_key)

    s3_client = boto3.client('s3',
                    endpoint_url=endpoint_url,
                    aws_access_key_id=aws_access_key_id,
                    aws_secret_access_key=aws_secret_access_key)

    # print(f'Target Bucket name: {bucket_name}') 
    # print(f'Target object Key: {object_key}') 
    
    try:
        response = s3_client.head_object(Bucket=bucket_name, Key=object_key)
        return response['ResponseMetadata']['HTTPStatusCode']
    except ClientError as e:
        # Return the error code if the object does not exist or another error occurs
        return e.response['ResponseMetadata']['HTTPStatusCode']

def read_csv_and_check_objects(file_path, check_target_bucket):
    """
    Read a CSV file and check for the existence of objects in S3.

    
    :param file_path: Path to the CSV file
    :param check_target_bucket: the bucket to check the object presence with HTTP HEAD

    :output
    CSV format
    Result message, checked bucket, checked object key, HEAD HTTP Response code
    Last lie:
    total objects count, presented objects count, missing objects count

    """
    with open(file_path, mode='r') as csvfile:
        csv_reader = csv.reader(csvfile)

        # initialize counters
        total_obj_count = 0
        found_obj_count = 0
        missing_object_count = 0

        for row in csv_reader:
            if len(row) != 2:
                print("Skipping invalid row:", row)
                continue

            # count up total objects
            total_obj_count += 1

            bucket_name, object_key = row
            status_code = check_object_exists(check_target_bucket, object_key)
            
            if status_code == 200:
                # count up found counter
                found_obj_count += 1
                print(f"Present ({status_code}), {check_target_bucket}, {object_key}, {status_code}")
            else:
                # count up missing counter
                missing_object_count += 1
                print(f"NOT present ({status_code}), {check_target_bucket}, {object_key}, {status_code}")
    print(f"# Total objects:, {total_obj_count}, Total found:, {found_obj_count}, Total missing:, {missing_object_count}")

# Example usage
if __name__ == "__main__":

    # check the object existance reading the target_CSV (manifest file)
    # The target bucket is target_bucket
    read_csv_and_check_objects(target_CSV, target_bucket)