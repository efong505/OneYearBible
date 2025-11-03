import boto3
import re
from datetime import datetime

def auto_rename_audio_files():
    """Automatically rename Polly audio files to MMDD.mp3 format"""
    s3 = boto3.client('s3')
    bucket_name = 'one-year-bible-ekewaka'
    
    print("Auto-renaming Polly audio files...")
    
    # Expected date codes for each month
    month_dates = {
        'january': [f"{i:02d}01" for i in range(1, 32)],
        'february': [f"{i:02d}02" for i in range(1, 29)],  # 2025 not leap year
        'march': [f"{i:02d}03" for i in range(1, 32)],
        'april': [f"{i:02d}04" for i in range(1, 31)],
        'may': [f"{i:02d}05" for i in range(1, 32)],
        'june': [f"{i:02d}06" for i in range(1, 31)],
        'july': [f"{i:02d}07" for i in range(1, 32)],
        'august': [f"{i:02d}08" for i in range(1, 32)],
        'september': [f"{i:02d}09" for i in range(1, 31)],
        'october': [f"{i:02d}10" for i in range(1, 32)],
        'november': [f"{i:02d}11" for i in range(1, 31)],
        'december': [f"{i:02d}12" for i in range(1, 32)]
    }
    
    renamed_count = 0
    
    try:
        # Process each month
        for month, date_codes in month_dates.items():
            print(f"\nProcessing {month}...")
            
            # List files in this month's folder
            response = s3.list_objects_v2(
                Bucket=bucket_name,
                Prefix=f'2025/{month}/'
            )
            
            if 'Contents' not in response:
                print(f"  No files found in 2025/{month}/")
                continue
            
            # Get all mp3 files, sorted by creation time
            mp3_files = []
            for obj in response['Contents']:
                if obj['Key'].endswith('.mp3'):
                    mp3_files.append({
                        'key': obj['Key'],
                        'modified': obj['LastModified']
                    })
            
            # Sort by creation time (oldest first)
            mp3_files.sort(key=lambda x: x['modified'])
            
            # Rename files to match expected date codes
            for i, file_info in enumerate(mp3_files):
                old_key = file_info['key']
                
                # Skip if already in correct format
                if re.match(r'2025/\w+/\d{4}\.mp3$', old_key):
                    print(f"  Already correct: {old_key}")
                    continue
                
                # Get the expected date code for this position
                if i < len(date_codes):
                    expected_date = date_codes[i]
                    new_key = f'2025/{month}/{expected_date}.mp3'
                    
                    try:
                        # Copy to new name
                        s3.copy_object(
                            Bucket=bucket_name,
                            CopySource={'Bucket': bucket_name, 'Key': old_key},
                            Key=new_key
                        )
                        
                        # Delete old file
                        s3.delete_object(Bucket=bucket_name, Key=old_key)
                        
                        print(f"  Renamed: {old_key} -> {new_key}")
                        renamed_count += 1
                        
                    except Exception as e:
                        print(f"  Error renaming {old_key}: {e}")
                else:
                    print(f"  Extra file (no date code): {old_key}")
    
    except Exception as e:
        print(f"Error: {e}")
    
    print(f"\nCompleted! Renamed {renamed_count} files.")

if __name__ == "__main__":
    auto_rename_audio_files()