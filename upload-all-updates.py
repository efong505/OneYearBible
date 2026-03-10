import boto3
import os

def upload_all_updated_files():
    """Upload all files that were updated during this session"""
    try:
        s3 = boto3.client('s3')
        bucket_name = 'one-year-bible-ekewaka'
        
        uploaded_count = 0
        
        # Upload main files
        main_files = [
            ('index.html', 'index.html', 'text/html'),
            ('assets/js/calendar.js', 'assets/js/calendar.js', 'application/javascript')
        ]
        
        print("Uploading main files...")
        for local_file, s3_key, content_type in main_files:
            s3.upload_file(
                local_file,
                bucket_name,
                s3_key,
                ExtraArgs={'ContentType': content_type}
            )
            print(f"  Uploaded: {s3_key}")
            uploaded_count += 1
        
        # Upload all reading pages (with updated branding and calendar.js version)
        print("\nUploading reading pages...")
        readings_dir = "readings"
        
        for month_dir in os.listdir(readings_dir):
            month_path = os.path.join(readings_dir, month_dir)
            if os.path.isdir(month_path):
                print(f"  Uploading {month_dir}...")
                
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
        
        print(f"\nTotal files uploaded: {uploaded_count}")
        print("\nAll updated files have been uploaded to S3!")
        print("Changes include:")
        print("- Fixed calendar year display issue")
        print("- Updated personal branding on all reading pages")
        print("- Calendar.js version 8 with URL parameter support")
        
        return True
        
    except Exception as e:
        print(f"Error uploading: {e}")
        return False

if __name__ == "__main__":
    upload_all_updated_files()