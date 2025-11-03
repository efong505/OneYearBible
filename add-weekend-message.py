#!/usr/bin/env python3
import os
import re
import glob
from datetime import datetime, date

def is_weekend(date_code):
    """Check if a date code represents a weekend (Saturday or Sunday)"""
    try:
        month = int(date_code[:2])
        day = int(date_code[2:])
        # Use 2025 as the year
        date_obj = date(2025, month, day)
        # 5 = Saturday, 6 = Sunday
        return date_obj.weekday() in [5, 6]
    except:
        return False

def add_weekend_message_to_file(file_path):
    """Add 'No New Testament Reading Scheduled' message to weekend files"""
    # Extract date code from filename
    filename = os.path.basename(file_path)
    date_code = filename.replace('.html', '')
    
    if not re.match(r'^\d{4}$', date_code):
        return False
    
    # Check if it's a weekend
    if not is_weekend(date_code):
        print(f"Skipping {filename} - not a weekend")
        return False
    
    # Read file content
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        return False
    
    # Check if New Testament tab already has the message
    if '* No New Testament Reading Scheduled *' in content:
        print(f"Skipping {filename} - already has weekend message")
        return False
    
    # Find the New Testament tab pane and check if it's empty or needs the message
    nt_pattern = r'(<div class="tab-pane fade" id="new\d+" role="tabpanel"[^>]*>)(.*?)(</div>)'
    match = re.search(nt_pattern, content, re.DOTALL)
    
    if match:
        opening_tag = match.group(1)
        tab_content = match.group(2).strip()
        closing_tag = match.group(3)
        
        # Check if tab is empty, only has comments, or only has empty h2 tags
        if (not tab_content or 
            re.match(r'^\s*<!--.*-->\s*$', tab_content, re.DOTALL) or
            re.match(r'^\s*<h2>\s*</h2>\s*$', tab_content, re.DOTALL)):
            # Replace with weekend message
            new_content = f'{opening_tag}\n                            <h2>New Testament</h2>\n                            <h5 class="mt-2">* No New Testament Reading Scheduled *</h5>\n                        {closing_tag}'
            content = content.replace(match.group(0), new_content)
            
            # Write back to file
            try:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                print(f"Added weekend message to {filename}")
                return True
            except Exception as e:
                print(f"Error writing {file_path}: {e}")
                return False
    
    print(f"No changes needed for {filename}")
    return False

def main():
    """Add weekend messages to all weekend HTML files"""
    base_dir = "c:/Users/Ed/Documents/Post Graduation/Projects/OneYearBible"
    readings_dir = os.path.join(base_dir, "readings")
    
    if not os.path.exists(readings_dir):
        print(f"Readings directory not found: {readings_dir}")
        return
    
    # Process all months
    months = ['september', 'october', 'november', 'december', 'january', 'february', 'march', 'april', 'may', 'june', 'july', 'august']
    
    updated_count = 0
    
    for month in months:
        month_dir = os.path.join(readings_dir, month)
        if not os.path.exists(month_dir):
            continue
        
        # Get all HTML files in month directory
        html_files = glob.glob(os.path.join(month_dir, "*.html"))
        
        for html_file in html_files:
            if add_weekend_message_to_file(html_file):
                updated_count += 1
    
    print(f"\nAdded weekend messages to {updated_count} files")
    print("All weekend files now have 'No New Testament Reading Scheduled' message!")

if __name__ == "__main__":
    main()