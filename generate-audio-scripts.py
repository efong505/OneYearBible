#!/usr/bin/env python3
import os
import re
import json
import random
from bs4 import BeautifulSoup
from datetime import datetime

# Personalized intros and outros
INTROS = [
    "Good morning sunshine! It's time for your daily dose of divine wisdom. This is {month} {day}, 2025, and Eddie has lovingly prepared today's Kenneth Copeland One-Year Bible reading just for his incredible wife Julia. Grab your coffee and let's dive into God's word together!",
    "Welcome to another blessed day, Julia! Your personal Bible reading service is now in session. Eddie wants you to know that you're more precious than rubies, and speaking of precious things, let's explore today's treasures from Scripture for {month} {day}, 2025.",
    "Rise and shine, beautiful! It's Bible time with your favorite narrator - well, Eddie's voice anyway. Today is {month} {day}, 2025, and we're continuing our journey through the Kenneth Copeland One-Year Bible plan. Julia, Eddie says you're his favorite person to read to, so let's get started!",
    "Hello gorgeous! Welcome to your VIP Bible reading experience for {month} {day}, 2025. This exclusive presentation has been curated by Eddie specifically for the amazing Julia Fong. Consider this your daily spiritual vitamin - now let's get blessed!",
    "Good morning my love! Eddie here with your personalized Bible reading for {month} {day}, 2025. Julia, you light up every room you enter, and today we're going to let God's word light up our hearts together!",
    "Wake up sleeping beauty! Your devoted husband Eddie has prepared another spiritual feast for you this {month} {day}, 2025. Julia, you're the answer to prayers I didn't even know I was praying. Now let's see what God has in store for us today!"
]

OUTROS = [
    "And that wraps up today's spiritual adventure for {month} {day}. Julia, Eddie wants you to know that you're his answered prayer and he's grateful for every moment with you. Until tomorrow's reading, may God's blessings follow you everywhere you go!",
    "That concludes our time in God's word for today. Julia, Eddie says you make every day brighter than the promises we just read about. He loves you more than words can express - even more than all these Bible verses we just heard!",
    "And scene! Another beautiful day of Scripture complete for {month} {day}. Julia, your personal reading assistant Eddie wants to remind you that you're fearfully and wonderfully made, and he feels blessed to be your husband. Sweet dreams and see you tomorrow!",
    "That's a wrap on today's Bible reading! Julia, Eddie hopes this filled your heart as much as you fill his every single day. Remember, you're loved beyond measure - by God and by your devoted husband. Catch you on the flip side tomorrow!",
    "Mission accomplished for {month} {day}! Julia, Eddie wants you to know that reading God's word for you is one of his favorite ways to show love. You're his treasure, his joy, and his best friend. Until next time, keep shining bright!",
    "Another day of divine wisdom complete! Julia, Eddie says you're the melody to his heart's song, and these scriptures are just the harmony. He loves you to the moon and back, and God loves you even more than that!"
]

def extract_reading_title(html_content):
    """Extract the reading title from HTML"""
    soup = BeautifulSoup(html_content, 'html.parser')
    # Look for h4 with reading info
    h4_element = soup.find('h4')
    if h4_element:
        return h4_element.get_text().strip()
    return ""

