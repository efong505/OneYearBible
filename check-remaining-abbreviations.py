import os
import re

# Common abbreviations to check for
abbreviations_to_check = [
    'Gen.', 'Ex.', 'Exod.', 'Lev.', 'Num.', 'Deut.', 'Josh.', 'Judg.', 'Jdgs.',
    '1 Sam.', '2 Sam.', '1 Kgs.', '2 Kgs.', '1 Chr.', '2 Chr.', 'Neh.', 'Est.', 'Esth.',
    'Ps.', 'Prov.', 'Eccl.', 'Song', 'Songs', 'Isa.', 'Jer.', 'Lam.', 'Ezek.', 'Dan.',
    'Hos.', 'Obad.', 'Jon.', 'Mic.', 'Nah.', 'Hab.', 'Zeph.', 'Hag.', 'Zech.', 'Mal.',
    'Matt.', 'Rom.', '1 Cor.', '2 Cor.', 'Gal.', 'Eph.', 'Phil.', 'Col.',
    '1 Thess.', '2 Thess.', '1 Tim.', '2 Tim.', 'Philem.', 'Heb.', 'Jas.',
    '1 Pet.', '2 Pet.', '1 Jn.', '2 Jn.', '3 Jn.', 'Rev.'
]

def check_file_for_abbreviations(file_path):
    """Check if file contains any abbreviations"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        found_abbrevs = []
        for abbrev in abbreviations_to_check:
            if abbrev == 'Song':
                # Special case: only flag if "Song" appears without "of Solomon" after it
                import re
                if re.search(r'\bSong\b(?!\s+of\s+Solomon)', content):
                    found_abbrevs.append(abbrev)
            elif abbrev in content:
                found_abbrevs.append(abbrev)
        
        return found_abbrevs
        
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        return []

def main():
    """Check all files for remaining abbreviations"""
    print("Checking for remaining abbreviations...")
    
    files_with_abbrevs = []
    readings_dir = "readings"
    
    for month_dir in sorted(os.listdir(readings_dir)):
        month_path = os.path.join(readings_dir, month_dir)
        if not os.path.isdir(month_path):
            continue
            
        for filename in sorted(os.listdir(month_path)):
            if filename.endswith('.html'):
                file_path = os.path.join(month_path, filename)
                abbrevs = check_file_for_abbreviations(file_path)
                
                if abbrevs:
                    date_code = filename.replace('.html', '')
                    files_with_abbrevs.append(date_code)
                    print(f"{date_code} ({month_dir}): {', '.join(abbrevs)}")
    
    print(f"\nFound {len(files_with_abbrevs)} files with abbreviations:")
    if files_with_abbrevs:
        print("Files to fix:", files_with_abbrevs)
    else:
        print("All files are clean!")

if __name__ == "__main__":
    main()