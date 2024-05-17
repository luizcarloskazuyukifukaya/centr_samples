import os
import random
import string
import boto3

def randomstr(n):
   randlst = [random.choice(string.ascii_letters + string.digits) for i in range(n)]
   return ''.join(randlst)

def create_dummy_file(file_name, size_in_bytes):
  b = bytearray()
  b.extend(map(ord, randomstr(size_in_bytes)))

  with open(file_name, 'wb') as f:
    f.write(b)
    
def rename_file(old_name, new_name):
    try:
        os.rename(old_name, new_name)
        print(f"File '{old_name}' has been renamed to '{new_name}'.")
    except OSError as e:
        print(f"An error occurred: {e}")

def upload_files_to_s3_bucket(original_file_name, num_of_files):
  # original_file_name: the original/template file
  # num_of_files: number of copy to be uploaded
  # (NOTE) The actual object key name will be named based on original_file_name+"xxxxx"
  
  # Define the target bucket and prefix
  target_bucket = "centr-source-bucket"

  print(target_bucket)

  session = boto3.Session(profile_name="wasabi")
  credentials = session.get_credentials()
  aws_access_key_id = credentials.access_key
  aws_secret_access_key = credentials.secret_key
  region = 'ap-southeast-2'
  endpoint_url = 'https://s3.' + region + '.wasabisys.com'

  print(region)
  print(endpoint_url)
  #print(aws_access_key_id)
  #print(aws_secret_access_key)

  s3 = boto3.client('s3',
                    endpoint_url=endpoint_url,
                    aws_access_key_id=aws_access_key_id,
                    aws_secret_access_key=aws_secret_access_key)

  for x in range(num_of_files):
    
    target_file = f"dummy_file_{x}"
    # upload an object (original_file + "xxxxx")
    r = s3.upload_file(
        original_file_name,
        target_bucket,
        target_file,
    )
    # print(r)
    print(f"{target_file} uploaded to {target_bucket}")    

  print(f"File upload completed. {num_of_files} files uploaded to {target_bucket}")



def main():
  # Specify the file name and size in bytes
  # file_name = "dummy_file.txt"
  # file_size = 1024  # 1 KB
  # file_size = 1024 * 1024  # 1 MB
  # file_size = 1024 * 1024 * 1024 # 1 GB
  # file_size = 1024 * 1024 * 512 # 0.5 GB

  # create_dummy_file(file_name, file_size)

  # print(f"Dummy file '{file_name}' created with size {file_size} bytes.")

  # # Specify the old and new file names
  # old_file_name = file_name
  # new_file_name = "new_file.txt"

  # rename_file(old_file_name, new_file_name)
  target_file_name = "new_file.txt"

  # num_of_files = 10
  # new_file.txt file size is 512MB (0.5 GB)
  num_of_files = 2 * 1024 * 350 # 0.5 x 2 (1G) x 1024 (1T) x 350 T
  upload_files_to_s3_bucket(target_file_name, num_of_files)

if __name__ == "__main__":
  main()