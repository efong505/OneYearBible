import boto3
import time

def force_upload_calendar():
    """Force upload calendar.js with maximum cache busting"""
    try:
        s3 = boto3.client('s3')
        bucket_name = 'one-year-bible-ekewaka'
        
        # Upload with maximum cache busting
        s3.upload_file(
            'assets/js/calendar.js', 
            bucket_name, 
            'assets/js/calendar.js',
            ExtraArgs={
                'ContentType': 'application/javascript',
                'CacheControl': 'no-cache, no-store, must-revalidate, max-age=0',
                'Expires': 'Thu, 01 Jan 1970 00:00:00 GMT'
            }
        )
        
        print("Successfully force uploaded calendar.js")
        return True
        
    except Exception as e:
        print(f"Error uploading: {e}")
        return False

if __name__ == "__main__":
    force_upload_calendar()