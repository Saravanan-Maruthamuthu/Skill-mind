import sys
import os

# Add current directory to path so we can import modules
sys.path.append(os.getcwd())

from modules.question_generator import QuestionGenerator
from config import Config

def test_generation():
    print("Testing QuestionGenerator...")
    try:
        # verify api key is present (don't print it)
        if not Config.OPENAI_API_KEY:
             print("ERROR: Config.OPENAI_API_KEY is missing or empty")
             return

        generator = QuestionGenerator()
        print(f"Model: {generator.model}")
        
        skill = "Python"
        proficiency = "Beginner"
        print(f"Generating questions for {skill} ({proficiency})...")
        
        questions = generator.generate_mcq_questions(skill, proficiency, num_questions=2)
        
        if not questions:
            print("FAILURE: No questions returned (empty list)")
        else:
            print(f"SUCCESS: Generated {len(questions)} questions")
            print("First question sample:", questions[0])
            
    except Exception as e:
        print(f"CRITICAL ERROR: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_generation()
