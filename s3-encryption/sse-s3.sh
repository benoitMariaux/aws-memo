#!/bin/bash

# SSE-S3
# Server side encryption using keys handled and managed by AWS
# See :
# https://cloudonaut.io/encrypting-sensitive-data-stored-on-s3/

BUCKET=sse-s3-demo-$(uuidgen | tr "[:upper:]" "[:lower:]")

# Create bucket
aws s3 mb s3://${BUCKET}

# Create a file
FILE=/tmp/sse-s3-file
echo "A text file" > $FILE

aws s3 cp $FILE s3://$BUCKET \
    --sse AES256 \

# Check object encryption
aws s3api head-object --bucket $BUCKET --key $(basename $FILE) 

# Retrieve the encrypted object
aws s3 cp s3://${BUCKET}/$(basename $FILE) /tmp/ 

cat /tmp/$(basename $FILE)

aws s3 rm s3://${BUCKET}/$(basename $FILE)
aws s3 rb s3://${BUCKET}
