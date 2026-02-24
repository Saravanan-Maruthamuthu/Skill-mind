"""
Enhanced HR Interview Module with behavioral and technical questions
"""

import json
from typing import List, Dict
import random

class EnhancedHRInterviewer:
    """Conduct enhanced HR interviews with behavioral and technical questions"""
    
    BEHAVIORAL_QUESTIONS = [
        {
            "id": "b1",
            "question": "Tell me about a time when you faced a technical challenge. How did you overcome it?",
            "category": "Problem Solving",
            "type": "behavioral",
            "evaluation_criteria": ["Clarity", "Problem Analysis", "Solution Approach", "Learning"]
        },
        {
            "id": "b2",
            "question": "Describe a situation where you had to work with a difficult team member. How did you handle it?",
            "category": "Teamwork",
            "type": "behavioral",
            "evaluation_criteria": ["Empathy", "Communication", "Conflict Resolution", "Professionalism"]
        },
        {
            "id": "b3",
            "question": "Share an example of when you had to learn a new technology quickly.",
            "category": "Learning Ability",
            "type": "behavioral",
            "evaluation_criteria": ["Adaptability", "Initiative", "Learning Speed", "Application"]
        },
        {
            "id": "b4",
            "question": "Tell me about a project you're proud of. What was your role and contribution?",
            "category": "Achievement",
            "type": "behavioral",
            "evaluation_criteria": ["Impact", "Technical Depth", "Leadership", "Communication"]
        },
        {
            "id": "b5",
            "question": "Describe a time when you failed. What did you learn from it?",
            "category": "Resilience",
            "type": "behavioral",
            "evaluation_criteria": ["Honesty", "Learning Mindset", "Accountability", "Growth"]
        },
        {
            "id": "b6",
            "question": "How do you prioritize when you have multiple tasks with the same deadline?",
            "category": "Time Management",
            "type": "behavioral",
            "evaluation_criteria": ["Priority Assessment", "Communication", "Organization", "Execution"]
        },
        {
            "id": "b7",
            "question": "Tell me about a time you had to debug production code. Walk me through your approach.",
            "category": "Technical Problem-Solving",
            "type": "behavioral",
            "evaluation_criteria": ["Systematic Thinking", "Debugging Skills", "Tools Knowledge", "Communication"]
        },
        {
            "id": "b8",
            "question": "Describe your experience with code reviews. Have you given or received critical feedback?",
            "category": "Code Quality",
            "type": "behavioral",
            "evaluation_criteria": ["Attention to Detail", "Constructiveness", "Openness", "Standards Knowledge"]
        }
    ]
    
    TECHNICAL_FOLLOWUP_QUESTIONS = {
        "Python": [
            "What are decorators in Python and when would you use them?",
            "Explain the difference between deep copy and shallow copy",
            "What is the GIL (Global Interpreter Lock)?",
        ],
        "JavaScript": [
            "Explain event delegation and why it's useful",
            "What is the difference between var, let, and const?",
            "How do closures work in JavaScript?",
        ],
        "Java": [
            "What are the 4 pillars of OOP?",
            "Explain the difference between abstract classes and interfaces",
            "What is the purpose of the 'final' keyword?",
        ],
        "React": [
            "Explain the virtual DOM and its importance",
            "What are React hooks and how do they change component logic?",
            "How does React handle state management?",
        ],
        "SQL": [
            "What is the difference between INNER JOIN and LEFT JOIN?",
            "Explain database normalization and its types",
            "What are indexes and when should you use them?",
        ]
    }
    
    def __init__(self):
        pass
    
    def get_interview_questions(self, skills: List[str], num_questions: int = 7) -> List[Dict]:
        """
        Get interview questions mix of behavioral and technical
        
        Args:
            skills: List of candidate's skills
            num_questions: Total questions to ask (default 7)
            
        Returns:
            List of interview questions
        """
        questions = []
        
        # 80% behavioral, 20% technical
        behavioral_count = int(num_questions * 0.8)
        technical_count = num_questions - behavioral_count
        
        # Add behavioral questions
        selected_behavioral = random.sample(self.BEHAVIORAL_QUESTIONS, min(behavioral_count, len(self.BEHAVIORAL_QUESTIONS)))
        questions.extend(selected_behavioral)
        
        # Add technical follow-up questions
        for skill in skills[:technical_count]:
            if skill in self.TECHNICAL_FOLLOWUP_QUESTIONS:
                technical_q = random.choice(self.TECHNICAL_FOLLOWUP_QUESTIONS[skill])
                questions.append({
                    "id": f"t_{skill.lower()}",
                    "question": technical_q,
                    "category": skill,
                    "type": "technical",
                    "evaluation_criteria": ["Technical Knowledge", "Clarity", "Depth", "Problem-Solving"]
                })
        
        return questions
    
    def evaluate_answer(self, answer: str, question: Dict, criteria: List[str] = None) -> Dict:
        """
        Evaluate an interview answer
        
        Args:
            answer: Candidate's answer
            question: The question object
            criteria: Evaluation criteria
            
        Returns:
            Score and feedback
        """
        criteria = criteria or question.get('evaluation_criteria', [])
        
        # Simple scoring based on answer length and keywords
        score = self._calculate_answer_score(answer, question, criteria)
        
        feedback = self._generate_feedback(answer, question, score)
        
        return {
            'question_id': question['id'],
            'question': question['question'],
            'answer': answer,
            'score': score,
            'criteria_scores': self._score_criteria(answer, criteria),
            'feedback': feedback,
            'category': question.get('category', 'Unknown')
        }
    
    def _calculate_answer_score(self, answer: str, question: Dict, criteria: List[str]) -> float:
        """Calculate score (0-100) for an answer"""
        if not answer or len(answer.strip()) == 0:
            return 0
        
        score = 50  # Base score
        
        # Bonus points for answer length (indicates detail)
        word_count = len(answer.split())
        if word_count > 50:
            score += 15
        elif word_count > 30:
            score += 10
        elif word_count > 20:
            score += 5
        
        # Bonus for specific examples/metrics
        if any(word in answer.lower() for word in ['example', 'specific', 'number', '%', 'result', 'outcome']):
            score += 15
        
        # Bonus for structure (multiple sentences)
        if answer.count('.') > 2:
            score += 10
        
        # Cap at 100
        score = min(score, 100)
        return score
    
    def _score_criteria(self, answer: str, criteria: List[str]) -> Dict[str, float]:
        """Score answer against specific criteria"""
        criteria_scores = {}
        avg_score = self._calculate_answer_score("dummy", {}, criteria) / 100 * 100
        
        for criterion in criteria:
            # Distribute score based on criteria
            criteria_scores[criterion] = round(avg_score * random.uniform(0.7, 1.0), 2)
        
        return criteria_scores
    
    def _generate_feedback(self, answer: str, question: Dict, score: float) -> str:
        """Generate feedback based on score"""
        if score >= 80:
            return "Excellent answer with specific examples and clear reasoning"
        elif score >= 65:
            return "Good answer but could include more specific examples or details"
        elif score >= 50:
            return "Average answer - try to provide specific examples and measurable outcomes"
        else:
            return "Consider providing more detailed explanation with real-world examples"
    
    def generate_interview_summary(self, answers: List[Dict]) -> Dict:
        """Generate interview summary with overall score and feedback"""
        if not answers:
            return {'overall_score': 0, 'feedback': 'No answers provided'}
        
        scores = [a['score'] for a in answers]
        overall_score = sum(scores) / len(scores) if scores else 0
        
        # Categorize feedback
        strengths = []
        weaknesses = []
        
        for answer in answers:
            if answer['score'] >= 75:
                strengths.append(f"Strong performance in {answer.get('category', 'General')}")
            elif answer['score'] < 60:
                weaknesses.append(f"Need improvement in {answer.get('category', 'General')}")
        
        return {
            'overall_score': round(overall_score, 2),
            'performance_level': self._get_performance_level(overall_score),
            'total_questions_answered': len(answers),
            'average_score': round(overall_score, 2),
            'strengths': strengths,
            'weaknesses': weaknesses,
            'detailed_answers': answers,
            'feedback': f"Overall performance: {self._get_performance_level(overall_score).capitalize()}. "
                       f"Continue to provide specific examples and measurable outcomes in interviews."
        }
    
    def _get_performance_level(self, score: float) -> str:
        """Get performance level description"""
        if score >= 85:
            return 'excellent'
        elif score >= 70:
            return 'good'
        elif score >= 55:
            return 'average'
        elif score >= 40:
            return 'needs_improvement'
        else:
            return 'not_ready'


class InterviewSession:
    """Manage an interview session"""
    
    def __init__(self, candidate_skills: List[str]):
        self.interviewer = EnhancedHRInterviewer()
        self.questions = self.interviewer.get_interview_questions(candidate_skills)
        self.current_question_idx = 0
        self.answers = []
        self.start_time = None
    
    def get_current_question(self) -> Dict:
        """Get current question"""
        if self.current_question_idx < len(self.questions):
            return self.questions[self.current_question_idx]
        return None
    
    def submit_answer(self, answer: str) -> Dict:
        """Submit answer for current question"""
        current_question = self.get_current_question()
        
        if not current_question:
            return {'error': 'No more questions'}
        
        evaluation = self.interviewer.evaluate_answer(answer, current_question)
        self.answers.append(evaluation)
        
        self.current_question_idx += 1
        
        return {
            'evaluation': evaluation,
            'next_question': self.get_current_question(),
            'progress': f"{self.current_question_idx}/{len(self.questions)}"
        }
    
    def is_complete(self) -> bool:
        """Check if interview is complete"""
        return self.current_question_idx >= len(self.questions)
    
    def get_summary(self) -> Dict:
        """Get interview summary"""
        return self.interviewer.generate_interview_summary(self.answers)
