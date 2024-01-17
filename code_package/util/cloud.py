import boto3


def get_aws_parameter(key):
    # session = boto3.session.Session(profile_name="personal", region_name="us-east-1")
    session = boto3.session.Session()
    ssm = session.client("ssm")
    response = ssm.get_parameter(Name=key, WithDecryption=True)
    return response["Parameter"]["Value"]
