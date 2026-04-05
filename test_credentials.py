import boto3
from dotenv import load_dotenv
import os

load_dotenv()

try:
    # Test IAM access
    iam = boto3.client(
        'iam',
        region_name=os.getenv('AWS_DEFAULT_REGION'),
        aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
        aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY')
    )
    
    user = iam.get_user()
    print("✅ Credentials working!")
    print(f"User: {user['User']['UserName']}")
    
except Exception as e:
    print("❌ Credentials failed:")
    print(f"{type(e).__name__}: {e}")