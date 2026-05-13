# Audio Intro/Outro Replacement - Handoff Document

## Project Goal
Replace the personalized intro/outro (addressed to "Julia") on all 365 daily Bible reading audio files with a generic intro/outro suitable for all listeners.

## Current State
- **Original audio files backed up** to `s3://one-year-bible-ekewaka/backups/2025-original-audio/`
- **Live audio files** are at `s3://one-year-bible-ekewaka/2025/[month]/[filename].mp3`
- **CloudFront URL**: `https://d24muyyuu3zj8g.cloudfront.net/2025/[month]/[filename].mp3`
- **File naming**: `0307.mp3` (MMDD format) per month folder
- **Total files**: ~365 MP3 files across 12 month folders
- **Total size**: ~6.3 GB
- **AWS Profile**: Use `--profile ekewaka` (account 371751795928)

## The Problem
- Each audio file has a randomized intro and outro addressed to the user's wife
- The intros/outros are NOT consistent in length or phrasing (5-6 random variations were used)
- Cannot simply trim by fixed time

## Proposed Solution
1. **Use OpenAI Whisper** (free, local) to transcribe each audio file with timestamps
2. **Compare transcription against known scripture text** (available in the HTML files at `readings/[month]/[MMDD].html`)
3. **Find the timestamp where the first Bible verse begins** → trim point for intro
4. **Find the timestamp where the last Bible verse ends** → trim point for outro
5. **Use pydub + FFmpeg** to trim the audio and splice in new generic intro/outro
6. **Upload processed files** back to S3, replacing the originals

## Why This Approach Works
- The Bible text for each day is known (it's in the HTML pages and `reading-plan.json`)
- Whisper provides word-level timestamps
- Matching the transcription against known scripture text is more reliable than trying to detect random intro phrases

## Tools Needed
- `pip install openai-whisper` (speech-to-text, runs locally)
- `pip install pydub` (audio manipulation)
- FFmpeg installed locally (pydub dependency)
- AWS CLI with `--profile ekewaka`

## Next Steps
1. **Install Whisper**: `pip install openai-whisper`
2. **Install FFmpeg** if not already installed: check with `ffmpeg -version`
3. **Download a sample audio file** for testing:
   ```bash
   aws s3 cp s3://one-year-bible-ekewaka/2025/march/0307.mp3 ./audio-test/0307.mp3 --profile ekewaka
   ```
4. **Test Whisper transcription** on the sample to see output format and timestamps
5. **Extract known scripture text** from the corresponding HTML file
6. **Build a matching algorithm** to find where scripture starts/ends in the transcription
7. **Trim and splice** using pydub
8. **Test on a few files** before batch processing all 365
9. **For new intro/outro**: Decide on approach (record yourself, or use free TTS like Edge TTS)
10. **Batch process** all files and upload to S3

## Key Files & Locations
| Item | Location |
|------|----------|
| Live audio | `s3://one-year-bible-ekewaka/2025/[month]/[MMDD].mp3` |
| Backup audio | `s3://one-year-bible-ekewaka/backups/2025-original-audio/` |
| Reading HTML files | `readings/[month]/[MMDD].html` (local project) |
| Reading plan JSON | `assets/data/reading-plan.json` |
| Project root | `c:\Users\Ed\Documents\Post Graduation\Projects\OneYearBible` |

## Restore Instructions (if something goes wrong)
```bash
aws s3 cp s3://one-year-bible-ekewaka/backups/2025-original-audio/ s3://one-year-bible-ekewaka/2025/ --recursive --profile ekewaka
```

## Open Questions for Next Session
- What should the new generic intro/outro say? (e.g., "Welcome to today's Bible reading for [date]. Today we'll be reading [passages]...")
- Record your own voice or use free TTS (Edge TTS)?
- Process all 365 at once or do a month at a time?

---

*Created: June 14, 2026*
