import os
import re

def find_sunday_abbreviations():
    """Find all Sunday files with Ps. and Prov. abbreviations"""
    sunday_files = []
    readings_dir = "readings"
    
    for month_dir in sorted(os.listdir(readings_dir)):
        month_path = os.path.join(readings_dir, month_dir)
        if not os.path.isdir(month_path):
            continue
            
        for filename in sorted(os.listdir(month_path)):
            if filename.endswith('.html'):
                file_path = os.path.join(month_path, filename)
                
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    # Check if it's a Sunday (look for "Sunday" in the content)
                    if 'Sunday' in content:
                        # Check for Ps. or Prov. abbreviations
                        if 'Ps.' in content or 'Prov.' in content:
                            date_code = filename.replace('.html', '')
                            sunday_files.append(date_code)
                            print(f"Found Sunday with abbreviations: {date_code} ({month_dir})")
                            
                            # Show what abbreviations were found
                            abbrevs = []
                            if 'Ps.' in content:
                                abbrevs.append('Ps.')
                            if 'Prov.' in content:
                                abbrevs.append('Prov.')
                            print(f"  Contains: {', '.join(abbrevs)}")
                
                except Exception as e:
                    print(f"Error reading {file_path}: {e}")
    
    return sunday_files

def main():
    print("Finding Sunday files with Ps. and Prov. abbreviations...")
    sunday_files = find_sunday_abbreviations()
    
    print(f"\nFound {len(sunday_files)} Sunday files with abbreviations:")
    print("Sunday files to fix:", sunday_files)

if __name__ == "__main__":
    main()