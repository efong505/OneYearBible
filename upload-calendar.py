import boto3

def upload_calendar_js():
    """Upload the fixed calendar.js file to S3"""
    try:
        s3 = boto3.client('s3')
        bucket_name = 'one-year-bible-ekewaka'
        
        local_file = 'assets/js/calendar.js'
        s3_key = 'assets/js/calendar.js'
        
        print(f"Uploading {local_file} to S3...")
        
        s3.upload_file(
            local_file, 
            bucket_name, 
            s3_key,
            ExtraArgs={'ContentType': 'application/javascript'}
        )
        
        print(f"Successfully uploaded: {s3_key}")
        return True
        
    except Exception as e:
        print(f"Error uploading: {e}")
        return False

if __name__ == "__main__":
    upload_calendar_js()