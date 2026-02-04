// Skill Analysis Display
const skillAnalysis = {
    // Display skill analysis results
    displaySkillAnalysis() {
        const container = document.getElementById('skillAnalysisContent');
        const analysis = app.skillAnalysis;
        const resumeData = app.resumeData;

        let html = `
            <div class="personal-info">
                <h3>👤 Personal Information</h3>
                <p><strong>Name:</strong> ${resumeData.personal_info.name || 'N/A'}</p>
                <p><strong>Email:</strong> ${resumeData.personal_info.email || 'N/A'}</p>
            </div>
            
            <div class="skill-summary" style="margin: 30px 0; padding: 20px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; border-radius: 12px;">
                <h3>📊 Skill Summary</h3>
                <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 20px; margin-top: 20px;">
                    <div>
                        <div style="font-size: 2.5rem; font-weight: bold;">${analysis.summary.total_skills}</div>
                        <div>Total Skills</div>
                    </div>
                    <div>
                        <div style="font-size: 2.5rem; font-weight: bold;">${analysis.summary.proficiency_distribution.advanced || 0}</div>
                        <div>Advanced Skills</div>
                    </div>
                    <div>
                        <div style="font-size: 2.5rem; font-weight: bold;">${analysis.summary.proficiency_distribution.intermediate || 0}</div>
                        <div>Intermediate Skills</div>
                    </div>
                    <div>
                        <div style="font-size: 2.5rem; font-weight: bold;">${analysis.summary.proficiency_distribution.beginner || 0}</div>
                        <div>Beginner Skills</div>
                    </div>
                </div>
            </div>
            
            <h3 style="margin-top: 30px;">🎯 Skills by Category</h3>
            <div class="skill-categories">
        `;

        // Display categorized skills
        for (const [category, skills] of Object.entries(analysis.categorized)) {
            if (skills.length > 0) {
                html += `
                    <div class="skill-category">
                        <h3>${category}</h3>
                        <div>
                `;

                skills.forEach(skill => {
                    // Find proficiency for this skill
                    const skillInfo = analysis.with_proficiency.find(s => s.skill === skill);
                    const proficiency = skillInfo ? skillInfo.proficiency : 'intermediate';

                    html += `<span class="skill-tag ${proficiency}">${skill}</span>`;
                });

                html += `
                        </div>
                    </div>
                `;
            }
        }

        html += `</div>`;

        // Display top skills
        if (analysis.summary.top_skills && analysis.summary.top_skills.length > 0) {
            html += `
                <div style="margin-top: 30px; padding: 20px; background: #f0fdf4; border-left: 4px solid #10b981; border-radius: 8px;">
                    <h3 style="color: #10b981;">⭐ Your Top Skills</h3>
                    <p>${analysis.summary.top_skills.join(', ')}</p>
                </div>
            `;
        }

        container.innerHTML = html;
    }
};
