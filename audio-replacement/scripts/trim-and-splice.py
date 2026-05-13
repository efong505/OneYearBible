"""
Trim old intro/outro from existing audio files and splice in new ones.

Strategy:
- Use Whisper to transcribe the first 30s and last 30s of each file
- Match against known scripture text to find where Bible verses start/end
- Trim the old intro/outro
- Splice: new intro + scripture body + new outro

Usage:
    python trim-and-splice.py 0307              # Process single file
    python trim-and-splice.py 0307 --detect     # Just detect trim points (no splice)
    python trim-and-splice.py --all             # Process all files
"""

import json
import os
import re
import sys
import time

import whisper
from pydub import AudioSegment

# Paths
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
AUDIO_REPLACEMENT_DIR = os.path.dirname(SCRIPT_DIR)
PROJECT_ROOT = os.path.dirname(AUDIO_REPLACEMENT_DIR)

INTRO_AUDIO_DIR = os.path.join(AUDIO_REPLACEMENT_DIR, "intro-outro-audio")
TEMP_AUDIO_DIR = os.path.join(AUDIO_REPLACEMENT_DIR, "temp-audio")
OUTPUT_DIR = os.path.join(AUDIO_REPLACEMENT_DIR, "processed-audio")
AUDIO_SCRIPTS_DIR = os.path.join(PROJECT_ROOT, "audio-scripts")

# Silence padding between segments (milliseconds)
SILENCE_PADDING_MS = 500


