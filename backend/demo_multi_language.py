"""
Demonstration: Generate questions for a sample resume with multiple programming languages
Shows the complete flow from resume skills to generated challenges
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from modules.question_generator import QuestionGenerator

def demo_multi_language_generation():
    """
    Demonstrate question generation for a resume with multiple programming languages
    """
    
    print("="*80)
    print("DEMO: Per-Language Question Generation")
    print("="*80)
    
    # Simulate a candidate's resume with multiple programming skills
    print("\nSample Resume Profile:")
    print("-" * 80)
    
    candidate_profile = {
        'name': 'John Doe',
        'experience_years': 5,
        'programming_skills': [
            {'skill': 'Python', 'proficiency': 'advanced', 'mentions': 15},
            {'skill': 'JavaScript', 'proficiency': 'intermediate', 'mentions': 8},
            {'skill': 'C++', 'proficiency': 'intermediate', 'mentions': 6}
        ]
    }
    
    print(f"  Name: {candidate_profile['name']}")
    print(f"  Experience: {candidate_profile['experience_years']} years")
    print(f"  Programming Languages:")
    for skill in candidate_profile['programming_skills']:
        print(f"    - {skill['skill']} ({skill['proficiency']})")
    
    print("\n" + "="*80)
    print("GENERATING CHALLENGES")
    print("="*80)
    print(f"Expected: {len(candidate_profile['programming_skills'])} languages × 3 challenges = {len(candidate_profile['programming_skills']) * 3} total")
    
    # Initialize generator
    generator = QuestionGenerator()
    
    # Generate challenges
    challenges = generator.generate_questions_per_language(
        programming_languages=candidate_profile['programming_skills'],
        years_of_experience=candidate_profile['experience_years']
    )
    
    # Display results
    print("\n" + "="*80)
    print("GENERATED CHALLENGES SUMMARY")
    print("="*80)
    
    for lang in ['Python', 'JavaScript', 'C++']:
        lang_challenges = [c for c in challenges if c.get('language') == lang]
        if lang_challenges:
            print(f"\n{lang} ({len(lang_challenges)} challenges):")
            for i, ch in enumerate(lang_challenges, 1):
                print(f"  {i}. {ch.get('title', 'Untitled')}")
                print(f"     Difficulty: {ch.get('difficulty', 'N/A')}")
                print(f"     Scenario: {ch.get('scenario', 'N/A').replace('_', ' ').title()}")
                print(f"     Test Cases: {len(ch.get('test_cases', []))}")
    
    print("\n" + "="*80)
    print(f"[SUCCESS] Generated {len(challenges)} challenges!")
    print("="*80)
    
    return challenges

if __name__ == "__main__":
    demo_multi_language_generation()
