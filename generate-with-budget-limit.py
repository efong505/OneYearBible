import os
import re
import boto3
import time
import random
import json
from datetime import datetime

# AWS Polly free tier limits (monthly)
FREE_TIER_CHARACTERS = 5000000  # 5 million characters per month
SAFETY_BUFFER = 100000  # Leave 100k character buffer

def load_progress():
    """Load progress from file"""
    try:
        with open('polly_progress.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {
            'characters_used': 0,
            'completed_dates': [],
            'current_month': datetime.now().strftime('%Y-%m')
        }

def save_progress(progress):
    """Save progress to file"""
    with open('polly_progress.json', 'w') as f:
        json.dump(progress, f, indent=2)

def reset_monthly_usage(progress):
    """Reset usage if new month"""
    current_month = datetime.now().strftime('%Y-%m')
    if progress['current_month'] != current_month:
        progress['characters_used'] = 0
        progress['current_month'] = current_month
        print(f"[RESET] New month detected, resetting character usage")
    return progress

def get_all_dates():
    """Get all HTML files from all months"""
    months = ['january', 'february', 'march', 'april', 'may', 'june', 
              'july', 'august', 'september', 'october', 'november', 'december']
    
    all_dates = []
    for month in months:
        month_dir = f"readings/{month}"
        if os.path.exists(month_dir):
            for file in os.listdir(month_dir):
                if file.endswith('.html'):
                    date_code = file.replace('.html', '')
                    all_dates.append((date_code, month))
    
    return all_dates

def should_skip_date(date_code):
    """Check if date should be skipped"""
    skip_dates = ['0101', '0102', '0103', '0104', '0105', '0106', 
                  '0107', '0108', '0109', '0110', '0111', '0112', '0113', '0114', '0115', '0116', 
                  '0117', '0118', '0119', '0120', '0121', '0122', '0123', '0917', '0918', '0919', 
                  '0920', '0921', '0922', '0923', '0924', '0925']
    return date_code in skip_dates

