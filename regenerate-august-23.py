import os
import re
import boto3
from datetime import datetime

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

def create_audio_script():
    """Create audio script for August 23rd"""
    html_file = "readings/august/0823.html"
    
    if not os.path.exists(html_file):
        print(f"File {html_file} not found!")
        return None
    
    scripture_text = extract_scripture_text(html_file)
    
    if not scripture_text:
        print("No scripture text found!")
        return None
    
    # Create personalized intro and outro
    intro = """Good morning, my beautiful Julia! It's time for our daily Bible reading together. 
    Today we're reading from Nehemiah chapter 13 and Esther chapters 1 through 2 verse 18. 
    Let's dive into God's Word and see what He has for us today."""
    
    outro = """That completes today's reading from Nehemiah 13 and Esther 1 through 2 verse 18. 
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
            print(f"Generating audio for chunk {i+1}/{len(chunks)}")
            
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
        
        print(f"Audio generated: {output_file}")
        return True
        
    except Exception as e:
        print(f"Error generating audio: {e}")
        return False

def upload_to_s3(local_file, s3_key):
    """Upload file to S3"""
    try:
        s3 = boto3.client('s3')
        bucket_name = 'one-year-bible-ekewaka'  # Your S3 bucket
        
        s3.upload_file(local_file, bucket_name, s3_key)
        print(f"Uploaded to S3: s3://{bucket_name}/{s3_key}")
        return True
        
    except Exception as e:
        print(f"Error uploading to S3: {e}")
        return False

def main():
    """Main function to regenerate August 23rd audio"""
    print("Regenerating August 23rd audio script and Polly audio...")
    
    # Create audio script
    script_text = create_audio_script()
    if not script_text:
        return
    
    # Ensure directories exist
    os.makedirs("audio-scripts", exist_ok=True)
    os.makedirs("temp-audio", exist_ok=True)
    
    # Save script
    script_file = "audio-scripts/0823.txt"
    with open(script_file, 'w', encoding='utf-8') as f:
        f.write(script_text)
    print(f"Audio script saved: {script_file}")
    
    # Generate audio
    audio_file = "temp-audio/0823.mp3"
    if generate_polly_audio(script_text, audio_file):
        # Upload to S3
        s3_key = "2025/august/0823.mp3"
        if upload_to_s3(audio_file, s3_key):
            print("Successfully regenerated August 23rd audio!")
            # Clean up temp file
            os.remove(audio_file)
        else:
            print("Failed to upload to S3")
    else:
        print("Failed to generate audio")

if __name__ == "__main__":
    main()