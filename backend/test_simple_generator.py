"""
Test the simplified question generator with static challenge bank
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from modules.question_generator_simple import QuestionGenerator

def test_simple_generation():
    """Test the simplified challenge generation"""
    
    print("="*80)
    print("TESTING SIMPLIFIED CHALLENGE BANK")
    print("="*80)
    
    # Sample candidate profile
    programming_skills = [
        {'skill': 'Python', 'proficiency': 'advanced', 'mentions': 10},
        {'skill': 'Java', 'proficiency': 'intermediate', 'mentions': 5},
        {'skill': 'JavaScript', 'proficiency': 'beginner', 'mentions': 3}
    ]
    
    print("\nCandidate Skills:")
    for skill in programming_skills:
        print(f"  - {skill['skill']} ({skill['proficiency']})")
    
    # Initialize generator
    generator = QuestionGenerator()
    
    # Generate challenges
    print("\n" + "="*80)
    print("GENERATING CHALLENGES")
    print("="*80)
    
    challenges = generator.generate_questions_per_language(
        programming_languages=programming_skills,
        years_of_experience=3
    )
    
    # Display results
    print("\n" + "="*80)
    print("RESULTS SUMMARY")
    print("="*80)
    
    print(f"\nTotal Challenges Generated: {len(challenges)}")
    print(f"Expected: {len(programming_skills) * 3}")
    
    # Group by language
    for lang in ['Python', 'Java', 'JavaScript']:
        lang_challenges = [c for c in challenges if c.get('language') == lang]
        if lang_challenges:
            print(f"\n{lang} ({len(lang_challenges)} challenges):")
            for i, ch in enumerate(lang_challenges, 1):
                print(f"  {i}. {ch.get('title', 'Untitled')}")
                print(f"     Difficulty: {ch.get('difficulty', 'N/A')}")
                print(f"     Test Cases: {len(ch.get('test_cases', []))}")
    
    # Validation
    print("\n" + "="*80)
    print("VALIDATION")
    print("="*80)
    
    # Check count
    if len(challenges) == len(programming_skills) * 3:
        print("[OK] Correct number of challenges generated")
    else:
        print(f"[FAIL] Expected {len(programming_skills) * 3}, got {len(challenges)}")
    
    # Check required fields
    required_fields = ['title', 'description', 'difficulty', 'test_cases', 'starter_code']
    all_valid = True
    for ch in challenges:
        for field in required_fields:
            if field not in ch:
                print(f"[FAIL] Challenge '{ch.get('title')}' missing field: {field}")
                all_valid = False
    
    if all_valid:
        print("[OK] All challenges have required fields")
    
    # Check uniqueness
    titles = [c.get('title') for c in challenges]
    if len(titles) == len(set(titles)):
        print("[OK] All challenge titles are unique")
    else:
        print("[FAIL] Duplicate challenge titles found")
    
    print("\n" + "="*80)
    print("[SUCCESS] Simplified challenge bank test complete!")
    print("="*80)

if __name__ == "__main__":
    test_simple_generation()
