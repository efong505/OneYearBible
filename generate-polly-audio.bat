@echo off
echo Generating audio with Polly and uploading to S3...
echo Make sure AWS credentials are configured!
echo.
python generate-polly-audio.py
pause