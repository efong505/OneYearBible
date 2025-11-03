import os
import re
import boto3
from datetime import datetime

# List of dates that had abbreviation corrections
corrected_dates = [
    "0816", "0817", "0820", "0821", "0823", "0824", "0825", "0826"
]

def extract_scripture_text(html_file):
    """Extract scripture text from HTML file, removing verse numbers"""
    with open(html_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Extract scripture text from paragraphs with class="fnb"
    scripture_pattern = r'<p class="fnb"><span>\d+\s*</span>(.*?)</p>'
    matches = re.findall(scripture_pattern, content, re.DOTALL)
    
    scripture_text = []
    for match in matches:
        # Clean up HTML tags and normalize whitespace
        clean_text = re.sub(r'<[^>]+>', '', match)
        clean_text = re.sub(r'\s+', ' ', clean_text).strip()
        if clean_text:
            scripture_text.append(clean_text)
    
    return ' '.join(scripture_text)

def get_reading_info(html_file):
    """Extract reading information from HTML file"""
    with open(html_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Extract the h4 tag content (main reading heading)
    h4_pattern = r'<h4 class="mt-3">(.*?)</h4>'
    h4_match = re.search(h4_pattern, content)
    
    if h4_match:
        reading_text = h4_match.group(1).strip()
        # Remove the " & " at the end if present
        reading_text = re.sub(r'\s*&\s*$', '', reading_text)
        return reading_text
    
    return "today's reading"

def create_audio_script(date_code):
    """Create audio script for a specific date"""
    html_file = f"readings/august/{date_code}.html"
    
    if not os.path.exists(html_file):
        print(f"File {html_file} not found!")
        return None
    
    scripture_text = extract_scripture_text(html_file)
    reading_info = get_reading_info(html_file)
    
    if not scripture_text:
        print(f"No scripture text found in {html_file}!")
        return None
    
    # Create personalized intro and outro
    intro = f"""Good morning, my beautiful Julia! It's time for our daily Bible reading together. 
    Today we're reading from {reading_info}. 
    Let's dive into God's Word and see what He has for us today."""
    
    outro = f"""That completes today's reading from {reading_info}. 
    I love you so much, Julia, and I pray that God's Word brings you peace, joy, and strength today. 
    Have a wonderful day, my love!"""
    
    # Combine intro, scripture, and outro
    full_script = f"{intro}\n\n{scripture_text}\n\n{outro}"
    
    return full_script

def generate_polly_audio(script_text, output_file):
    """Generate audio using AWS Polly"""
    try:
        polly = boto3.client('polly', region_name='us-east-1')
        
        # Split text into chunks if too long (Polly has a 3000 character limit)
        max_chars = 2900
        chunks = []
        
        if len(script_text) <= max_chars:
            chunks = [script_text]
        else:
            # Split by sentences to avoid cutting words
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
            print(f"  Generating audio chunk {i+1}/{len(chunks)}")
            
            response = polly.synthesize_speech(
                Text=chunk,
                OutputFormat='mp3',
                VoiceId='Danielle',
                Engine='neural'
            )
            
            audio_data += response['AudioStream'].read()
        
        # Save combined audio
        with open(output_file, 'wb') as f:
            f.write(audio_data)
        
        return True
        
    except Exception as e:
        print(f"  Error generating audio: {e}")
        return False

def upload_to_s3(local_file, s3_key):
    """Upload file to S3"""
    try:
        s3 = boto3.client('s3')
        bucket_name = 'one-year-bible-ekewaka'
        
        s3.upload_file(local_file, bucket_name, s3_key)
        return True
        
    except Exception as e:
        print(f"  Error uploading to S3: {e}")
        return False

def main():
    """Main function to regenerate all corrected audio files"""
    print("Regenerating audio for all dates with corrected book names...")
    
    # Ensure directories exist
    os.makedirs("audio-scripts", exist_ok=True)
    os.makedirs("temp-audio", exist_ok=True)
    
    success_count = 0
    
    for date_code in corrected_dates:
        print(f"\nProcessing {date_code}...")
        
        # Create audio script
        script_text = create_audio_script(date_code)
        if not script_text:
            continue
        
        # Save script
        script_file = f"audio-scripts/{date_code}.txt"
        with open(script_file, 'w', encoding='utf-8') as f:
            f.write(script_text)
        print(f"  Audio script saved: {script_file}")
        
        # Generate audio
        audio_file = f"temp-audio/{date_code}.mp3"
        if generate_polly_audio(script_text, audio_file):
            # Upload to S3
            s3_key = f"2025/august/{date_code}.mp3"
            if upload_to_s3(audio_file, s3_key):
                print(f"  Successfully uploaded to S3: {s3_key}")
                success_count += 1
                # Clean up temp file
                os.remove(audio_file)
            else:
                print(f"  Failed to upload to S3")
        else:
            print(f"  Failed to generate audio")
    
    print(f"\nCompleted! Successfully regenerated {success_count}/{len(corrected_dates)} audio files.")

if __name__ == "__main__":
    main()