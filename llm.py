import boto3
import json
import streamlit as st
import os

class BedrockClient:
    def __init__(self):
        # Try Streamlit secrets first (for cloud deployment)
        try:
            aws_key = st.secrets["AWS_ACCESS_KEY_ID"]
            aws_secret = st.secrets["AWS_SECRET_ACCESS_KEY"]
            region = st.secrets["AWS_DEFAULT_REGION"]
        except Exception as e:
            # Fallback to .env (for local testing)
            from dotenv import load_dotenv
            load_dotenv()
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
        
        # Create Bedrock client
        self.client = boto3.client(
            'bedrock-runtime',
            region_name=region,
            aws_access_key_id=aws_key,
            aws_secret_access_key=aws_secret
        )
    
    def generate(self, prompt: str, system_prompt: str = "") -> str:
        """Generate text using Claude 3 Haiku"""
        
        # Build the full prompt
        if system_prompt:
            full_prompt = f"{system_prompt}\n\nUser: {prompt}\nAssistant:"
        else:
            full_prompt = prompt
        
        # Create request body
        body = json.dumps({
            "anthropic_version": "bedrock-2023-05-31",
            "max_tokens": 1000,
            "messages": [
                {"role": "user", "content": full_prompt}
            ]
        })
        
        # Call Bedrock
        response = self.client.invoke_model(
            modelId='anthropic.claude-3-haiku-20240307-v1:0',
            body=body
        )
        
        # Parse response
        result = json.loads(response['body'].read())
        return result['content'][0]['text']

# ============================================
# Create global instance (this is what agents.py imports)
# ============================================
bedrock = BedrockClient()