// Amazon Polly Text-to-Speech Integration
class PollyTTS {
    constructor() {
        this.isPlaying = false;
        this.currentAudio = null;
    }

    async synthesizeSpeech(text, voiceId = 'Joanna') {
        try {
            const response = await fetch('/api/polly-synthesize', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    text: text,
                    voiceId: voiceId,
                    outputFormat: 'mp3'
                })
            });

            if (!response.ok) throw new Error('Polly synthesis failed');
            
            const audioBlob = await response.blob();
            return URL.createObjectURL(audioBlob);
        } catch (error) {
            console.error('Polly TTS Error:', error);
            return null;
        }
    }

    async playText(text, voiceId = 'Joanna') {
        if (this.isPlaying) this.stop();

        const audioUrl = await this.synthesizeSpeech(text, voiceId);
        if (!audioUrl) return;

        this.currentAudio = new Audio(audioUrl);
        this.currentAudio.onended = () => this.isPlaying = false;
        
        this.isPlaying = true;
        this.currentAudio.play();
    }

    stop() {
        if (this.currentAudio) {
            this.currentAudio.pause();
            this.currentAudio = null;
        }
        this.isPlaying = false;
    }
}

// Initialize Polly TTS
const pollyTTS = new PollyTTS();

// Add TTS buttons to scripture sections
document.addEventListener('DOMContentLoaded', function() {
    const scriptureContainers = document.querySelectorAll('.tab-pane');
    
    scriptureContainers.forEach(container => {
        const ttsButton = document.createElement('button');
        ttsButton.className = 'btn btn-sm btn-outline-secondary mb-3';
        ttsButton.innerHTML = '🔊 Listen';
        ttsButton.onclick = () => {
            const text = container.textContent.replace(/\s+/g, ' ').trim();
            pollyTTS.playText(text);
        };
        
        container.insertBefore(ttsButton, container.firstChild);
    });
});