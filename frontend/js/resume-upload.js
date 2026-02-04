// Resume Upload Handler
const resumeUpload = {
    // Handle file selection
    async handleFileSelect(file) {
        // Validate file
        const validTypes = ['application/pdf', 'application/msword', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'];

        if (!validTypes.includes(file.type)) {
            app.showError('Please upload a PDF or DOCX file');
            return;
        }

        if (file.size > 16 * 1024 * 1024) {
            app.showError('File size must be less than 16MB');
            return;
        }

        // Show loading state
        document.getElementById('uploadArea').style.display = 'none';
        document.getElementById('uploadStatus').style.display = 'block';

        // Upload file
        await this.uploadResume(file);
    },

    // Upload resume to server
    async uploadResume(file) {
        const formData = new FormData();
        formData.append('resume', file);

        try {
            const response = await fetch(`${app.apiUrl}/upload-resume`, {
                method: 'POST',
                body: formData
            });

            const data = await response.json();

            if (data.success) {
                app.sessionId = data.session_id;
                app.resumeData = data.resume_data;
                app.skillAnalysis = data.skill_analysis;

                app.showSuccess('Resume parsed successfully!');

                // Move to skill analysis step
                setTimeout(() => {
                    app.goToStep(2);
                    skillAnalysis.displaySkillAnalysis();
                }, 1000);
            } else {
                throw new Error(data.error || 'Upload failed');
            }
        } catch (error) {
            console.error('Upload error:', error);
            app.showError(error.message);

            // Reset upload area
            document.getElementById('uploadArea').style.display = 'block';
            document.getElementById('uploadStatus').style.display = 'none';
        }
    }
};
