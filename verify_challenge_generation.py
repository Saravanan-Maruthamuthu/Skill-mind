
import sys
import os
sys.path.append(os.path.join(os.getcwd(), 'backend'))

from modules.question_generator import QuestionGenerator

def verify():
    gen = QuestionGenerator()
    
    print("Testing generate_coding_challenge for JavaScript...")
    # This might hit the API or fallback depending on config/keys
    challenge = gen.generate_coding_challenge('JavaScript', 'intermediate')
    
    print(f"Title: {challenge.get('title')}")
    print(f"Starter Code present: {'starter_code' in challenge}")
    if 'starter_code' in challenge:
        print("Starter Code Preview:")
        print(challenge['starter_code'][:100] + "...")
    else:
        print("ERROR: No starter_code found!")
        
    # Check fallback specifically if possible, but the above call likely hits it if no API key or on error
    # Let's force fallback check by calling _get_fallback_coding directly
    print("\nTesting fallback directly...")
    fallback = gen._get_fallback_coding('JavaScript', 'intermediate')
    print(f"Fallback Title: {fallback['title']}")
    print(f"Fallback Starter Code present: {'starter_code' in fallback}")

if __name__ == "__main__":
    verify()
