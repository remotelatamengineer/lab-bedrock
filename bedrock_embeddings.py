import json
from bedrock_utils import get_bedrock_client

def generate_embeddings(text, model_id='amazon.titan-embed-text-v1'):
    """
    Generates embeddings for the given text using the specified Bedrock model.
    """
    client = get_bedrock_client()
    if not client:
        return

    print(f"Generating embeddings with model: {model_id}")
    
    try:
        body = json.dumps({
            "inputText": text
        })

        response = client.invoke_model(
            body=body,
            modelId=model_id,
            accept='application/json',
            contentType='application/json'
        )

        response_body = json.loads(response.get('body').read())
        
        embedding = response_body.get('embedding')
        print(f"Embedding generated. Vector length: {len(embedding)}")
        print(f"First 5 elements: {embedding[:5]}")
            
    except Exception as e:
        print(f"Error invoking model: {e}")

if __name__ == "__main__":
    text = "This is a test sentence for generating embeddings."
    generate_embeddings(text)
