import os
import re

# Files that have the cascade issue
files_to_fix = ['0919', '0920', '0922']

def fix_song_cascade(file_path):
    """Fix the cascading Song of Solomon issue"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # Fix the cascade: "Song of Solomon of Solomon..." -> "Song of Solomon"
        pattern = r'Song of Solomon(?: of Solomon)+'
        content = re.sub(pattern, 'Song of Solomon', content)
        
        if content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            return True
        
        return False
        
    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        return False

def main():
    """Fix cascading Song of Solomon issues"""
    print("Fixing cascading Song of Solomon issues...")
    
    fixed_count = 0
    
    for date_code in files_to_fix:
        month_name = 'september'
        file_path = f"readings/{month_name}/{date_code}.html"
        
        if os.path.exists(file_path):
            if fix_song_cascade(file_path):
                print(f"Fixed cascade in: {date_code}.html")
                fixed_count += 1
            else:
                print(f"No cascade found: {date_code}.html")
        else:
            print(f"File not found: {file_path}")
    
    print(f"\nFixed {fixed_count} files.")

if __name__ == "__main__":
    main()