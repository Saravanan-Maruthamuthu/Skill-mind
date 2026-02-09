from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from werkzeug.utils import secure_filename
import os
import json
from datetime import datetime
import logging

from config import Config
from modules.resume_parser import ResumeParser
from modules.skill_analyzer import SkillAnalyzer
from modules.question_generator import QuestionGenerator
from modules.evaluator import Evaluator
from modules.hr_interviewer import HRInterviewer
from modules.report_generator import ReportGenerator
from modules.emotion_analyzer import EmotionAnalyzer

# Configure logging
logging.basicConfig(
    level=logging.DEBUG if Config.DEBUG else logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.config.from_object(Config)

# Enhanced CORS configuration
CORS(app, resources={
    r"/api/*": {
        "origins": ["http://localhost:5000", "http://127.0.0.1:5000"],
        "methods": ["GET", "POST", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization"],
        "supports_credentials": True
    }
})

# Initialize modules
resume_parser = ResumeParser()
skill_analyzer = SkillAnalyzer()
question_generator = QuestionGenerator()
evaluator = Evaluator()
report_generator = ReportGenerator()

# Store session data (in production, use a proper database)
sessions = {}

# Ensure upload folder exists
os.makedirs(Config.UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in Config.ALLOWED_EXTENSIONS

def normalize_language(lang: str) -> str:
    """Normalize language names for comparison"""
    if not lang:
        return ''
    
    lang_lower = lang.lower().strip()
    
    # Map variant names to canonical names
    language_map = {
        'python': 'python',
        'python3': 'python',
        'py': 'python',
        
        'c': 'c',
        
        'cpp': 'cpp',
        'c++': 'cpp',
        'cpp14': 'cpp',
        'cpp17': 'cpp',
        'cpp20': 'cpp',
        'c++14': 'cpp',
        'c++17': 'cpp',
        'c++20': 'cpp',
        
        'java': 'java',
        
        'javascript': 'javascript',
        'js': 'javascript',
        'node': 'javascript',
        
        'csharp': 'csharp',
        'c#': 'csharp',
        'cs': 'csharp',
        'dotnet': 'csharp',
        
        'typescript': 'typescript',
        'ts': 'typescript',
        
        'go': 'go',
        'golang': 'go',
        
        'rust': 'rust',
        'ruby': 'ruby',
        'php': 'php',
        'bash': 'bash',
        'sh': 'bash'
    }
    
    return language_map.get(lang_lower, lang_lower)

@app.route('/')
def index():
    """Serve the frontend"""
    return send_from_directory('../frontend', 'index.html')

@app.route('/favicon.ico')
def favicon():
    """Serve favicon to prevent 404 errors"""
    from flask import Response
    import base64
    # Minimal valid ICO file (1x1 transparent pixel)
    favicon_data = base64.b64decode(
        'AAABAAEAEBAAAAEAIABoBAAAFgAAACgAAAAQAAAAIAAAAAEAIAAAAAAAAAQAAAAAAAAAAAAAAAAAAAAAAA'
        'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA'
        'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA'
        'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA'
        'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA'
        'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA'
        'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA'
        'AAAAAA=='
    )
    return Response(favicon_data, mimetype='image/x-icon')

@app.route('/<path:path>')
def serve_static(path):
    """Serve static files"""
    return send_from_directory('../frontend', path)

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'version': '1.0.0'
    })

@app.route('/api/upload-resume', methods=['POST'])
def upload_resume():
    """Upload and parse resume"""
    try:
        if 'resume' not in request.files:
            return jsonify({'error': 'No file provided'}), 400
        
        file = request.files['resume']
        
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        if not allowed_file(file.filename):
            return jsonify({'error': 'Invalid file type. Use PDF or DOCX'}), 400
        
        # Save file
        filename = secure_filename(file.filename)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"{timestamp}_{filename}"
        filepath = os.path.join(Config.UPLOAD_FOLDER, filename)
        file.save(filepath)
        
        # Parse resume
        resume_data = resume_parser.parse_resume(filepath)
        
        # Analyze skills
        skill_analysis = skill_analyzer.analyze_skills(
            resume_data['skills'],
            resume_data['raw_text']
        )
        
        # Create session
        session_id = timestamp
        sessions[session_id] = {
            'resume_data': resume_data,
            'skill_analysis': skill_analysis,
            'filepath': filepath
        }
        
        return jsonify({
            'success': True,
            'session_id': session_id,
            'resume_data': {
                'personal_info': resume_data['personal_info'],
                'education': resume_data['education'],
                'skills': resume_data['skills'],
                'projects': resume_data['projects'][:5],  # Limit to 5 projects
                'experience': resume_data['experience']
            },
            'skill_analysis': skill_analysis
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/generate-quiz', methods=['POST'])
def generate_quiz():
    """Generate quiz based on skills"""
    try:
        data = request.json
        session_id = data.get('session_id')
        
        if session_id not in sessions:
            return jsonify({'error': 'Invalid session'}), 400
        
        session = sessions[session_id]
        skill_analysis = session['skill_analysis']
        resume_data = session['resume_data']
        
        # Get top skills for assessment
        skills_for_assessment = skill_analyzer.get_skills_for_assessment(
            skill_analysis['with_proficiency'],
            max_skills=5
        )
        
        # Generate MCQ questions for all skills
        all_mcqs = []
        for skill_info in skills_for_assessment:
            skill = skill_info['skill']
            proficiency = skill_info['proficiency']
            
            # Generate MCQs
            mcqs = question_generator.generate_mcq_questions(skill, proficiency, Config.MCQ_PER_SKILL)
            all_mcqs.extend(mcqs)
        
        # Calculate years of experience for difficulty calibration
        years_of_exp = skill_analyzer.calculate_total_experience(resume_data.get('experience', []))
        
        # Extract all skills for batch coding challenge generation
        all_skills = [s['skill'] for s in skill_analysis['with_proficiency']]
        
        # Generate 3 dynamic coding challenges based on ALL candidate skills
        coding_challenges = question_generator.generate_coding_challenges_for_candidate(
            skills=all_skills,
            years_of_experience=years_of_exp
        )
        
        # Fallback: If batch generation returns empty, use the old method
        if not coding_challenges:
            logger.warning("Batch generation failed, falling back to individual generation")
            coding_challenges = []
            prog_languages = skill_analyzer.get_best_programming_languages(
                skill_analysis['with_proficiency'],
                count=2
            )
            
            for lang_info in prog_languages[:1]:  # Generate for top language only
                for i in range(3):
                    challenge = question_generator.generate_coding_challenge(
                        skill=lang_info['skill'],
                        proficiency=lang_info['proficiency'],
                        avoid_topics=[c.get('title', '') for c in coding_challenges],
                        years_of_experience=years_of_exp
                    )
                    if challenge:
                        coding_challenges.append(challenge)
        
        # Build quiz response
        quiz = {
            'mcq_questions': all_mcqs,
            'coding_challenges': coding_challenges,
            'total_mcqs': len(all_mcqs),
            'total_coding': len(coding_challenges),
            'time_limit_mcq': Config.QUIZ_TIME_LIMIT,
            'time_limit_coding': Config.CODING_TIME_LIMIT
        }
        
        # Store quiz in session
        session['quiz'] = quiz
        session['quiz_start_time'] = datetime.now().isoformat()
        
        return jsonify({
            'success': True,
            'quiz': quiz
        })
        
    except Exception as e:
        logger.error(f"Quiz generation error: {str(e)}", exc_info=True)
        return jsonify({'error': str(e)}), 500

@app.route('/api/submit-quiz', methods=['POST'])
def submit_quiz():
    """Submit and evaluate quiz answers"""
    try:
        data = request.json
        session_id = data.get('session_id')
        answers = data.get('answers', {})
        
        if session_id not in sessions:
            return jsonify({'error': 'Invalid session'}), 400
        
        session = sessions[session_id]
        quiz = session.get('quiz')
        
        if not quiz:
            return jsonify({'error': 'No quiz found'}), 400
        
        # Evaluate MCQ
        mcq_results = evaluator.evaluate_mcq_quiz(
            quiz['mcq_questions'],
            answers
        )
        
        # Store results
        session['mcq_results'] = mcq_results
        
        return jsonify({
            'success': True,
            'results': mcq_results
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/submit-code', methods=['POST'])
def submit_code():
    """Submit and evaluate code"""
    try:
        data = request.json
        session_id = data.get('session_id')
        code = data.get('code')
        language = data.get('language')
        challenge_index = data.get('challenge_index', 0)
        is_preview = data.get('is_preview', False)
        
        if session_id not in sessions:
            return jsonify({'error': 'Invalid session'}), 400
        
        session = sessions[session_id]
        quiz = session.get('quiz')
        
        if not quiz or not quiz.get('coding_challenges'):
            return jsonify({'error': 'No coding challenge found'}), 400
        
        challenge = quiz['coding_challenges'][challenge_index]
        test_cases = challenge.get('test_cases', [])
        
        # Language validation removed - users can now solve challenges in any supported language
        
        # Evaluate code
        result = evaluator.evaluate_code(code, language, test_cases)
        
        # Store results ONLY if not in preview mode
        if not is_preview:
            if 'coding_results' not in session:
                session['coding_results'] = []
            session['coding_results'].append(result)
        
        return jsonify({
            'success': True,
            'result': result
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/start-interview', methods=['POST'])
def start_interview():
    """Start HR interview"""
    try:
        data = request.json
        session_id = data.get('session_id')
        
        if session_id not in sessions:
            return jsonify({'error': 'Invalid session'}), 400
        
        session = sessions[session_id]
        resume_data = session['resume_data']
        
        # Initialize HR interviewer
        hr_interviewer = HRInterviewer()
        first_question = hr_interviewer.initialize_interview(resume_data)
        
        # Initialize emotion analyzer for video interview
        emotion_analyzer = EmotionAnalyzer()
        emotion_analyzer.start_session()
        
        # Initialize attention analyzer for eye tracking
        # from modules.attention_analyzer import AttentionAnalyzer
        # attention_analyzer = AttentionAnalyzer()
        # attention_analyzer.start_session()
        
        # Store interviewer, emotion analyzer, and attention analyzer in session
        session['hr_interviewer'] = hr_interviewer
        session['emotion_analyzer'] = emotion_analyzer
        session['attention_analyzer'] = None
        
        return jsonify({
            'success': True,
            'message': first_question['message']
        })
        
    except Exception as e:
        logger.error(f"Interview start error: {str(e)}", exc_info=True)
        return jsonify({'error': str(e)}), 500

@app.route('/api/analyze-emotion', methods=['POST'])
def analyze_emotion():
    """Receive and store emotion data from video interview"""
    try:
        data = request.json
        session_id = data.get('session_id')
        emotion = data.get('emotion')
        confidence = data.get('confidence')
        timestamp = data.get('timestamp')
        
        if session_id not in sessions:
            return jsonify({'error': 'Invalid session'}), 400
        
        session = sessions[session_id]
        emotion_analyzer = session.get('emotion_analyzer')
        
        if not emotion_analyzer:
            # Create emotion analyzer if it doesn't exist
            emotion_analyzer = EmotionAnalyzer()
            emotion_analyzer.start_session()
            session['emotion_analyzer'] = emotion_analyzer
        
        # Add emotion data
        emotion_analyzer.add_emotion_data(emotion, confidence, timestamp)
        
        return jsonify({
            'success': True,
            'message': 'Emotion data recorded'
        })
        
    except Exception as e:
        logger.error(f"Emotion analysis error: {str(e)}", exc_info=True)
        return jsonify({'error': str(e)}), 500

@app.route('/api/track-attention', methods=['POST'])
def track_attention():
    """Receive and store attention tracking data"""
    try:
        # Attention tracking is disabled
        return jsonify({
            'success': True,
            'message': 'Attention tracking disabled'
        })
        
    except Exception as e:
        logger.error(f"Attention tracking error: {str(e)}", exc_info=True)
        return jsonify({'error': str(e)}), 500

@app.route('/api/final-attention', methods=['POST'])
def final_attention():
    """Store final attention summary"""
    try:
        data = request.json
        session_id = data.get('session_id')
        summary = data.get('summary', {})
        
        if session_id not in sessions:
            return jsonify({'error': 'Invalid session'}), 400
        
        session = sessions[session_id]
        session['final_attention_summary'] = summary
        
        return jsonify({
            'success': True,
            'message': 'Final attention data recorded'
        })
        
    except Exception as e:
        logger.error(f"Final attention error: {str(e)}", exc_info=True)
        return jsonify({'error': str(e)}), 500

@app.route('/api/interview-response', methods=['POST'])
def interview_response():
    """Send candidate response and get next question"""
    try:
        data = request.json
        session_id = data.get('session_id')
        response = data.get('response')
        
        if session_id not in sessions:
            return jsonify({'error': 'Invalid session'}), 400
        
        session = sessions[session_id]
        hr_interviewer = session.get('hr_interviewer')
        
        if not hr_interviewer:
            return jsonify({'error': 'Interview not started'}), 400
        
        # Get next question
        next_question = hr_interviewer.get_next_question(response)
        
        return jsonify({
            'success': True,
            'message': next_question['message']
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/end-interview', methods=['POST'])
def end_interview():
    """End HR interview and get evaluation"""
    try:
        data = request.json
        session_id = data.get('session_id')
        
        if session_id not in sessions:
            return jsonify({'error': 'Invalid session'}), 400
        
        session = sessions[session_id]
        hr_interviewer = session.get('hr_interviewer')
        emotion_analyzer = session.get('emotion_analyzer')
        attention_analyzer = session.get('attention_analyzer')
        
        if not hr_interviewer:
            return jsonify({'error': 'Interview not started'}), 400
        
        # End interview
        closing = hr_interviewer.end_interview()
        
        # End emotion tracking
        if emotion_analyzer:
            emotion_analyzer.end_session()
            emotion_summary = emotion_analyzer.get_emotion_summary()
            session['emotion_summary'] = emotion_summary
        else:
            session['emotion_summary'] = {}
        
        # Get attention tracking summary
        if attention_analyzer:
            attention_analyzer.end_session()
            attention_summary = attention_analyzer.get_attention_summary()
            session['attention_summary'] = attention_summary
        else:
            # Use final summary if available, otherwise empty
            attention_summary = session.get('final_attention_summary', {})
            session['attention_summary'] = attention_summary
        
        # Evaluate performance
        evaluation = hr_interviewer.evaluate_interview_performance()
        
        # Add engagement score to evaluation
        if attention_summary:
            evaluation['engagement_score'] = attention_summary.get('engagement_score', 0)
            evaluation['attention_percentage'] = attention_summary.get('attention_percentage', 0)
        
        # Store evaluation
        session['hr_evaluation'] = evaluation
        
        return jsonify({
            'success': True,
            'closing_message': closing['message'],
            'evaluation': evaluation
        })
        
    except Exception as e:
        logger.error(f"End interview error: {str(e)}", exc_info=True)
        return jsonify({'error': str(e)}), 500

@app.route('/api/final-report', methods=['POST'])
def final_report():
    """Generate final assessment report"""
    try:
        data = request.json
        session_id = data.get('session_id')
        
        if session_id not in sessions:
            return jsonify({'error': 'Invalid session'}), 400
        
        session = sessions[session_id]
        
        # Generate report
        report = report_generator.generate_final_report(
            resume_data=session.get('resume_data', {}),
            skill_analysis=session.get('skill_analysis', {}),
            mcq_results=session.get('mcq_results', {}),
            coding_results=session.get('coding_results', []),
            hr_evaluation=session.get('hr_evaluation', {}),
            emotion_summary=session.get('emotion_summary', {})
        )
        
        # Store report
        session['final_report'] = report
        
        return jsonify({
            'success': True,
            'report': report
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/download-report', methods=['GET'])
def download_report():
    """Download report as HTML"""
    try:
        session_id = request.args.get('session_id')
        
        if session_id not in sessions:
            return jsonify({'error': 'Invalid session'}), 400
        
        session = sessions[session_id]
        report = session.get('final_report')
        
        if not report:
            return jsonify({'error': 'No report found'}), 400
        
        # Generate HTML
        html = report_generator.export_report_html(report)
        
        return html, 200, {'Content-Type': 'text/html'}
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=Config.DEBUG, host='0.0.0.0', port=5000)
