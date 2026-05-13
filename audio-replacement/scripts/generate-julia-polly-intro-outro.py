"""
Generate Julia's intro/outro audio files using AWS Polly (Danielle Long-Form Neural).
Reads text from julia-intro-outro-scripts/ and outputs MP3 files.

Usage:
    python generate-julia-polly-intro-outro.py          # Generate all 365
    python generate-julia-polly-intro-outro.py 0101     # Generate single day
    python generate-julia-polly-intro-outro.py --dry-run  # Show what would be generated
"""

import boto3
import os
import sys
import time

AWS_PROFILE = "ekewaka"
AWS_REGION = "us-east-1"
VOICE_ID = "Danielle"
ENGINE = "long-form"
OUTPUT_FORMAT = "mp3"
SAMPLE_RATE = "24000"


def synthesize_speech(polly_client, text, output_path):
    """Call Polly to synthesize text and save as MP3."""
    ssml_text = f"<speak>{text}</speak>"

    response = polly_client.synthesize_speech(
        Text=ssml_text,
        TextType="ssml",
        OutputFormat=OUTPUT_FORMAT,
        VoiceId=VOICE_ID,
        Engine=ENGINE,
        SampleRate=SAMPLE_RATE,
    )

    with open(output_path, "wb") as f:
        f.write(response["AudioStream"].read())


def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    audio_replacement_dir = os.path.dirname(script_dir)
    input_dir = os.path.join(audio_replacement_dir, "julia-intro-outro-scripts")
    output_dir = os.path.join(audio_replacement_dir, "julia-intro-outro-audio")
    os.makedirs(output_dir, exist_ok=True)

    # Parse arguments
    dry_run = "--dry-run" in sys.argv
    single_day = None
    for arg in sys.argv[1:]:
        if arg.isdigit() and len(arg) == 4:
            single_day = arg

    # Get list of intro and outro files to process
    if single_day:
        files = [f"{single_day}_intro.txt", f"{single_day}_outro.txt"]
    else:
        files = sorted(f for f in os.listdir(input_dir) if f.endswith(".txt"))

    # Verify files exist
    for f in files:
        if not os.path.exists(os.path.join(input_dir, f)):
            print(f"ERROR: {f} not found in {input_dir}")
            return

    total_chars = 0
    for f in files:
        with open(os.path.join(input_dir, f), "r", encoding="utf-8") as fh:
            total_chars += len(fh.read())

    print(f"Files to process: {len(files)}")
    print(f"Total characters: {total_chars:,}")
    print(f"Voice: {VOICE_ID} ({ENGINE})")
    print(f"Output: {output_dir}")
    print()

    if dry_run:
        print("[DRY RUN] No audio will be generated.")
        print(f"Sample files that would be created:")
        for f in files[:8]:
            mp3_name = f.replace(".txt", ".mp3")
            print(f"  {mp3_name}")
        if len(files) > 8:
            print(f"  ... and {len(files) - 8} more")
        return

    # Initialize Polly client
    session = boto3.Session(profile_name=AWS_PROFILE)
    polly_client = session.client("polly", region_name=AWS_REGION)

    # Generate audio
    success = 0
    errors = 0
    start_time = time.time()

    for i, f in enumerate(files):
        txt_path = os.path.join(input_dir, f)
        mp3_name = f.replace(".txt", ".mp3")
        mp3_path = os.path.join(output_dir, mp3_name)

        # Skip if already generated
        if os.path.exists(mp3_path):
            print(f"  [{i+1}/{len(files)}] SKIP (exists): {mp3_name}")
            success += 1
            continue

        with open(txt_path, "r", encoding="utf-8") as fh:
            text = fh.read().strip()

        try:
            synthesize_speech(polly_client, text, mp3_path)
            success += 1
            print(f"  [{i+1}/{len(files)}] OK: {mp3_name}")
        except Exception as e:
            errors += 1
            print(f"  [{i+1}/{len(files)}] ERROR: {mp3_name} - {e}")

        # Small delay to avoid throttling
        if i % 20 == 19:
            time.sleep(1)

    elapsed = time.time() - start_time
    print(f"\nDone in {elapsed:.1f}s")
    print(f"Success: {success}, Errors: {errors}")
    print(f"Audio files saved to: {output_dir}")


if __name__ == "__main__":
    main()
