# Migration Tools 

## Setup Environment (Client PC: Mac) 

- Install Python  (https://www.youtube.com/watch?v=nhv82tvFfkM) 
- Install Git (https://www.youtube.com/watch?v=B4qsvQ5IqWk) 
- Install AWS boto3 (https://aws.amazon.com/sdk-for-python/?nc1=h_ls) 

With the terminal opend, execute the following command: 
```
pip install boto3 
```

## AWS S3 Access configuration 

The following configuration is required to execute the python program provided so it can access Wasabi Cloud Storage APIs. Details here for your reference, but you can follow the steps below: 

Profile and region 

Set up a default region and the profile for Wasabi by manually creating the configuration file in your home directory (in ~/.aws/config): 
```
[default] 
region = ap-southeast-2 
[profile wasabi] 
region = ap-southeast-2 
s3 = 
    endpoint_url = https://s3.ap-southeast-2.wasabisys.com 
s3api = 
    endpoint_url = https://s3.ap-southeast-2.wasabisys.com 
```

(Note) The home directory path (.ex. '~' for Linux) is different depending on the type of Operating System used. 

## Credentials 

Then, specify the credentials provided per account to access Wasabi S3 by manually creating the credential file in your home directory (in ~/.aws/credentials): 
```
[default] 
aws_access_key_id = YOUR_ACCESS_KEY_ID 
aws_secret_access_key = YOUR_SECRET_ACCESS_KEY 
[wasabi] 
aws_access_key_id = YOUR_ACCESS_KEY_ID 
aws_secret_access_key = YOUR_SECRET_ACCESS_KEY 
```

(Note) The home directory path (.ex. '~' for Linux) is different depending on the type of Operating System used. 

## Clone GitHub Repository 

Then, you will need to clone this GitHub repository to your local environment, so you can execute the codes. Select any folder/directory where you want to clone the samples with the following command: 
```
git clone https://github.com/luizcarloskazuyukifukaya/centr_samples 
cd centr_samples 
```

## Python Code Execution 

Now, you are ready to start executing the samples with the following command: 

```
python <python file> 
```


## Fetch Bucket Object List  

You can retrieve all objects (we call it “bucket inventory”) from the specified bucket by executing the following commend: 
```
python s3ListAllObjectsForABucketV2.py <bucket-name> <region> <Timestamp flag> 
```


Example: 
The following is the command to retrieve the bucket inventory from the bucket name "centr-target-bucket-half-tb", region "ap-southeast-2" which is for Sydney, and the timestamp flag with "false".
```
xfukaya@kfukaya:~/projects/python/s3pythonsamples$ python3 s3ListAllObjectsForABucketV2.py centr-target-bucket-half-tb ap-southeast-2 false 
Bucket name: centr-target-bucket-half-tb 
dummy_file_0 
dummy_file_0.txt 
dummy_file_1.txt 
dummy_file_10.txt 
dummy_file_100.txt 
dummy_file_1000.txt 
... 

Total objects 2467 
Total Size: 1.2026 TB 
Total Size: 1322313289518 bytes 
xfukaya@kfukaya:~/projects/python/centr_samples$ 
```
(Note) The timestamp flag is to be used from you need to get all timestamp of each objects.