import boto3
import time

def upload_versioned_calendar():
    """Upload calendar.js with cache-busting and versioned filename"""
    try:
        s3 = boto3.client('s3')
        bucket_name = 'one-year-bible-ekewaka'
        
        # Upload with timestamp to force refresh
        timestamp = str(int(time.time()))
        
        # Upload the original file with cache-busting headers
        s3.upload_file(
            'assets/js/calendar.js', 
            bucket_name, 
            'assets/js/calendar.js',
            ExtraArgs={
                'ContentType': 'application/javascript',
                'CacheControl': 'no-cache, no-store, must-revalidate',
                'Expires': '0'
            }
        )
        
        print(f"Successfully uploaded calendar.js with cache-busting headers")
        
        # Also upload with versioned name as backup
        s3.upload_file(
            'assets/js/calendar.js', 
            bucket_name, 
            f'assets/js/calendar-{timestamp}.js',
            ExtraArgs={'ContentType': 'application/javascript'}
        )
        
        print(f"Also uploaded versioned file: calendar-{timestamp}.js")
        return True
        
    except Exception as e:
        print(f"Error uploading: {e}")
        return False

if __name__ == "__main__":
    upload_versioned_calendar()