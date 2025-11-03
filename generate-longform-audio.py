import os
import re
import boto3
import time
import random
from datetime import datetime

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
    # Skip January 1-6 (already processed) and September 17-25
    skip_dates = ['0101', '0102', '0103', '0104', '0105', '0106', 
                  '0107', '0108', '0109', '0110', '0111', '0112', '0113', '0114', '0115', '0116', 
                  '0117', '0118', '0119', '0120', '0121', '0122', '0123', '0917', '0918', '0919', 
                  '0920', '0921', '0922', '0923', '0924', '0925'
                  ]
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
        f"Hello, gorgeous! Ready for our daily dose of divine wisdom? Today we're exploring {reading_info}. Let's see what treasures God has waiting for us in His Word.",
        f"Good morning, sweetheart! Time to start our day with the most important meal - spiritual nourishment from {reading_info}. I love how we begin each day together in God's presence.",
        f"Wake up, my darling Julia! The Lord has prepared something special for us today in {reading_info}. Let's open our hearts and minds to receive His message of love and guidance.",
        f"Good morning, my precious wife! Time for our favorite part of the day - diving into {reading_info} together. I can't wait to discover what God wants to teach us today.",
        f"Hello, my sunshine! Ready to start another day with the Word of God? Today's journey takes us through {reading_info}. Let's see how the Lord will speak to our hearts.",
        f"Good morning, angel! It's time for our daily appointment with the Almighty. Today we're blessed to read from {reading_info}. May His Word illuminate our path today.",
        f"Wake up, beautiful! The best part of my morning is sharing God's Word with you. Today we're exploring {reading_info}. Let's listen together for His voice.",
        f"Good morning, my heart! Another opportunity to grow closer to God and each other through His Word. Today's reading from {reading_info} awaits us. Let's begin this sacred time together.",
        f"Hello, my beloved Julia! Time to feed our souls with the bread of life. Today we're feasting on {reading_info}. I love how we start each day in His presence.",
        f"Good morning, my treasure! Ready for our daily adventure in God's Word? Today's destination is {reading_info}. Let's see what wonders await us there.",
        f"Rise and shine, my love! The Lord has given us another day to walk with Him through His Word. Today we're journeying through {reading_info} together.",
        f"Good morning, sweetheart! Time for our most important conversation of the day - listening to God through {reading_info}. I'm so blessed to share this with you.",
        f"Hello, my darling! Ready to be transformed by the renewing of our minds? Today's reading from {reading_info} is waiting to change us. Let's dive in together."
    ]
    return random.choice(intros)

