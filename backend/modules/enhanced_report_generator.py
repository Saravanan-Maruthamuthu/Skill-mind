"""
Enhanced Report Generator with detailed score breakdown and improvement recommendations
"""

from typing import Dict, List
import json
from datetime import datetime

class EnhancedReportGenerator:
    """Generate comprehensive interview performance reports with recommendations"""
    
    def __init__(self):
        self.score_thresholds = {
            'excellent': (85, 100),
            'good': (70, 84),
            'average': (55, 69),
            'needs_improvement': (40, 54),
            'not_ready': (0, 39)
        }
        
        self.weights = {
            'mcq': 0.30,
            'coding': 0.40,
            'hr_interview': 0.30
        }
    
    def calculate_scores(self, 
                        mcq_results: Dict,
                        coding_results: Dict, 
                        hr_results: Dict) -> Dict:
        """
        Calculate weighted scores for all components
        
        Args:
            mcq_results: {skill: {correct: count, total: count}}
            coding_results: {skill: {passed: count, total: count}}
            hr_results: {score: float, analysis: str}
            
        Returns:
            Detailed score breakdown
        """
        
        # MCQ Score calculation
        mcq_data = self._calculate_mcq_scores(mcq_results)
        
        # Coding Score calculation
        coding_data = self._calculate_coding_scores(coding_results)
        
        # HR Interview Score
        hr_data = self._calculate_hr_scores(hr_results)
        
        # Calculate weighted final score
        final_score = (
            mcq_data['overall_percentage'] * self.weights['mcq'] +
            coding_data['overall_percentage'] * self.weights['coding'] +
            hr_data['score'] * self.weights['hr_interview']
        )
        
        return {
            'mcq': mcq_data,
            'coding': coding_data,
            'hr_interview': hr_data,
            'final_score': round(final_score, 2),
            'overall_level': self._get_performance_level(final_score),
            'weights': self.weights
        }
    
    def _calculate_mcq_scores(self, mcq_results: Dict) -> Dict:
        """Calculate MCQ scores by skill and overall"""
        skill_scores = {}
        total_correct = 0
        total_questions = 0
        
        for skill, result in mcq_results.items():
            correct = result.get('correct', 0)
            total = result.get('total', 5)
            percentage = (correct / total * 100) if total > 0 else 0
            
            skill_scores[skill] = {
                'correct': correct,
                'total': total,
                'percentage': round(percentage, 2),
                'level': self._get_proficiency_level(percentage)
            }
            
            total_correct += correct
            total_questions += total
        
        overall_percentage = (total_correct / total_questions * 100) if total_questions > 0 else 0
        
        return {
            'by_skill': skill_scores,
            'total_correct': total_correct,
            'total_questions': total_questions,
            'overall_percentage': round(overall_percentage, 2),
            'performance_level': self._get_performance_level(overall_percentage)
        }
    
    def _calculate_coding_scores(self, coding_results: Dict) -> Dict:
        """Calculate coding challenge scores by skill and difficulty"""
        skill_scores = {}
        total_passed = 0
        total_challenges = 0
        
        for skill, result in coding_results.items():
            by_difficulty = {}
            skill_total_passed = 0
            skill_total_challenges = 0
            
            for difficulty in ['basic', 'intermediate', 'advanced']:
                if difficulty in result:
                    passed = result[difficulty].get('passed', 0)
                    total = result[difficulty].get('total', 0)
                    percentage = (passed / total * 100) if total > 0 else 0
                    
                    by_difficulty[difficulty] = {
                        'passed': passed,
                        'total': total,
                        'percentage': round(percentage, 2)
                    }
                    skill_total_passed += passed
                    skill_total_challenges += total
            
            skill_percentage = (skill_total_passed / skill_total_challenges * 100) if skill_total_challenges > 0 else 0
            
            skill_scores[skill] = {
                'by_difficulty': by_difficulty,
                'total_passed': skill_total_passed,
                'total_challenges': skill_total_challenges,
                'percentage': round(skill_percentage, 2),
                'level': self._get_proficiency_level(skill_percentage)
            }
            
            total_passed += skill_total_passed
            total_challenges += skill_total_challenges
        
        overall_percentage = (total_passed / total_challenges * 100) if total_challenges > 0 else 0
        
        return {
            'by_skill': skill_scores,
            'total_passed': total_passed,
            'total_challenges': total_challenges,
            'overall_percentage': round(overall_percentage, 2),
            'performance_level': self._get_performance_level(overall_percentage)
        }
    
    def _calculate_hr_scores(self, hr_results: Dict) -> Dict:
        """Calculate HR interview scores"""
        score = hr_results.get('score', 0)
        analysis = hr_results.get('analysis', '')
        
        return {
            'score': round(score, 2),
            'percentage': round(score, 2),
            'level': self._get_performance_level(score),
            'analysis': analysis
        }
    
    def _get_performance_level(self, score: float) -> str:
        """Get performance level based on score"""
        for level, (min_score, max_score) in self.score_thresholds.items():
            if min_score <= score <= max_score:
                return level
        return 'unknown'
    
    def _get_proficiency_level(self, percentage: float) -> str:
        """Get proficiency level based on percentage"""
        if percentage >= 85:
            return 'Advanced'
        elif percentage >= 70:
            return 'Intermediate'
        elif percentage >= 55:
            return 'Beginner'
        else:
            return 'Needs Practice'
    
    def generate_recommendations(self, scores: Dict, skills_with_proficiency: Dict) -> List[Dict]:
        """
        Generate personalized improvement recommendations
        
        Args:
            scores: Score breakdown from calculate_scores()
            skills_with_proficiency: {skill: proficiency}
            
        Returns:
            List of recommendations
        """
        recommendations = []
        
        # Analyze weak areas
        mcq_by_skill = scores['mcq'].get('by_skill', {})
        coding_by_skill = scores['coding'].get('by_skill', {})
        
        for skill, mcq_result in mcq_by_skill.items():
            if mcq_result['percentage'] < 60:
                recommendations.append({
                    'skill': skill,
                    'area': 'MCQ Knowledge',
                    'issue': f"Weak MCQ performance ({mcq_result['percentage']}%)",
                    'recommendation': f"Study fundamentals of {skill} and practice more concept-based questions",
                    'priority': 'high'
                })
        
        for skill, coding_result in coding_by_skill.items():
            # Check basic level
            basic = coding_result['by_difficulty'].get('basic', {})
            if basic.get('passed', 0) < basic.get('total', 1):
                recommendations.append({
                    'skill': skill,
                    'area': f"{skill} - Basic Coding",
                    'issue': f"Struggling with basic {skill} problems",
                    'recommendation': f"Practice basic data structures and syntax in {skill}",
                    'priority': 'critical'
                })
            
            # Check intermediate level
            intermediate = coding_result['by_difficulty'].get('intermediate', {})
            if intermediate.get('percentage', 0) < 50:
                recommendations.append({
                    'skill': skill,
                    'area': f"{skill} - Problem Solving",
                    'issue': f"Difficulty with intermediate {skill} algorithms",
                    'recommendation': f"Practice algorithmic thinking and complexity analysis for {skill}",
                    'priority': 'high'
                })
            
            # Check advanced level
            advanced = coding_result['by_difficulty'].get('advanced', {})
            if advanced.get('percentage', 0) < 40:
                recommendations.append({
                    'skill': skill,
                    'area': f"{skill} - Advanced Topics",
                    'issue': f"Advanced {skill} problems need improvement",
                    'recommendation': f"Build expertise in advanced {skill} patterns and optimization techniques",
                    'priority': 'medium'
                })
        
        # HR Interview feedback
        hr_score = scores['hr_interview']['score']
        if hr_score < 70:
            recommendations.append({
                'area': 'Communication & Soft Skills',
                'issue': 'HR interview performance below average',
                'recommendation': 'Work on clear communication, confidence, and providing structured answers to behavioral questions',
                'priority': 'high'
            })
        
        # Add strengths
        strengths = []
        for skill, result in mcq_by_skill.items():
            if result['percentage'] >= 85:
                strengths.append(f"{skill} (MCQ: {result['percentage']}%)")
        
        for skill, result in coding_by_skill.items():
            if result['percentage'] >= 80:
                strengths.append(f"{skill} (Coding: {result['percentage']}%)")
        
        return {
            'recommendations': recommendations,
            'strengths': strengths,
            'focus_areas': [r['area'] for r in recommendations if r.get('priority') in ['critical', 'high']],
            'total_recommendations': len(recommendations)
        }
    
    def generate_full_report(self, 
                            mcq_results: Dict,
                            coding_results: Dict,
                            hr_results: Dict,
                            skills_with_proficiency: Dict) -> Dict:
        """Generate complete interview report"""
        
        scores = self.calculate_scores(mcq_results, coding_results, hr_results)
        recommendations = self.generate_recommendations(scores, skills_with_proficiency)
        
        # Determine if ready for position
        readiness = self._assess_job_readiness(scores)
        
        report = {
            'timestamp': datetime.now().isoformat(),
            'overall_score': scores['final_score'],
            'performance_level': scores['overall_level'],
            'component_scores': {
                'mcq': {
                    'score': scores['mcq']['overall_percentage'],
                    'weight': self.weights['mcq'],
                    'weighted_contribution': round(scores['mcq']['overall_percentage'] * self.weights['mcq'], 2)
                },
                'coding': {
                    'score': scores['coding']['overall_percentage'],
                    'weight': self.weights['coding'],
                    'weighted_contribution': round(scores['coding']['overall_percentage'] * self.weights['coding'], 2)
                },
                'hr_interview': {
                    'score': scores['hr_interview']['score'],
                    'weight': self.weights['hr_interview'],
                    'weighted_contribution': round(scores['hr_interview']['score'] * self.weights['hr_interview'], 2)
                }
            },
            'skill_wise_performance': {
                'mcq': scores['mcq']['by_skill'],
                'coding': scores['coding']['by_skill']
            },
            'recommendations': recommendations,
            'job_readiness': readiness,
            'next_steps': self._generate_next_steps(scores, recommendations)
        }
        
        return report
    
    def _assess_job_readiness(self, scores: Dict) -> Dict:
        """Assess readiness for different positions"""
        final_score = scores['final_score']
        
        readiness = {
            'senior_positions': {
                'ready': final_score >= 85,
                'score': final_score,
                'feedback': 'Excellent - Ready for Senior/Lead positions' if final_score >= 85 
                           else 'Not ready yet - Target: 85+'
            },
            'mid_level_positions': {
                'ready': final_score >= 70,
                'score': final_score,
                'feedback': 'Good - Ready for Mid-Level positions' if final_score >= 70 
                           else 'Not ready yet - Target: 70+'
            },
            'entry_level_positions': {
                'ready': final_score >= 55,
                'score': final_score,
                'feedback': 'Average - Ready for Entry-Level positions' if final_score >= 55 
                           else 'Needs preparation - Target: 55+'
            }
        }
        
        return readiness
    
    def _generate_next_steps(self, scores: Dict, recommendations: Dict) -> List[str]:
        """Generate actionable next steps"""
        next_steps = []
        
        final_score = scores['final_score']
        
        if final_score < 55:
            next_steps.extend([
                "1. Focus on fundamental concepts in weak skills",
                "2. Solve at least 20 basic coding problems",
                "3. Practice MCQ questions daily (30 min)",
                "4. Work on communication skills with mock interviews"
            ])
        elif final_score < 70:
            next_steps.extend([
                "1. Strengthen intermediate problem-solving skills",
                "2. Solve 15-20 intermediate coding problems",
                "3. Review MCQ answers for weak topics",
                "4. Practice behavioral questions with sample answers"
            ])
        elif final_score < 85:
            next_steps.extend([
                "1. Master advanced algorithms and data structures",
                "2. Solve 10-15 advanced coding problems",
                "3. Refine problem-solving efficiency",
                "4. Prepare for technical discussions in interviews"
            ])
        else:
            next_steps.extend([
                "1. You're ready! Start applying to senior positions",
                "2. Prepare system design interview questions",
                "3. Keep skill sharp with 2-3 problems weekly",
                "4. Mentor junior developers and strengthen leadership"
            ])
        
        return next_steps
