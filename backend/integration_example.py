"""
Integration Example: Using Dynamic Challenge Generator in Your Interview System
This shows how to integrate the dynamic generator with your existing resume-based system
"""

from modules.dynamic_challenge_generator import DynamicChallengeGenerator
from modules.skill_analyzer import SkillAnalyzer
from modules.resume_parser import ResumeParser


def generate_resume_based_challenges(resume_path: str):
    """
    Generate dynamic challenges based on resume skills
    
    This integrates with your existing system to:
    1. Parse resume
    2. Analyze skills
    3. Generate unique challenges for each skill
    """
    
    print("🎯 Resume-Based Dynamic Challenge Generation")
    print("=" * 70)
    
    # Step 1: Parse Resume (using your existing parser)
    parser = ResumeParser()
    resume_data = parser.parse_resume(resume_path)
    
    print(f"\n✅ Resume parsed successfully")
    print(f"   Candidate: {resume_data['personal_info'].get('name', 'Unknown')}")
    
    # Step 2: Analyze Skills (using your existing analyzer)
    analyzer = SkillAnalyzer()
    skill_analysis = analyzer.analyze_skills(
        resume_data['skills'],
        resume_data['raw_text']
    )
    
    print(f"\n✅ Skills analyzed")
    print(f"   Total skills: {len(skill_analysis['with_proficiency'])}")
    
    # Step 3: Generate Dynamic Challenges
    generator = DynamicChallengeGenerator()
    
    # Filter programming languages
    programming_langs = ['Python', 'Java', 'JavaScript', 'C++', 'C', 'C#', 
                        'Ruby', 'Go', 'Rust', 'Swift', 'Kotlin']
    
    programming_skills = [
        skill for skill in skill_analysis['with_proficiency']
        if skill['skill'] in programming_langs
    ]
    
    print(f"\n✅ Found {len(programming_skills)} programming languages")
    
    # Generate challenges for each programming skill
    all_challenges = []
    
    for skill_info in programming_skills[:3]:  # Limit to top 3 for demo
        language = skill_info['skill']
        difficulty = skill_info['proficiency']
        
        # Map proficiency to difficulty
        difficulty_map = {
            'beginner': 'Beginner',
            'intermediate': 'Intermediate',
            'advanced': 'Advanced'
        }
        difficulty = difficulty_map.get(difficulty.lower(), 'Intermediate')
        
        print(f"\n📝 Generating challenge for {language} ({difficulty})")
        print("-" * 70)
        
        # Generate 3 challenges per language with different topics
        topics = ['Arrays', 'Strings', 'Algorithms']
        
        for topic in topics:
            challenge = generator.generate_challenge(
                language=language,
                difficulty=difficulty,
                topic=topic
            )
            
            all_challenges.append(challenge)
            print(f"   ✅ {topic}: {challenge['title']}")
    
    print(f"\n{'=' * 70}")
    print(f"✅ Generated {len(all_challenges)} unique challenges!")
    print(f"{'=' * 70}")
    
    return all_challenges


def compare_static_vs_dynamic():
    """
    Compare static challenge bank vs dynamic generation
    """
    print("\n\n🔄 Static vs Dynamic Comparison")
    print("=" * 70)
    
    # Your existing static generator
    from modules.question_generator_simple import QuestionGenerator as StaticGen
    
    # New dynamic generator
    generator = DynamicChallengeGenerator()
    
    print("\n📊 STATIC CHALLENGE BANK:")
    print("-" * 70)
    static_gen = StaticGen()
    
    # Count available challenges
    python_beginner = len(static_gen.CHALLENGE_BANK.get('Python', {}).get('beginner', []))
    python_intermediate = len(static_gen.CHALLENGE_BANK.get('Python', {}).get('intermediate', []))
    python_advanced = len(static_gen.CHALLENGE_BANK.get('Python', {}).get('advanced', []))
    
    print(f"Python Beginner: {python_beginner} challenges")
    print(f"Python Intermediate: {python_intermediate} challenges")
    print(f"Python Advanced: {python_advanced} challenges")
    print(f"Total: {python_beginner + python_intermediate + python_advanced} challenges")
    print("⚠️  LIMITATION: Same challenges repeat after exhausting the bank")
    
    print("\n📊 DYNAMIC GENERATOR:")
    print("-" * 70)
    print("Python Beginner: ∞ (infinite unique challenges)")
    print("Python Intermediate: ∞ (infinite unique challenges)")
    print("Python Advanced: ∞ (infinite unique challenges)")
    print("✅ ADVANTAGE: Every generation creates a NEW challenge")
    
    # Demonstrate uniqueness
    print("\n🎲 Uniqueness Demo - Generating 5 Python/Intermediate/Arrays:")
    print("-" * 70)
    
    titles = []
    for i in range(5):
        ch = generator.generate_challenge("Python", "Intermediate", "Arrays")
        titles.append(ch['title'])
        print(f"   {i+1}. {ch['title']}")
    
    unique_count = len(set(titles))
    print(f"\n✅ {unique_count}/5 challenges were unique!")


def integration_guide():
    """
    Show how to integrate into existing app.py
    """
    print("\n\n📚 Integration Guide")
    print("=" * 70)
    
    guide = """
OPTION 1: Replace Static Generator
-----------------------------------
In app.py, replace:
    from modules.question_generator_simple import QuestionGenerator
    
With:
    from modules.dynamic_challenge_generator import DynamicChallengeGenerator as QuestionGenerator

Then modify the generate_coding_challenge method to use:
    challenge = generator.generate_challenge(skill, proficiency, topic)


OPTION 2: Add as New Endpoint
------------------------------
Keep existing system and add dynamic generation as a new feature:

1. Add to app.py:
    from api_dynamic_challenges import dynamic_challenges_bp
    app.register_blueprint(dynamic_challenges_bp)

2. Frontend can now call:
    POST /api/generate-dynamic-challenge
    {
        "language": "Python",
        "difficulty": "Intermediate", 
        "topic": "Arrays"
    }


OPTION 3: Hybrid Approach
--------------------------
Use static bank for quick responses, dynamic for variety:

    def generate_challenge(skill, difficulty):
        # Try static first (fast)
        static_challenge = static_generator.get_challenge(skill, difficulty)
        
        # If exhausted or user wants variety, use dynamic
        if not static_challenge or request.args.get('dynamic'):
            return dynamic_generator.generate_challenge(skill, difficulty, topic)
        
        return static_challenge
"""
    
    print(guide)


if __name__ == "__main__":
    print("\n" + "=" * 70)
    print("  DYNAMIC CHALLENGE GENERATOR - INTEGRATION EXAMPLES")
    print("=" * 70)
    
    # Example 1: Compare approaches
    compare_static_vs_dynamic()
    
    # Example 2: Show integration options
    integration_guide()
    
    print("\n\n✅ Integration examples complete!")
    print("=" * 70)
    
    # Uncomment to test with actual resume:
    # challenges = generate_resume_based_challenges("path/to/resume.pdf")
