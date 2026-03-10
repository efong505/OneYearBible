import boto3
import os

def upload_all_readings():
    """Upload all reading pages to S3"""
    try:
        s3 = boto3.client('s3')
        bucket_name = 'one-year-bible-ekewaka'
        
        readings_dir = "readings"
        uploaded_count = 0
        
        # Walk through all month directories
        for month_dir in os.listdir(readings_dir):
            month_path = os.path.join(readings_dir, month_dir)
            if os.path.isdir(month_path):
                print(f"Uploading {month_dir}...")
                
                # Upload all HTML files in the month directory
                for filename in os.listdir(month_path):
                    if filename.endswith('.html'):
                        local_file = os.path.join(month_path, filename)
                        s3_key = f"readings/{month_dir}/{filename}"
                        
                        s3.upload_file(
                            local_file,
                            bucket_name,
                            s3_key,
                            ExtraArgs={'ContentType': 'text/html'}
                        )
                        
                        uploaded_count += 1
        
        print(f"\nUploaded {uploaded_count} reading pages")
        return True
        
    except Exception as e:
        print(f"Error uploading: {e}")
        return False

if __name__ == "__main__":
    upload_all_readings()