import sys
import csv
import boto3
from botocore.exceptions import ClientError
from concurrent.futures import ThreadPoolExecutor, as_completed

# Define global variables
DEFAULT_REGION = 'us-east-1'  # ALWAYS
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
    session = boto3.Session(profile_name="centr")
    credentials = session.get_credentials()
    aws_access_key_id = credentials.access_key
    aws_secret_access_key = credentials.secret_key

    endpoint_url = f'https://s3.{target_region}.wasabisys.com'

    s3_client = boto3.client('s3',
                              endpoint_url=endpoint_url,
                              aws_access_key_id=aws_access_key_id,
                              aws_secret_access_key=aws_secret_access_key)

    try:
        response = s3_client.head_object(Bucket=bucket_name, Key=object_key)
        return (object_key, response['ResponseMetadata']['HTTPStatusCode'])
    except ClientError as e:
        return (object_key, e.response['ResponseMetadata']['HTTPStatusCode'])

def read_csv_and_check_objects(file_path, check_target_bucket):
    """
    Read a CSV file and check for the existence of objects in S3.
    
    :param file_path: Path to the CSV file
    :param check_target_bucket: The bucket to check the object presence with HTTP HEAD

    :output:
    CSV format result message, checked bucket, checked object key, HEAD HTTP Response code.
    Last line: total objects count, presented objects count, missing objects count.
    """
    with open(file_path, mode='r') as csvfile:
        csv_reader = csv.reader(csvfile)

        # Initialize counters
        total_obj_count = 0
        found_obj_count = 0
        missing_object_count = 0

        # Use ThreadPoolExecutor for multithreading
        with ThreadPoolExecutor(max_workers=10) as executor:
            future_to_object = {executor.submit(check_object_exists, check_target_bucket, row[1]): row[1] for row in csv_reader if len(row) == 2}
            
            for future in as_completed(future_to_object):
                total_obj_count += 1
                object_key = future_to_object[future]
                status_code = future.result()[1]

                if status_code == 200:
                    found_obj_count += 1
                    print(f"Present ({status_code}), {check_target_bucket}, {object_key}, {status_code}")
                else:
                    missing_object_count += 1
                    print(f"NOT present ({status_code}), {check_target_bucket}, {object_key}, {status_code}")

        print(f"# Total objects:, {total_obj_count}, Total found:, {found_obj_count}, Total missing:, {missing_object_count}")

# Example usage
if __name__ == "__main__":
    read_csv_and_check_objects(target_CSV, target_bucket)
