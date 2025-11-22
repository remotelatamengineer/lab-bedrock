import json
import base64
import os
from bedrock_utils import get_bedrock_client

def generate_image(prompt, output_file='output_image.png', model_id='amazon.titan-image-generator-v1'):
    """
    Generates an image using the specified Bedrock model.
    """
    client = get_bedrock_client()
    if not client:
        return

    print(f"Generating image with model: {model_id}")
    
    try:
        if 'titan' in model_id:
            body = json.dumps({
                "taskType": "TEXT_IMAGE",
                "textToImageParams": {
                    "text": prompt
                },
                "imageGenerationConfig": {
                    "numberOfImages": 1,
                    "height": 512,
                    "width": 512,
                    "cfgScale": 8.0
                }
            })
        elif 'stability' in model_id:
             body = json.dumps({
                "text_prompts": [{"text": prompt}],
                "cfg_scale": 10,
                "seed": 0,
                "steps": 30
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
            base64_image = response_body.get('images')[0]
        elif 'stability' in model_id:
            base64_image = response_body.get('artifacts')[0].get('base64')
            
        with open(output_file, 'wb') as f:
            f.write(base64.b64decode(base64_image))
            
        print(f"Image saved to {output_file}")

    except Exception as e:
        print(f"Error invoking model: {e}")

if __name__ == "__main__":
    prompt = "A fox jump over a lazy dog."
    generate_image(prompt)
    # generate_image(prompt, model_id='stability.stable-diffusion-xl-v1')