def extract_scripture_text(html_content):
    """Extract clean scripture text from HTML without verse numbers"""
    soup = BeautifulSoup(html_content, 'html.parser')
    
    text_parts = []
    current_verses = []
    
    # Get reading title first
    reading_title = extract_reading_title(html_content)
    if reading_title:
        text_parts.append(f"Today's reading is {reading_title}.\n")
    
    # Combine headings and paragraphs in order
    all_elements = soup.find_all(['h2', 'h5', 'p'])
    
    for element in all_elements:
        if element.name in ['h2', 'h5'] and element.get_text().strip():
            # Chapter/section heading
            heading_text = element.get_text().strip()
            if any(book in heading_text for book in ['Isaiah', 'Timothy', 'Thessalonians', 'Psalms', 'Proverbs', 'Matthew', 'Mark', 'Luke', 'John', 'Acts', 'Romans', 'Corinthians', 'Galatians', 'Ephesians', 'Philippians', 'Colossians', 'Peter', 'James', 'Jude', 'Revelation', 'Hebrews']):
                # Add any accumulated verses before new chapter
                if current_verses:
                    text_parts.append(' '.join(current_verses))
                    current_verses = []
                
                # Add chapter heading with period for pause
                text_parts.append(f"\n{heading_text}.\n")
        elif element.name == 'p' and 'fnb' in element.get('class', []):
            # Scripture verse - remove verse numbers
            verse_text = element.get_text().strip()
            if verse_text:
                # Remove verse numbers (digits at start in span tags)
                clean_verse = re.sub(r'^\d+\s+', '', verse_text)
                if clean_verse:
                    current_verses.append(clean_verse)
    
    # Add any remaining verses
    if current_verses:
        text_parts.append(' '.join(current_verses))
    
    return '\n'.join(text_parts)

def get_month_name(month_num):
    """Convert month number to name"""
    months = ['January', 'February', 'March', 'April', 'May', 'June',
              'July', 'August', 'September', 'October', 'November', 'December']
    return months[month_num - 1]

def generate_audio_script(date_code, html_file_path):
    """Generate complete audio script for a date"""
    # Parse date
    month_num = int(date_code[:2])
    day_num = int(date_code[2:])
    month_name = get_month_name(month_num)
    
    # Read HTML file
    try:
        with open(html_file_path, 'r', encoding='utf-8') as f:
            html_content = f.read()
    except Exception as e:
        print(f"Error reading {html_file_path}: {e}")
        return None
    
    # Extract scripture text
    scripture_text = extract_scripture_text(html_content)
    
    if not scripture_text.strip():
        print(f"No scripture text found for {date_code}")
        return None
    
    # Select random intro and outro
    intro = random.choice(INTROS).format(month=month_name, day=day_num)
    outro = random.choice(OUTROS).format(month=month_name, day=day_num)
    
    # Combine into full script
    full_script = f"{intro}\n\n{scripture_text}\n\n{outro}"
    
    return full_script

def main():
    # Base directory
    base_dir = "c:/Users/Ed/Documents/Post Graduation/Projects/OneYearBible"
    readings_dir = os.path.join(base_dir, "readings")
    output_dir = os.path.join(base_dir, "audio-scripts")
    
    # Create output directory
    os.makedirs(output_dir, exist_ok=True)
    
    # Days that already have audio (skip these)
    completed_days = ['0918', '0919', '0920', '0921', '0922', '0923', '0924', '0925', '0926']
    
    # Process all months
    months = ['september', 'october', 'november', 'december', 'january', 'february', 'march', 'april', 'may', 'june', 'july', 'august']
    
    generated_count = 0
    
    for month in months:
        month_dir = os.path.join(readings_dir, month)
        if not os.path.exists(month_dir):
            continue
            
        # Get all HTML files in month directory
        html_files = [f for f in os.listdir(month_dir) if f.endswith('.html')]
        
        for html_file in html_files:
            date_code = html_file.replace('.html', '')
            
            # Skip if already completed
            if date_code in completed_days:
                print(f"Skipping {date_code} - already has audio")
                continue
            
            html_file_path = os.path.join(month_dir, html_file)
            
            # Generate script
            script = generate_audio_script(date_code, html_file_path)
            
            if script:
                # Save script to file
                script_filename = f"{date_code}_audio_script.txt"
                script_path = os.path.join(output_dir, script_filename)
                
                with open(script_path, 'w', encoding='utf-8') as f:
                    f.write(script)
                
                print(f"Generated script for {date_code}")
                generated_count += 1
            else:
                print(f"Failed to generate script for {date_code}")
    
    print(f"\nGenerated {generated_count} audio scripts in {output_dir}")
    print("You can now copy these scripts to Amazon Polly for audio generation!")

if __name__ == "__main__":
    main()