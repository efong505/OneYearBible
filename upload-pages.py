import boto3
import os
from pathlib import Path

s3 = boto3.client('s3')
bucket_name = 'one-year-bible-ekewaka'

def upload_file(local_path, s3_key):
    try:
        s3.upload_file(local_path, bucket_name, s3_key, ExtraArgs={'ContentType': 'text/html'})
        print(f"Uploaded: {s3_key}")
        return True
    except Exception as e:
        print(f"Error uploading {s3_key}: {e}")
        return False

# Upload index.html
upload_file('index.html', 'index.html')

# Upload all reading pages
months = ['january', 'february', 'march', 'april', 'may', 'june', 
          'july', 'august', 'september', 'october', 'november', 'december']

for month in months:
    month_dir = f'readings/{month}'
    if os.path.exists(month_dir):
        for file in os.listdir(month_dir):
            if file.endswith('.html'):
                local_path = f'{month_dir}/{file}'
                s3_key = f'readings/{month}/{file}'
                upload_file(local_path, s3_key)

print("Upload complete!")