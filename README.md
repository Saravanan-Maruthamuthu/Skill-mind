# 🎯 AI Interview Readiness Assistant

A comprehensive full-stack application that helps candidates prepare for technical interviews through AI-powered assessments, coding challenges, and HR interview simulations.

## ✨ Features

### 📄 Resume Analysis
- Upload PDF/DOCX resumes
- Automatic skill extraction and proficiency analysis
- Identifies technical skills, experience, and education

### 📝 Dynamic Quiz Generation
- **10 MCQ questions per skill** for comprehensive assessment
- AI-generated questions tailored to your proficiency level
- Covers multiple programming languages and technologies
- Real-time evaluation with detailed explanations

### 💻 HackerRank-Style Coding Challenges
- Professional problem format similar to LeetCode/HackerRank
- Detailed problem descriptions with examples
- Multiple test cases (visible + hidden)
- Hints and approach suggestions
- Time and space complexity requirements
- Problem categorization with tags

### 🎤 AI HR Interview Simulation
- Face-to-face conversational interview experience
- Behavioral and situational questions
- Natural follow-up questions based on responses
- Communication skills evaluation

### 📊 Comprehensive Scoring System
- **Weighted evaluation**: MCQ (30%) + Coding (40%) + HR (30%)
- Detailed score breakdown by category
- Skill-wise performance analysis
- Performance level classification
- Personalized recommendations

### 📈 Final Assessment Report
- Overall interview readiness score
- Strengths and weaknesses identification
- Actionable improvement suggestions
- Downloadable HTML report

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- OpenAI API key (for dynamic question generation)

### Installation

1. **Clone the repository**
```bash
cd "e:\Skill Mind AI Antigravity"
```

2. **Install Python dependencies**
```bash
cd backend
pip install Flask Flask-CORS PyPDF2 python-docx openai python-dotenv Werkzeug nltk
```

3. **Configure environment**

The `.env` file is already created. Verify it contains:
```env
OPENAI_API_KEY=your-api-key-here
OPENAI_MODEL=gpt-4
DEBUG=True
```

4. **Run the application**
```bash
python app.py
```

5. **Access the application**

Open your browser and navigate to:
```
http://127.0.0.1:5000
```

## 📖 How It Works

### 1. Upload Resume
Upload your resume (PDF/DOCX) to start the assessment process.

### 2. Skill Analysis
The system analyzes your resume and identifies:
- Technical skills (Python, JavaScript, Java, etc.)
- Proficiency levels (Beginner, Intermediate, Advanced)
- Years of experience
- Project experience

### 3. Take Assessments

**MCQ Quiz (30% weight)**
- 10 questions per identified skill
- Multiple choice format
- 30-minute time limit
- Immediate feedback with explanations

**Coding Challenges (40% weight)**
- HackerRank-style problems
- Real-time code execution
- Multiple test cases
- 45-minute time limit

**HR Interview (30% weight)**
- AI-powered conversational interview
- Behavioral questions
- Communication assessment
- 20-minute duration

### 4. Get Results
Receive a comprehensive report with:
- Overall interview readiness score
- Category-wise breakdown
- Strengths and improvement areas
- Personalized recommendations

## 🎯 Scoring System

| Component | Weight | Focus Area |
|-----------|--------|------------|
| MCQ Quiz | 30% | Technical knowledge |
| Coding Challenges | 40% | Problem-solving ability |
| HR Interview | 30% | Communication & soft skills |

**Performance Levels:**
- 85-100: Excellent (Senior-level ready)
- 70-84: Good (Mid-level ready)
- 55-69: Average (Entry-level ready)
- 40-54: Needs Improvement
- 0-39: Significant preparation needed

## 🏗️ Architecture

### Backend (Python/Flask)
- **Resume Parser**: Extracts information from resumes
- **Skill Analyzer**: Analyzes and categorizes skills
- **Question Generator**: Creates MCQ and coding challenges
- **Evaluator**: Scores answers and code submissions
- **HR Interviewer**: Manages interview conversation
- **Report Generator**: Creates final assessment reports

### Frontend (HTML/CSS/JavaScript)
- Responsive single-page application
- Interactive quiz interface
- Code editor for coding challenges
- Real-time interview chat
- Results visualization

## 📁 Project Structure

```
Skill Mind AI Antigravity/
├── backend/
│   ├── app.py                    # Main Flask application
│   ├── config.py                 # Configuration
│   ├── .env                      # Environment variables
│   ├── requirements.txt          # Dependencies
│   ├── modules/
│   │   ├── resume_parser.py      # Resume parsing
│   │   ├── skill_analyzer.py     # Skill analysis
│   │   ├── question_generator.py # Quiz generation
│   │   ├── evaluator.py          # Answer evaluation
│   │   ├── hr_interviewer.py     # HR interview
│   │   └── report_generator.py   # Report generation
│   └── uploads/                  # Resume storage
└── frontend/
    ├── index.html                # Main page
    ├── css/
    │   └── styles.css            # Styling
    └── js/
        ├── quiz-interface.js     # Quiz UI
        └── ...                   # Other modules
```

## 🔧 Configuration

Edit `backend/config.py` to customize:

```python
# Assessment settings
MCQ_PER_SKILL = 10              # Questions per skill
QUIZ_TIME_LIMIT = 30            # Minutes
CODING_TIME_LIMIT = 45          # Minutes

# Scoring weights
SCORING_WEIGHTS = {
    'mcq': 0.30,                # 30%
    'coding': 0.40,             # 40%
    'hr_interview': 0.30        # 30%
}

# Performance thresholds
SCORE_EXCELLENT = 85
SCORE_GOOD = 70
SCORE_AVERAGE = 50
```

## 🧪 Testing

Run the test suite:
```bash
python test_enhancements.py
```

Expected output:
```
✓ PASSED: MCQ Generation (10 questions)
✓ PASSED: HackerRank-Style Coding
✓ PASSED: Weighted Scoring
```

## 🔐 Security & Privacy

- All data stored locally
- No cloud storage of resumes
- Secure API key management
- Session-based data handling

## 📊 API Usage

The application uses OpenAI API for:
- Dynamic question generation
- Coding challenge creation
- HR interview conversation

**Estimated cost per session**: $0.20-0.40

## 🛠️ Troubleshooting

See [HOW_TO_RUN.md](HOW_TO_RUN.md) for detailed troubleshooting guide.

Common issues:
- **Dependencies**: Run `pip install -r requirements.txt`
- **API errors**: Check OpenAI API key in `.env`
- **Port conflict**: Change port in `app.py`

## 📝 Documentation

- [How to Run](HOW_TO_RUN.md) - Detailed setup and usage guide
- [Implementation Plan](implementation_plan.md) - Technical details
- [Walkthrough](walkthrough.md) - Feature overview

## 🎓 Technologies Used

**Backend:**
- Flask (Web framework)
- OpenAI API (AI generation)
- PyPDF2 (PDF parsing)
- python-docx (DOCX parsing)
- NLTK (Natural language processing)

**Frontend:**
- HTML5/CSS3
- Vanilla JavaScript
- Responsive design

## 🚧 Future Enhancements

- [ ] Database integration for persistent storage
- [ ] User authentication and profiles
- [ ] Progress tracking over time
- [ ] More programming languages support
- [ ] Video interview simulation
- [ ] Company-specific interview prep
- [ ] Mock interview scheduling

## 📄 License

This project is for educational and personal use.

## 🤝 Contributing

This is a personal project. Feel free to fork and customize for your needs.

---

**Ready to ace your next interview?** 🚀

Run `python app.py` and start your preparation journey!