def get_first_scripture_line(date_code):
    """Get the first line of scripture from the audio script to match against."""
    script_path = os.path.join(AUDIO_SCRIPTS_DIR, f"{date_code}_audio_script.txt")
    if not os.path.exists(script_path):
        script_path = os.path.join(AUDIO_SCRIPTS_DIR, f"{date_code}.txt")
    if not os.path.exists(script_path):
        return None

    with open(script_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Split into paragraphs
    paragraphs = [p.strip() for p in content.split("\n\n") if p.strip()]

    # The scripture is typically the longest paragraph (the middle one)
    # Skip first paragraph (intro) and find the scripture start
    for i, para in enumerate(paragraphs):
        if i == 0:
            continue  # Skip intro
        # Skip "Today's reading is..." lines and chapter headers
        if para.startswith("Today's reading") or len(para) < 50:
            continue
        # This should be the scripture - return first 10 words
        words = para.split()[:10]
        return " ".join(words)

    return None


def get_last_scripture_words(date_code):
    """Get the last few words of scripture from the audio script."""
    script_path = os.path.join(AUDIO_SCRIPTS_DIR, f"{date_code}_audio_script.txt")
    if not os.path.exists(script_path):
        script_path = os.path.join(AUDIO_SCRIPTS_DIR, f"{date_code}.txt")
    if not os.path.exists(script_path):
        return None

    with open(script_path, "r", encoding="utf-8") as f:
        content = f.read()

    paragraphs = [p.strip() for p in content.split("\n\n") if p.strip()]

    # Last paragraph is the outro - get the one before it
    if len(paragraphs) >= 2:
        # Find the last long paragraph (scripture body)
        for para in reversed(paragraphs[:-1]):
            if len(para) > 100:
                words = para.split()[-10:]
                return " ".join(words)

    return None


def detect_trim_points(audio_path, date_code, model):
    """Use Whisper to find where scripture starts and ends."""
    audio = AudioSegment.from_mp3(audio_path)
    total_duration_ms = len(audio)
    total_duration_s = total_duration_ms / 1000

    # Transcribe the full file (Whisper base model is fast enough for ~7min files)
    result = model.transcribe(audio_path, word_timestamps=True)
    segments = result["segments"]

    if not segments:
        return None, None

    # Find intro end: look for the "Today's reading is..." segment
    # The scripture starts in the segment AFTER that
    intro_end_s = None
    for i, seg in enumerate(segments):
        text = seg["text"].lower()
        if "today" in text and "reading" in text:
            # Scripture starts at the next segment
            if i + 1 < len(segments):
                intro_end_s = segments[i + 1]["start"]
            break
        # Also check for patterns like "let's dive into" or "in his presence"
        if any(phrase in text for phrase in ["let's dive", "his presence", "let's begin", "here we go"]):
            if i + 1 < len(segments):
                intro_end_s = segments[i + 1]["start"]
            break

    # If we couldn't find the pattern, use a fallback: look for the first segment
    # that starts after 10s and contains Bible-like text
    if intro_end_s is None:
        first_scripture = get_first_scripture_line(date_code)
        if first_scripture:
            first_words = first_scripture.lower().split()[:5]
            for seg in segments:
                if seg["start"] > 8:  # Must be after at least 8 seconds
                    seg_words = seg["text"].lower().split()
                    # Check if any of the first scripture words appear
                    if any(w in seg["text"].lower() for w in first_words[:3]):
                        intro_end_s = seg["start"]
                        break

    # If still not found, default to 15 seconds (typical intro length)
    if intro_end_s is None:
        intro_end_s = 15.0

    # Find outro start: look for closing phrases in the last 30 seconds
    outro_start_s = None
    for seg in reversed(segments):
        text = seg["text"].lower()
        if any(phrase in text for phrase in [
            "that's a wrap", "and so we finish", "what a beautiful",
            "carry these words", "julia", "eddie hopes",
            "have a magnificent", "catch you", "until tomorrow",
            "god bless you", "see you tomorrow", "that concludes"
        ]):
            outro_start_s = seg["start"]
            break

    # If not found, look for the last segment that's clearly not scripture
    if outro_start_s is None:
        last_scripture = get_last_scripture_words(date_code)
        if last_scripture:
            last_words = last_scripture.lower().split()[-5:]
            for i, seg in enumerate(segments):
                if any(w in seg["text"].lower() for w in last_words):
                    # Outro starts at the next segment
                    if i + 1 < len(segments):
                        outro_start_s = segments[i + 1]["start"]

    # If still not found, default to last 15 seconds
    if outro_start_s is None:
        outro_start_s = total_duration_s - 15.0

    return intro_end_s, outro_start_s


def splice_audio(date_code, scripture_audio, output_path):
    """Splice new intro + scripture + new outro."""
    intro_path = os.path.join(INTRO_AUDIO_DIR, f"{date_code}_intro.mp3")
    outro_path = os.path.join(INTRO_AUDIO_DIR, f"{date_code}_outro.mp3")

    if not os.path.exists(intro_path) or not os.path.exists(outro_path):
        print(f"  ERROR: Missing intro/outro audio for {date_code}")
        return False

    intro_audio = AudioSegment.from_mp3(intro_path)
    outro_audio = AudioSegment.from_mp3(outro_path)
    silence = AudioSegment.silent(duration=SILENCE_PADDING_MS)

    # Concatenate: intro + silence + scripture + silence + outro
    final_audio = intro_audio + silence + scripture_audio + silence + outro_audio

    # Export
    final_audio.export(output_path, format="mp3", bitrate="48k",
                       parameters=["-ar", "24000", "-ac", "1"])
    return True


def process_file(date_code, model, detect_only=False):
    """Process a single audio file."""
    audio_path = os.path.join(TEMP_AUDIO_DIR, f"{date_code}.mp3")

    if not os.path.exists(audio_path):
        print(f"  ERROR: {audio_path} not found. Download it first.")
        return False

    print(f"  Detecting trim points for {date_code}...")
    intro_end_s, outro_start_s = detect_trim_points(audio_path, date_code, model)

    print(f"  Intro ends at: {intro_end_s:.1f}s")
    print(f"  Outro starts at: {outro_start_s:.1f}s")
    print(f"  Scripture duration: {outro_start_s - intro_end_s:.1f}s")

    if detect_only:
        return True

    # Load and trim
    audio = AudioSegment.from_mp3(audio_path)
    scripture_body = audio[int(intro_end_s * 1000):int(outro_start_s * 1000)]

    # Splice
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    output_path = os.path.join(OUTPUT_DIR, f"{date_code}.mp3")
    success = splice_audio(date_code, scripture_body, output_path)

    if success:
        final = AudioSegment.from_mp3(output_path)
        print(f"  Output: {output_path}")
        print(f"  Final duration: {len(final)/1000:.1f}s")

    return success


def main():
    detect_only = "--detect" in sys.argv
    process_all = "--all" in sys.argv

    date_codes = []
    for arg in sys.argv[1:]:
        if arg.isdigit() and len(arg) == 4:
            date_codes.append(arg)

    if not date_codes and not process_all:
        print("Usage:")
        print("  python trim-and-splice.py 0307              # Process single file")
        print("  python trim-and-splice.py 0307 --detect     # Just detect trim points")
        print("  python trim-and-splice.py --all             # Process all files")
        return

    if process_all:
        # Get all files in temp-audio
        date_codes = sorted(
            f.replace(".mp3", "")
            for f in os.listdir(TEMP_AUDIO_DIR)
            if f.endswith(".mp3")
        )

    print(f"Loading Whisper model (base)...")
    model = whisper.load_model("base")
    print(f"Model loaded.\n")

    success = 0
    errors = 0

    for i, code in enumerate(date_codes):
        print(f"[{i+1}/{len(date_codes)}] Processing {code}...")
        if process_file(code, model, detect_only):
            success += 1
        else:
            errors += 1
        print()

    print(f"Done. Success: {success}, Errors: {errors}")


if __name__ == "__main__":
    main()
