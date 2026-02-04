// Results Dashboard
const resultsDashboard = {
    // Display final results
    async displayResults() {
        try {
            const response = await fetch(`${app.apiUrl}/final-report`, {
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
                this.renderReport(data.report);
            } else {
                throw new Error(data.error || 'Failed to generate report');
            }
        } catch (error) {
            console.error('Report generation error:', error);
            app.showError(error.message);
        }
    },

    // Render report
    renderReport(report) {
        const container = document.getElementById('resultsContent');

        let html = `
            <!-- Overall Score -->
            <div class="score-card">
                <div class="score-label">Interview Readiness Score</div>
                <div class="score-value">${report.interview_readiness_score}</div>
                <div class="score-label">${report.overall_assessment.readiness_level}</div>
            </div>
            
            <!-- Score Breakdown -->
            <div class="results-grid">
                <div class="result-card">
                    <h3>📝 MCQ Assessment</h3>
                    <div style="font-size: 2.5rem; font-weight: bold; color: #6366f1; margin: 15px 0;">
                        ${report.assessment_scores.mcq.score}%
                    </div>
                    <p>${report.assessment_scores.mcq.correct_answers} / ${report.assessment_scores.mcq.total_questions} correct</p>
                    <p><strong>Level:</strong> ${report.assessment_scores.mcq.performance_level}</p>
                </div>
                
                <div class="result-card">
                    <h3>💻 Coding Challenges</h3>
                    <div style="font-size: 2.5rem; font-weight: bold; color: #8b5cf6; margin: 15px 0;">
                        ${report.assessment_scores.coding.average_score}%
                    </div>
                    <p>${report.assessment_scores.coding.total_tests_passed} / ${report.assessment_scores.coding.total_tests} tests passed</p>
                    <p><strong>Challenges:</strong> ${report.assessment_scores.coding.challenges_completed}</p>
                </div>
                
                <div class="result-card">
                    <h3>🎤 HR Interview</h3>
                    <div style="font-size: 2.5rem; font-weight: bold; color: #10b981; margin: 15px 0;">
                        ${report.assessment_scores.hr_interview.overall_score}%
                    </div>
                    <p><strong>Communication:</strong> ${report.assessment_scores.hr_interview.communication_skills}%</p>
                    <p><strong>Confidence:</strong> ${report.assessment_scores.hr_interview.confidence}%</p>
                </div>
            </div>
            
            <!-- Skill-wise Performance Chart -->
            <div class="chart-container">
                <h3>📊 Skill-wise Performance</h3>
                <canvas id="skillChart" style="max-height: 300px;"></canvas>
            </div>
            
            <!-- Strengths and Weaknesses -->
            <div class="results-grid">
                <div class="result-card" style="background: #f0fdf4; border-left: 4px solid #10b981;">
                    <h3 style="color: #10b981;">💪 Strengths</h3>
                    <ul style="list-style: none; padding: 0;">
                        ${report.strengths.map(s => `<li style="padding: 8px 0; border-bottom: 1px solid #e5e7eb;">✓ ${s}</li>`).join('')}
                    </ul>
                </div>
                
                <div class="result-card" style="background: #fef2f2; border-left: 4px solid #ef4444;">
                    <h3 style="color: #ef4444;">📈 Areas for Improvement</h3>
                    <ul style="list-style: none; padding: 0;">
                        ${report.weaknesses.map(w => `<li style="padding: 8px 0; border-bottom: 1px solid #e5e7eb;">→ ${w}</li>`).join('')}
                    </ul>
                </div>
            </div>
            
            <!-- Recommendations -->
            <div class="recommendations">
                <h3>💡 Personalized Recommendations</h3>
                <ul>
                    ${report.recommendations.map(r => `<li>${r}</li>`).join('')}
                </ul>
            </div>
            
            <!-- Download Button -->
            <div class="button-group">
                <button class="btn btn-primary" onclick="resultsDashboard.downloadReport()">
                    📥 Download Full Report
                </button>
                <button class="btn btn-secondary" onclick="location.reload()">
                    🔄 Start New Assessment
                </button>
            </div>
        `;

        container.innerHTML = html;

        // Render skill chart
        this.renderSkillChart(report.assessment_scores.mcq.skill_wise_scores);

        // Render detailed MCQ review
        this.renderMCQDetail(report.assessment_scores.mcq.detailed_results);
    },

    // Render detailed MCQ review
    renderMCQDetail(detailedResults) {
        if (!detailedResults || detailedResults.length === 0) return;

        const container = document.getElementById('resultsContent');

        let html = `
            <div class="result-card" style="margin-top: 20px; grid-column: 1 / -1;">
                <h3>📝 Detailed MCQ Review</h3>
                <div class="mcq-review-list" style="max-height: 400px; overflow-y: auto; margin-top: 15px;">
        `;

        detailedResults.forEach((result, index) => {
            const isCorrect = result.is_correct;
            const statusClass = isCorrect ? 'correct' : 'incorrect';
            const statusIcon = isCorrect ? '✓' : '✗';
            const statusColor = isCorrect ? '#10b981' : '#ef4444';

            html += `
                <div class="review-item" style="padding: 15px; border-bottom: 1px solid #e5e7eb; display: flex; flex-direction: column; gap: 8px;">
                    <div style="display: flex; justify-content: space-between; align-items: start;">
                        <div style="font-weight: 600; color: #1f2937;">Q${index + 1}. ${result.question}</div>
                        <div style="color: ${statusColor}; font-weight: bold; min-width: 80px; text-align: right;">${statusIcon} ${isCorrect ? 'Correct' : 'Incorrect'}</div>
                    </div>
                    
                    <div style="font-size: 0.9rem; color: #4b5563;">
                        <div style="margin-bottom: 4px;">Your Answer: <span style="font-weight: 500; color: ${statusColor}">${result.user_answer || 'Skipped'}</span></div>
                        ${!isCorrect ? `<div style="margin-bottom: 4px;">Correct Answer: <span style="font-weight: 500; color: #10b981;">${result.correct_answer}</span></div>` : ''}
                    </div>
                    
                    ${result.explanation ? `
                    <div style="font-size: 0.85rem; background: #f9fafb; padding: 8px; border-radius: 4px; color: #6b7280; font-style: italic;">
                        💡 ${result.explanation}
                    </div>` : ''}
                </div>
            `;
        });

        html += `
                </div>
            </div>
        `;

        // Append to existing content
        const reviewContainer = document.createElement('div');
        reviewContainer.innerHTML = html;
        container.appendChild(reviewContainer.firstElementChild);
    },

    // Render skill chart
    renderSkillChart(skillScores) {
        const ctx = document.getElementById('skillChart');
        if (!ctx) return;

        const skills = Object.keys(skillScores);
        const scores = Object.values(skillScores).map(s => s.score);

        new Chart(ctx, {
            type: 'bar',
            data: {
                labels: skills,
                datasets: [{
                    label: 'Score (%)',
                    data: scores,
                    backgroundColor: [
                        'rgba(99, 102, 241, 0.8)',
                        'rgba(139, 92, 246, 0.8)',
                        'rgba(16, 185, 129, 0.8)',
                        'rgba(245, 158, 11, 0.8)',
                        'rgba(239, 68, 68, 0.8)'
                    ],
                    borderColor: [
                        'rgb(99, 102, 241)',
                        'rgb(139, 92, 246)',
                        'rgb(16, 185, 129)',
                        'rgb(245, 158, 11)',
                        'rgb(239, 68, 68)'
                    ],
                    borderWidth: 2
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: true,
                scales: {
                    y: {
                        beginAtZero: true,
                        max: 100,
                        ticks: {
                            callback: function (value) {
                                return value + '%';
                            }
                        }
                    }
                },
                plugins: {
                    legend: {
                        display: false
                    },
                    tooltip: {
                        callbacks: {
                            label: function (context) {
                                return 'Score: ' + context.parsed.y + '%';
                            }
                        }
                    }
                }
            }
        });
    },

    // Download report
    downloadReport() {
        window.open(`${app.apiUrl}/download-report?session_id=${app.sessionId}`, '_blank');
    }
};
