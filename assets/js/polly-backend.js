// Backend API for Amazon Polly integration (Node.js/Express)
const AWS = require('aws-sdk');
const express = require('express');
const app = express();

// Configure AWS Polly
const polly = new AWS.Polly({
    region: 'us-east-1' // Change to your preferred region
});

app.use(express.json());

app.post('/api/polly-synthesize', async (req, res) => {
    try {
        const { text, voiceId = 'Joanna', outputFormat = 'mp3' } = req.body;

        const params = {
            Text: text,
            OutputFormat: outputFormat,
            VoiceId: voiceId,
            TextType: 'text'
        };

        const result = await polly.synthesizeSpeech(params).promise();
        
        res.set({
            'Content-Type': `audio/${outputFormat}`,
            'Content-Length': result.AudioStream.length
        });
        
        res.send(result.AudioStream);
    } catch (error) {
        console.error('Polly Error:', error);
        res.status(500).json({ error: 'Text-to-speech synthesis failed' });
    }
});

app.listen(3000, () => {
    console.log('Polly TTS server running on port 3000');
});