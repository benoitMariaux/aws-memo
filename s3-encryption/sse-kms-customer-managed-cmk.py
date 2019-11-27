import boto3
import uuid
import os

BUCKET = "sse-kms-2-demo-"+str(uuid.uuid4())

s3 = boto3.client('s3')

# Create bucket
s3.create_bucket(Bucket=BUCKET)

# Create a file
FILE = "/tmp/sse-kms-2-file"
OBJECT_KEY=os.path.basename(FILE)

# Create a KMS Key
kms = boto3.client('kms')
response = kms.create_key()
kms_key_id = response['KeyMetadata']['KeyId']

file_object = open(FILE, "w")
for i in range(3):
    file_object.write("Line %d\n" % (i+1))

file_object.close()

s3.put_object(
    Bucket=BUCKET,
    Key=OBJECT_KEY,
    Body=open(FILE, "r").read(),
    ServerSideEncryption='aws:kms',
    SSEKMSKeyId=kms_key_id
)

file_object.close()

# Check object encryption
r = s3.head_object(
    Bucket=BUCKET,
    Key=OBJECT_KEY
)

print(f"ServerSideEncryption: {r['ServerSideEncryption']}")
print(f"SSEKMSKeyId: {r['SSEKMSKeyId']}")

# Retrieve the encrypted object
r = s3.get_object(
    Bucket=BUCKET,
    Key=OBJECT_KEY
)

print(r['Body'].read())

kms.schedule_key_deletion(
    KeyId=kms_key_id,
    PendingWindowInDays=7
)

s3.delete_object(
    Bucket=BUCKET,
    Key=OBJECT_KEY
)

s3.delete_bucket(
    Bucket=BUCKET
)