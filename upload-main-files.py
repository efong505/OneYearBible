import boto3

def upload_main_files():
    """Upload index.html and calendar.js to S3"""
    try:
        s3 = boto3.client('s3')
        bucket_name = 'one-year-bible-ekewaka'
        
        files_to_upload = [
            ('index.html', 'index.html', 'text/html'),
            ('assets/js/calendar.js', 'assets/js/calendar.js', 'application/javascript')
        ]
        
        for local_file, s3_key, content_type in files_to_upload:
            print(f"Uploading {local_file} to S3...")
            
            s3.upload_file(
                local_file, 
                bucket_name, 
                s3_key,
                ExtraArgs={
                    'ContentType': content_type,
                    'CacheControl': 'no-cache, no-store, must-revalidate',
                    'Expires': '0'
                }
            )
            
            print(f"Successfully uploaded: {s3_key}")
        
        return True
        
    except Exception as e:
        print(f"Error uploading: {e}")
        return False

if __name__ == "__main__":
    upload_main_files()