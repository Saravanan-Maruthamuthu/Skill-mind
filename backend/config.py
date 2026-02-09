import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Application configuration"""
    
    # Flask settings
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    DEBUG = os.getenv('DEBUG', 'True') == 'True'
    
    # File upload settings
    UPLOAD_FOLDER = 'uploads'
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
    ALLOWED_EXTENSIONS = {'pdf', 'doc', 'docx'}
    
    # OpenAI API settings
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY', '')
    OPENAI_MODEL = os.getenv('OPENAI_MODEL', 'gpt-4o-mini')
    
    # Database settings
    DATABASE_PATH = 'database/interviews.db'
    
    # Assessment settings
    QUIZ_TIME_LIMIT = 30  # minutes
    CODING_TIME_LIMIT = 45  # minutes
    HR_INTERVIEW_DURATION = 20  # minutes
    
    # Scoring thresholds
    SCORE_EXCELLENT = 85
    SCORE_GOOD = 70
    SCORE_AVERAGE = 50
    SCORE_NEEDS_IMPROVEMENT = 30
    
    # Skill proficiency levels
    SKILL_LEVELS = {
        'beginner': {'min_score': 0, 'max_score': 40},
        'intermediate': {'min_score': 41, 'max_score': 70},
        'advanced': {'min_score': 71, 'max_score': 100}
    }
    
    # Question difficulty settings
    DIFFICULTY_DISTRIBUTION = {
        'beginner': {'easy': 70, 'medium': 25, 'hard': 5},
        'intermediate': {'easy': 30, 'medium': 50, 'hard': 20},
        'advanced': {'easy': 10, 'medium': 40, 'hard': 50}
    }
    
    # Number of questions per skill
    MCQ_PER_SKILL = 10  # Increased from 5 to 10 for better assessment
    CODING_CHALLENGES_PER_SKILL = 3  # 3 coding challenges per technical skill
    
    # Weighted scoring for final evaluation
    SCORING_WEIGHTS = {
        'mcq': 0.30,           # 30% weight for MCQ questions
        'coding': 0.40,        # 40% weight for coding challenges
        'hr_interview': 0.30   # 30% weight for HR interview
    }
    
    # Code execution settings
    CODE_EXECUTION_TIMEOUT = 10  # seconds
    MAX_OUTPUT_LENGTH = 10000  # characters
    
    # Judge0 API settings (for online code execution)
    JUDGE0_API_URL = os.getenv('JUDGE0_API_URL', 'https://ce.judge0.com')
    JUDGE0_API_KEY = os.getenv('JUDGE0_API_KEY', '')  # Optional RapidAPI key
    JUDGE0_API_HOST = os.getenv('JUDGE0_API_HOST', 'judge0-ce.p.rapidapi.com')
    JUDGE0_TIMEOUT = 30  # seconds to wait for code execution
