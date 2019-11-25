import boto3
import uuid
import os

BUCKET = "sse-c-demo-"+str(uuid.uuid4())

s3 = boto3.client('s3')

# Create bucket
s3.create_bucket(Bucket=BUCKET)

# Create a file
FILE = "/tmp/sse-c-file"
OBJECT_KEY=os.path.basename(FILE)

file_object = open(FILE, "w")
for i in range(3):
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
