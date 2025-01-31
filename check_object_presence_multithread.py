import sys
import csv
import boto3
from botocore.exceptions import ClientError
from concurrent.futures import ThreadPoolExecutor, as_completed
import argparse
import logging
import time

# Define global variables
DEFAULT_REGION = 'us-east-1'  # ALWAYS
default_target_region = 'ap-southeast-2'
default_target_bucket = "centr-backup-november2024"
default_target_CSV = "centr.csv"
default_log_file = "s3_check.log"

# Global S3 client variable
s3_client = None

def parse_arguments():
    """
    Parse command-line arguments.
    
    :return: Parsed arguments object
    """
    parser = argparse.ArgumentParser(description='Check S3 object existence.')
    parser.add_argument('--csv', type=str, default=default_target_CSV, help='Path to CSV file')
    parser.add_argument('--bucket', type=str, default=default_target_bucket, help='S3 bucket name')
    parser.add_argument('--region', type=str, default=default_target_region, help='AWS region')
    parser.add_argument('--log', type=str, default=default_log_file, help='Log file path')
    return parser.parse_args()

def setup_logging(log_file):
    """
    Set up logging to both console and a log file.
    
    :param log_file: Path to the log file
    """
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    # Create file handler for logging to a file
    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(logging.INFO)

    # Create console handler for logging to the console
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)

    # Create formatter and add it to handlers (without timestamp)
    formatter = logging.Formatter('%(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)

    # Add handlers to the logger
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

def initialize_s3_client(target_region):
    """
    Initialize the S3 client and store it in a global variable.
    
    :param target_region: AWS region for the S3 endpoint
    """
    global s3_client
    
    session = boto3.Session(profile_name="centr")
    credentials = session.get_credentials()
    
    aws_access_key_id = credentials.access_key
    aws_secret_access_key = credentials.secret_key

    endpoint_url = f'https://s3.{target_region}.wasabisys.com'

    s3_client = boto3.client('s3',
                              endpoint_url=endpoint_url,
                              aws_access_key_id=aws_access_key_id,
                              aws_secret_access_key=aws_secret_access_key)

def check_object_exists(bucket_name, object_key):
    """
    Check if an object exists in an S3 bucket using HTTP HEAD.
    
    :param bucket_name: Name of the S3 bucket
    :param object_key: Key of the object to check
    :return: Tuple of object key and HTTP status code from the HEAD request
    """
    
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
      Log messages indicating presence or absence of objects,
      along with counts of total, found, and missing objects.
      
      Last line logged includes total objects count,
      presented objects count, missing objects count.
      
      If an error occurs during reading or processing,
      appropriate error messages are logged.
     """
    
    try:
        with open(file_path, mode='r') as csvfile:
            csv_reader = csv.reader(csvfile)

            # Initialize counters
            total_obj_count = 0
            found_obj_count = 0
            missing_object_count = 0

            # Use ThreadPoolExecutor for multithreading
            with ThreadPoolExecutor(max_workers=10) as executor:
                future_to_object = {executor.submit(check_object_exists, check_target_bucket, row[1]): row[1] 
                                     for row in csv_reader if len(row) == 2}
                
                for future in as_completed(future_to_object):
                    total_obj_count += 1
                    object_key = future_to_object[future]
                    status_code = future.result()[1]

                    if status_code == 200:
                        found_obj_count += 1
                        logging.info(f"Present ({status_code}), {check_target_bucket}, {object_key}, {status_code}")
                    else:
                        missing_object_count += 1
                        logging.info(f"NOT present ({status_code}), {check_target_bucket}, {object_key}, {status_code}")

            logging.info(f"# Total objects:, {total_obj_count}, Total found:, {found_obj_count}, Total missing:, {missing_object_count}")

    except FileNotFoundError:
        logging.error(f"# Error: The file {file_path} was not found.")
        return
    
    except Exception as e:
        logging.error(f"# An error occurred: {e}")
        return

if __name__ == "__main__":
    args = parse_arguments()
    
    setup_logging(args.log)  # Set up logging with specified log file
    
    initialize_s3_client(args.region)  # Initialize S3 client once
    
    start_time = time.time()
    
    read_csv_and_check_objects(args.csv, args.bucket)
    
    end_time = time.time()
    
    logging.info(f"# Time taken: {end_time - start_time:.2f} seconds")
