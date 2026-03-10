import os
import re

def update_branding_size():
    """Replace existing branding with larger heading"""
    
    readings_dir = "readings"
    updated_count = 0
    
    # New larger branding header
    new_branding = '''        <!-- Personal Branding -->
        <div class="text-center mb-4">
            <h1 class="display-3 mb-2">One Year Bible Reading Plan</h1>
            <p class="text-muted mb-0">By Edward Fong | <a href="https://ekewaka.com" target="_blank" class="text-decoration-none">ekewaka.com</a></p>
        </div>
        
'''
    
    # Walk through all month directories
    for month_dir in os.listdir(readings_dir):
        month_path = os.path.join(readings_dir, month_dir)
        if os.path.isdir(month_path):
            print(f"Processing {month_dir}...")
            
            # Process all HTML files in the month directory
            for filename in os.listdir(month_path):
                if filename.endswith('.html'):
                    file_path = os.path.join(month_path, filename)
                    
                    # Read the file
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    # Remove existing branding
                    content = re.sub(
                        r'\s*<!-- Personal Branding -->.*?</div>\s*\n\s*',
                        '\n\n',
                        content,
                        flags=re.DOTALL
                    )
                    
                    # Add new larger branding after container div
                    content = re.sub(
                        r'(<div class="container mt-5">)\s*\n',
                        r'\1\n\n' + new_branding,
                        content
                    )
                    
                    # Write back to file
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(content)
                    
                    updated_count += 1
    
    print(f"\nUpdated branding on {updated_count} reading pages")
    return updated_count

if __name__ == "__main__":
    update_branding_size()