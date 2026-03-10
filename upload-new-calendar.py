import boto3

def upload_new_calendar():
    """Upload the new calendar file"""
    try:
        s3 = boto3.client('s3')
        bucket_name = 'one-year-bible-ekewaka'
        
        # Upload new calendar file
        s3.upload_file(
            'assets/js/calendar-new.js', 
            bucket_name, 
            'assets/js/calendar-new.js',
            ExtraArgs={'ContentType': 'application/javascript'}
        )
        
        print("Successfully uploaded calendar-new.js")
        return True
        
    except Exception as e:
        print(f"Error uploading: {e}")
        return False

if __name__ == "__main__":
    upload_new_calendar()