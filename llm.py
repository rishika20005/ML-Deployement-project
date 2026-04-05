import boto3
import json
from dotenv import load_dotenv
import os

load_dotenv()

class BedrockClient:
    def __init__(self):
        self.client = boto3.client(
            'bedrock-runtime',
            region_name=os.getenv('AWS_DEFAULT_REGION'),
            aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
            aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY')
        )
    
    def generate(self, prompt: str, system_prompt: str = "") -> str:
        """Generate text using Claude 3 Haiku"""
        
        full_prompt = f"{system_prompt}\n\nUser: {prompt}\nAssistant:" if system_prompt else prompt
        
        body = json.dumps({
            "anthropic_version": "bedrock-2023-05-31",
            "max_tokens": 1000,
            "messages": [
                {"role": "user", "content": full_prompt}
            ]
        })
        
        response = self.client.invoke_model(
            modelId='anthropic.claude-3-haiku-20240307-v1:0',
            body=body
        )
        
        result = json.loads(response['body'].read())
        return result['content'][0]['text']

# Create global instance
bedrock = BedrockClient()