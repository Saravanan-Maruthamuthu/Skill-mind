"""
Test script to verify enhanced quiz and coding challenge generation
"""
import sys
sys.path.append('e:/Skill Mind AI Antigravity/backend')

from modules.question_generator import QuestionGenerator
from config import Config

def test_mcq_generation():
    """Test that MCQ generates 10 questions"""
    print("=" * 60)
    print("Testing MCQ Generation (10 questions per skill)")
    print("=" * 60)
    
    qg = QuestionGenerator()
    
    # Test with fallback (no API key needed)
    questions = qg._get_fallback_mcq('Python', 'intermediate', 10)
    
    print(f"\n✓ Generated {len(questions)} MCQ questions")
    print(f"✓ Expected: {Config.MCQ_PER_SKILL} questions")
    print(f"✓ Match: {len(questions) == Config.MCQ_PER_SKILL}")
    
    if questions:
        print(f"\n Sample Question:")
        print(f"  Q: {questions[0]['question']}")
        print(f"  Skill: {questions[0]['skill']}")
        print(f"  Difficulty: {questions[0]['difficulty']}")
    
    return len(questions) == Config.MCQ_PER_SKILL

def test_coding_challenge():
    """Test HackerRank-style coding challenge"""
    print("\n" + "=" * 60)
    print("Testing HackerRank-Style Coding Challenge")
    print("=" * 60)
    
    qg = QuestionGenerator()
    
    # Test with fallback
    challenge = qg._get_fallback_coding('Python', 'intermediate')
    
    print(f"\n✓ Challenge Title: {challenge.get('title')}")
    print(f"✓ Has Description: {bool(challenge.get('description'))}")
    print(f"✓ Has Input Format: {bool(challenge.get('input_format'))}")
    print(f"✓ Has Output Format: {bool(challenge.get('output_format'))}")
    print(f"✓ Has Constraints: {bool(challenge.get('constraints'))}")
    print(f"✓ Has Test Cases: {len(challenge.get('test_cases', []))} test cases")
    print(f"✓ Has Hints: {bool(challenge.get('hints'))}")
    print(f"✓ Has Time Complexity: {challenge.get('time_complexity')}")
    print(f"✓ Has Space Complexity: {challenge.get('space_complexity')}")
    print(f"✓ Has Tags: {challenge.get('tags')}")
    
    # Check for HackerRank-style fields
    required_fields = ['title', 'description', 'input_format', 'output_format', 
                      'constraints', 'test_cases', 'hints', 'time_complexity', 
                      'space_complexity', 'tags']
    
    has_all_fields = all(field in challenge for field in required_fields)
    print(f"\n✓ Has all HackerRank-style fields: {has_all_fields}")
    
    return has_all_fields

def test_weighted_scoring():
    """Test weighted scoring configuration"""
    print("\n" + "=" * 60)
    print("Testing Weighted Scoring Configuration")
    print("=" * 60)
    
    weights = Config.SCORING_WEIGHTS
    
    print(f"\n✓ MCQ Weight: {weights['mcq'] * 100}%")
    print(f"✓ Coding Weight: {weights['coding'] * 100}%")
    print(f"✓ HR Interview Weight: {weights['hr_interview'] * 100}%")
    
    total_weight = sum(weights.values())
    print(f"\n✓ Total Weight: {total_weight * 100}%")
    print(f"✓ Weights sum to 100%: {total_weight == 1.0}")
    
    return total_weight == 1.0

def main():
    print("\n" + "=" * 60)
    print("ENHANCED QUIZ SYSTEM - VERIFICATION TESTS")
    print("=" * 60)
    
    results = {
        'MCQ Generation (10 questions)': test_mcq_generation(),
        'HackerRank-Style Coding': test_coding_challenge(),
        'Weighted Scoring': test_weighted_scoring()
    }
    
    print("\n" + "=" * 60)
    print("TEST RESULTS SUMMARY")
    print("=" * 60)
    
    for test_name, passed in results.items():
        status = "✓ PASSED" if passed else "✗ FAILED"
        print(f"{status}: {test_name}")
    
    all_passed = all(results.values())
    print("\n" + "=" * 60)
    if all_passed:
        print("✓ ALL TESTS PASSED!")
    else:
        print("✗ SOME TESTS FAILED")
    print("=" * 60)
    
    return all_passed

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)
