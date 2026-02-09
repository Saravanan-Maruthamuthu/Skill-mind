"""
Test Challenge Uniqueness and Diversity

This script tests that the enhanced question generator creates unique challenges
and that the fallback system generates diverse template-based problems.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from modules.question_generator import QuestionGenerator
from config import Config

def test_challenge_uniqueness():
    """Test that multiple generated challenges are unique"""
    print("=" * 60)
    print("TEST 1: Challenge Uniqueness (API-based)")
    print("=" * 60)
    
    generator = QuestionGenerator()
    
    # Generate 5 challenges for the same skill
    skill = "Python"
    proficiency = "intermediate"
    challenges = []
    
    for i in range(5):
        print(f"\nGenerating challenge {i+1}...")
        challenge = generator.generate_coding_challenge(skill, proficiency, avoid_topics=[c['title'] for c in challenges])
        challenges.append(challenge)
        print(f"  Title: {challenge['title']}")
        print(f"  Scenario: {challenge.get('scenario', 'N/A')}")
        print(f"  Description length: {len(challenge['description'])} chars")
    
    # Verify uniqueness
    titles = [c['title'] for c in challenges]
    unique_titles = set(titles)
    
    print(f"\nResults:")
    print(f"  Total challenges generated: {len(challenges)}")
    print(f"  Unique titles: {len(unique_titles)}/{len(titles)}")
    print(f"  All titles: {titles}")
    
    if len(unique_titles) == len(titles):
        print("  ✅ PASS: All challenges have unique titles!")
    else:
        print("  ❌ FAIL: Some challenges have duplicate titles")
    
    return len(unique_titles) == len(titles)


def test_fallback_diversity():
    """Test that fallback challenges are diverse"""
    print("\n" + "=" * 60)
    print("TEST 2: Fallback Diversity (Template-based)")
    print("=" * 60)
    
    generator = QuestionGenerator()
    
    # Test fallback generation directly
    challenges = []
    
    for i in range(5):
        print(f"\nGenerating fallback challenge {i+1}...")
        challenge = generator._get_fallback_coding("Python", "beginner", avoid_topics=[c['title'] for c in challenges])
        challenges.append(challenge)
        print(f"  Title: {challenge['title']}")
        print(f"  Scenario: {challenge.get('scenario', 'N/A')}")
        print(f"  Template-based: {'scenario' in challenge}")
    
    # Verify diversity
    titles = [c['title'] for c in challenges]
    scenarios = [c.get('scenario', '') for c in challenges]
    unique_titles = set(titles)
    unique_scenarios = set(scenarios)
    
    print(f"\nResults:")
    print(f"  Total fallback challenges: {len(challenges)}")
    print(f"  Unique titles: {len(unique_titles)}/{len(titles)}")
    print(f"  Unique scenarios: {len(unique_scenarios)}/{len(scenarios)}")
    print(f"  Scenarios used: {list(unique_scenarios)}")
    
    # Check that none are "Two Sum" or other old hardcoded challenges
    old_challenges = ["Two Sum", "Palindrome Check", "Reverse Integer", "FizzBuzz"]
    has_old = any(title in old_challenges for title in titles)
    
    if has_old:
        print("  ❌ FAIL: Found old hardcoded challenges!")
        return False
    else:
        print("  ✅ PASS: No old hardcoded challenges found!")
    
    if len(unique_titles) >= 4:  # At least 4 out of 5 should be unique
        print("  ✅ PASS: Good title diversity!")
        return True
    else:
        print("  ❌ FAIL: Insufficient title diversity")
        return False


def test_scenario_coverage():
    """Test that different scenarios are being used"""
    print("\n" + "=" * 60)
    print("TEST 3: Scenario Template Coverage")
    print("=" * 60)
    
    generator = QuestionGenerator()
    
    # Generate many challenges to see scenario diversity
    scenarios_used = set()
    
    for i in range(10):
        challenge = generator._get_fallback_coding("Python", "intermediate")
        scenarios_used.add(challenge.get('scenario', ''))
    
    print(f"\nGenerated 10 challenges")
    print(f"Unique scenarios used: {len(scenarios_used)}/10")
    print(f"Scenarios: {list(scenarios_used)}")
    
    if len(scenarios_used) >= 5:
        print("✅ PASS: Good scenario diversity!")
        return True
    else:
        print("❌ FAIL: Low scenario diversity")
        return False


def main():
    """Run all tests"""
    print("\n" + "="*60)
    print("CHALLENGE UNIQUENESS TEST SUITE")
    print("="*60)
    
    results = []
    
    try:
        # Test 1: Uniqueness (requires API)
        try:
            result1 = test_challenge_uniqueness()
            results.append(("API Challenge Uniqueness", result1))
        except Exception as e:
            print(f"\n⚠️  Test 1 skipped (API error): {e}")
            results.append(("API Challenge Uniqueness", None))
        
        # Test 2: Fallback diversity (no API needed)
        result2 = test_fallback_diversity()
        results.append(("Fallback Diversity", result2))
        
        # Test 3: Scenario coverage (no API needed)
        result3 = test_scenario_coverage()
        results.append(("Scenario Coverage", result3))
        
    except Exception as e:
        print(f"\n❌ Tests failed with error: {e}")
        import traceback
        traceback.print_exc()
    
    # Summary
    print("\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60)
    for test_name, result in results:
        if result is None:
            status = "⏭️  SKIPPED"
        elif result:
            status = "✅ PASS"
        else:
            status = "❌ FAIL"
        print(f"{status} - {test_name}")
    
    passed = sum(1 for _, r in results if r == True)
    total = len([r for _, r in results if r is not None])
    print(f"\nTotal: {passed}/{total} tests passed")


if __name__ == "__main__":
    main()
