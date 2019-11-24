import boto3
import uuid
import os
import sys

# SSE-C
# Server side encryption, but Custom encryption key provided

# debug
# import sys

# file_object = open('/tmp/tttt', "r+")
# for item in range(1,100):
#     file_object.write("A text file: " + str(item) + "\n")
    


# sys.exit();

BUCKET = "sse-c-demo-"+str(uuid.uuid4())

s3 = boto3.client('s3')

# Create bucket
s3.create_bucket(Bucket=BUCKET)

# Create a file
FILE = "/tmp/sse-c-file"
OBJECT_KEY=os.path.basename(FILE)

file_object = open(FILE, "w")
for i in range(100):
    file_object.write("Line %d\n" % (i+1))

file_object.close()

# Generate a random 32 bytes (256 bits) 
SECRET_KEY = os.urandom(32)

s3.put_object(
    Bucket=BUCKET,
    Key=OBJECT_KEY,
    Body=open(FILE, "r").read(),
    SSECustomerKey=SECRET_KEY,
    SSECustomerAlgorithm='AES256'
)

file_object.close()


# Check object encryption
r = s3.head_object(
    Bucket=BUCKET,
    Key=OBJECT_KEY,
    SSECustomerKey=SECRET_KEY,
    SSECustomerAlgorithm='AES256'
)

print(r['ResponseMetadata']['HTTPHeaders']['x-amz-server-side-encryption-customer-algorithm'])

# Retrieve the encrypted object
r = s3.get_object(
    Bucket=BUCKET,
    Key=OBJECT_KEY,
    SSECustomerKey=SECRET_KEY,
    SSECustomerAlgorithm='AES256'
)

print(r['Body'].read())

# TODO
#r = s3.download_file(BUCKET, OBJECT_KEY, FILE)




