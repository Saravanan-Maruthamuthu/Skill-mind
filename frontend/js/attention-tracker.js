// Attention Tracker Module using WebGazer.js
const AttentionTracker = {
    isInitialized: false,
    isCalibrated: false,
    isTracking: false,
    gazeData: [],
    attentionData: {
        totalTime: 0,
        focusedTime: 0,
        distractedTime: 0,
        distractions: [],
        startTime: null
    },
    currentlyFocused: true,
    distractionStartTime: null,
    screenBounds: null,
    calibrationPoints: 9,
    calibrationProgress: 0,

    // Initialize WebGazer
    async init() {
        if (this.isInitialized) return true;

        try {
            console.log('Initializing WebGazer eye tracking...');

            // Suppress TensorFlow/WebGazer kernel registration warnings
            this.suppressTensorFlowWarnings();

            // Load WebGazer
            await this.loadWebGazer();

            // Initialize WebGazer
            await webgazer.setGazeListener((data, timestamp) => {
                if (data && this.isTracking) {
                    this.processGazeData(data, timestamp);
                }
            }).begin();

            // Set regression type and video settings
            webgazer.setRegression('ridge');
            webgazer.showVideoPreview(true)
                .showPredictionPoints(false);

            this.isInitialized = true;
            this.screenBounds = this.getScreenBounds();

            console.log('WebGazer initialized successfully');
            return true;
        } catch (error) {
            console.error('Failed to initialize WebGazer:', error);
            return false;
        }
    },

    // Suppress TensorFlow kernel registration warnings
    suppressTensorFlowWarnings() {
        const originalWarn = console.warn;
        const originalError = console.error;

        console.warn = function (...args) {
            const message = args.join(' ');
            // Suppress specific TensorFlow/WebGazer kernel warnings
            if (message.includes('already registered') ||
                message.includes('kernel') ||
                message.includes('backend') ||
                message.includes('cpu backend was already registered')) {
                return;
            }
            originalWarn.apply(console, args);
        };

        console.error = function (...args) {
            const message = args.join(' ');
            // Suppress specific TensorFlow/WebGazer kernel errors
            if (message.includes('already registered') ||
                message.includes('kernel') && message.includes('backend')) {
                return;
            }
            originalError.apply(console, args);
        };
    },

    // Load WebGazer library
    loadWebGazer() {
        return new Promise((resolve, reject) => {
            if (typeof webgazer !== 'undefined') {
                resolve();
                return;
            }

            const script = document.createElement('script');
            // Use the correct WebGazer CDN URL
            script.src = 'https://webgazer.cs.brown.edu/webgazer.js';
            script.onload = () => {
                console.log('WebGazer loaded successfully');
                resolve();
            };
            script.onerror = (error) => {
                console.error('Failed to load WebGazer from CDN:', error);
                reject(new Error('Failed to load WebGazer library. Please check your internet connection.'));
            };
            document.head.appendChild(script);
        });
    },

    // Get screen bounds for attention detection
    getScreenBounds() {
        return {
            left: 0,
            top: 0,
            right: window.innerWidth,
            bottom: window.innerHeight,
            // Define a margin where we still consider user "focused"
            marginX: window.innerWidth * 0.1,  // 10% margin
            marginY: window.innerHeight * 0.1
        };
    },

    // Start calibration process
    async startCalibration() {
        if (!this.isInitialized) {
            await this.init();
        }

        this.calibrationProgress = 0;
        this.showCalibrationUI();

        return new Promise((resolve) => {
            this.runCalibration(resolve);
        });
    },

    // Show calibration UI
    showCalibrationUI() {
        const overlay = document.createElement('div');
        overlay.id = 'calibration-overlay';
        overlay.innerHTML = `
            <div class="calibration-container">
                <h2>Eye Tracking Calibration</h2>
                <p>Please click on each point as it appears and keep your eyes on it.</p>
                <div class="calibration-grid">
                    <div class="calibration-point" data-point="0"></div>
                    <div class="calibration-point" data-point="1"></div>
                    <div class="calibration-point" data-point="2"></div>
                    <div class="calibration-point" data-point="3"></div>
                    <div class="calibration-point" data-point="4"></div>
                    <div class="calibration-point" data-point="5"></div>
                    <div class="calibration-point" data-point="6"></div>
                    <div class="calibration-point" data-point="7"></div>
                    <div class="calibration-point" data-point="8"></div>
                </div>
                <div class="calibration-progress">
                    <div class="progress-bar">
                        <div class="progress-fill" style="width: 0%"></div>
                    </div>
                    <p class="progress-text">0/9 points calibrated</p>
                </div>
            </div>
        `;

        // Add styles
        const style = document.createElement('style');
        style.textContent = `
            #calibration-overlay {
                position: fixed;
                top: 0;
                left: 0;
                right: 0;
                bottom: 0;
                background: rgba(0, 0, 0, 0.95);
                z-index: 999999;
                display: flex;
                align-items: center;
                justify-content: center;
            }
            .calibration-container {
                text-align: center;
                color: white;
            }
            .calibration-container h2 {
                margin-bottom: 10px;
                font-size: 28px;
            }
            .calibration-container p {
                margin-bottom: 30px;
                font-size: 16px;
            }
            .calibration-grid {
                display: grid;
                grid-template-columns: repeat(3, 1fr);
                gap: 20vw;
                width: 80vw;
                height: 60vh;
                margin: 0 auto 30px;
            }
            .calibration-point {
                width: 30px;
                height: 30px;
                background: #ff4444;
                border-radius: 50%;
                cursor: pointer;
                transition: all 0.3s;
                opacity: 0.3;
                position: relative;
            }
            .calibration-point.active {
                opacity: 1;
                animation: pulse 1s infinite;
                box-shadow: 0 0 20px #ff4444;
            }
            .calibration-point.completed {
                background: #4CAF50;
                opacity: 0.5;
            }
            @keyframes pulse {
                0%, 100% { transform: scale(1); }
                50% { transform: scale(1.2); }
            }
            .calibration-progress {
                margin-top: 20px;
            }
            .progress-bar {
                width: 300px;
                height: 10px;
                background: #333;
                border-radius: 5px;
                margin: 0 auto 10px;
                overflow: hidden;
            }
            .progress-fill {
                height: 100%;
                background: linear-gradient(90deg, #4CAF50, #8BC34A);
                transition: width 0.3s;
            }
            .progress-text {
                font-size: 14px;
                color: #ccc;
            }
        `;
        document.head.appendChild(style);
        document.body.appendChild(overlay);
    },

    // Run calibration sequence
    runCalibration(onComplete) {
        const points = document.querySelectorAll('.calibration-point');
        let currentPoint = 0;

        const activatePoint = (index) => {
            if (index >= points.length) {
                this.completeCalibration(onComplete);
                return;
            }

            points[index].classList.add('active');

            points[index].onclick = () => {
                // Click registered - WebGazer automatically collects data
                points[index].classList.remove('active');
                points[index].classList.add('completed');

                this.calibrationProgress++;
                this.updateCalibrationProgress();

                // Move to next point after brief delay
                setTimeout(() => {
                    activatePoint(index + 1);
                }, 500);
            };
        };

        activatePoint(0);
    },

    // Update calibration progress UI
    updateCalibrationProgress() {
        const progressFill = document.querySelector('.progress-fill');
        const progressText = document.querySelector('.progress-text');

        const percentage = (this.calibrationProgress / this.calibrationPoints) * 100;
        progressFill.style.width = percentage + '%';
        progressText.textContent = `${this.calibrationProgress}/${this.calibrationPoints} points calibrated`;
    },

    // Complete calibration
    completeCalibration(onComplete) {
        setTimeout(() => {
            const overlay = document.getElementById('calibration-overlay');
            if (overlay) {
                overlay.remove();
            }

            this.isCalibrated = true;
            console.log('Calibration completed');
            onComplete(true);
        }, 1000);
    },

    // Start tracking attention
    startTracking() {
        if (!this.isCalibrated) {
            console.warn('Cannot start tracking without calibration');
            return false;
        }

        this.isTracking = true;
        this.attentionData.startTime = Date.now();
        this.showAttentionIndicator();

        console.log('Attention tracking started');
        return true;
    },

    // Stop tracking attention
    stopTracking() {
        this.isTracking = false;
        this.hideAttentionIndicator();

        // Calculate total time
        if (this.attentionData.startTime) {
            this.attentionData.totalTime = Date.now() - this.attentionData.startTime;
        }

        console.log('Attention tracking stopped');
        return this.getAttentionSummary();
    },

    // Process gaze data
    processGazeData(data, timestamp) {
        const { x, y } = data;

        // Debug: Log gaze position occasionally
        if (this.gazeData.length % 30 === 0) {
            console.log(`Gaze: (${Math.round(x)}, ${Math.round(y)}) | Screen: ${window.innerWidth}x${window.innerHeight}`);
        }

        // Store gaze point
        this.gazeData.push({ x, y, timestamp });

        // Keep only last 100 points to avoid memory issues
        if (this.gazeData.length > 100) {
            this.gazeData.shift();
        }

        // Check if user is looking at screen
        const isFocused = this.isLookingAtScreen(x, y);

        if (isFocused !== this.currentlyFocused) {
            console.log(`Focus changed: ${isFocused ? 'FOCUSED' : 'DISTRACTED'}`);
            this.handleFocusChange(isFocused, timestamp);
        }
    },

    // Check if gaze is within screen bounds
    isLookingAtScreen(x, y) {
        const bounds = this.screenBounds;
        return x >= (bounds.left - bounds.marginX) &&
            x <= (bounds.right + bounds.marginX) &&
            y >= (bounds.top - bounds.marginY) &&
            y <= (bounds.bottom + bounds.marginY);
    },

    // Handle focus change
    handleFocusChange(isFocused, timestamp) {
        if (isFocused) {
            // User looked back at screen
            if (this.distractionStartTime) {
                const distractionDuration = timestamp - this.distractionStartTime;
                this.attentionData.distractions.push({
                    start: this.distractionStartTime,
                    end: timestamp,
                    duration: distractionDuration
                });
                this.attentionData.distractedTime += distractionDuration;
                this.distractionStartTime = null;
            }
            this.updateAttentionIndicator('focused');
        } else {
            // User looked away
            this.distractionStartTime = timestamp;
            this.updateAttentionIndicator('distracted');
        }

        this.currentlyFocused = isFocused;
    },

    // Show attention indicator
    showAttentionIndicator() {
        const indicator = document.createElement('div');
        indicator.id = 'attention-indicator';
        indicator.innerHTML = `
            <div class="indicator-dot focused"></div>
            <span class="indicator-text">Focused</span>
        `;

        const style = document.createElement('style');
        style.textContent = `
            #attention-indicator {
                position: fixed;
                top: 20px;
                right: 20px;
                display: flex;
                align-items: center;
                gap: 10px;
                background: rgba(0, 0, 0, 0.7);
                padding: 12px 20px;
                border-radius: 25px;
                z-index: 9999;
                font-family: Arial, sans-serif;
            }
            .indicator-dot {
                width: 16px;
                height: 16px;
                border-radius: 50%;
                transition: background-color 0.3s;
            }
            .indicator-dot.focused {
                background: #4CAF50;
                box-shadow: 0 0 10px #4CAF50;
            }
            .indicator-dot.distracted {
                background: #f44336;
                box-shadow: 0 0 10px #f44336;
                animation: blink 0.5s infinite;
            }
            .indicator-text {
                color: white;
                font-size: 14px;
                font-weight: 500;
            }
            @keyframes blink {
                0%, 100% { opacity: 1; }
                50% { opacity: 0.5; }
            }
        `;
        document.head.appendChild(style);
        document.body.appendChild(indicator);
    },

    // Update attention indicator
    updateAttentionIndicator(status) {
        const dot = document.querySelector('.indicator-dot');
        const text = document.querySelector('.indicator-text');

        if (!dot || !text) return;

        if (status === 'focused') {
            dot.classList.remove('distracted');
            dot.classList.add('focused');
            text.textContent = 'Focused';
        } else {
            dot.classList.remove('focused');
            dot.classList.add('distracted');
            text.textContent = 'Distracted';
        }
    },

    // Hide attention indicator
    hideAttentionIndicator() {
        const indicator = document.getElementById('attention-indicator');
        if (indicator) {
            indicator.remove();
        }
    },

    // Get attention summary
    getAttentionSummary() {
        const totalTime = this.attentionData.totalTime;
        const distractedTime = this.attentionData.distractedTime;
        const focusedTime = totalTime - distractedTime;

        const attentionPercentage = totalTime > 0 ? (focusedTime / totalTime) * 100 : 0;

        return {
            totalTime: totalTime,
            focusedTime: focusedTime,
            distractedTime: distractedTime,
            attentionPercentage: attentionPercentage.toFixed(2),
            distractionCount: this.attentionData.distractions.length,
            avgDistractionDuration: this.attentionData.distractions.length > 0
                ? (distractedTime / this.attentionData.distractions.length).toFixed(2)
                : 0,
            distractions: this.attentionData.distractions
        };
    },

    // Cleanup
    cleanup() {
        if (typeof webgazer !== 'undefined') {
            webgazer.end();
        }
        this.isTracking = false;
        this.isInitialized = false;
        this.isCalibrated = false;
        this.hideAttentionIndicator();
    }
};

// Export for use in other modules
if (typeof module !== 'undefined' && module.exports) {
    module.exports = AttentionTracker;
}
