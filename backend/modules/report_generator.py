from typing import Dict, List
from datetime import datetime
import json

class ReportGenerator:
    """Generate comprehensive assessment reports"""
    
    def __init__(self):
        self.report_data = {}
    
    def generate_final_report(
        self,
        resume_data: Dict,
        skill_analysis: Dict,
        mcq_results: Dict,
        coding_results: List[Dict],
        hr_evaluation: Dict,
        emotion_summary: Dict = None
    ) -> Dict:
        """
        Generate comprehensive final assessment report
        
        Args:
            resume_data: Parsed resume information
            skill_analysis: Skill analysis results
            mcq_results: MCQ quiz evaluation
            coding_results: Coding challenge evaluations
            hr_evaluation: HR interview evaluation
            emotion_summary: Facial expression analysis (optional)
            
        Returns:
            Complete assessment report
        """
        # Calculate overall scores
        overall_assessment = self._calculate_overall_assessment(
            mcq_results, coding_results, hr_evaluation
        )
        
        # Generate recommendations
        recommendations = self._generate_recommendations(
            skill_analysis, mcq_results, coding_results, hr_evaluation
        )
        
        # Identify strengths and weaknesses
        strengths_weaknesses = self._analyze_strengths_weaknesses(
            skill_analysis, mcq_results, coding_results, hr_evaluation
        )
        
        report = {
            'candidate_info': {
                'name': resume_data.get('personal_info', {}).get('name', 'Candidate'),
                'email': resume_data.get('personal_info', {}).get('email', ''),
                'assessment_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            },
            'skill_summary': {
                'total_skills': skill_analysis.get('summary', {}).get('total_skills', 0),
                'top_skills': skill_analysis.get('summary', {}).get('top_skills', []),
                'proficiency_distribution': skill_analysis.get('summary', {}).get('proficiency_distribution', {})
            },
            'assessment_scores': {
                'mcq': {
                    'score': mcq_results.get('score', 0),
                    'correct_answers': mcq_results.get('correct_answers', 0),
                    'total_questions': mcq_results.get('total_questions', 0),
                    'performance_level': mcq_results.get('performance_level', 'N/A'),
                    'skill_wise_scores': mcq_results.get('skill_scores', {}),
                    'detailed_results': mcq_results.get('detailed_results', [])
                },
                'coding': {
                    'challenges_completed': len(coding_results),
                    'average_score': self._calculate_average_coding_score(coding_results),
                    'total_tests_passed': sum(r.get('passed_tests', 0) for r in coding_results),
                    'total_tests': sum(r.get('total_tests', 0) for r in coding_results)
                },
                'hr_interview': {
                    'overall_score': hr_evaluation.get('overall_score', 0),
                    'communication_skills': hr_evaluation.get('communication_skills', 0),
                    'confidence': hr_evaluation.get('confidence', 0),
                    'relevance': hr_evaluation.get('relevance', 0),
                    'depth': hr_evaluation.get('depth', 0),
                    'cultural_fit': hr_evaluation.get('cultural_fit', 0)
                }
            },
            'emotion_analysis': {
                'emotion_distribution': emotion_summary.get('emotion_distribution', {}) if emotion_summary else {},
                'dominant_emotion': emotion_summary.get('dominant_emotion', 'N/A') if emotion_summary else 'N/A',
                'engagement_score': emotion_summary.get('engagement_score', 0) if emotion_summary else 0,
                'confidence_score': emotion_summary.get('confidence_score', 0) if emotion_summary else 0,
                'consistency_score': emotion_summary.get('consistency_score', 0) if emotion_summary else 0,
                'timeline': emotion_summary.get('timeline', []) if emotion_summary else [],
                'feedback': emotion_summary.get('feedback', {}) if emotion_summary else {},
                'total_detections': emotion_summary.get('total_detections', 0) if emotion_summary else 0,
                'session_duration': emotion_summary.get('session_duration', 0) if emotion_summary else 0
            },
            'overall_assessment': overall_assessment,
            'strengths': strengths_weaknesses['strengths'],
            'weaknesses': strengths_weaknesses['weaknesses'],
            'recommendations': recommendations,
            'interview_readiness_score': overall_assessment['interview_readiness_score'],
            'readiness_level': overall_assessment['readiness_level']
        }
        
        return report
    
    def _calculate_overall_assessment(
        self,
        mcq_results: Dict,
        coding_results: List[Dict],
        hr_evaluation: Dict
    ) -> Dict:
        """Calculate overall assessment scores using weighted evaluation"""
        from config import Config
        
        # Get individual scores
        mcq_score = mcq_results.get('score', 0)
        coding_score = self._calculate_average_coding_score(coding_results)
        hr_score = hr_evaluation.get('overall_score', 0)
        
        # Get weights from config
        weights = Config.SCORING_WEIGHTS
        
        # Calculate weighted interview readiness score
        if coding_results:
            # All three components available
            interview_readiness_score = (
                mcq_score * weights['mcq'] +
                coding_score * weights['coding'] +
                hr_score * weights['hr_interview']
            )
        else:
            # If no coding challenges, adjust weights: MCQ and HR only
            total_weight = weights['mcq'] + weights['hr_interview']
            interview_readiness_score = (
                mcq_score * (weights['mcq'] / total_weight) +
                hr_score * (weights['hr_interview'] / total_weight)
            )
        
        # Determine readiness level
        if interview_readiness_score >= 85:
            readiness_level = 'Excellent - Ready for Senior Positions'
        elif interview_readiness_score >= 70:
            readiness_level = 'Good - Ready for Mid-Level Positions'
        elif interview_readiness_score >= 55:
            readiness_level = 'Average - Ready for Entry-Level Positions'
        elif interview_readiness_score >= 40:
            readiness_level = 'Needs Improvement - Requires More Preparation'
        else:
            readiness_level = 'Not Ready - Significant Preparation Needed'
        
        return {
            'interview_readiness_score': round(interview_readiness_score, 2),
            'readiness_level': readiness_level,
            'technical_score': round((mcq_score + coding_score) / 2, 2) if coding_results else mcq_score,
            'soft_skills_score': hr_score,
            'score_breakdown': {
                'mcq_contribution': round(mcq_score * weights['mcq'], 2),
                'coding_contribution': round(coding_score * weights['coding'], 2),
                'hr_contribution': round(hr_score * weights['hr_interview'], 2)
            }
        }
    
    def _calculate_average_coding_score(self, coding_results: List[Dict]) -> float:
        """Calculate average coding challenge score"""
        if not coding_results:
            return 0
        
        total_score = sum(r.get('score', 0) for r in coding_results)
        return round(total_score / len(coding_results), 2)
    
    def _analyze_strengths_weaknesses(
        self,
        skill_analysis: Dict,
        mcq_results: Dict,
        coding_results: List[Dict],
        hr_evaluation: Dict
    ) -> Dict:
        """Identify candidate's strengths and weaknesses"""
        strengths = []
        weaknesses = []
        
        # Analyze MCQ performance
        skill_scores = mcq_results.get('skill_scores', {})
        for skill, data in skill_scores.items():
            if data['score'] >= 80:
                strengths.append(f'Strong knowledge in {skill} ({data["score"]}%)')
            elif data['score'] < 50:
                weaknesses.append(f'Needs improvement in {skill} ({data["score"]}%)')
        
        # Analyze coding performance
        if coding_results:
            avg_coding = self._calculate_average_coding_score(coding_results)
            if avg_coding >= 75:
                strengths.append(f'Excellent problem-solving skills ({avg_coding}%)')
            elif avg_coding < 50:
                weaknesses.append(f'Coding skills need practice ({avg_coding}%)')
        
        # Analyze HR interview
        hr_strengths = hr_evaluation.get('strengths', [])
        hr_weaknesses = hr_evaluation.get('areas_for_improvement', [])
        
        strengths.extend(hr_strengths)
        weaknesses.extend(hr_weaknesses)
        
        # Analyze communication
        comm_score = hr_evaluation.get('communication_skills', 0)
        if comm_score >= 80:
            strengths.append('Excellent communication skills')
        elif comm_score < 60:
            weaknesses.append('Communication skills need improvement')
        
        return {
            'strengths': strengths[:5],  # Top 5 strengths
            'weaknesses': weaknesses[:5]  # Top 5 weaknesses
        }
    
    def _generate_recommendations(
        self,
        skill_analysis: Dict,
        mcq_results: Dict,
        coding_results: List[Dict],
        hr_evaluation: Dict
    ) -> List[str]:
        """Generate personalized recommendations"""
        recommendations = []
        
        # Technical recommendations
        skill_scores = mcq_results.get('skill_scores', {})
        weak_skills = [skill for skill, data in skill_scores.items() if data['score'] < 60]
        
        if weak_skills:
            recommendations.append(
                f"Focus on improving: {', '.join(weak_skills[:3])}. "
                "Consider online courses or practice problems."
            )
        
        # Coding recommendations
        if coding_results:
            avg_coding = self._calculate_average_coding_score(coding_results)
            if avg_coding < 70:
                recommendations.append(
                    "Practice more coding problems on platforms like LeetCode, HackerRank, or CodeForces. "
                    "Focus on data structures and algorithms."
                )
        
        # Communication recommendations
        comm_score = hr_evaluation.get('communication_skills', 0)
        if comm_score < 70:
            recommendations.append(
                "Work on communication skills. Practice explaining technical concepts clearly. "
                "Consider mock interviews with peers or mentors."
            )
        
        # Confidence recommendations
        confidence = hr_evaluation.get('confidence', 0)
        if confidence < 70:
            recommendations.append(
                "Build confidence through more interview practice. "
                "Prepare STAR method responses for behavioral questions."
            )
        
        # General recommendations
        overall_score = (mcq_results.get('score', 0) + 
                        self._calculate_average_coding_score(coding_results) + 
                        hr_evaluation.get('overall_score', 0)) / 3
        
        if overall_score < 60:
            recommendations.append(
                "Consider taking additional courses or bootcamps to strengthen fundamentals. "
                "Build more projects to gain practical experience."
            )
        
        # Improvement areas from skill analysis
        improvement_areas = skill_analysis.get('summary', {}).get('improvement_areas', [])
        if improvement_areas:
            recommendations.append(
                f"Develop skills in: {', '.join(improvement_areas[:3])} to broaden your expertise."
            )
        
        return recommendations[:5]  # Top 5 recommendations
    
    def export_report_json(self, report: Dict) -> str:
        """Export report as JSON string"""
        return json.dumps(report, indent=2)
    
    def export_report_html(self, report: Dict) -> str:
        """Export report as HTML"""
        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Interview Assessment Report</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 40px; }}
                h1 {{ color: #2c3e50; }}
                h2 {{ color: #34495e; margin-top: 30px; }}
                .score {{ font-size: 48px; font-weight: bold; color: #27ae60; }}
                .section {{ margin: 20px 0; padding: 15px; background: #f8f9fa; border-radius: 5px; }}
                .strength {{ color: #27ae60; }}
                .weakness {{ color: #e74c3c; }}
                ul {{ line-height: 1.8; }}
            </style>
        </head>
        <body>
            <h1>Interview Readiness Assessment Report</h1>
            <div class="section">
                <h2>Candidate Information</h2>
                <p><strong>Name:</strong> {report['candidate_info']['name']}</p>
                <p><strong>Email:</strong> {report['candidate_info']['email']}</p>
                <p><strong>Assessment Date:</strong> {report['candidate_info']['assessment_date']}</p>
            </div>
            
            <div class="section">
                <h2>Overall Interview Readiness Score</h2>
                <div class="score">{report['interview_readiness_score']}/100</div>
                <p><strong>Readiness Level:</strong> {report['overall_assessment']['readiness_level']}</p>
            </div>
            
            <div class="section">
                <h2>Assessment Breakdown</h2>
                <p><strong>MCQ Score:</strong> {report['assessment_scores']['mcq']['score']}%</p>
                <p><strong>Coding Score:</strong> {report['assessment_scores']['coding']['average_score']}%</p>
                <p><strong>HR Interview Score:</strong> {report['assessment_scores']['hr_interview']['overall_score']}%</p>
            </div>
            
            <div class="section">
                <h2>Strengths</h2>
                <ul>
                    {''.join([f'<li class="strength">{s}</li>' for s in report['strengths']])}
                </ul>
            </div>
            
            <div class="section">
                <h2>Areas for Improvement</h2>
                <ul>
                    {''.join([f'<li class="weakness">{w}</li>' for w in report['weaknesses']])}
                </ul>
            </div>
            
            <div class="section">
                <h2>Recommendations</h2>
                <ul>
                    {''.join([f'<li>{r}</li>' for r in report['recommendations']])}
                </ul>
            </div>
        </body>
        </html>
        """
        return html
