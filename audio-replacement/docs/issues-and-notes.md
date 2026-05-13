# Audio Replacement - Issues & Notes

## Known Issues

### 0307.mp3 - Missing Old Testament Scripture
- **Problem**: The audio file and `0307_audio_script.txt` only contain Luke 4 (New Testament). The Old Testament reading (Leviticus 27 through Numbers 1:29) is completely missing.
- **File size**: 2.4 MB (compared to typical 5-7 MB for complete readings)
- **Root cause**: The original script generation likely failed to include the OT portion.
- **Fix needed**: Extract OT text from `march/0307.html`, generate OT audio via Polly (Danielle Long-Form), then splice: new intro + OT audio + existing NT audio (trimmed) + new outro.
- **OT text length**: ~8,500 characters (within free tier)
- **Status**: Deferred — will fix after main trim-and-splice pipeline is validated.

### 0306.mp3 - Verified Complete
- **Initially suspected** to be missing OT, but confirmed it contains both Leviticus 25:47-26:46 AND Luke 3.
- **File size**: 5.7 MB (normal)
- **Status**: No issue. Process normally with trim-and-splice.

## Action Items
- [ ] Fix 0307 by generating missing OT audio and splicing with existing NT
- [ ] After fixing, verify the final 0307.mp3 has both OT and NT readings
- [ ] Check if any other days have similar missing content (scan file sizes for anomalies)

## Potential Check: Find Other Incomplete Files
Run this to find suspiciously small files that might be missing content:
```bash
aws s3 ls s3://one-year-bible-ekewaka/2025/ --recursive --profile ekewaka | sort -k3 -n | head -20
```
Or locally after downloading, check files under 3MB which may indicate missing OT/NT portions.

---

*Created: June 14, 2026*
