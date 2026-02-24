"""
Enhanced question generator with 5 MCQ per skill and difficulty-based coding challenges
"""

import json
import random
from typing import List, Dict
from config import Config
from modules.fallback_questions import get_mcq_questions, get_coding_challenges

class EnhancedQuestionGenerator:
    """Generate structured questions: 5 MCQ per skill + coding challenges by difficulty"""
    
    def __init__(self):
        pass
    
    def generate_skill_based_mcq(self, skills_with_proficiency: Dict[str, str]) -> Dict[str, List[Dict]]:
        """
        Generate 5 MCQ questions per skill based on proficiency level
        
        Args:
            skills_with_proficiency: {skill: proficiency_level}
            
        Returns:
            {skill: [list of 5 MCQ questions]}
        """
        all_questions = {}
        
        for skill, proficiency in skills_with_proficiency.items():
            # Normalize skill name
            skill_normalized = skill.strip()
            
            # Try to get questions (fallback if API fails)
            try:
                questions = get_mcq_questions(skill_normalized, proficiency, count=5)
                if questions:
                    all_questions[skill_normalized] = questions
                else:
                    # If no specific proficiency level, try beginner
                    questions = get_mcq_questions(skill_normalized, "beginner", count=5)
                    if questions:
                        all_questions[skill_normalized] = questions
            except Exception as e:
                print(f"Error generating questions for {skill}: {e}")
                continue
        
        return all_questions
    
    def generate_coding_challenges(self, skills_with_proficiency: Dict[str, str]) -> Dict[str, Dict]:
        """
        Generate coding challenges per skill:
        - 1 basic challenge
        - 2 intermediate challenges
        - 2 advanced challenges
        
        Args:
            skills_with_proficiency: {skill: proficiency_level}
            
        Returns:
            {skill: {basic: [], intermediate: [], advanced: []}}
        """
        all_challenges = {}
        
        # Programming languages that typically have coding challenges
        programming_languages = ['Python', 'JavaScript', 'Java', 'C++', 'C#', 'Go', 'Rust']
        
        for skill, proficiency in skills_with_proficiency.items():
            skill_normalized = skill.strip()
            
            # Only generate coding challenges for programming languages
            if any(lang.lower() in skill_normalized.lower() for lang in programming_languages):
                challenges = get_coding_challenges(skill_normalized)
                
                if challenges:
                    # Ensure we have the right structure
                    structured_challenges = {
                        'basic': challenges.get('basic', [])[:1],      # 1 basic
                        'intermediate': challenges.get('intermediate', [])[:2],  # 2 intermediate
                        'advanced': challenges.get('advanced', [])[:2]  # 2 advanced
                    }
                    all_challenges[skill_normalized] = structured_challenges
        
        return all_challenges
    
    def get_skill_based_assessment(self, skills_with_proficiency: Dict[str, str]) -> Dict:
        """
        Generate complete assessment: MCQ + Coding Challenges
        
        Returns:
            {
                'mcq_questions': {...},
                'coding_challenges': {...},
                'total_mcq': total_count,
                'total_coding': total_count,
                'assessment_structure': description
            }
        """
        mcq = self.generate_skill_based_mcq(skills_with_proficiency)
        coding = self.generate_coding_challenges(skills_with_proficiency)
        
        # Calculate totals
        total_mcq = sum(len(questions) for questions in mcq.values())
        total_coding = sum(
            len(coding.get(skill, {}).get('basic', [])) +
            len(coding.get(skill, {}).get('intermediate', [])) +
            len(coding.get(skill, {}).get('advanced', []))
            for skill in skills_with_proficiency.keys()
        )
        
        return {
            'mcq_questions': mcq,
            'coding_challenges': coding,
            'total_mcq': total_mcq,
            'total_coding': total_coding,
            'assessment_structure': {
                'mcq_per_skill': 5,
                'coding_per_skill': {
                    'basic': 1,
                    'intermediate': 2,
                    'advanced': 2,
                    'total': 5
                }
            }
        }
