import os
import re

def add_personal_branding():
    """Add personal branding header to all reading pages"""
    
    readings_dir = "readings"
    updated_count = 0
    
    # Personal branding header
    branding_header = '''        <!-- Personal Branding -->
        <div class="text-center mb-4">
            <h1 class="display-4 mb-2">One Year Bible Reading Plan</h1>
            <p class="text-muted mb-0">Created by Ed | <a href="https://ekewaka.com" target="_blank" class="text-decoration-none">ekewaka.com</a></p>
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
                    
                    # Add branding after the container div
                    content = re.sub(
                        r'(<div class="container mt-5">)\s*\n\s*<!-- Intro Section -->',
                        r'\1\n\n' + branding_header + '        <!-- Intro Section -->',
                        content
                    )
                    
                    # Write back to file
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(content)
                    
                    updated_count += 1
    
    print(f"\nAdded branding to {updated_count} reading pages")
    return updated_count

if __name__ == "__main__":
    add_personal_branding()