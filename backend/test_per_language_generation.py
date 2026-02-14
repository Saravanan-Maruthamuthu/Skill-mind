"""
Test script to verify per-language question generation
Generates 3 coding challenges for each programming language skill
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from modules.question_generator import QuestionGenerator
from config import Config

def test_per_language_generation():
    """Test generating 3 questions per programming language"""
    
    print("="*80)
    print("Testing Per-Language Question Generation")
    print("="*80)
    
    # Initialize generator
    generator = QuestionGenerator()
    
    # Sample programming languages from a resume
    programming_skills = [
        {'skill': 'Python', 'proficiency': 'advanced', 'mentions': 10},
        {'skill': 'Java', 'proficiency': 'intermediate', 'mentions': 5},
        {'skill': 'C', 'proficiency': 'beginner', 'mentions': 2}
    ]
    
    years_of_experience = 3
    
    print(f"\nTest Configuration:")
    print(f"  - Languages: {[s['skill'] for s in programming_skills]}")
    print(f"  - Years of Experience: {years_of_experience}")
    print(f"  - Expected Challenges: {len(programming_skills) * 3}")
    
    # Generate challenges
    challenges = generator.generate_questions_per_language(
        programming_languages=programming_skills,
        years_of_experience=years_of_experience
    )
    
    # Verify results
    print("\n" + "="*80)
    print("VERIFICATION RESULTS")
    print("="*80)
    
    print(f"\nTotal challenges generated: {len(challenges)}")
    print(f"Expected: {len(programming_skills) * 3}")
    
    # Group by language
    by_language = {}
    for challenge in challenges:
        lang = challenge.get('language', challenge.get('skill', 'Unknown'))
        if lang not in by_language:
            by_language[lang] = []
        by_language[lang].append(challenge)
    
    print("\nBreakdown by language:")
    for lang, lang_challenges in by_language.items():
        print(f"\n  {lang}: {len(lang_challenges)} challenges")
        for i, ch in enumerate(lang_challenges, 1):
            print(f"    {i}. {ch.get('title', 'Untitled')}")
            print(f"       - Difficulty: {ch.get('difficulty', 'N/A')}")
            print(f"       - Scenario: {ch.get('scenario', 'N/A')}")
            print(f"       - Test cases: {len(ch.get('test_cases', []))}")
    
    # Check uniqueness
    print("\n" + "-"*80)
    print("Uniqueness Check:")
    all_titles = [ch.get('title', '') for ch in challenges]
    unique_titles = set(all_titles)
    
    print(f"  Total titles: {len(all_titles)}")
    print(f"  Unique titles: {len(unique_titles)}")
    
    if len(all_titles) == len(unique_titles):
        print("  [OK] All challenges have unique titles")
    else:
        print("  [FAIL] Some duplicate titles found:")
        duplicates = [title for title in all_titles if all_titles.count(title) > 1]
        for dup in set(duplicates):
            print(f"    - '{dup}' appears {all_titles.count(dup)} times")
    
    # Verify required fields
    print("\n" + "-"*80)
    print("Field Validation:")
    required_fields = ['title', 'description', 'test_cases', 'difficulty', 'skill']
    
    all_valid = True
    for i, challenge in enumerate(challenges, 1):
        missing = [field for field in required_fields if field not in challenge]
        if missing:
            print(f"  [FAIL] Challenge {i} missing fields: {missing}")
            all_valid = False
    
    if all_valid:
        print(f"  [OK] All {len(challenges)} challenges have required fields")
    
    print("\n" + "="*80)
    print("TEST COMPLETE")
    print("="*80)
    
    return challenges

if __name__ == "__main__":
    try:
        challenges = test_per_language_generation()
        print(f"\n[OK] Test completed successfully!")
        print(f"[OK] Generated {len(challenges)} total challenges")
    except Exception as e:
        print(f"\n[ERROR] Test failed with error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
