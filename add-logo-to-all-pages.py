import os
import re

def add_logo_to_reading_page(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check if logo already exists
    if 'BibleReadingPlanLogo.png' in content:
        return False
    
    # Find the pattern and add logo
    pattern = r'(<h1 class="display-3 mb-2">One Year Bible Reading Plan</h1>)'
    replacement = r'\1\n            <div class="text-center mb-4">\n                <img src="../../BibleReadingPlanLogo.png" alt="Logo" class="img-fluid" style="max-height: 200px;">\n            </div>'
    
    new_content = re.sub(pattern, replacement, content)
    
    if new_content != content:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        return True
    return False

# Process all reading files
readings_dir = 'readings'
months = ['january', 'february', 'march', 'april', 'may', 'june', 
          'july', 'august', 'september', 'october', 'november', 'december']

updated_count = 0

for month in months:
    month_dir = os.path.join(readings_dir, month)
    if os.path.exists(month_dir):
        for file in os.listdir(month_dir):
            if file.endswith('.html'):
                file_path = os.path.join(month_dir, file)
                if add_logo_to_reading_page(file_path):
                    updated_count += 1
                    print(f"Updated: {file_path}")

print(f"Total files updated: {updated_count}")