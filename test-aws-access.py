import boto3

try:
    # Test Polly access
    polly = boto3.client('polly', region_name='us-east-1')
    voices = polly.describe_voices(Engine='long-form')
    print("[OK] Polly access working")
    
    # Test S3 access
    s3 = boto3.client('s3')
    s3.head_bucket(Bucket='one-year-bible-ekewaka')
    print("[OK] S3 bucket access working")
    
    print("AWS credentials are properly configured!")
    
except Exception as e:
    print(f"AWS Error: {e}")
    print("Please check your AWS credentials and permissions")