#!/bin/bash

# SSE-KMS 2
# Server side encryption using keys created via KMS (Customer managed CMK)
# See :
# https://cloudonaut.io/encrypting-sensitive-data-stored-on-s3/

BUCKET=sse-kms-demo-$(uuidgen | tr "[:upper:]" "[:lower:]")

# Create bucket
aws s3 mb s3://${BUCKET}

# Create a file
FILE=/tmp/sse-kms-file
echo "A text file" > $FILE

# Create a KMS Key
KMS_KEY_ID=$(aws kms create-key --output text --query 'KeyMetadata.KeyId')

aws s3 cp $FILE s3://$BUCKET \
    --sse aws:kms \
    --sse-kms-key-id $KMS_KEY_ID 

# Check object encryption
aws s3api head-object --bucket $BUCKET --key $(basename $FILE) 

# Retrieve the encrypted object
aws s3 cp s3://${BUCKET}/$(basename $FILE) /tmp/ 

cat /tmp/$(basename $FILE)

aws s3 rm s3://${BUCKET}/$(basename $FILE)
aws s3 rb s3://${BUCKET}

# Schedule Key Deletion
aws kms schedule-key-deletion --key-id $KMS_KEY_ID --pending-window-in-days 7
