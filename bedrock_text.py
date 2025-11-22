import json
from bedrock_utils import get_bedrock_client

def generate_text(prompt, model_id='amazon.titan-text-express-v1'):
    """
    Generates text using the specified Bedrock model.
    """
    client = get_bedrock_client()
    if not client:
        return

    print(f"Generating text with model: {model_id}")
    
    # Payload structure varies by model. This is for Amazon Titan.
    # For Claude, the body structure is different.
    
    try:
        if 'titan' in model_id:
            body = json.dumps({
                "inputText": prompt,
                "textGenerationConfig": {
                    "maxTokenCount": 512,
                    "stopSequences": [],
                    "temperature": 0.7,
                    "topP": 0.9
                }
            })
        elif 'claude' in model_id:
             body = json.dumps({
                "prompt": f"\n\nHuman: {prompt}\n\nAssistant:",
                "max_tokens_to_sample": 300,
                "temperature": 0.5,
                "top_k": 250,
                "top_p": 1,
                "stop_sequences": ["\n\nHuman:"],
                "anthropic_version": "bedrock-2023-05-31"
            })
        else:
            print(f"Unsupported model for this simple script: {model_id}")
            return

        response = client.invoke_model(
            body=body,
            modelId=model_id,
            accept='application/json',
            contentType='application/json'
        )

        response_body = json.loads(response.get('body').read())
        
        if 'titan' in model_id:
            print("Output:")
            print(response_body.get('results')[0].get('outputText'))
        elif 'claude' in model_id:
            print("Output:")
            print(response_body.get('completion'))
            
    except Exception as e:
        print(f"Error invoking model: {e}")

if __name__ == "__main__":
    prompt = "Explain the concept of quantum computing in simple terms."
    generate_text(prompt)
    # generate_text(prompt, model_id='anthropic.claude-v2') 
