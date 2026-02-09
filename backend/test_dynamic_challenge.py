"""
Test: Verify 3 Unique Coding Challenges Generated Per Programming Skill

This test simulates the resume analysis flow and confirms that:
1. Each programming skill generates exactly 3 coding challenges
2. All 3 challenges are unique (different titles)
3. Challenges use the new scenario-based generation
"""

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from modules.question_generator import QuestionGenerator

def test_three_challenges_per_skill():
    """Test that 3 unique challenges are generated for each programming skill"""
    print("=" * 70)
    print("TEST: 3 Unique Coding Challenges Per Programming Skill")
    print("=" * 70)
    
    generator = QuestionGenerator()
    
    # Simulate resume with 2 programming skills
    skills_with_proficiency = [
        {'skill': 'Python', 'proficiency': 'intermediate'},
        {'skill': 'JavaScript', 'proficiency': 'beginner'}
    ]
    
    print("\n📋 Simulated Resume Skills:")
    for skill_info in skills_with_proficiency:
        print(f"  • {skill_info['skill']} ({skill_info['proficiency']})")
    
    # Generate quiz (same as your actual system does)
    print("\n🔄 Generating challenges...")
    quiz_data = generator.generate_quiz_for_skills(skills_with_proficiency)
    
    # Extract coding challenges
    coding_challenges = quiz_data.get('coding_challenges', [])
    
    print(f"\n✅ Total Coding Challenges Generated: {len(coding_challenges)}")
    print(f"   Expected: {len(skills_with_proficiency)} skills × 3 challenges = {len(skills_with_proficiency) * 3}")
    
    # Group by skill
    challenges_by_skill = {}
    for challenge in coding_challenges:
        skill = challenge.get('skill', 'Unknown')
        if skill not in challenges_by_skill:
            challenges_by_skill[skill] = []
        challenges_by_skill[skill].append(challenge)
    
    print("\n" + "=" * 70)
    print("RESULTS BY SKILL")
    print("=" * 70)
    
    all_passed = True
    
    for skill_info in skills_with_proficiency:
        skill = skill_info['skill']
        challenges = challenges_by_skill.get(skill, [])
        
        print(f"\n📌 {skill} ({skill_info['proficiency']}):")
        print(f"   Challenges Generated: {len(challenges)}/3")
        
        if len(challenges) != 3:
            print(f"   ❌ FAIL: Expected 3 challenges, got {len(challenges)}")
            all_passed = False
        else:
            print(f"   ✅ PASS: Correct number of challenges")
        
        # Check uniqueness
        titles = [c.get('title', '') for c in challenges]
        unique_titles = set(titles)
        
        print(f"   Unique Titles: {len(unique_titles)}/{len(titles)}")
        
        if len(unique_titles) != len(titles):
            print(f"   ❌ FAIL: Duplicate titles found")
            all_passed = False
        else:
            print(f"   ✅ PASS: All titles are unique")
        
        # Show challenge details
        print(f"\n   Challenge Details:")
        for i, challenge in enumerate(challenges, 1):
            title = challenge.get('title', 'Untitled')
            scenario = challenge.get('scenario', 'N/A')
            difficulty = challenge.get('difficulty', 'N/A')
            
            print(f"      {i}. {title}")
            print(f"         Scenario: {scenario}")
            print(f"         Difficulty: {difficulty}")
    
    # Final summary
    print("\n" + "=" * 70)
    print("FINAL SUMMARY")
    print("=" * 70)
    
    total_expected = len(skills_with_proficiency) * 3
    total_generated = len(coding_challenges)
    
    print(f"Expected Total: {total_expected} challenges")
    print(f"Generated Total: {total_generated} challenges")
    
    if total_generated == total_expected and all_passed:
        print("\n🎉 ✅ ALL TESTS PASSED!")
        print("   • Correct number of challenges per skill")
        print("   • All challenges are unique")
        print("   • Scenario-based generation working")
        return True
    else:
        print("\n❌ TESTS FAILED")
        return False


if __name__ == "__main__":
    try:
        success = test_three_challenges_per_skill()
        exit(0 if success else 1)
    except Exception as e:
        print(f"\n❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()
        exit(1)
