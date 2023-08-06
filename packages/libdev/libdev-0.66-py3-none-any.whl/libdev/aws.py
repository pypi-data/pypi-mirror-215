"""
Functionality of Amazon Web Services
"""

import io

import requests
import boto3
from botocore.exceptions import ClientError

from .cfg import cfg
from .gen import generate


LINK = (
    f"https://{cfg('amazon.bucket')}.s3."
    f"{cfg('amazon.region')}.amazonaws.com/"
)


s3 = boto3.resource(
    's3',
    region_name=cfg('amazon.region'),
    aws_access_key_id=cfg('amazon.id'),
    aws_secret_access_key=cfg('amazon.secret'),
)
s3client = s3.meta.client


def upload_file(
    file,
    bucket=cfg('amazon.bucket'),
    directory=cfg('mode').lower(),
    file_type=None,
):
    """ Upload file """

    if not file_type and isinstance(file, str) and '.' in file:
        file_type = file.split('.')[-1]
    file_type = '.' + file_type.lower() if file_type else ''

    name = f"{directory}/{generate()}{file_type}"

    if isinstance(file, str):
        if file[:4] == 'http':
            file = io.BytesIO(requests.get(file, timeout=30).content)
            handler = s3client.upload_fileobj
        else:
            handler = s3client.upload_file
    elif isinstance(file, bytes):
        file = io.BytesIO(file)
        handler = s3client.upload_fileobj
    else:
        handler = s3client.upload_fileobj

    handler(
        file, bucket, name,
        ExtraArgs={'ACL': 'public-read'},
    )

    return LINK + name

def get_policy(bucket=cfg('amazon.bucket')):
    """ Get bucket policy """
    return s3client.get_bucket_policy(Bucket=bucket)


__all__ = (
    's3',
    's3client',
    'ClientError',
    'upload_file',
    'get_policy',
)
