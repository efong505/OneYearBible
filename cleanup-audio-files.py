import boto3
import re
from datetime import datetime

def get_all_dates():
    """Get all expected date codes and months"""
    months = ['january', 'february', 'march', 'april', 'may', 'june', 
              'july', 'august', 'september', 'october', 'november', 'december']
    
    all_dates = []
    for month in months:
        if month == 'january':
            days = range(1, 32)
        elif month == 'february':
            days = range(1, 29)  # 2025 is not a leap year
        elif month in ['april', 'june', 'september', 'november']:
            days = range(1, 31)
        else:
            days = range(1, 32)
        
        for day in days:
            date_code = f"{day:02d}{['', '01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12'][['', 'january', 'february', 'march', 'april', 'may', 'june', 'july', 'august', 'september', 'october', 'november', 'december'].index(month)]}"
            all_dates.append((date_code, month))
    
    return all_dates

def cleanup_s3_audio_files():
    """Find and rename all Polly-generated audio files to correct format"""
    s3 = boto3.client('s3')
    bucket_name = 'one-year-bible-ekewaka'
    
    print("Scanning S3 bucket for audio files to rename...")
    
    # Get all expected dates
    all_dates = get_all_dates()
    date_to_month = {date_code: month for date_code, month in all_dates}
    
    renamed_count = 0
    found_count = 0
    
    try:
        # List all objects in the bucket
        paginator = s3.get_paginator('list_objects_v2')
        pages = paginator.paginate(Bucket=bucket_name, Prefix='2025/')
        
        for page in pages:
            if 'Contents' not in page:
                continue
                
            for obj in page['Contents']:
                key = obj['Key']
                
                # Skip files that are already in correct format
                if re.match(r'2025/\w+/\d{4}\.mp3$', key):
                    continue
                
                # Look for Polly-generated files (usually have task IDs or timestamps)
                if key.endswith('.mp3') and '2025/' in key:
                    found_count += 1
                    print(f"Found audio file: {key}")
                    
                    # Try to determine which date this belongs to based on creation time or prefix
                    # For now, we'll need to match based on the month folder
                    parts = key.split('/')
                    if len(parts) >= 3:
                        year = parts[0]  # 2025
                        month = parts[1]  # january, february, etc.
                        
                        # Find the corresponding date code for this month
                        # This is a simplified approach - you might need to match based on creation time
                        month_dates = [date_code for date_code, m in all_dates if m == month]
                        
                        if month_dates:
                            # For now, let's just list what we found and let user decide
                            print(f"  Month: {month}")
                            print(f"  Available dates for {month}: {month_dates[:5]}...")  # Show first 5
                            print(f"  Manual rename needed: {key}")
                            print()
    
    except Exception as e:
        print(f"Error scanning bucket: {e}")
    
    print(f"Found {found_count} audio files that may need renaming")
    print("Since automatic matching is complex, here's a manual approach:")
    print("1. Check the creation timestamps of files")
    print("2. Match them to the order of date processing")
    print("3. Use AWS CLI or console to rename them")

def list_files_by_month():
    """List all audio files organized by month for easier manual renaming"""
    s3 = boto3.client('s3')
    bucket_name = 'one-year-bible-ekewaka'
    
    print("Listing all audio files by month:")
    print("=" * 50)
    
    try:
        paginator = s3.get_paginator('list_objects_v2')
        pages = paginator.paginate(Bucket=bucket_name, Prefix='2025/')
        
        files_by_month = {}
        
        for page in pages:
            if 'Contents' not in page:
                continue
                
            for obj in page['Contents']:
                key = obj['Key']
                if key.endswith('.mp3'):
                    parts = key.split('/')
                    if len(parts) >= 2:
                        month = parts[1]
                        if month not in files_by_month:
                            files_by_month[month] = []
                        files_by_month[month].append({
                            'key': key,
                            'modified': obj['LastModified'],
                            'size': obj['Size']
                        })
        
        for month in sorted(files_by_month.keys()):
            print(f"\n{month.upper()}:")
            files = sorted(files_by_month[month], key=lambda x: x['modified'])
            for i, file_info in enumerate(files, 1):
                print(f"  {i:2d}. {file_info['key']} ({file_info['size']} bytes, {file_info['modified']})")
    
    except Exception as e:
        print(f"Error listing files: {e}")

if __name__ == "__main__":
    print("Audio File Cleanup Utility")
    print("=" * 30)
    
    choice = input("Choose option:\n1. Scan for files to rename\n2. List files by month\nEnter 1 or 2: ")
    
    if choice == "1":
        cleanup_s3_audio_files()
    elif choice == "2":
        list_files_by_month()
    else:
        print("Invalid choice")