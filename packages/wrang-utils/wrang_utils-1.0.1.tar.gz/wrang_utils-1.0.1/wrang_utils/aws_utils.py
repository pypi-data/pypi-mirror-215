import json
import logging
import time
import urllib.parse
import urllib.request
from collections import defaultdict
from typing import Any, Dict

import boto3
from boto3.dynamodb.types import TypeDeserializer
from mypy_boto3_amplify import AmplifyClient
from mypy_boto3_amplifybackend import AmplifyBackendClient
from mypy_boto3_appsync import AppSyncClient
from mypy_boto3_dynamodb import DynamoDBClient
from mypy_boto3_ssm import SSMClient

def amplify_resource_details(
    amplify_app_name: str,
    debug: bool = False,
) -> Dict[str, Any]:
    """
    Fetch amplify resource details given the amplify app name. Returns details for each environment.
    """

    amplify_details = defaultdict(dict)

    amplify_client: AmplifyClient = boto3.client("amplify")

    amplify_app_id = None
    amplify_app_list = amplify_client.list_apps()
    for item in amplify_app_list["apps"]:
        if item["name"] == amplify_app_name:
            amplify_app_id = item["appId"]
            # print(item)
            break

    amplifybackend_client: AmplifyBackendClient = boto3.client("amplifybackend")
    backend_environments = amplify_client.list_backend_environments(appId=amplify_app_id)

    for backend_environment in backend_environments.get("backendEnvironments", []):
        env_name = backend_environment["environmentName"]
        backend = amplifybackend_client.get_backend(
            AppId=amplify_app_id, BackendEnvironmentName=env_name
        )
        parsed_backend = json.loads(backend.get("AmplifyMetaConfig"))
        backend_apis: Dict[str, Any] = parsed_backend.get("api", {})

        for key, value in backend_apis.items():
            # Get appsync details
            if value.get("service") == "AppSync":
                appsync_details = value["output"]
                graphql_endpoint = appsync_details["GraphQLAPIEndpointOutput"]
                graphql_api_key = appsync_details["GraphQLAPIKeyOutput"]
                graphql_api_id = appsync_details["GraphQLAPIIdOutput"]

                amplify_details[env_name]["API_WRANGLED_GRAPHQL_ENDPOINT"] = graphql_endpoint
                amplify_details[env_name]["API_WRANGLED_API_KEY"] = graphql_api_key
                amplify_details[env_name]["API_WRANGLED_GRAPHQL_ID"] = graphql_api_id
                if debug:
                    # Print all the available tables connected to the appsync client
                    appsync_client: AppSyncClient = boto3.client("appsync")

                    for item in appsync_client.list_data_sources(
                        apiId=appsync_details["GraphQLAPIIdOutput"]
                    ).get("dataSources"):
                        print(json.dumps(item, indent=4, sort_keys=True))
                break

        storage: Dict[str, Any] = parsed_backend.get("storage", {})
        for key, value in storage.items():
            if value.get("service") == "S3":
                bucket_name = value["output"]["BucketName"]
                amplify_details[env_name]["API_WRANGLED_S3_BUCKET"] = bucket_name

    return amplify_details

def fetch_table_stream_arn(table_name: str) -> str:
    """
    Fetch the stream arn for a dynamodb table
    """
    dynamodb_client: DynamoDBClient = boto3.client("dynamodb")
    table = dynamodb_client.describe_table(TableName=table_name)

    stream_arn = table.get("Table", {}).get("LatestStreamArn")

    if stream_arn is None:
        raise ValueError(f"No stream arn found for table: {table_name}")

    return stream_arn

def fetch_credentials(key_location: str, region: str = "us-east-1") -> Dict:
    """
    fetch ssm credentials with key
    """
    ssm: SSMClient = boto3.client("ssm", region)
    parameter = ssm.get_parameter(Name=key_location, WithDecryption=True)

    value = parameter.get("Parameter", {}).get("Value")

    if value is None:
        raise ValueError(f"No value found in SSM parameter for key: {key_location}")

    return json.loads(value)


deserializer = TypeDeserializer()


def clean_dynamo_data(item: Dict[str, Any]) -> Dict[str, Any]:
    """
    Deserialize json data from dynamodb
    """
    return {k: deserializer.deserialize(v) for k, v in item.items()}

def gen_delete_key_params(keys: list[str], value: Dict[str, Any]):
    """
    Simplify the gen_delete_key_params function
    """
    return {key: value[key] for key in keys}


def truncate_table(table_name: str, keys: list[str], limit: int):
    """
    Delete all items in a table
    """
    try:
        flag = False
        dynamodb = boto3.resource("dynamodb")
        table = dynamodb.Table(table_name)
        scan = table.scan(Limit=limit)

        while not flag:
            with table.batch_writer() as bw:
                for item in scan["Items"]:
                    bw.delete_item(Key={key: item[key] for key in keys})

                flag = True

        time.sleep(0.1)

        if len(scan["Items"]) > 0:
            return False

        return True

    except Exception as exception:
        logging.error("truncate error %s.", exception)
        return False


def latest_image_tag(ecr_repo: str) -> str:
    """
    Fetch the latest image version from ECR (the hash)
    """

    jmespath_expression = "sort_by(imageDetails, &to_string(imagePushedAt))[-1].imageTags"

    client = boto3.client("ecr")

    paginator = client.get_paginator("describe_images")

    iterator = paginator.paginate(repositoryName=ecr_repo)
    filter_iterator = iterator.search(jmespath_expression)
    result = list(filter_iterator)
    for item in result:
        if item != "latest":
            return item

    return "latest"


def list_files_s3(path):
    """
    List all files under a path in s3
    """
    values = urllib.parse.urlparse(path)
    bucket = values.netloc
    key = values.path[1:]
    logging.info(f"querying {bucket} {key}")

    s3 = boto3.client("s3")
    return [
        f"s3://{bucket}/" + item["Key"]
        for item in s3.list_objects_v2(Bucket=bucket, Prefix=key).get("Contents", [])
    ]
