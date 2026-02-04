import sys
import os
import traceback

sys.path.append(os.getcwd())
from modules.question_generator import QuestionGenerator
from config import Config

def diagnose():
    try:
        print("Starting diagnosis...")
        generator = QuestionGenerator()
        print(f"Model: {generator.model}")
        
        # Test generation
        questions = generator.generate_mcq_questions("Python", "Beginner", 1)
        if not questions:
            print("Returned empty questions list")
            
    except Exception:
        with open("error_log.txt", "w") as f:
            f.write(traceback.format_exc())
        print("Exception caught and written to error_log.txt")

if __name__ == "__main__":
    diagnose()
