# AWS MEMO
## S3 Encryption

There are 4 methods of encrypting objects in S3
* SSE-S3: encrypts S3 objects using keys handled & managed by AWS
* SSE-KMS: leverage AWS Key Management Service to manage encryption keys
* SSE-C: when you want to manage your own encryption keys
* Client Side Encryption (TODO)

Working examples in BASH and Python are in `s3-encryption/`
