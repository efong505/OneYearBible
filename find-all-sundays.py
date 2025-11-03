import os

def find_all_sundays():
    """Find all Sunday files in the year"""
    sunday_files = []
    readings_dir = "readings"
    
    for month_dir in sorted(os.listdir(readings_dir)):
        month_path = os.path.join(readings_dir, month_dir)
        if not os.path.isdir(month_path):
            continue
            
        for filename in sorted(os.listdir(month_path)):
            if filename.endswith('.html'):
                file_path = os.path.join(month_path, filename)
                
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    # Check if it's a Sunday
                    if 'Sunday' in content:
                        date_code = filename.replace('.html', '')
                        sunday_files.append(date_code)
                        print(f"Found Sunday: {date_code} ({month_dir})")
                
                except Exception as e:
                    print(f"Error reading {file_path}: {e}")
    
    return sunday_files

def main():
    print("Finding all Sunday files...")
    sunday_files = find_all_sundays()
    
    print(f"\nFound {len(sunday_files)} Sunday files:")
    
    # Format for upload script
    print("\n=== SUNDAY FILES LIST (for upload-corrected-html.py) ===")
    print("sunday_dates = [")
    for i, date_code in enumerate(sunday_files):
        if i == len(sunday_files) - 1:
            print(f'    "{date_code}"')
        else:
            print(f'    "{date_code}",')
    print("]")

if __name__ == "__main__":
    main()