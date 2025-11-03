#!/usr/bin/env python3
import os
import boto3
import json
from datetime import datetime
import time

# AWS Configuration
S3_BUCKET = "one-year-bible-ekewaka"
POLLY_VOICE = "Danielle"
POLLY_ENGINE = "neural"  # Use neural engine for Danielle voice

def get_month_name(month_num):
    """Convert month number to name"""
    months = ['january', 'february', 'march', 'april', 'may', 'june',
              'july', 'august', 'september', 'october', 'november', 'december']
    return months[month_num - 1]

def split_text_for_polly(text, max_length=2000):
    """Split text into chunks that fit Polly's limits"""
    if len(text) <= max_length:
        return [text]
    
    chunks = []
    current_chunk = ""
    
    # Split by sentences first for better breaks
    sentences = text.replace('.\n', '. ').split('. ')
    
    for sentence in sentences:
        sentence = sentence.strip()
        if not sentence:
            continue
            
        # Add period back if it was removed
        if not sentence.endswith('.'):
            sentence += '.'
            
        if len(current_chunk) + len(sentence) + 1 <= max_length:
            if current_chunk:
                current_chunk += ' ' + sentence
            else:
                current_chunk = sentence
        else:
            if current_chunk:
                chunks.append(current_chunk)
            current_chunk = sentence
            
            # If single sentence is too long, split by words
            if len(current_chunk) > max_length:
                words = current_chunk.split()
                current_chunk = ""
                for word in words:
                    if len(current_chunk) + len(word) + 1 <= max_length:
                        if current_chunk:
                            current_chunk += ' ' + word
                        else:
                            current_chunk = word
                    else:
                        if current_chunk:
                            chunks.append(current_chunk)
                        current_chunk = word
    
    if current_chunk:
        chunks.append(current_chunk)
    
    return chunks

def create_polly_audio(text, output_file):
    """Generate audio using Amazon Polly with text chunking"""
    polly = boto3.client('polly')
    
    try:
        print(f"Text length: {len(text)} characters")
        
        # Check if text is too long and split if needed
        if len(text) > 2000:
            print(f"Text too long ({len(text)} chars), splitting into chunks...")
            text_chunks = split_text_for_polly(text)
            print(f"Split into {len(text_chunks)} chunks")
            
            temp_files = []
            
            for i, chunk in enumerate(text_chunks):
                print(f"Processing chunk {i+1}/{len(text_chunks)} ({len(chunk)} chars)")
                temp_file = output_file.replace('.mp3', f'_chunk_{i}.mp3')
                temp_files.append(temp_file)
                
                response = polly.synthesize_speech(
                    Text=chunk,
                    OutputFormat='mp3',
                    VoiceId=POLLY_VOICE,
                    Engine=POLLY_ENGINE
                )
                
                with open(temp_file, 'wb') as f:
                    f.write(response['AudioStream'].read())
            
            # Combine audio files (simple concatenation)
            print("Combining audio chunks...")
            with open(output_file, 'wb') as outfile:
                for temp_file in temp_files:
                    with open(temp_file, 'rb') as infile:
                        outfile.write(infile.read())
                    os.remove(temp_file)  # Clean up temp file
        else:
            # Single chunk - process normally
            response = polly.synthesize_speech(
                Text=text,
                OutputFormat='mp3',
                VoiceId=POLLY_VOICE,
                Engine=POLLY_ENGINE
            )
            
            with open(output_file, 'wb') as f:
                f.write(response['AudioStream'].read())
        
        print(f"Generated audio: {output_file}")
        return True
        
    except Exception as e:
        print(f"Error generating audio for {output_file}: {e}")
        return False

def upload_to_s3(local_file, s3_key):
    """Upload file to S3"""
    s3 = boto3.client('s3')
    
    try:
        s3.upload_file(
            local_file, 
            S3_BUCKET, 
            s3_key,
            ExtraArgs={'ContentType': 'audio/mpeg'}
        )
        print(f"Uploaded to S3: s3://{S3_BUCKET}/{s3_key}")
        return True
        
    except Exception as e:
        print(f"Error uploading {local_file} to S3: {e}")
        return False

def process_audio_scripts():
    """Process all audio scripts and generate/upload audio files"""
    base_dir = "c:/Users/Ed/Documents/Post Graduation/Projects/OneYearBible"
    scripts_dir = os.path.join(base_dir, "audio-scripts")
    temp_audio_dir = os.path.join(base_dir, "temp-audio")
    
    # Create temp directory for audio files
    os.makedirs(temp_audio_dir, exist_ok=True)
    
    # Days that already have audio (skip these)
    completed_days = ['0918', '0919', '0920', '0921', '0922', '0923', '0924', '0925', '0926']
    
    if not os.path.exists(scripts_dir):
        print(f"Scripts directory not found: {scripts_dir}")
        print("Please run generate-audio-scripts.py first!")
        return
    
    # Get all script files
    script_files = [f for f in os.listdir(scripts_dir) if f.endswith('_audio_script.txt')]
    
    processed_count = 0
    
    for script_file in script_files:
        # Extract date code from filename
        date_code = script_file.replace('_audio_script.txt', '')
        
        # Skip if already completed
        if date_code in completed_days:
            print(f"Skipping {date_code} - already has audio")
            continue
        
        # Parse date
        month_num = int(date_code[:2])
        day_num = int(date_code[2:])
        month_name = get_month_name(month_num)
        
        # Read script content
        script_path = os.path.join(scripts_dir, script_file)
        try:
            with open(script_path, 'r', encoding='utf-8') as f:
                script_text = f.read()
        except Exception as e:
            print(f"Error reading script {script_file}: {e}")
            continue
        
        # Generate audio filename in 0927.mp3 format
        audio_filename = f"{date_code}.mp3"
        temp_audio_path = os.path.join(temp_audio_dir, audio_filename)
        
        # Generate audio with Polly
        print(f"Generating audio for {date_code}...")
        if create_polly_audio(script_text, temp_audio_path):
            # Upload to S3 (create month folder if needed)
            s3_key = f"2025/{month_name.lower()}/{audio_filename}"
            if upload_to_s3(temp_audio_path, s3_key):
                processed_count += 1
                
                # Clean up temp file
                try:
                    os.remove(temp_audio_path)
                except:
                    pass
            
            # Add delay to avoid rate limiting
            time.sleep(1)
        
        print(f"Completed {date_code}")
        print("-" * 50)
    
    print(f"\nProcessed {processed_count} audio files")
    print("All audio files have been generated and uploaded to S3!")

def main():
    """Main function"""
    print("Starting Polly audio generation and S3 upload...")
    print("Make sure you have AWS credentials configured!")
    print("=" * 60)
    
    # Check AWS credentials
    try:
        boto3.client('sts').get_caller_identity()
        print("AWS credentials verified ✓")
    except Exception as e:
        print(f"AWS credentials error: {e}")
        print("Please configure AWS credentials using 'aws configure' or environment variables")
        return
    
    process_audio_scripts()

if __name__ == "__main__":
    main()