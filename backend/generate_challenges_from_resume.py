import sys
import os
import json
from datetime import datetime

# Add the backend directory to sys.path to import modules
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

try:
    from modules.skill_analyzer import SkillAnalyzer
    from modules.question_generator import QuestionGenerator
except ImportError:
    # Handle case where script is run from backend root
    try:
        from modules.skill_analyzer import SkillAnalyzer
        from modules.question_generator import QuestionGenerator
    except ImportError:
        print("Error: Could not import modules. Make sure you are in the correct directory.")
        sys.exit(1)

def main():
    print("=== Resume-Based Dynamic Coding Challenge Generator ===\n")

    # Mock Resume Data (representing a strong mid-level/senior Python developer)
    mock_resume_data = {
        'skills': [
            'C', 'Python', 'Django', 'PostgreSQL'
        ],
        'experience': [
            {
                'position': 'Senior Software Engineer',
                'company': 'Tech Corp',
                'duration': 'Jan 2023 - Present'
            }
        ]
    }

    print(f"Mock Resume Data Loaded:")
    print(f"Skills: {', '.join(mock_resume_data['skills'])}")
    print(f"Experience Entries: {len(mock_resume_data['experience'])}")
    print("-" * 50)

    # Step 1: Analyze Skills and Experience
    analyzer = SkillAnalyzer()
    years_of_exp = analyzer.calculate_total_experience(mock_resume_data['experience'])
    print(f"\n[Analysis] Calculated Total Experience: {years_of_exp} years")

    # Analyze Skills
    skill_analysis = analyzer.analyze_skills(mock_resume_data['skills'])
    
    # Get Top Programming Languages
    # We want to test C specifically as requested
    target_skills = [s for s in skill_analysis['with_proficiency'] if s['skill'] == 'C']
    if not target_skills:
        target_skills = analyzer.get_best_programming_languages(skill_analysis['with_proficiency'], count=1)

    if not target_skills:
        print("No programming languages found.")
        return

    target_skill = target_skills[0]
    print(f"[Analysis] Targeted Skill for Challenge: {target_skill['skill']} ({target_skill['proficiency']})")
    
    # Step 2: Generate Coding Challenges using the new batch method
    print(f"\n[Generation] Generating 3 distinct coding challenges based on candidate profile...")
    print(f"Skills: {', '.join(mock_resume_data['skills'])}")
    
    generator = QuestionGenerator()
    
    try:
        challenges = generator.generate_coding_challenges_for_candidate(
            skills=mock_resume_data['skills'],
            years_of_experience=years_of_exp
        )
        
        if challenges:
            for i, challenge in enumerate(challenges):
                print(f"\n--- Generated Challenge {i+1}/3 ---")
                print(f"Title: {challenge.get('title')}")
                print(f"Skill: {challenge.get('skill', 'General')}")
                print(f"Difficulty: {challenge.get('difficulty')}")
                
                # Print starter code to verify
                starter = challenge.get('starter_code', '')
                if starter:
                    print("Starter Code Snippet:")
                    print(starter[:150] + "...")
                else:
                    print("No starter code provided.")
                    
            print(f"\n[Success] Generated {len(challenges)} challenges.")
        else:
            print("\n[Error] No challenges were generated.")
            
    except Exception as e:
        print(f"Error during challenge generation: {e}")

if __name__ == "__main__":
    main()
