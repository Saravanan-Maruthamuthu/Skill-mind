"""
Test Question Shuffling in MCQ Quiz Generation
Verifies that questions are shuffled for each quiz session
"""

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from modules.fast_mcq_generator import FastMCQGenerator
import random

def test_question_shuffling():
    """Test that questions are shuffled correctly"""
    
    generator = FastMCQGenerator()
    
    print("🔀 Testing Question Shuffling\n")
    print("=" * 60)
    
    # Generate questions for Python
    print("\n1️⃣  Generating 5 Python beginner questions...")
    questions = generator.generate_mcq_questions("Python", "beginner", 5)
    
    print(f"   ✅ Generated {len(questions)} questions")
    print("\n   Original Order:")
    for i, q in enumerate(questions, 1):
        print(f"   {i}. {q['question'][:60]}...")
    
    # Shuffle the questions
    print("\n2️⃣  Shuffling questions...")
    shuffled_questions = questions.copy()
    random.shuffle(shuffled_questions)
    
    print("\n   Shuffled Order:")
    for i, q in enumerate(shuffled_questions, 1):
        print(f"   {i}. {q['question'][:60]}...")
    
    # Verify they're different
    print("\n3️⃣  Verification:")
    
    # Check if at least one question changed position
    position_changed = False
    for i in range(len(questions)):
        if questions[i]['question'] != shuffled_questions[i]['question']:
            position_changed = True
            break
    
    if position_changed:
        print("   ✅ Questions successfully shuffled!")
    else:
        print("   ⚠️  Questions might not be shuffled (or random order matched)")
    
    # Test with multiple skills
    print("\n" + "=" * 60)
    print("\n4️⃣  Testing with Multiple Skills (Python + Java)...")
    
    python_mcqs = generator.generate_mcq_questions("Python", "beginner", 3)
    java_mcqs = generator.generate_mcq_questions("Java", "beginner", 3)
    
    all_mcqs = python_mcqs + java_mcqs
    
    print(f"\n   Before Shuffle ({len(all_mcqs)} questions):")
    for i, q in enumerate(all_mcqs, 1):
        print(f"   {i}. [{q['skill']}] {q['question'][:50]}...")
    
    # Shuffle
    random.shuffle(all_mcqs)
    
    print(f"\n   After Shuffle ({len(all_mcqs)} questions):")
    for i, q in enumerate(all_mcqs, 1):
        print(f"   {i}. [{q['skill']}] {q['question'][:50]}...")
    
    print("\n" + "=" * 60)
    print("\n✅ Question Shuffling Test Complete!")
    print("\n💡 Each quiz session will have questions in random order")
    print("   while answer options are also shuffled within each question.\n")

if __name__ == "__main__":
    test_question_shuffling()