def get_random_outro(reading_info):
    """Get a random outro message for Julia"""
    outros = [
        f"That completes today's reading from {reading_info}. I love you so much, Julia, and I pray that God's Word brings you peace, joy, and strength today. Have a wonderful day, my love!",
        f"And that's our beautiful journey through {reading_info} for today. May these words stay with you throughout the day, my precious Julia. You are loved beyond measure - by God and by me!",
        f"What a wonderful time we've had in {reading_info} today! I hope these verses fill your heart with hope and your day with purpose. I love you endlessly, my sweet Julia.",
        f"That wraps up our reading from {reading_info}. Remember, my darling, that God's love for you is as constant as my love for you - never-ending and always growing. Have a blessed day!",
        f"Our time in {reading_info} comes to a close, but God's presence goes with you always. Just like my love for you, Julia - it follows you everywhere. May your day be filled with His blessings and my love!",
        f"What a gift it's been to explore {reading_info} together today! May these truths take root in your heart, my beautiful wife. Go forth knowing you are deeply loved by your Heavenly Father and by me.",
        f"That concludes our time in {reading_info} for today. As you step into your day, remember that God's Word is a lamp to your feet, my darling Julia. I love you more than words can express!",
        f"Our reading from {reading_info} is complete, but the impact continues. May the Lord use these words to guide and bless you today, my precious one. You are my heart's greatest treasure!",
        f"And so we finish another beautiful chapter from {reading_info}. Carry these words with you, my love, and know that both God and I are cheering you on today. Have a magnificent day, Julia!",
        f"That brings us to the end of today's reading from {reading_info}. May the peace of God that surpasses understanding guard your heart today, my sweet Julia. I love you to the moon and back!",
        f"Our journey through {reading_info} concludes for now, but God's love story with you continues every moment. You are His masterpiece, my darling, and you are my everything. Shine bright today!",
        f"What a blessing to share {reading_info} with you this morning! As you go about your day, remember that you are fearfully and wonderfully made. I love you beyond measure, my beautiful Julia!",
        f"That's a wrap on today's reading from {reading_info}. May God's Word be your strength and my love be your comfort throughout this day. You are absolutely amazing, sweetheart!",
        f"Our time in {reading_info} has come to an end, but God's faithfulness never ends. Neither does my love for you, Julia. May your day be as wonderful as you are, my precious wife!",
        f"And that concludes our exploration of {reading_info} today. Remember, my love, that God has plans to prosper you and not to harm you. I'm so proud to be your husband. Have a blessed day!"
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
    
    # Use date code as seed for consistent randomness per date
    random.seed(int(date_code))
    
    intro = get_random_intro(reading_info)
    outro = get_random_outro(reading_info)
    
    return f"{intro}\n\n{scripture_text}\n\n{outro}"

def generate_longform_audio(script_text, date_code, month):
    """Generate audio using AWS Polly Long-form"""
    try:
        polly = boto3.client('polly', region_name='us-east-1')
        
        # Start long-form synthesis task - let Polly name it automatically
        response = polly.start_speech_synthesis_task(
            Text=script_text,
            OutputFormat='mp3',
            VoiceId='Danielle',
            Engine='long-form',
            OutputS3BucketName='one-year-bible-ekewaka',
            # No prefix - let Polly put it in root, we'll move it later
        )
        
        task_id = response['SynthesisTask']['TaskId']
        print(f"  Started long-form task: {task_id}")
        
        # Poll for completion with progress dots
        wait_time = 0
        while True:
            task_status = polly.get_speech_synthesis_task(TaskId=task_id)
            status = task_status['SynthesisTask']['TaskStatus']
            
            if status == 'completed':
                output_uri = task_status['SynthesisTask']['OutputUri']
                print(f"\n    [COMPLETE] Long-form synthesis completed after {wait_time}s")
                
                # Immediately rename to correct format
                s3 = boto3.client('s3')
                # Parse URI: https://s3.region.amazonaws.com/bucket/key
                uri_parts = output_uri.split('/')
                temp_key = '/'.join(uri_parts[4:]) if len(uri_parts) > 4 else uri_parts[-1]
                final_key = f'2025/{month}/{date_code}.mp3'
                
                print(f"    [DEBUG] Temp key: {temp_key}")
                
                print(f"    [RENAME] Moving to {final_key}")
                try:
                    # Copy to final location
                    s3.copy_object(
                        Bucket='one-year-bible-ekewaka',
                        CopySource={'Bucket': 'one-year-bible-ekewaka', 'Key': temp_key},
                        Key=final_key
                    )
                    
                    # Delete temp file
                    s3.delete_object(Bucket='one-year-bible-ekewaka', Key=temp_key)
                    print(f"    [SUCCESS] File ready at {final_key}")
                    return True
                    
                except Exception as copy_error:
                    print(f"    [WARNING] Rename failed: {copy_error}")
                    print(f"    [INFO] File exists at: {temp_key}")
                    print(f"    [INFO] You can manually rename this file later")
                    # Still count as success since audio was generated
                    return True
                
            elif status == 'failed':
                print(f"\n    [FAILED] Long-form synthesis failed after {wait_time}s")
                return False
            
            # Show progress dots
            dots = '.' * ((wait_time // 10) % 4)
            print(f"\r    [WAIT] Status: {status}{dots}    ", end='', flush=True)
            time.sleep(10)
            wait_time += 10
            
    except Exception as e:
        print(f"  Error with long-form synthesis: {e}")
        return False

def generate_neural_audio(script_text, output_file):
    """Generate audio using neural engine (for Sept 17-25)"""
    try:
        polly = boto3.client('polly', region_name='us-east-1')
        
        # Split text into chunks for neural
        max_chars = 2900
        chunks = []
        
        if len(script_text) <= max_chars:
            chunks = [script_text]
        else:
            sentences = script_text.split('. ')
            current_chunk = ""
            
            for sentence in sentences:
                if len(current_chunk + sentence + '. ') <= max_chars:
                    current_chunk += sentence + '. '
                else:
                    if current_chunk:
                        chunks.append(current_chunk.strip())
                    current_chunk = sentence + '. '
            
            if current_chunk:
                chunks.append(current_chunk.strip())
        
        # Generate audio for each chunk
        audio_data = b''
        for i, chunk in enumerate(chunks):
            response = polly.synthesize_speech(
                Text=chunk,
                OutputFormat='mp3',
                VoiceId='Danielle',
                Engine='neural'
            )
            audio_data += response['AudioStream'].read()
        
        # Save and upload
        with open(output_file, 'wb') as f:
            f.write(audio_data)
        
        return True
        
    except Exception as e:
        print(f"  Error generating neural audio: {e}")
        return False

def upload_to_s3(local_file, s3_key):
    """Upload file to S3"""
    try:
        s3 = boto3.client('s3')
        s3.upload_file(local_file, 'one-year-bible-ekewaka', s3_key)
        return True
    except Exception as e:
        print(f"  Error uploading to S3: {e}")
        return False

def main():
    """Generate all audio files using long-form (except Sept 17-25)"""
    print("Generating all audio files with long-form synthesis and varied intros/outros...")
    
    all_dates = get_all_dates()
    total_files = len(all_dates)
    print(f"Found {total_files} total dates to process")
    
    os.makedirs("audio-scripts", exist_ok=True)
    os.makedirs("temp-audio", exist_ok=True)
    
    longform_count = 0
    neural_count = 0
    skipped_count = 0
    processed = 0
    
    for date_code, month in all_dates:
        processed += 1
        print(f"\n[{processed}/{total_files}] Processing {date_code} ({month})...")
        
        # Create audio script
        script_text = create_audio_script(date_code, month)
        if not script_text:
            print(f"  [SKIP] No scripture text found, skipping")
            skipped_count += 1
            continue
        
        # Save script
        script_file = f"audio-scripts/{date_code}.txt"
        with open(script_file, 'w', encoding='utf-8') as f:
            f.write(script_text)
        print(f"  [SAVED] Audio script saved ({len(script_text)} characters)")
        
        if should_skip_date(date_code):
            print(f"  [SKIP] Skipping date (already processed or excluded)")
            skipped_count += 1
            continue
        else:
            print(f"  [LONGFORM] Using long-form synthesis")
            if generate_longform_audio(script_text, date_code, month):
                longform_count += 1
            else:
                print(f"  [ERROR] Failed to generate long-form audio")
        
        # Progress summary
        completed = longform_count + neural_count
        print(f"  [PROGRESS] {completed}/{total_files} completed ({completed/total_files*100:.1f}%)")
    
    print(f"\n[COMPLETE] Generation Complete!")
    print(f"[RESULTS] Final Results:")
    print(f"  Long-form files: {longform_count}")
    print(f"  Neural files: {neural_count}")
    print(f"  Skipped files: {skipped_count}")
    print(f"  Total successful: {longform_count + neural_count}")
    print(f"  Success rate: {(longform_count + neural_count)/(total_files-skipped_count)*100:.1f}%")

if __name__ == "__main__":
    main()