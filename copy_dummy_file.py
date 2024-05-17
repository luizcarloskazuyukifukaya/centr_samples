import boto3

def multiply_object(bucket_name, original_key):

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
  # num_of_files = 10
  # new_file.txt file size is 512MB (0.5 GB)
  num_of_files = 2 * 1024 * 350 # 0.5 x 2 (1G) x 1024 (1T) x 350 T
  # num_of_files = 5 # test

  # copy source
  copy_source = {
      'Bucket': bucket_name,
      'Key': original_key
  }
    
  for x in range(num_of_files):
    # new key name is created based on the numbering
    new_key = f"dummy_file_{x}.txt"
    try:
        
        s3.copy_object(CopySource=copy_source, Bucket=bucket_name, Key=new_key)
        print(f"Object '{original_key}' copied to '{new_key}' in bucket '{bucket_name}'.")
    except Exception as e:
        print(f"An error occurred: {e}")

def main():
  # Specify the bucket name, old key, and new key
  bucket_name = 'centr-source-bucket'
  template_key = "dummy_file_0"

  multiply_object(bucket_name, template_key)

if __name__ == "__main__":
  main()