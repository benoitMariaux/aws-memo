#!/bin/bash

# SSE-KMS
# Server side encryption using keys created via KMS (AWS managed CMK)
# See :
# https://cloudonaut.io/encrypting-sensitive-data-stored-on-s3/

BUCKET=sse-kms-demo-$(uuidgen | tr "[:upper:]" "[:lower:]")

# Create bucket
aws s3 mb s3://${BUCKET}

# Create a file
FILE=/tmp/sse-kms-file
echo "A text file" > $FILE

aws s3 cp $FILE s3://$BUCKET \
    --sse aws:kms \

# Check object encryption
aws s3api head-object --bucket $BUCKET --key $(basename $FILE) 

# Retrieve the encrypted object
aws s3 cp s3://${BUCKET}/$(basename $FILE) /tmp/ 

cat /tmp/$(basename $FILE)

aws s3 rm s3://${BUCKET}/$(basename $FILE)
aws s3 rb s3://${BUCKET}
