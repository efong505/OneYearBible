import boto3
import os

# List of dates that had abbreviation corrections
corrected_dates = [
    "0405",
    "0406",
    "0412",
    "0413",
    "0419",
    "0420",
    "0426",
    "0427",
    "0803",
    "0810",
    "0817",
    "0824",
    "0831",
    "1207",
    "1214",
    "1221",
    "1228",
    "0201",
    "0202",
    "0209",
    "0216",
    "0223",
    "0105",
    "0112",
    "0119",
    "0126",
    "0706",
    "0713",
    "0720",
    "0727",
    "0601",
    "0608",
    "0615",
    "0622",
    "0629",
    "0302",
    "0309",
    "0316",
    "0323",
    "0330",
    "0504",
    "0511",
    "0518",
    "0525",
    "1102",
    "1109",
    "1116",
    "1123",
    "1130",
    "1005",
    "1012",
    "1019",
    "1026",
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