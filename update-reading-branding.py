import os
import re

def update_reading_pages_branding():
    """Remove KCM references and update branding in all reading pages"""
    
    readings_dir = "readings"
    updated_count = 0
    
    # Walk through all month directories
    for month_dir in os.listdir(readings_dir):
        month_path = os.path.join(readings_dir, month_dir)
        if os.path.isdir(month_path):
            print(f"Processing {month_dir}...")
            
            # Process all HTML files in the month directory
            for filename in os.listdir(month_path):
                if filename.endswith('.html'):
                    file_path = os.path.join(month_path, filename)
                    
                    # Read the file
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    # Remove KCM image and update title
                    content = re.sub(r'<img src="../../assets/images/KCMCenterlineWebUse4ColorBlackText\.png"[^>]*>', '', content)
                    content = re.sub(r'<title>Kenneth Copeland One Year Bible Reading</title>', '<title>One Year Bible Reading</title>', content)
                    
                    # Update calendar.js reference
                    content = re.sub(r'<script src="../../assets/js/calendar\.js(\?v=\d+)?"></script>', '<script src="../../assets/js/calendar.js?v=7"></script>', content)
                    
                    # Write back to file
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(content)
                    
                    updated_count += 1
    
    print(f"\nUpdated {updated_count} reading pages")
    return updated_count

if __name__ == "__main__":
    update_reading_pages_branding()