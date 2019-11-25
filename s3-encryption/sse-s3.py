import boto3
import uuid
import os

BUCKET = "sse-s3-demo-"+str(uuid.uuid4())

s3 = boto3.client('s3')

# Create bucket
s3.create_bucket(Bucket=BUCKET)

# Create a file
FILE = "/tmp/sse-s3-file"
OBJECT_KEY=os.path.basename(FILE)

file_object = open(FILE, "w")
for i in range(3):
    file_object.write("Line %d\n" % (i+1))

file_object.close()

s3.put_object(
    Bucket=BUCKET,
    Key=OBJECT_KEY,
    Body=open(FILE, "r").read(),
    ServerSideEncryption='AES256'
)

file_object.close()

# Check object encryption
r = s3.head_object(
    Bucket=BUCKET,
    Key=OBJECT_KEY
)

print(r['ResponseMetadata']['HTTPHeaders']['x-amz-server-side-encryption'])

# Retrieve the encrypted object
r = s3.get_object(
    Bucket=BUCKET,
    Key=OBJECT_KEY
)

print(r['Body'].read())

s3.delete_object(
    Bucket=BUCKET,
    Key=OBJECT_KEY
)

s3.delete_bucket(
    Bucket=BUCKET
)