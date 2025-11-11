import os

# October dates 13-30 that need abbreviation fixes
october_dates = [
    "1013", "1014", "1015", "1016", "1017", "1018", "1019", "1020", 
    "1021", "1022", "1023", "1024", "1025", "1026", "1027", "1028", 
    "1029", "1030"
]

# Abbreviation mappings
abbreviations = {
    'Gen.': 'Genesis', 'Ex.': 'Exodus', 'Exod.': 'Exodus', 'Lev.': 'Leviticus',
    'Num.': 'Numbers', 'Deut.': 'Deuteronomy', 'Josh.': 'Joshua', 'Judg.': 'Judges',
    'Jdgs.': 'Judges', '1 Sam.': '1 Samuel', '2 Sam.': '2 Samuel', '1 Kgs.': '1 Kings',
    '2 Kgs.': '2 Kings', '1 Chr.': '1 Chronicles', '2 Chr.': '2 Chronicles',
    'Neh.': 'Nehemiah', 'Est.': 'Esther', 'Esth.': 'Esther', 'Ps.': 'Psalms',
    'Prov.': 'Proverbs', 'Eccl.': 'Ecclesiastes', 'Song': 'Song of Solomon',
    'Songs': 'Song of Solomon', 'Isa.': 'Isaiah', 'Jer.': 'Jeremiah',
    'Lam.': 'Lamentations', 'Ezek.': 'Ezekiel', 'Dan.': 'Daniel', 'Hos.': 'Hosea',
    'Obad.': 'Obadiah', 'Jon.': 'Jonah', 'Mic.': 'Micah', 'Nah.': 'Nahum',
    'Hab.': 'Habakkuk', 'Zeph.': 'Zephaniah', 'Hag.': 'Haggai', 'Zech.': 'Zechariah',
    'Mal.': 'Malachi', 'Matt.': 'Matthew', 'Rom.': 'Romans', '1 Cor.': '1 Corinthians',
    '2 Cor.': '2 Corinthians', 'Gal.': 'Galatians', 'Eph.': 'Ephesians',
    'Phil.': 'Philippians', 'Col.': 'Colossians', '1 Thess.': '1 Thessalonians',
    '2 Thess.': '2 Thessalonians', '1 Tim.': '1 Timothy', '2 Tim.': '2 Timothy',
    'Philem.': 'Philemon', 'Heb.': 'Hebrews', 'Jas.': 'James', '1 Pet.': '1 Peter',
    '2 Pet.': '2 Peter', '1 Jn.': '1 John', '2 Jn.': '2 John', '3 Jn.': '3 John',
    'Rev.': 'Revelation'
}

def fix_abbreviations_in_file(file_path):
    """Fix abbreviations in a single file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        changes_made = False
        
        # Fix abbreviations
        for abbrev, full_name in abbreviations.items():
            if abbrev in content:
                content = content.replace(abbrev, full_name)
                changes_made = True
        
        if changes_made:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            return True
        
        return False
        
    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        return False

def main():
    """Fix abbreviations in October 13-30 files"""
    print("Fixing abbreviations in October 13-30 files...")
    
    fixed_count = 0
    
    for date_code in october_dates:
        file_path = f"readings/october/{date_code}.html"
        
        if os.path.exists(file_path):
            if fix_abbreviations_in_file(file_path):
                print(f"Fixed: {date_code}.html")
                fixed_count += 1
            else:
                print(f"No changes needed: {date_code}.html")
        else:
            print(f"File not found: {file_path}")
    
    print(f"\nFixed {fixed_count} files.")
    
    # Also add 1102 since it was manually updated
    print("\nFiles to upload:")
    upload_list = october_dates + ["1102"]
    for date in upload_list:
        print(f'    "{date}",')

if __name__ == "__main__":
    main()