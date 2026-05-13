"""
Update reading-plan.json dayOfWeek values for a given year.
Run at the start of each new year to keep the JSON metadata consistent.

Usage: python update-reading-plan-year.py [year]
If no year is provided, defaults to the current year.
"""

import json
import sys
from datetime import datetime
from pathlib import Path

def update_reading_plan_year(year):
    plan_path = Path(__file__).parent / 'assets' / 'data' / 'reading-plan.json'
    
    with open(plan_path, 'r') as f:
        plan = json.load(f)
    
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    
    updated = 0
    for date_code, entry in plan.items():
        month = int(date_code[:2])
        day = int(date_code[2:])
        try:
            date = datetime(year, month, day)
            new_day = days[date.weekday()]
            if entry.get('dayOfWeek') != new_day:
                entry['dayOfWeek'] = new_day
                updated += 1
        except ValueError:
            # Skip invalid dates (e.g., Feb 29 in non-leap years)
            print(f"Skipping invalid date: {date_code} for year {year}")
    
    with open(plan_path, 'w') as f:
        json.dump(plan, f, indent=2)
    
    print(f"Updated {updated} entries in reading-plan.json for year {year}")

if __name__ == '__main__':
    year = int(sys.argv[1]) if len(sys.argv) > 1 else datetime.now().year
    update_reading_plan_year(year)
