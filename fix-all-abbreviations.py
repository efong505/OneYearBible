import os
import re

# Comprehensive abbreviation mapping
abbreviations = {
    # Old Testament - all variants
    'Gen.': 'Genesis',
    'Ex.': 'Exodus',
    'Exod.': 'Exodus', 
    'Lev.': 'Leviticus',
    'Num.': 'Numbers',
    'Deut.': 'Deuteronomy',
    'Josh.': 'Joshua',
    'Judg.': 'Judges',
    'Jdgs.': 'Judges',
    'Ruth': 'Ruth',
    '1 Sam.': '1 Samuel',
    '2 Sam.': '2 Samuel', 
    '1 Kings': '1 Kings',
    '2 Kings': '2 Kings',
    '1 Kgs.': '1 Kings',
    '2 Kgs.': '2 Kings',
    '1 Chron.': '1 Chronicles',
    '2 Chron.': '2 Chronicles',
    '1 Chr.': '1 Chronicles',
    '2 Chr.': '2 Chronicles',
    'Ezra': 'Ezra',
    'Neh.': 'Nehemiah',
    'Esth.': 'Esther',
    'Est.': 'Esther',
    'Job': 'Job',
    'Ps.': 'Psalms',
    'Prov.': 'Proverbs',
    'Eccl.': 'Ecclesiastes',
    'Song of Solomon': 'Song of Solomon',  # Already full
    'Song': 'Song of Solomon',
    'Songs': 'Song of Solomon',
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
    'Jon.': 'Jonah',
    'Mic.': 'Micah',
    'Nah.': 'Nahum',
    'Hab.': 'Habakkuk',
    'Zeph.': 'Zephaniah',
    'Hag.': 'Haggai',
    'Zech.': 'Zechariah',
    'Mal.': 'Malachi',
    # New Testament - all variants
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
    'Jas.': 'James',
    'James': 'James',
    '1 Pet.': '1 Peter',
    '2 Pet.': '2 Peter',
    '1 Jn.': '1 John',
    '2 Jn.': '2 John',
    '3 Jn.': '3 John',
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
        changes_made = False
        
        # Fix abbreviations in h4 tags (reading titles)
        for abbrev, full_name in abbreviations.items():
            # Simple string replacement - safer than regex
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
    """Fix abbreviations in all HTML files"""
    print("Fixing abbreviations in all HTML files...")
    
    total_files = 0
    fixed_files = 0
    corrected_files = []  # Track files that were corrected
    
    # Process all HTML files in readings directory
    readings_dir = "readings"
    
    for month_dir in sorted(os.listdir(readings_dir)):
        month_path = os.path.join(readings_dir, month_dir)
        if not os.path.isdir(month_path):
            continue
            
        print(f"Processing {month_dir}...")
        
        for filename in sorted(os.listdir(month_path)):
            if filename.endswith('.html'):
                file_path = os.path.join(month_path, filename)
                total_files += 1
                
                changes_made = fix_abbreviations_in_file(file_path)
                if changes_made:
                    print(f"  Fixed: {filename}")
                    fixed_files += 1
                    date_code = filename.replace('.html', '')
                    corrected_files.append(f'"{date_code}"')  # Format for Python list
    
    print(f"\nSummary:")
    print(f"Total files processed: {total_files}")
    print(f"Files changed: {fixed_files}")
    
    # Print corrected files list for upload script
    if corrected_files:
        print(f"\n=== CORRECTED FILES LIST (for upload-corrected-html.py) ===")
        print(f"corrected_dates = [")
        for i, file_code in enumerate(corrected_files):
            if i == len(corrected_files) - 1:
                print(f"    {file_code}")
            else:
                print(f"    {file_code},")
        print(f"]")
        print(f"\nCopy the above list to update upload-corrected-html.py")

if __name__ == "__main__":
    main()