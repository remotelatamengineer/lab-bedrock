import boto3
import os
from dotenv import load_dotenv

load_dotenv()

def get_bedrock_client(service_name='bedrock-runtime', region_name=None):
    """
    Creates and returns a boto3 client for AWS Bedrock.
    
    Args:
        service_name (str): The name of the service (default: 'bedrock-runtime').
        region_name (str): The AWS region (optional).
        
    Returns:
        boto3.client: The Bedrock client.
    """
    region = region_name or os.getenv('AWS_DEFAULT_REGION', 'us-east-1')
    
    try:
        client = boto3.client(
            service_name=service_name,
            region_name=region
        )
        return client
    except Exception as e:
        print(f"Error creating Bedrock client: {e}")
        return None
