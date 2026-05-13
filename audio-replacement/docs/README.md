# Audio Intro/Outro Replacement - Implementation Guide

## Overview

This project replaces personalized intro/outro audio segments (originally addressed to "Julia") on 365 daily Bible reading MP3 files with generic intro/outro segments suitable for a public audience.

## Project Structure

```
audio-replacement/
├── docs/
│   ├── audio-replacement-handoff.md    # Original handoff document
│   └── README.md                       # This file
├── scripts/
│   └── generate-intro-outro-scripts.py # Generates text for all 365 intros/outros
└── intro-outro-scripts/
    ├── 0101_intro.txt                  # January 1st intro text
    ├── 0101_outro.txt                  # January 1st outro text
    ├── 0102_intro.txt
    ├── ...
    └── 1231_outro.txt                  # 730 files total (365 x 2)
```

## What the Scripts Do

### generate-intro-outro-scripts.py

Reads `assets/data/reading-plan.json` and generates plain-text intro/outro scripts for each of the 365 days.

**Key features:**
- Expands all book abbreviations to full names (e.g., "Rev." → "Revelation", "Deut." → "Deuteronomy")
- Formats dates with ordinals (e.g., "January 1st, 2025")
- Replaces hyphens between references with "through" for natural speech
- Escapes SSML-unsafe characters (& → "and")
- Calculates total character count for Polly billing estimation

**Usage:**
```bash
cd c:\Users\Ed\Documents\Post Graduation\Projects\OneYearBible
python audio-replacement\scripts\generate-intro-outro-scripts.py
```

## Intro/Outro Script Templates

### Intro (unique per day, ~8-12 seconds spoken):
> "Welcome to today's One Year Bible reading for [date]. We're so glad you're joining us on this journey of reading through the Bible in one year. Today's passages are [passages]. Let's begin."

### Outro (same for all days, ~5 seconds spoken):
> "That concludes today's reading. May God's word richly bless you today. We look forward to seeing you tomorrow."

## AWS Polly Configuration

| Setting | Value |
|---------|-------|
| Voice | Danielle (Long-Form Neural) |
| Engine | neural |
| Output format | mp3 |
| Sample rate | 24000 Hz |
| AWS Profile | `ekewaka` |

### Cost Estimate

| Metric | Value |
|--------|-------|
| Total characters (all intros + outros) | ~124,000 |
| Neural free tier (first 12 months) | 1,000,000 chars/month |
| Percentage of free tier used | 12.4% |
| Cost if beyond free tier | $16/million chars = ~$2.00 |

**Bottom line: This will cost $0 if within the free tier period.**

### SSML Notes
- Ampersands (`&`) must be escaped as `&amp;` or replaced with "and" (we use "and")
- The generated text files are plain text, NOT wrapped in `<speak>` tags
- When sending to Polly, wrap in `<speak>...</speak>` tags

## Full Pipeline (Steps to Complete)

### Step 1: Generate intro/outro text scripts ✅ DONE
```bash
python audio-replacement\scripts\generate-intro-outro-scripts.py
```

### Step 2: Generate intro/outro audio via Polly (NEXT)
- Use Danielle Long-Form Neural voice
- Output as MP3 files to `audio-replacement/intro-audio/` and `audio-replacement/outro-audio/`

### Step 3: Identify trim points in existing audio
- Use the known intro/outro text from `audio-scripts/MMDD_audio_script.txt` files
- Use Whisper (or pydub silence detection) to find where scripture begins/ends
- The first paragraph = intro to trim, last paragraph = outro to trim

### Step 4: Trim existing audio files
- Download from S3: `s3://one-year-bible-ekewaka/2025/[month]/[MMDD].mp3`
- Remove the intro segment (beginning of file to scripture start)
- Remove the outro segment (scripture end to end of file)
- Save as trimmed scripture-only audio

