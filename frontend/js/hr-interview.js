// HR Interview Handler
const hrInterview = {
    // Start interview
    async startInterview() {
        try {
            // First, start video mode
            app.showInfo('Initializing video interview...');
            const videoStarted = await videoInterview.autoStartInterview();

            if (!videoStarted) {
                app.showError('Video mode is required for the HR interview. Please allow camera access.');
                return;
            }

            // Then start the interview conversation
            const response = await fetch(`${app.apiUrl}/start-interview`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    session_id: app.sessionId
                })
            });

            const data = await response.json();

            if (data.success) {
                this.addMessage(data.message, 'interviewer');
                // Speak the first question
                if (videoInterview.synthesis) {
                    videoInterview.speakText(data.message);
                }
            } else {
                throw new Error(data.error || 'Failed to start interview');
            }
        } catch (error) {
            console.error('Interview start error:', error);
            app.showError(error.message);
        }
    },

    // Send response
    async sendResponse(responseText = null) {
        const input = document.getElementById('chatInput');
        const response = responseText || (input ? input.value.trim() : '');

        if (!response) {
            return null;
        }

        // Add candidate message
        this.addMessage(response, 'candidate');
        if (input && !responseText) input.value = '';

        // Show typing indicator
        this.showTypingIndicator();

        try {
            const apiResponse = await fetch(`${app.apiUrl}/interview-response`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    session_id: app.sessionId,
                    response: response
                })
            });

            const data = await apiResponse.json();

            // Remove typing indicator
            this.removeTypingIndicator();

            if (data.success) {
                this.addMessage(data.message, 'interviewer');
                return data.message; // Return message for TTS
            } else {
                throw new Error(data.error || 'Failed to get response');
            }
        } catch (error) {
            console.error('Interview response error:', error);
            this.removeTypingIndicator();
            app.showError(error.message);
            return null;
        }
    },

    // Add message to chat
    addMessage(text, sender) {
        const messagesContainer = document.getElementById('chatMessages');
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${sender}`;
        messageDiv.textContent = text;
        messagesContainer.appendChild(messageDiv);

        // Scroll to bottom
        messagesContainer.scrollTop = messagesContainer.scrollHeight;
    },

    // Show typing indicator
    showTypingIndicator() {
        const messagesContainer = document.getElementById('chatMessages');
        const typingDiv = document.createElement('div');
        typingDiv.className = 'message interviewer typing-indicator';
        typingDiv.id = 'typingIndicator';
        typingDiv.innerHTML = '<span>●</span><span>●</span><span>●</span>';
        messagesContainer.appendChild(typingDiv);
        messagesContainer.scrollTop = messagesContainer.scrollHeight;
    },

    // Remove typing indicator
    removeTypingIndicator() {
        const indicator = document.getElementById('typingIndicator');
        if (indicator) {
            indicator.remove();
        }
    },

    // End interview
    async endInterview() {
        if (!confirm('Are you sure you want to end the interview?')) {
            return;
        }

        try {
            const response = await fetch(`${app.apiUrl}/end-interview`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    session_id: app.sessionId
                })
            });

            const data = await response.json();

            if (data.success) {
                this.addMessage(data.closing_message, 'interviewer');

                // Move to results after a delay
                setTimeout(() => {
                    app.goToStep(6);
                    resultsDashboard.displayResults();
                }, 3000);
            } else {
                throw new Error(data.error || 'Failed to end interview');
            }
        } catch (error) {
            console.error('End interview error:', error);
            app.showError(error.message);
        }
    }
};
