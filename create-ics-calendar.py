import json
import os
from datetime import datetime, timedelta

def create_ics_calendar():
    """Create an ICS calendar file with all Bible readings for 2026"""
    
    # Load the reading plan
    try:
        with open('assets/data/reading-plan.json', 'r') as f:
            reading_plan = json.load(f)
    except FileNotFoundError:
        print("reading-plan.json not found!")
        return
    
    # ICS file header
    ics_content = [
        "BEGIN:VCALENDAR",
        "VERSION:2.0",
        "PRODID:-//One Year Bible//Bible Reading Plan//EN",
        "CALSCALE:GREGORIAN",
        "METHOD:PUBLISH",
        "X-WR-CALNAME:One Year Bible Reading Plan 2025",
        "X-WR-CALDESC:Daily Bible readings for the One Year Bible plan"
    ]
    
    # Generate events for each reading
    for date_code, reading_info in reading_plan.items():
        # Parse date code (MMDD)
        month = int(date_code[:2])
        day = int(date_code[2:])
        
        # Create 2025 date (the Bible reading plan year)
        event_date = datetime(2025, month, day)
        
        # Format date for ICS (YYYYMMDD)
        date_str = event_date.strftime("%Y%m%d")
        
        # Create event
        old_testament = reading_info.get('oldTestament', '')
        new_testament = reading_info.get('newTestament', '')
        
        # Build reading title
        reading_parts = []
        if old_testament:
            reading_parts.append(old_testament)
        if new_testament:
            reading_parts.append(new_testament)
        
        reading_title = ' & '.join(reading_parts) if reading_parts else 'Bible Reading'
        
        title = f"Bible Reading: {reading_title}"
        description = f"Today's Bible reading:\n{reading_title}\n\nRead online: https://daily.mytestimony.click/readings/{get_month_name(month)}/{date_code}.html"
        
        # Generate unique ID
        uid = f"{date_code}-2025@daily.mytestimony.click"
        
        # Add event to ICS
        ics_content.extend([
            "BEGIN:VEVENT",
            f"UID:{uid}",
            f"DTSTART;VALUE=DATE:{date_str}",
            f"DTEND;VALUE=DATE:{date_str}",
            f"SUMMARY:{title}",
            f"DESCRIPTION:{description}",
            "STATUS:CONFIRMED",
            "TRANSP:TRANSPARENT",
            f"CREATED:{datetime.now().strftime('%Y%m%dT%H%M%SZ')}",
            f"LAST-MODIFIED:{datetime.now().strftime('%Y%m%dT%H%M%SZ')}",
            "END:VEVENT"
        ])
    
    # ICS file footer
    ics_content.append("END:VCALENDAR")
    
    # Write to file
    with open('one-year-bible-2025.ics', 'w', encoding='utf-8') as f:
        f.write('\n'.join(ics_content))
    
    print(f"Created one-year-bible-2025.ics with {len(reading_plan)} events")

def get_month_name(month_num):
    """Convert month number to name"""
    months = ['', 'january', 'february', 'march', 'april', 'may', 'june',
              'july', 'august', 'september', 'october', 'november', 'december']
    return months[month_num]

if __name__ == "__main__":
    create_ics_calendar()