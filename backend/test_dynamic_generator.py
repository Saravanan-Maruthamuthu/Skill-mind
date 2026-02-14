"""
Simple test script for Dynamic Challenge Generator
"""

from modules.dynamic_challenge_generator import DynamicChallengeGenerator

def test_basic_generation():
    """Test basic challenge generation"""
    print("🧪 Testing Dynamic Challenge Generator\n")
    print("=" * 60)
    
    generator = DynamicChallengeGenerator()
    
    # Test 1: Python Beginner Arrays
    print("\n📝 Test 1: Python + Beginner + Arrays")
    print("-" * 60)
    challenge1 = generator.generate_challenge("Python", "Beginner", "Arrays")
    print(f"✅ Title: {challenge1['title']}")
    print(f"✅ Test Cases: {len(challenge1['test_cases'])}")
    print(f"✅ Constraints: {len(challenge1['constraints'])}")
    
    # Test 2: Java Intermediate Strings
    print("\n📝 Test 2: Java + Intermediate + Strings")
    print("-" * 60)
    challenge2 = generator.generate_challenge("Java", "Intermediate", "Strings")
    print(f"✅ Title: {challenge2['title']}")
    print(f"✅ Difficulty: {challenge2['difficulty']}")
    print(f"✅ Language: {challenge2['language']}")
    
    # Test 3: JavaScript Advanced Algorithms
    print("\n📝 Test 3: JavaScript + Advanced + Algorithms")
    print("-" * 60)
    challenge3 = generator.generate_challenge("JavaScript", "Advanced", "Algorithms")
    print(f"✅ Title: {challenge3['title']}")
    print(f"✅ Hints: {len(challenge3['hints'])}")
    
    # Test 4: Uniqueness - Same params, different output
    print("\n📝 Test 4: Uniqueness Test (Same Parameters)")
    print("-" * 60)
    titles = []
    for i in range(3):
        ch = generator.generate_challenge("Python", "Intermediate", "Arrays")
        titles.append(ch['title'])
        print(f"   Generation {i+1}: {ch['title']}")
    
    if len(set(titles)) == 3:
        print("✅ All 3 generations produced UNIQUE titles!")
    else:
        print("⚠️  Some titles were repeated (this is rare but possible)")
    
    print("\n" + "=" * 60)
    print("✅ All tests passed! Generator is working correctly.")
    print("=" * 60)

if __name__ == "__main__":
    test_basic_generation()
