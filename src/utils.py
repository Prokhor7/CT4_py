import boto3
import yaml
from attrdict import AttrDict

CONFIG_PATH = "config.yaml"


def load_config():
    """
    Load variables from config file;
    :return: config file variables in dictionary format.
    """
    try:
        with open(CONFIG_PATH, 'r') as conf_file:
            # Load variables from yaml file
            config = yaml.safe_load(conf_file)
    except Exception as e:
        print(f"Error reading the config file!: {e}")

    return AttrDict(config)


def connect_to_boto_client(client_type="ec2"):
    """
    Connecting to determined AWS services through boto3 client instance;
    :param client_type: service type for connection;
    :return: boto client instance with connection with determined  service.
    """
    # Define config variable
    config = load_config()
    # Define empty client variable
    client = None
    match client_type:
        case "ec2": client = boto3.client("ec2", region_name=config.boto.region)
        case "s3": client = boto3.client("s3", region_name=config.boto.region)
        case _: print("Please choose available client type [ec2|s3]")

    return client
