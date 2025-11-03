import os
import re

# Target files and their replacements
files_to_fix = [
    "readings/august/0816.html",
    "readings/august/0817.html", 
    "readings/august/0818.html",
    "readings/august/0819.html",
    "readings/august/0820.html",
    "readings/august/0821.html",
    "readings/august/0822.html",
    "readings/august/0823.html",
    "readings/august/0824.html",
    "readings/august/0825.html",
    "readings/august/0826.html"
]

abbreviations = {
    'Neh.': 'Nehemiah',
    'Gal.': 'Galatians'
}

for file_path in files_to_fix:
    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        changes = []
        
        for abbrev, full_name in abbreviations.items():
            pattern = r'\b' + re.escape(abbrev) + r'\b'
            matches = re.findall(pattern, content)
            if matches:
                content = re.sub(pattern, full_name, content)
                changes.append(f"{abbrev} -> {full_name} ({len(matches)} occurrences)")
        
        if content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"{file_path}: {', '.join(changes)}")
        else:
            print(f"{file_path}: No changes needed")
    else:
        print(f"{file_path}: File not found")