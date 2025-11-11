import boto3
import os

# List of dates that had abbreviation corrections
corrected_dates = [
   
    "1102",
    "1109",
    "1116",
    "1123",
    "1130",
    "1005",
    "1007",
    "1008",
    "1009",
    "1010",
    "1012",
    "1013",
    "1014",
    "1015",
    "1016",
    "1017",
    "1018",
    "1019",
    "1020",
    "1021",
    "1022",
    "1023",
    "1024",
    "1025",
    "1026",
    "1027",
    "1028",
    "1029",
    "1030",
    "1031",
    "0907",
    "0914",
    "0921"
]

def upload_to_s3(local_file, s3_key):
    """Upload file to S3"""
    try:
        s3 = boto3.client('s3')
        bucket_name = 'one-year-bible-ekewaka'
        
        s3.upload_file(
            local_file, 
            bucket_name, 
            s3_key,
            ExtraArgs={'ContentType': 'text/html'}
        )
        return True
        
    except Exception as e:
        print(f"  Error uploading to S3: {e}")
        return False

def get_month_name(date_code):
    """Convert date code to month name"""
    month_map = {
        '01': 'january', '02': 'february', '03': 'march', '04': 'april',
        '05': 'may', '06': 'june', '07': 'july', '08': 'august', 
        '09': 'september', '10': 'october', '11': 'november', '12': 'december'
    }
    month_num = date_code[:2]
    return month_map.get(month_num, 'unknown')

def main():
    """Upload all corrected HTML files to S3"""
    print("Uploading corrected HTML files to S3...")
    
    success_count = 0
    not_found_count = 0
    
    for date_code in corrected_dates:
        month_name = get_month_name(date_code)
        local_file = f"readings/{month_name}/{date_code}.html"
        
        if not os.path.exists(local_file):
            print(f"File {local_file} not found!")
            not_found_count += 1
            continue
        
        print(f"Uploading {date_code}.html from {month_name}...")
        
        # S3 key should match your website structure
        s3_key = f"readings/{month_name}/{date_code}.html"
        
        if upload_to_s3(local_file, s3_key):
            print(f"  Successfully uploaded: {s3_key}")
            success_count += 1
        else:
            print(f"  Failed to upload {date_code}.html")
    
    print(f"\nCompleted! Successfully uploaded {success_count}/{len(corrected_dates)} HTML files.")
    if not_found_count > 0:
        print(f"Files not found: {not_found_count}")

if __name__ == "__main__":
    main()