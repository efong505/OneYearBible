#!/usr/bin/env python3
import os
import re
import glob

def get_month_name(month_num):
    """Convert month number to name"""
    months = ['january', 'february', 'march', 'april', 'may', 'june',
              'july', 'august', 'september', 'october', 'november', 'december']
    return months[month_num - 1]

def fix_audio_path_in_file(file_path):
    """Fix audio source path in a single HTML file"""
    # Extract date code from filename
    filename = os.path.basename(file_path)
    date_code = filename.replace('.html', '')
    
    if not re.match(r'^\d{4}$', date_code):
        print(f"Skipping {filename} - not a date file")
        return False
    
    # Skip September 18-26 (already correct)
    if date_code in ['0918', '0919', '0920', '0921', '0922', '0923', '0924', '0925', '0926']:
        print(f"Skipping {filename} - already correct")
        return False
    
    # Parse date
    month_num = int(date_code[:2])
    day_num = int(date_code[2:])
    month_name = get_month_name(month_num)
    
    # Read file content
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        return False
    
    # Find and replace audio source paths
    # Pattern matches various incorrect formats
    old_patterns = [
        rf'https://d24muyyuu3zj8g\.cloudfront\.net/2025/\w+/\d+/\w+\.mp3',
        rf'https://d24muyyuu3zj8g\.cloudfront\.net/temp\.mp3'
    ]
    
    # Correct path
    new_path = f"https://d24muyyuu3zj8g.cloudfront.net/2025/{month_name.lower()}/{date_code}.mp3"
    
    updated = False
    for pattern in old_patterns:
        if re.search(pattern, content):
            content = re.sub(pattern, new_path, content)
            updated = True
    
    # Also handle cases where there might be commented out sources
    # Look for source tags and update them
    source_pattern = r'<source src="[^"]*" type="audio/mpeg">'
    if re.search(source_pattern, content):
        new_source = f'<source src="{new_path}" type="audio/mpeg">'
        content = re.sub(source_pattern, new_source, content)
        updated = True
    
    if updated:
        # Write back to file
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"Fixed audio path in {filename}")
            return True
        except Exception as e:
            print(f"Error writing {file_path}: {e}")
            return False
    else:
        print(f"No audio path found to fix in {filename}")
        return False

def main():
    """Fix audio paths in all HTML files"""
    base_dir = "c:/Users/Ed/Documents/Post Graduation/Projects/OneYearBible"
    readings_dir = os.path.join(base_dir, "readings")
    
    if not os.path.exists(readings_dir):
        print(f"Readings directory not found: {readings_dir}")
        return
    
    # Process all months
    months = ['september', 'october', 'november', 'december', 'january', 'february', 'march', 'april', 'may', 'june', 'july', 'august']
    
    fixed_count = 0
    
    for month in months:
        month_dir = os.path.join(readings_dir, month)
        if not os.path.exists(month_dir):
            print(f"Month directory not found: {month_dir}")
            continue
        
        # Get all HTML files in month directory
        html_files = glob.glob(os.path.join(month_dir, "*.html"))
        
        for html_file in html_files:
            if fix_audio_path_in_file(html_file):
                fixed_count += 1
    
    print(f"\nFixed audio paths in {fixed_count} files")
    print("All HTML files now have correct audio source paths!")

if __name__ == "__main__":
    main()