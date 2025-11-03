import os
import re

# Book abbreviation mappings
abbreviations = {
    '1 Kgs.': '1 Kings',
    '2 Kgs.': '2 Kings', 
    '1 Chr.': '1 Chronicles',
    '2 Chr.': '2 Chronicles',
    'Neh.': 'Nehemiah',
    'Est.': 'Esther',
    'Ps.': 'Psalms',
    'Prov.': 'Proverbs',
    'Eccl.': 'Ecclesiastes',
    'Song': 'Song of Solomon',
    'Isa.': 'Isaiah',
    'Jer.': 'Jeremiah',
    'Lam.': 'Lamentations',
    'Ezek.': 'Ezekiel',
    'Dan.': 'Daniel',
    'Hos.': 'Hosea',
    'Joel': 'Joel',
    'Amos': 'Amos',
    'Obad.': 'Obadiah',
    'Jonah': 'Jonah',
    'Mic.': 'Micah',
    'Nah.': 'Nahum',
    'Hab.': 'Habakkuk',
    'Zeph.': 'Zephaniah',
    'Hag.': 'Haggai',
    'Zech.': 'Zechariah',
    'Mal.': 'Malachi',
    'Matt.': 'Matthew',
    'Mark': 'Mark',
    'Luke': 'Luke',
    'John': 'John',
    'Acts': 'Acts',
    'Rom.': 'Romans',
    '1 Cor.': '1 Corinthians',
    '2 Cor.': '2 Corinthians',
    'Gal.': 'Galatians',
    'Eph.': 'Ephesians',
    'Phil.': 'Philippians',
    'Col.': 'Colossians',
    '1 Thess.': '1 Thessalonians',
    '2 Thess.': '2 Thessalonians',
    '1 Tim.': '1 Timothy',
    '2 Tim.': '2 Timothy',
    'Titus': 'Titus',
    'Philem.': 'Philemon',
    'Heb.': 'Hebrews',
    'James': 'James',
    '1 Pet.': '1 Peter',
    '2 Pet.': '2 Peter',
    '1 John': '1 John',
    '2 John': '2 John',
    '3 John': '3 John',
    'Jude': 'Jude',
    'Rev.': 'Revelation'
}

def fix_abbreviations_in_file(file_path):
    """Fix abbreviations in a single HTML file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        changes_made = []
        
        # Fix abbreviations in h4 tags and h2 tags
        for abbrev, full_name in abbreviations.items():
            if abbrev in content:
                content = content.replace(abbrev, full_name)
                changes_made.append(f"{abbrev} -> {full_name}")
        
        if changes_made:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            return changes_made
        
        return None
        
    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        return None

def main():
    """Find and fix all remaining abbreviations"""
    print("Scanning for remaining book abbreviations...")
    
    months = ['january', 'february', 'march', 'april', 'may', 'june', 
              'july', 'august', 'september', 'october', 'november', 'december']
    
    fixed_files = []
    
    for month in months:
        month_dir = f"readings/{month}"
        if os.path.exists(month_dir):
            for file in os.listdir(month_dir):
                if file.endswith('.html'):
                    file_path = os.path.join(month_dir, file)
                    changes = fix_abbreviations_in_file(file_path)
                    
                    if changes:
                        date_code = file.replace('.html', '')
                        print(f"\nFixed {date_code} ({month}):")
                        for change in changes:
                            print(f"  {change}")
                        fixed_files.append((date_code, month))
    
    print(f"\nCompleted! Fixed {len(fixed_files)} files.")
    
    if fixed_files:
        print("\nFiles that need audio regeneration:")
        for date_code, month in fixed_files:
            print(f"  {date_code} ({month})")

if __name__ == "__main__":
    main()