def extract_scripture_text(html_file):
    """Extract scripture text from HTML file"""
    with open(html_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    scripture_pattern = r'<p class="fnb"><span>\d+\s*</span>(.*?)</p>'
    matches = re.findall(scripture_pattern, content, re.DOTALL)
    
    scripture_text = []
    for match in matches:
        clean_text = re.sub(r'<[^>]+>', '', match)
        clean_text = re.sub(r'\s+', ' ', clean_text).strip()
        if clean_text:
            scripture_text.append(clean_text)
    
    return ' '.join(scripture_text)

def get_reading_info(html_file):
    """Extract reading information from HTML file"""
    with open(html_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    h4_pattern = r'<h4 class="mt-3">(.*?)</h4>'
    h4_match = re.search(h4_pattern, content)
    
    if h4_match:
        reading_text = h4_match.group(1).strip()
        reading_text = re.sub(r'\s*&\s*$', '', reading_text)
        return reading_text
    
    return "today's reading"

def get_random_intro(reading_info):
    """Get a random intro message for Julia"""
    intros = [
        f"Good morning, my beautiful Julia! It's time for our daily Bible reading together. Today we're reading from {reading_info}. Let's dive into God's Word and see what He has for us today.",
        f"Rise and shine, my love! Another beautiful day to spend time in God's Word together. Today's reading is from {reading_info}. I'm so grateful we can share this spiritual journey together.",
        f"Hello, gorgeous! Ready for our daily dose of divine wisdom? Today we're exploring {reading_info}. Let's see what treasures God has waiting for us in His Word."
    ]
    return random.choice(intros)

def get_random_outro(reading_info):
    """Get a random outro message for Julia"""
    outros = [
        f"That completes today's reading from {reading_info}. I love you so much, Julia, and I pray that God's Word brings you peace, joy, and strength today. Have a wonderful day, my love!",
        f"And that's our beautiful journey through {reading_info} for today. May these words stay with you throughout the day, my precious Julia. You are loved beyond measure - by God and by me!",
        f"What a wonderful time we've had in {reading_info} today! I hope these verses fill your heart with hope and your day with purpose. I love you endlessly, my sweet Julia."
    ]
    return random.choice(outros)

def create_audio_script(date_code, month):
    """Create audio script for a specific date"""
    html_file = f"readings/{month}/{date_code}.html"
    
    if not os.path.exists(html_file):
        return None
    
    scripture_text = extract_scripture_text(html_file)
    reading_info = get_reading_info(html_file)
    
    if not scripture_text:
        return None
    
    random.seed(int(date_code))
    intro = get_random_intro(reading_info)
    outro = get_random_outro(reading_info)
    
    return f"{intro}\n\n{scripture_text}\n\n{outro}"

def generate_longform_audio(script_text, date_code, month):
    """Generate audio using AWS Polly Long-form"""
    try:
        polly = boto3.client('polly', region_name='us-east-1')
        
        response = polly.start_speech_synthesis_task(
            Text=script_text,
            OutputFormat='mp3',
            VoiceId='Danielle',
            Engine='long-form',
            OutputS3BucketName='one-year-bible-ekewaka'
        )
        
        task_id = response['SynthesisTask']['TaskId']
        print(f"  Started long-form task: {task_id}")
        
        wait_time = 0
        while True:
            task_status = polly.get_speech_synthesis_task(TaskId=task_id)
            status = task_status['SynthesisTask']['TaskStatus']
            
            if status == 'completed':
                output_uri = task_status['SynthesisTask']['OutputUri']
                print(f"\n    [COMPLETE] Long-form synthesis completed after {wait_time}s")
                
                s3 = boto3.client('s3')
                uri_parts = output_uri.split('/')
                temp_key = '/'.join(uri_parts[4:]) if len(uri_parts) > 4 else uri_parts[-1]
                final_key = f'2025/{month}/{date_code}.mp3'
                
                try:
                    s3.copy_object(
                        Bucket='one-year-bible-ekewaka',
                        CopySource={'Bucket': 'one-year-bible-ekewaka', 'Key': temp_key},
                        Key=final_key
                    )
                    s3.delete_object(Bucket='one-year-bible-ekewaka', Key=temp_key)
                    print(f"    [SUCCESS] File ready at {final_key}")
                    return True
                except Exception as copy_error:
                    print(f"    [WARNING] Rename failed: {copy_error}")
                    return True
                
            elif status == 'failed':
                print(f"\n    [FAILED] Long-form synthesis failed after {wait_time}s")
                return False
            
            dots = '.' * ((wait_time // 10) % 4)
            print(f"\r    [WAIT] Status: {status}{dots}    ", end='', flush=True)
            time.sleep(10)
            wait_time += 10
            
    except Exception as e:
        print(f"  Error with long-form synthesis: {e}")
        return False

def main():
    """Generate audio files with budget tracking"""
    print("Generating audio files with budget tracking...")
    
    # Load progress
    progress = load_progress()
    progress = reset_monthly_usage(progress)
    
    print(f"Characters used this month: {progress['characters_used']:,}/{FREE_TIER_CHARACTERS:,}")
    print(f"Remaining budget: {FREE_TIER_CHARACTERS - progress['characters_used']:,} characters")
    
    all_dates = get_all_dates()
    remaining_dates = [(d, m) for d, m in all_dates if d not in progress['completed_dates'] and not should_skip_date(d)]
    
    print(f"Remaining dates to process: {len(remaining_dates)}")
    
    os.makedirs("audio-scripts", exist_ok=True)
    
    for date_code, month in remaining_dates:
        print(f"\n[BUDGET CHECK] Processing {date_code} ({month})...")
        
        # Create script and check character count
        script_text = create_audio_script(date_code, month)
        if not script_text:
            print(f"  [SKIP] No scripture text found")
            continue
        
        script_length = len(script_text)
        projected_usage = progress['characters_used'] + script_length
        
        # Check if this would exceed budget
        if projected_usage > (FREE_TIER_CHARACTERS - SAFETY_BUFFER):
            print(f"  [BUDGET LIMIT] Would exceed free tier limit!")
            print(f"  Script length: {script_length:,} characters")
            print(f"  Current usage: {progress['characters_used']:,}")
            print(f"  Projected usage: {projected_usage:,}")
            print(f"  Free tier limit: {FREE_TIER_CHARACTERS:,}")
            print(f"\n[STOPPED] Stopping to stay within budget.")
            print(f"Remaining dates: {len(remaining_dates) - remaining_dates.index((date_code, month))}")
            break
        
        # Save script
        script_file = f"audio-scripts/{date_code}.txt"
        with open(script_file, 'w', encoding='utf-8') as f:
            f.write(script_text)
        print(f"  [SAVED] Script: {script_length:,} characters")
        
        # Generate audio
        print(f"  [LONGFORM] Using long-form synthesis")
        if generate_longform_audio(script_text, date_code, month):
            # Update progress
            progress['characters_used'] += script_length
            progress['completed_dates'].append(date_code)
            save_progress(progress)
            
            print(f"  [SUCCESS] Audio completed")
            print(f"  [BUDGET] Used: {progress['characters_used']:,}/{FREE_TIER_CHARACTERS:,} ({progress['characters_used']/FREE_TIER_CHARACTERS*100:.1f}%)")
        else:
            print(f"  [ERROR] Failed to generate audio")
    
    print(f"\n[COMPLETE] Session finished")
    print(f"Total characters used: {progress['characters_used']:,}")
    print(f"Completed dates: {len(progress['completed_dates'])}")

if __name__ == "__main__":
    main()