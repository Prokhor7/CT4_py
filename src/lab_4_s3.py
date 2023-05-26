# Importing libraries for interaction with AWS
from botocore.exceptions import ClientError
# Importing standard libraries
import os

# Import utils for load config
from src.utils import load_config

CONFIG = load_config()


def create_bucket(s3_client, bucket_name):
    """
    Create s3 bucket on AWS S3 server through boto3 client command;
    :param s3_client: boto3 client connection with s3 service;
    :param bucket_name: name of bucket for creation;
    :return: True if the operation was successful, otherwise False.
    """
    try:
        location = {"LocationConstraint": CONFIG.boto.region}
        s3_client.create_bucket(Bucket=bucket_name, CreateBucketConfiguration=location)
    except ClientError as e:
        print(f"Creation bucket error: {e}")
        return False
    print(f"Bucket '{bucket_name}' was create successfully!")
    return True


def upload_file(s3_client, bucket_name, file_path, bucket_file_name=None):
    """
    Upload a file to on S3 bucket;
    :param s3_client: boto3 client connection with s3 service;
    :param bucket_name: to which bucket upload to;
    :param file_path: file to upload;
    :param bucket_file_name: S3 object name (if not specified then file_name is used);
    :return: True if file was uploaded, else False.
    """
    # If s3 bucket file name was not specified, use file_name with 's3_' in begin of the file name
    if bucket_file_name is None:
        bucket_file_name = "s3_" + os.path.basename(file_path)

    # Upload the file
    try:
        s3_client.upload_file(file_path, bucket_name, bucket_file_name)
    except ClientError as e:
        print(f"Upload file error: {e}")
        return False
    except FileNotFoundError as e:
        print(f"File not found error: {e}")
        return False
    return True


def download_file(s3_client, bucket_name, bucket_file_name, file_path=None):
    """
    Download a file from S3 bucket;
    :param s3_client: boto3 client connection with s3 service;
    :param bucket_name: from which bucket download;
    :param bucket_file_name: S3 object name (if not specified then file_path is used);
    :param file_path: file path to download;
    :return: True if file was downloaded, else False.
    """
    # If file_name was not specified, use file_name
    if file_path is None:
        file_path = "../output/" + os.path.basename(bucket_file_name)

    # Download the file
    try:
        s3_client.download_file(bucket_name, bucket_file_name, file_path)
    except ClientError as e:
        print(f"Download file error: {e}")
        return False
    except FileNotFoundError as e:
        print(f"File not found error: {e}")
        return False
    return True


def bucket_manipulation(s3_client, bucket_name, action=None, file_path=None, bucket_file=None):
    """
    Granting access to manipulation to s3 bucket;
    :param s3_client: boto3 client connection with s3 service;
    :param bucket_name: bucket name for manipulation;
    :param action: which action needs to be done with s3 bucket;
    :param file_path: file path for download|upload a file to|from s3 bucket;
    :param bucket_file: file name for containing in s3 bucket;
    """
    match action:
        case "upload": upload_file(s3_client, bucket_name, file_path, bucket_file)
        case "download": download_file(s3_client, bucket_name, bucket_file, file_path)
        case _: print("Please choose available actions [upload|download].")


def get_existing_buckets(s3_client):
    """
    Printing list of all existing s3 bucket on s3 server for your credentials;
    :param s3_client: boto3 client connection with s3 service;
    """
    response = s3_client.list_buckets()

    # Output the bucket names list
    print("Existing buckets in your region:")
    for bucket in response["Buckets"]:
        print(f"\t{bucket['Name']}")


def get_files_in_bucket(s3_client, bucket_name=None):
    """
    Printing list of all files in s3 bucket (with limits of 10 objects);
    :param s3_client: boto3 client connection with s3 service;
    :param bucket_name: bucket which will be checking;
    """
    contents = []
    if bucket_name is None:
        print("Please enter bucket name!!")
    try:
        contents = s3_client.list_objects(Bucket=bucket_name, MaxKeys=10).get("Contents")
    except ClientError as e:
        print(f"Get Files object error: {e}")

    print("List of object in bucket:")
    for bucket_obj in contents:
        print(f"File: {bucket_obj['Key']}")
        print(f"Storage Class: {bucket_obj['StorageClass']}")
        print("---------------------------")


def get_bucket_info(s3_client, bucket_name=None, info_type="list"):
    """
    Grant access to information about s3 buckets;
    :param s3_client: boto3 client connection with s3 service;
    :param bucket_name: bucket which will be checking for info;
    :param info_type: information type which needs to show;
    """
    match info_type:
        case "list": get_existing_buckets(s3_client)
        case "files": get_files_in_bucket(s3_client, bucket_name)
        case _: print("Please choose available info type [list|files].")


def delete_bucket(s3_client, bucket_name):
    """
    Delete s3 bucket on AWS servers through boto3 client command;
    :param s3_client: boto3 client connection with s3 service;
    :param bucket_name: bucket which needs to be deleted;
    :return: True if the operation was successful, otherwise False.
    """
    try:
        # Define objects list for deletion
        objects = []
        # Download objects list
        contents = s3_client.list_objects(Bucket=bucket_name).get("Contents")
        # Parse objects keys
        for bucket_obj in contents:
            objects.append({"Key": bucket_obj["Key"]})
        # Deleting objects from s3 bucket
        s3_client.delete_objects(Bucket=bucket_name, Delete={
            "Objects": objects,
            "Quiet": True
        })
        # Deleting s3 bucket
        s3_client.delete_bucket(Bucket=bucket_name)
    except ClientError as e:
        print(f"Deletion bucket error: {e}")
        return False
    print(f"Bucket '{bucket_name}' was delete successfully!")
    return True
