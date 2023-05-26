import boto3
import os

# Import utils for load config
from src.utils import load_config

CONFIG = load_config()


def create_pairs():
    """
    Creates key pair for secure connection with AWS services through SDK;
    And saving the private key on the local machine.
    """
    ec2_client = boto3.client("ec2", region_name=CONFIG.boto.region)
    key_pair = ec2_client.create_key_pair(KeyName=CONFIG.key_pairs.name)

    private_key = key_pair["KeyMaterial"]
    with os.fdopen(os.open(CONFIG.key_pairs.path, os.O_WRONLY | os.O_CREAT, 0o400), 'w+') as key_handle:
        key_handle.write(private_key)


def delete_pairs():
    """
    Delete key pair for secure connection and delete private key on local machine;
    """
    ec2_client = boto3.client("ec2", region_name=CONFIG.boto.region)
    ec2_client.delete_key_pair(KeyName=CONFIG.key_pairs.name)

    os.remove(CONFIG.key_pairs.path)
