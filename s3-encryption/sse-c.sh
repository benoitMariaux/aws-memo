#!/bin/bash

# SSE-C
# Server side encryption, but Custom encryption key provided
# See :
# https://cloudonaut.io/encrypting-sensitive-data-stored-on-s3/

BUCKET=sse-c-demo-$(uuidgen | tr "[:upper:]" "[:lower:]")
# BUCKET=sse-c-demo-aaaaaaaaaaaaaaaaaaa

# Create bucket
aws s3 mb s3://${BUCKET}

# Create a file
FILE=/tmp/sse-c-file
echo "A text file" > $FILE

# Generate a random 32 bytes (256 bits) key with openssl:
SECRET_KEY=/tmp/sse-c.key
openssl rand -out $SECRET_KEY 32

aws s3 cp $FILE s3://$BUCKET \
    --sse-c AES256 \
    --sse-c-key fileb://${SECRET_KEY} \

# Check object encryption
aws s3api head-object --bucket $BUCKET --key $(basename $FILE) \
    --sse-customer-key fileb://${SECRET_KEY} \
    --sse-customer-algorithm AES256 \

# Retrieve the encrypted object
aws s3 cp s3://${BUCKET}/$(basename $FILE) /tmp/ \
    --sse-c AES256 \
    --sse-c-key fileb://${SECRET_KEY} \

cat /tmp/$(basename $FILE)

aws s3 rm s3://${BUCKET}/$(basename $FILE)
aws s3 rb s3://${BUCKET}
