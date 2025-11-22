import boto3
import os
from dotenv import load_dotenv

load_dotenv()

def verify_credentials():
    """
    Verifies AWS credentials by calling STS GetCallerIdentity.
    """
    print("Attempting to verify credentials...")
    
    # Print masked credentials for debugging (never print full secrets!)
    key_id = os.getenv('AWS_ACCESS_KEY_ID')
    secret_key = os.getenv('AWS_SECRET_ACCESS_KEY')
    token = os.getenv('AWS_SESSION_TOKEN')
    
    print(f"AWS_ACCESS_KEY_ID: {'*' * 16 + key_id[-4:] if key_id else 'Not Set'}")
    print(f"AWS_SECRET_ACCESS_KEY: {'Set' if secret_key else 'Not Set'}")
    print(f"AWS_SESSION_TOKEN: {'Set' if token else 'Not Set'}")
    print(f"AWS_DEFAULT_REGION: {os.getenv('AWS_DEFAULT_REGION', 'Not Set')}")

    try:
        client = boto3.client(
                service_name="bedrock-runtime",
                region_name="us-east-1")
        # Define the model and message
        model_id = "us.anthropic.claude-3-5-haiku-20241022-v1:0"
        messages = [{"role": "user", "content": [{"text": "Hello! Can you tell me about Amazon Bedrock?"}]}]

        # Make the API call
        response = client.converse(
            modelId=model_id,
            messages=messages,
        )


        # Print the response
        print(response['output']['message']['content'][0]['text'])    

    except Exception as e:
        print(f"\nFAILURE: Could not verify credentials.")
        print(f"Error: {e}")

if __name__ == "__main__":
    verify_credentials()
