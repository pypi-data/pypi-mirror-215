"""
Utils for interacting with AWS
"""

import json
from typing import Any, Dict

import boto3
from boto3.dynamodb.types import TypeDeserializer


def fetch_credentials(key_location: str, region: str="us-east-1") -> Dict:
    """
    fetch ssm credentials with key
    """
    ssm = boto3.client("ssm", region)
    parameter = ssm.get_parameter(Name=key_location, WithDecryption=True)
    params = json.loads(parameter["Parameter"]["Value"])

    return params


deserializer = TypeDeserializer()


def clean_dynamo_data(item: Dict[str, Any]) -> Dict[str, Any]:
    """
    Deserialize json data from dynamodb
    """
    return {k: deserializer.deserialize(v) for k, v in item.items()}