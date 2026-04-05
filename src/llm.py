import boto3
import json
import streamlit as st
import os

class BedrockClient:
    def __init__(self):
        # Get AWS credentials from Streamlit secrets or environment
        try:
            # Try Streamlit Cloud secrets first
            aws_key = st.secrets["AWS_ACCESS_KEY_ID"]
            aws_secret = st.secrets["AWS_SECRET_ACCESS_KEY"]
            region = st.secrets.get("AWS_DEFAULT_REGION", "us-east-1")
        except Exception as e:
            # Fallback to environment variables
            aws_key = os.getenv('AWS_ACCESS_KEY_ID')
            aws_secret = os.getenv('AWS_SECRET_ACCESS_KEY')
            region = os.getenv('AWS_DEFAULT_REGION', 'us-east-1')
            
            # If still empty, raise error
            if not aws_key or not aws_secret:
                raise ValueError(
                    "AWS credentials not found! "
                    "Please add them to GitHub Secrets: "
                    "AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_DEFAULT_REGION"
                )
        
        # Create Bedrock client with explicit region
        self.client = boto3.client(
            'bedrock-runtime',
            region_name=region,
            aws_access_key_id=aws_key,
            aws_secret_access_key=aws_secret
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