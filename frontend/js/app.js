// Main Application State and Controller
const app = {
    currentStep: 1,
    sessionId: null,
    resumeData: null,
    skillAnalysis: null,
    quiz: null,
    currentQuestionIndex: 0,
    userAnswers: {},

    // API Base URL - use relative path to avoid CORS issues
    apiUrl: '/api',

    // Initialize the application
    init() {
        console.log('AI Interview Assistant initialized');
        this.setupEventListeners();
    },

    // Setup event listeners
    setupEventListeners() {
        // File input change
        document.getElementById('fileInput').addEventListener('change', (e) => {
            if (e.target.files.length > 0) {
                resumeUpload.handleFileSelect(e.target.files[0]);
            }
        });

        // Drag and drop
        const uploadArea = document.getElementById('uploadArea');
        uploadArea.addEventListener('dragover', (e) => {
            e.preventDefault();
            uploadArea.classList.add('dragover');
        });

        uploadArea.addEventListener('dragleave', () => {
            uploadArea.classList.remove('dragover');
        });

        uploadArea.addEventListener('drop', (e) => {
            e.preventDefault();
            uploadArea.classList.remove('dragover');
            if (e.dataTransfer.files.length > 0) {
                resumeUpload.handleFileSelect(e.dataTransfer.files[0]);
            }
        });

        // Chat input enter key
        const chatInput = document.getElementById('chatInput');
        if (chatInput) {
            chatInput.addEventListener('keypress', (e) => {
                if (e.key === 'Enter' && !e.shiftKey) {
                    e.preventDefault();
                    this.sendInterviewResponse();
                }
            });
        }
    },

    // Navigate to a specific step
    goToStep(stepNumber) {
        // Hide all steps
        document.querySelectorAll('.step-content').forEach(step => {
            step.classList.remove('active');
        });

        // Show current step
        document.getElementById(`step${stepNumber}`).classList.add('active');

        // Update step indicator
        document.querySelectorAll('.step').forEach((step, index) => {
            if (index + 1 < stepNumber) {
                step.classList.add('completed');
                step.classList.remove('active');
            } else if (index + 1 === stepNumber) {
                step.classList.add('active');
                step.classList.remove('completed');
            } else {
                step.classList.remove('active', 'completed');
            }
        });

        // Update progress bar
        const progress = (stepNumber / 6) * 100;
        document.getElementById('progressBar').style.width = `${progress}%`;

        this.currentStep = stepNumber;
    },

    // Proceed to quiz
    proceedToQuiz() {
        this.goToStep(3);
        quizInterface.generateQuiz();
    },

    // Quiz navigation
    nextQuestion() {
        if (this.quiz && this.quiz.mcq_questions && this.currentQuestionIndex < this.quiz.mcq_questions.length - 1) {
            this.currentQuestionIndex++;
            quizInterface.displayQuestion(this.currentQuestionIndex);
        }
    },

    previousQuestion() {
        if (this.quiz && this.quiz.mcq_questions && this.currentQuestionIndex > 0) {
            this.currentQuestionIndex--;
            quizInterface.displayQuestion(this.currentQuestionIndex);
        }
    },

    // Submit quiz
    async submitQuiz() {
        const result = await quizInterface.submitQuiz();
        if (result) {
            // Check if there are coding challenges
            if (this.quiz.coding_challenges && this.quiz.coding_challenges.length > 0) {
                this.goToStep(4);
                codingChallenge.displayChallenge(0);
            } else {
                // Skip to HR interview
                this.goToStep(5);
                hrInterview.startInterview();
            }
        }
    },

    // Send interview response
    async sendInterviewResponse() {
        await hrInterview.sendResponse();
    },

    // End interview
    async endInterview() {
        await hrInterview.endInterview();
    },

    // Show error message
    showError(message) {
        alert(`Error: ${message}`);
    },

    // Show info message
    showInfo(message) {
        console.log(`Info: ${message}`);
    },

    // Show success message
    showSuccess(message) {
        console.log(`Success: ${message}`);
    }
};

// Initialize app when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    app.init();
});
