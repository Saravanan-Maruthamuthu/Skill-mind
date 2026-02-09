// Video Interview Handler with Facial Expression Analysis
const videoInterview = {
    isVideoMode: true,  // Mandatory video mode
    videoStream: null,
    faceApiLoaded: false,
    detectionInterval: null,
    recognition: null,
    synthesis: window.speechSynthesis,
    attentionTracker: null,
    attentionSendInterval: null,

    // Initialize video interview
    async init() {
        try {
            // Load face-api.js models
            await this.loadFaceApiModels();
            this.faceApiLoaded = true;
            console.log('Face-api.js models loaded successfully');
        } catch (error) {
            console.error('Failed to load face-api.js models:', error);
            this.faceApiLoaded = false;
        }

        // Initialize speech recognition if available
        if ('webkitSpeechRecognition' in window || 'SpeechRecognition' in window) {
            const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
            this.recognition = new SpeechRecognition();
            this.recognition.continuous = false;
            this.recognition.interimResults = false;
            this.recognition.lang = 'en-US';
        }
    },

    // Load face-api.js models
    async loadFaceApiModels() {
        const MODEL_URL = 'https://cdn.jsdelivr.net/npm/@vladmandic/face-api/model/';

        await faceapi.nets.tinyFaceDetector.loadFromUri(MODEL_URL);
        await faceapi.nets.faceExpressionNet.loadFromUri(MODEL_URL);
        await faceapi.nets.faceLandmark68Net.loadFromUri(MODEL_URL);
    },

    // Start video interview (without eye tracking)
    async startVideoInterview() {
        // Ensure any previous stream is stopped to prevent conflicts
        this.stopVideoInterview();

        try {
            // Request camera permission
            this.videoStream = await navigator.mediaDevices.getUserMedia({
                video: { width: 640, height: 480 },
                audio: false
            });

            // Display video feed
            const videoElement = document.getElementById('videoFeed');
            if (videoElement) {
                videoElement.srcObject = this.videoStream;
                videoElement.play();
            }

            // Eye tracking disabled - removed to prevent platform conflicts
            // and simplify the interview process

            // Start emotion detection
            this.startEmotionDetection();

            this.isVideoMode = true;
            this.updateUI();

            app.showSuccess('Video mode started successfully!');
            return true;
        } catch (error) {
            console.error('Camera access error:', error);

            let errorMessage = 'Unable to access camera. ';

            if (error.name === 'NotAllowedError' || error.name === 'PermissionDeniedError') {
                errorMessage += 'Please allow camera access in your browser settings. Video mode is required for this interview.';
            } else if (error.name === 'NotFoundError' || error.name === 'DevicesNotFoundError') {
                errorMessage += 'No camera device found. Please connect a camera to continue.';
            } else if (error.name === 'NotReadableError' || error.name === 'TrackStartError') {
                errorMessage += 'Camera is currently in use by another application. Please close other apps (Zoom, Teams, etc.) and try again.';
            } else {
                errorMessage += 'Please check your device settings or try a different browser.';
            }

            app.showError(errorMessage);
            return false;
        }
    },

    // Stop video interview
    stopVideoInterview() {
        if (this.videoStream) {
            this.videoStream.getTracks().forEach(track => track.stop());
            this.videoStream = null;
        }

        if (this.detectionInterval) {
            clearInterval(this.detectionInterval);
            this.detectionInterval = null;
        }

        // Attention tracking removed - no cleanup needed

        this.isVideoMode = false;
        this.updateUI();
    },

    // Start emotion detection
    startEmotionDetection() {
        if (!this.faceApiLoaded) {
            console.warn('Face-api.js not loaded, skipping emotion detection');
            return;
        }

        const videoElement = document.getElementById('videoFeed');

        // Detect emotions every 2 seconds
        this.detectionInterval = setInterval(async () => {
            try {
                const detections = await faceapi
                    .detectSingleFace(videoElement, new faceapi.TinyFaceDetectorOptions())
                    .withFaceLandmarks()
                    .withFaceExpressions();

                if (detections) {
                    this.processEmotionData(detections.expressions);
                }
            } catch (error) {
                console.error('Emotion detection error:', error);
            }
        }, 2000);
    },

    // Process and send emotion data
    async processEmotionData(expressions) {
        // Find dominant emotion
        let maxEmotion = 'neutral';
        let maxConfidence = 0;

        for (const [emotion, confidence] of Object.entries(expressions)) {
            if (confidence > maxConfidence) {
                maxConfidence = confidence;
                maxEmotion = emotion;
            }
        }

        // Display emotion on UI
        this.displayEmotion(maxEmotion, maxConfidence);

        // Send to backend
        await this.sendEmotionData(maxEmotion, maxConfidence);
    },

    // Send emotion data to backend
    async sendEmotionData(emotion, confidence) {
        try {
            await fetch(`${app.apiUrl}/analyze-emotion`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    session_id: app.sessionId,
                    emotion: emotion,
                    confidence: confidence,
                    timestamp: new Date().toISOString()
                })
            });
        } catch (error) {
            console.error('Failed to send emotion data:', error);
        }
    },

    // Display emotion on UI
    displayEmotion(emotion, confidence) {
        const emotionDisplay = document.getElementById('emotionDisplay');
        if (!emotionDisplay) return;

        const emotionEmojis = {
            'happy': '😊',
            'sad': '😢',
            'angry': '😠',
            'neutral': '😐',
            'surprised': '😲',
            'fearful': '😨',
            'disgusted': '🤢'
        };

        const emoji = emotionEmojis[emotion] || '😐';
        const percentage = (confidence * 100).toFixed(0);

        emotionDisplay.innerHTML = `
            <div class="emotion-indicator">
                <span class="emotion-emoji">${emoji}</span>
                <span class="emotion-label">${emotion}</span>
                <span class="emotion-confidence">${percentage}%</span>
            </div>
        `;
    },

    // Start speech recognition
    startSpeechRecognition() {
        return new Promise((resolve, reject) => {
            if (!this.recognition) {
                reject(new Error('Speech recognition not supported'));
                return;
            }

            this.recognition.onresult = (event) => {
                const transcript = event.results[0][0].transcript;
                resolve(transcript);
            };

            this.recognition.onerror = (event) => {
                reject(event.error);
            };

            this.recognition.start();
        });
    },

    // Speak text using text-to-speech
    speakText(text) {
        if (!this.synthesis) {
            console.warn('Speech synthesis not supported');
            return;
        }

        // Cancel any ongoing speech
        this.synthesis.cancel();

        const utterance = new SpeechSynthesisUtterance(text);
        utterance.rate = 0.9;
        utterance.pitch = 1.0;
        utterance.volume = 1.0;

        this.synthesis.speak(utterance);
    },

    // Attention tracking methods removed - feature disabled

    // Update UI based on video mode (always video mode now)
    updateUI() {
        const videoContainer = document.getElementById('videoContainer');
        if (videoContainer) videoContainer.style.display = 'block';
    },

    // Auto-start video mode when interview begins
    async autoStartInterview() {
        const success = await this.startVideoInterview();
        if (!success) {
            app.showError('Unable to start video interview. Please check your camera and try again.');
            return false;
        }
        return true;
    },

    // Send response (voice or text)
    async sendResponse() {
        let response = '';

        if (this.isVideoMode && this.recognition) {
            try {
                // Show listening indicator
                this.showListeningIndicator();

                // Get voice input
                response = await this.startSpeechRecognition();

                // Hide listening indicator
                this.hideListeningIndicator();
            } catch (error) {
                this.hideListeningIndicator();

                // Handle different error types with appropriate messages
                let promptMessage = 'Please type your response:';

                // Only log unexpected errors (network errors are common without internet)
                if (error === 'no-speech') {
                    // Silent - user didn't speak within timeout
                    promptMessage = 'No speech detected. Please type your response:';
                } else if (error === 'aborted') {
                    // Silent - user cancelled
                    promptMessage = 'Please type your response:';
                } else if (error === 'network') {
                    // Network error - requires internet connection
                    console.warn('Speech recognition requires internet connection. Falling back to text input.');
                    promptMessage = 'Voice recognition requires internet. Please type your response:';
                } else {
                    // Other unexpected errors
                    console.error('Speech recognition error:', error);
                    promptMessage = 'Voice recognition failed. Please type your response:';
                }

                response = prompt(promptMessage);

                if (!response) return;
            }
        } else {
            // Text mode
            const input = document.getElementById('chatInput');
            response = input ? input.value.trim() : '';
            if (input) input.value = '';
        }

        if (!response) return;

        // Add message to chat
        hrInterview.addMessage(response, 'candidate');

        // Send to backend and get AI response
        const aiResponse = await hrInterview.sendResponse(response);

        // Speak AI response if in video mode
        if (this.isVideoMode && aiResponse) {
            this.speakText(aiResponse);
        }
    },

    // Show listening indicator
    showListeningIndicator() {
        const indicator = document.getElementById('listeningIndicator');
        if (indicator) {
            indicator.style.display = 'block';
            indicator.innerHTML = '🎤 Listening...';
        }
    },

    // Hide listening indicator
    hideListeningIndicator() {
        const indicator = document.getElementById('listeningIndicator');
        if (indicator) {
            indicator.style.display = 'none';
        }
    }
};

// Initialize video interview when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    videoInterview.init();
});
