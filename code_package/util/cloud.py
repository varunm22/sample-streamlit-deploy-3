import boto3
from typing import List
import yaml
from yaml.loader import SafeLoader


def get_aws_parameter(key):
    # session = boto3.session.Session(profile_name="personal", region_name="us-east-1")
    session = boto3.session.Session()
    ssm = session.client("ssm")
    response = ssm.get_parameter(Name=key, WithDecryption=True)
    return response["Parameter"]["Value"]


def bucket_key_from_s3_uri(s3_uri: str) -> str:
    parts = s3_uri.split("/")
    bucket, key = parts[2], "/".join(parts[3:])
    return bucket, key


def s3_uri_from_bucket_key(bucket: str, key: str) -> str:
    return f"s3://{bucket}/{key}"


def read_yml_from_s3(s3_uri: str):
    session = boto3.session.Session(profile_name="personal", region_name="us-east-1")
    # session = boto3.session.Session()
    s3 = session.client("s3")
    bucket, key = bucket_key_from_s3_uri(s3_uri)
    response = s3.get_object(Bucket=bucket, Key=key)
    return yaml.load(response["Body"], Loader=SafeLoader)


def write_yml_to_s3(yml: dict, s3_uri: str):
    session = boto3.session.Session(profile_name="personal", region_name="us-east-1")
    # session = boto3.session.Session()
    s3 = session.client("s3")
    bucket, key = bucket_key_from_s3_uri(s3_uri)
    s3.put_object(Bucket=bucket, Key=key, Body=yaml.dump(yml))


def s3_ls(s3_uri: str) -> List[str]:
    session = boto3.session.Session(profile_name="personal", region_name="us-east-1")
    # session = boto3.session.Session()
    s3 = session.client("s3")
    objects = []
    bucket, key = bucket_key_from_s3_uri(s3_uri)
    paginator = s3.get_paginator("list_objects_v2")
    pages = list(paginator.paginate(Bucket=bucket, Prefix=key, Delimiter="/"))

    for page in pages:
        for cur in page.get("CommonPrefixes", []):
            objects.append(s3_uri_from_bucket_key(bucket, cur["Prefix"]))
        for cur in page.get("Contents", []):
            # If the user manually creates the dir, then there is an obj representing the dir itself
            if cur["Key"] != key:
                objects.append(s3_uri_from_bucket_key(bucket, cur["Key"]))
    return objects