### Step 5: Splice new intro + scripture + outro
- Concatenate: new intro MP3 + trimmed scripture MP3 + new outro MP3
- Add brief silence (0.5s) between segments for natural transitions
- Export as final MP3

### Step 6: Upload to S3
```bash
aws s3 cp [processed-file] s3://one-year-bible-ekewaka/2025/[month]/[MMDD].mp3 --profile ekewaka
```

### Step 7: Invalidate CloudFront cache
```bash
aws cloudfront create-invalidation --distribution-id [ID] --paths "/2025/*" --profile ekewaka
```

## Abbreviation Mapping (66 books)

The script handles all standard Bible book abbreviations:

| Abbreviation | Full Name |
|-------------|-----------|
| Gen. | Genesis |
| Ex. | Exodus |
| Lev. | Leviticus |
| Num. | Numbers |
| Deut. | Deuteronomy |
| Josh. | Joshua |
| Jdgs. | Judges |
| 1 Sam. | 1 Samuel |
| 2 Sam. | 2 Samuel |
| 1 Kgs. | 1 Kings |
| 2 Kgs. | 2 Kings |
| 1 Chr. | 1 Chronicles |
| 2 Chr. | 2 Chronicles |
| Ez. | Ezra |
| Neh. | Nehemiah |
| Est. | Esther |
| Ps. | Psalms |
| Prov. | Proverbs |
| Eccl. | Ecclesiastes |
| Songs | Song of Solomon |
| Isa. | Isaiah |
| Jer. | Jeremiah |
| Lam. | Lamentations |
| Ezek. | Ezekiel |
| Dan. | Daniel |
| Hos. | Hosea |
| Obad. | Obadiah |
| Jon. | Jonah |
| Mic. | Micah |
| Nah. | Nahum |
| Hab. | Habakkuk |
| Zeph. | Zephaniah |
| Hag. | Haggai |
| Zech. | Zechariah |
| Mal. | Malachi |
| Matt. | Matthew |
| Rom. | Romans |
| 1 Cor. | 1 Corinthians |
| 2 Cor. | 2 Corinthians |
| Gal. | Galatians |
| Eph. | Ephesians |
| Phil. | Philippians |
| Col. | Colossians |
| 1 Thess. | 1 Thessalonians |
| 2 Thess. | 2 Thessalonians |
| 1 Tim. | 1 Timothy |
| 2 Tim. | 2 Timothy |
| Philem. | Philemon |
| Heb. | Hebrews |
| Jas. | James |
| 1 Pet. | 1 Peter |
| 2 Pet. | 2 Peter |
| 1 Jn. | 1 John |
| 2 Jn. | 2 John |
| 3 Jn. | 3 John |
| Rev. | Revelation |

## Reproducing This for a Future Year

To regenerate for a different year (e.g., 2026):

1. Update the year in `generate-intro-outro-scripts.py` (search for `2025` in the `format_date_for_speech` function)
2. Re-run the script
3. Re-generate Polly audio
4. Re-splice with the scripture body audio

If the reading plan changes, update `assets/data/reading-plan.json` first.

## Key AWS Resources

| Resource | Value |
|----------|-------|
| S3 Bucket | `s3://one-year-bible-ekewaka` |
| CloudFront | `https://d24muyyuu3zj8g.cloudfront.net` |
| AWS Profile | `ekewaka` |
| Account | 371751795928 |
| Backup location | `s3://one-year-bible-ekewaka/backups/2025-original-audio/` |

## Restore Instructions

If something goes wrong, restore originals from backup:
```bash
aws s3 cp s3://one-year-bible-ekewaka/backups/2025-original-audio/ s3://one-year-bible-ekewaka/2025/ --recursive --profile ekewaka
```

## Dependencies

- Python 3.x
- AWS CLI with `ekewaka` profile configured
- `boto3` (for Polly script)
- `pydub` + FFmpeg (for audio trimming/splicing)
- `openai-whisper` (optional, for trim point detection)

---

*Created: June 14, 2026*
