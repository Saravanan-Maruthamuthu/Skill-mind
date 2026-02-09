// Quiz Interface Handler
const quizInterface = {
    timerInterval: null,
    timeRemaining: 0,

    // Helper to escape HTML to prevent tags from rendering invisibly
    escapeHtml(text) {
        if (!text) return text;
        return text
            .replace(/&/g, "&amp;")
            .replace(/</g, "&lt;")
            .replace(/>/g, "&gt;")
            .replace(/"/g, "&quot;")
            .replace(/'/g, "&#039;");
    },

    // Generate quiz
    async generateQuiz() {
        try {
            const response = await fetch(`${app.apiUrl}/generate-quiz`, {
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
                app.quiz = data.quiz;
                app.currentQuestionIndex = 0;
                app.userAnswers = {};

                // Validate that we have questions
                if (!app.quiz.mcq_questions || app.quiz.mcq_questions.length === 0) {
                    throw new Error('No questions were generated. This may be due to an API error. Please try again.');
                }

                // Start timer
                this.timeRemaining = data.quiz.time_limit_mcq * 60; // Convert to seconds
                this.startTimer();

                // Display first question
                this.displayQuestion(0);
            } else {
                throw new Error(data.error || 'Failed to generate quiz');
            }
        } catch (error) {
            console.error('Quiz generation error:', error);
            app.showError(error.message);
        }
    },

    // Display question
    displayQuestion(index) {
        const question = app.quiz.mcq_questions[index];
        const container = document.getElementById('quizContent');

        // Update counter
        document.getElementById('questionCounter').textContent =
            `Question ${index + 1} of ${app.quiz.mcq_questions.length}`;

        // Build question HTML
        let html = `
            <div class="question-card">
                <div class="question-text">
                    <strong>Q${index + 1}.</strong> ${question.question}
                </div>
                <div class="options">
        `;

        const optionKeys = ['A', 'B', 'C', 'D'];
        const userAnswer = app.userAnswers[index];
        const correctAnswer = question.correct_answer;
        const isAnswered = userAnswer !== undefined;

        // Shuffle options if not already shuffled for this question
        if (!question.shuffled_options) {
            // Create array of option entries
            const optionEntries = optionKeys
                .filter(key => question.options[key])
                .map(key => ({ key, value: question.options[key] }));

            // Shuffle the array
            for (let i = optionEntries.length - 1; i > 0; i--) {
                const j = Math.floor(Math.random() * (i + 1));
                [optionEntries[i], optionEntries[j]] = [optionEntries[j], optionEntries[i]];
            }

            // Store shuffled order
            question.shuffled_options = optionEntries;
        }

        // Use shuffled options
        // We want the UI labels to be A, B, C, D in order, regardless of which content is there.
        const positionLabels = ['A', 'B', 'C', 'D'];

        question.shuffled_options.forEach((option, idx) => {
            const originalKey = option.key;      // e.g., 'C' (the correct answer key from backend)
            const visualLabel = positionLabels[idx]; // e.g., 'A' (because it's the first option shown)

            // We need to check if this specific option (originalKey) matches the user's stored answer.
            // app.userAnswers stores the ORIGINAL KEY (e.g., 'C').
            const isSelected = userAnswer === originalKey;
            const isCorrect = originalKey === correctAnswer;

            let optionClass = 'option';
            let feedbackHtml = '';

            if (isAnswered) {
                // Show feedback after answer is selected
                if (isSelected && isCorrect) {
                    optionClass += ' correct';
                    feedbackHtml = '<span class="feedback-icon">✓</span>';
                } else if (isSelected && !isCorrect) {
                    optionClass += ' incorrect';
                    feedbackHtml = '<span class="feedback-text">✗ Incorrect</span>';
                } else if (isCorrect) {
                    // Show correct answer even if not selected
                    optionClass += ' correct';
                    feedbackHtml = '<span class="feedback-icon">✓</span>';
                }
            } else if (isSelected) {
                optionClass += ' selected';
            }

            const rawValue = option.value ? option.value : '';
            const escapedValue = this.escapeHtml(rawValue);
            const optionText = rawValue ? escapedValue : '<span class="text-muted fst-italic">Option text missing</span>';

            html += `
                <div class="${optionClass}" onclick="quizInterface.selectAnswer(${index}, '${originalKey}')">
                    <div class="option-content">
                        <span class="option-label">${visualLabel}</span>
                        <span class="option-text">${optionText}</span>
                    </div>
                    ${feedbackHtml}
                </div>
            `;
        });

        html += `
                </div>
            </div>
        `;

        container.innerHTML = html;

        // Update navigation buttons
        document.getElementById('prevBtn').style.display = index === 0 ? 'none' : 'inline-block';
        document.getElementById('nextBtn').style.display =
            index === app.quiz.mcq_questions.length - 1 ? 'none' : 'inline-block';
        document.getElementById('submitQuizBtn').style.display =
            index === app.quiz.mcq_questions.length - 1 ? 'inline-block' : 'none';
    },

    // Select answer
    selectAnswer(questionIndex, originalKey) {
        // We store the original key (e.g., 'C') so backend validation works
        app.userAnswers[questionIndex] = originalKey;
        this.displayQuestion(questionIndex);
    },

    // Start timer
    startTimer() {
        this.timerInterval = setInterval(() => {
            this.timeRemaining--;

            const minutes = Math.floor(this.timeRemaining / 60);
            const seconds = this.timeRemaining % 60;

            document.getElementById('timeRemaining').textContent =
                `${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`;

            if (this.timeRemaining <= 0) {
                clearInterval(this.timerInterval);
                this.submitQuiz();
            }
        }, 1000);
    },

    // Submit quiz
    async submitQuiz() {
        clearInterval(this.timerInterval);

        try {
            const response = await fetch(`${app.apiUrl}/submit-quiz`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    session_id: app.sessionId,
                    answers: app.userAnswers
                })
            });

            const data = await response.json();

            if (data.success) {
                app.showSuccess('Quiz submitted successfully!');
                return true;
            } else {
                throw new Error(data.error || 'Failed to submit quiz');
            }
        } catch (error) {
            console.error('Quiz submission error:', error);
            app.showError(error.message);
            return false;
        }
    }
};
