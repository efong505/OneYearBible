import os

# Files that need Song -> Song of Solomon fix
files_to_fix = ['0919', '0920', '0922']

def fix_song_abbreviation(file_path):
    """Fix Song abbreviation in a single file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Replace "Song" with "Song of Solomon" but be careful not to replace "Song of Solomon"
        if 'Song' in content and 'Song of Solomon' not in content:
            content = content.replace('Song', 'Song of Solomon')
            
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            return True
        elif 'Song' in content:
            # More careful replacement - only replace standalone "Song"
            import re
            pattern = r'\bSong\b(?!\s+of\s+Solomon)'
            if re.search(pattern, content):
                content = re.sub(pattern, 'Song of Solomon', content)
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                return True
        
        return False
        
    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        return False

def main():
    """Fix Song abbreviations in specific files"""
    print("Fixing Song abbreviations...")
    
    fixed_count = 0
    
    for date_code in files_to_fix:
        month_name = 'september'  # All 3 files are in September
        file_path = f"readings/{month_name}/{date_code}.html"
        
        if os.path.exists(file_path):
            if fix_song_abbreviation(file_path):
                print(f"Fixed: {date_code}.html")
                fixed_count += 1
            else:
                print(f"No changes needed: {date_code}.html")
        else:
            print(f"File not found: {file_path}")
    
    print(f"\nFixed {fixed_count} files.")

if __name__ == "__main__":
    main()