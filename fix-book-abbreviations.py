import os
import re

# Define the abbreviation mappings
abbreviations = {
    # Old Testament
    'Gen.': 'Genesis',
    'Ex.': 'Exodus', 
    'Exod.': 'Exodus',
    'Lev.': 'Leviticus',
    'Num.': 'Numbers',
    'Deut.': 'Deuteronomy',
    'Josh.': 'Joshua',
    'Jdgs.': 'Judges',
    'Judg.': 'Judges',

    'Ruth': 'Ruth',  # Already full
    '1 Sam.': '1 Samuel',
    '2 Sam.': '2 Samuel', 
    '1 Kings': '1 Kings',  # Already full
    '2 Kings': '2 Kings',  # Already full
    '1 Chr.': '1 Chronicles',
    '2 Chr.': '2 Chronicles',
    'Ezra': 'Ezra',  # Already full
    'Neh.': 'Nehemiah',
    'Est.': 'Esther',
    'Job': 'Job',  # Already full
    'Ps.': 'Psalms',
    'Prov.': 'Proverbs',
    'Eccl.': 'Ecclesiastes',
    'Songs': 'Song of Solomon',
    'Isa.': 'Isaiah',
    'Jer.': 'Jeremiah',
    'Lam.': 'Lamentations',
    'Ezek.': 'Ezekiel',
    'Dan.': 'Daniel',
    'Hos.': 'Hosea',
    'Joel': 'Joel',  # Already full
    'Amos': 'Amos',  # Already full
    'Obad.': 'Obadiah',
    'Jon.': 'Jonah',
    'Mic.': 'Micah',
    'Nah.': 'Nahum',
    'Hab.': 'Habakkuk',
    'Zeph.': 'Zephaniah',
    'Hag.': 'Haggai',
    'Zech.': 'Zechariah',
    'Mal.': 'Malachi',
    
    # New Testament
    'Matt.': 'Matthew',
    'Mark': 'Mark',  # Already full
    'Luke': 'Luke',  # Already full
    'John': 'John',  # Already full
    'Acts': 'Acts',  # Already full
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
    'Titus': 'Titus',  # Already full
    'Philem.': 'Philemon',
    'Heb.': 'Hebrews',
    'Jas.': 'James',
    'James': 'James',  # Already full
    '1 Pet.': '1 Peter',
    '2 Pet.': '2 Peter',
    '1 Jn.': '1 John',
    '2 Jn.': '2 John', 
    '3 Jn.': '3 John',
    '1 John': '1 John',  # Already full
    '2 John': '2 John',  # Already full
    '3 John': '3 John',  # Already full
    'Jude': 'Jude',  # Already full
    'Rev.': 'Revelation'
}

def fix_abbreviations_in_file(file_path):
    """Fix book abbreviations in a single HTML file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        changes_made = []
        
        # Fix abbreviations - sort by length (longest first) to avoid partial replacements
        sorted_abbrevs = sorted(abbreviations.items(), key=lambda x: len(x[0]), reverse=True)
        
        for abbrev, full_name in sorted_abbrevs:
            # Pattern to match abbreviations - handle numbers at start differently
            if abbrev[0].isdigit():
                # For abbreviations starting with numbers, use lookahead/lookbehind
                pattern = r'(?<!\w)' + re.escape(abbrev) + r'(?!\w)'
            else:
                # For regular abbreviations, use word boundaries
                pattern = r'\b' + re.escape(abbrev) + r'\b'
            
            matches = re.findall(pattern, content)
            if matches:
                content = re.sub(pattern, full_name, content)
                changes_made.append(f"{abbrev} -> {full_name} ({len(matches)} occurrences)")
        
        # Clean up trailing ampersands for weekend readings
        ampersand_pattern = r'\s*&\s*</h4>'
        if re.search(ampersand_pattern, content):
            content = re.sub(ampersand_pattern, '</h4>', content)
            changes_made.append("Removed trailing &")
        
        # Only write if changes were made
        if content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            return changes_made
        
        return []
        
    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        return []

def main():
    """Process all HTML files in the readings directory"""
    readings_dir = "readings"
    total_files = 0
    files_changed = 0
    corrected_files = []  # Track files that were corrected
    
    if not os.path.exists(readings_dir):
        print(f"Directory {readings_dir} not found!")
        return
    
    # Process each month directory
    for month_dir in os.listdir(readings_dir):
        month_path = os.path.join(readings_dir, month_dir)
        
        if not os.path.isdir(month_path):
            continue
            
        print(f"\nProcessing {month_dir}...")
        
        # Process each HTML file in the month
        for filename in sorted(os.listdir(month_path)):
            if filename.endswith('.html'):
                file_path = os.path.join(month_path, filename)
                total_files += 1
                
                changes = fix_abbreviations_in_file(file_path)
                
                if changes:
                    files_changed += 1
                    date_code = filename.replace('.html', '')
                    corrected_files.append(f'"{date_code}"')  # Format for Python list
                    print(f"  {filename}: {', '.join(changes)}")
    
    print(f"\nSummary:")
    print(f"Total files processed: {total_files}")
    print(f"Files changed: {files_changed}")
    
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