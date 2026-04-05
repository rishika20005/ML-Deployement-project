import boto3
import json
from dotenv import load_dotenv
import os

# Load credentials from .env
load_dotenv()

print("🔄 Testing Bedrock connection...")

try:
    # Create Bedrock client
    client = boto3.client(
        'bedrock-runtime',
        region_name=os.getenv('AWS_DEFAULT_REGION'),
        aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
        aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY')
    )
    
    # Call Claude 3 Haiku
    response = client.invoke_model(
        modelId='anthropic.claude-3-haiku-20240307-v1:0',
        body=json.dumps({
            "anthropic_version": "bedrock-2023-05-31",
            "max_tokens": 100,
            "messages": [
                {"role": "user", "content": "Hello! I'm building a multi-agent AI system."}
            ]
        })
    )
    
    result = json.loads(response['body'].read())
    print("✅ SUCCESS! Bedrock is working!")
    print(f"\nResponse: {result['content'][0]['text']}")
    
except Exception as e:
    print("❌ Error:")
    print(f"{type(e).__name__}: {e}")