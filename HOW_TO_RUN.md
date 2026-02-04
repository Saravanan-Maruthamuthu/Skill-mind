# How to Run the AI Interview Assistant

## 📋 Prerequisites

Before running the application, ensure you have:

1. **Python 3.8+** installed
2. **Node.js** (optional, for JavaScript code evaluation)
3. **OpenAI API Key** (for dynamic question generation)

## 🚀 Quick Start

### Step 1: Install Dependencies

Open terminal in the `backend` folder and run:

```bash
cd "e:\Skill Mind AI Antigravity\backend"
pip install Flask Flask-CORS PyPDF2 python-docx openai python-dotenv Werkzeug nltk
```

### Step 2: Configure Environment

The `.env` file is already created with your API key. Verify it contains:

```env
OPENAI_API_KEY=your-api-key-here
OPENAI_MODEL=gpt-4
DEBUG=True
UPLOAD_FOLDER=uploads
```

### Step 3: Start the Server

Run the Flask application:

```bash
python app.py
```

You should see:

```
 * Running on http://127.0.0.1:5000
 * Running on http://10.23.74.57:5000
```

### Step 4: Access the Application

Open your web browser and navigate to:

```
http://127.0.0.1:5000
```

## 📖 How to Use the Application

### 1. Upload Resume

- Click on the resume upload area
- Select a PDF or DOCX file containing your resume
- Wait for the system to parse and analyze your skills

### 2. Take the Quiz

**MCQ Questions:**
- You'll receive **10 questions per skill** identified in your resume
- Each question has 4 options (A, B, C, D)
- Select your answer and click "Next"
- Time limit: 30 minutes for all MCQ questions

**Example:**
- If you have Python and JavaScript skills
- You'll get 10 Python questions + 10 JavaScript questions = 20 total

### 3. Solve Coding Challenges

**HackerRank-Style Problems:**
- Each programming language gets 1-2 coding challenges
- Read the problem description carefully
- Check the constraints and example test cases
- Write your solution in the code editor
- Click "Submit" to test against all test cases

**Challenge Format:**
```
Title: Two Sum
Description: Given an array of integers...
Input Format: First line contains space-separated integers...
Output Format: Two space-separated integers...
Constraints: 2 <= nums.length <= 10^4
Test Cases: 3 visible + 2 hidden
Hints: Use a hash map...
Time Complexity: O(n)
```

### 4. HR Interview

- Answer behavioral and situational questions
- The AI interviewer will ask follow-up questions
- Speak naturally and provide detailed responses
- Duration: ~20 minutes

### 5. View Final Report

After completing all sections, you'll receive:

**Overall Score Breakdown:**
- MCQ Score (30% weight)
- Coding Score (40% weight)
- HR Interview Score (30% weight)
- **Final Interview Readiness Score**

**Performance Analysis:**
- Strengths identified
- Areas for improvement
- Personalized recommendations
- Skill-wise performance breakdown

## 🎯 Scoring System

The application uses a **weighted scoring system**:

| Component | Weight | Description |
|-----------|--------|-------------|
| MCQ Quiz | 30% | Knowledge assessment across skills |
| Coding Challenges | 40% | Problem-solving and coding ability |
| HR Interview | 30% | Communication and soft skills |

**Final Score Calculation:**
```
Overall Score = (MCQ × 0.30) + (Coding × 0.40) + (HR × 0.30)
```

**Performance Levels:**
- **85-100**: Excellent - Ready for Senior Positions
- **70-84**: Good - Ready for Mid-Level Positions
- **55-69**: Average - Ready for Entry-Level Positions
- **40-54**: Needs Improvement - Requires More Preparation
- **0-39**: Not Ready - Significant Preparation Needed

## 🔧 Troubleshooting

### Issue: "No module named 'Flask'"
**Solution:** Install dependencies
```bash
pip install Flask Flask-CORS PyPDF2 python-docx openai python-dotenv Werkzeug nltk
```

### Issue: "OpenAI API Error"
**Solution:** Check your API key in `.env` file
- Ensure `OPENAI_API_KEY` is set correctly
- Verify your OpenAI account has credits
- Check internet connection

### Issue: "Resume parsing failed"
**Solution:** 
- Ensure resume is in PDF or DOCX format
- File should be less than 16MB
- Resume should contain clear sections (Skills, Experience, Education)

### Issue: Questions are the same every time
**Solution:** 
- This happens when OpenAI API is not working
- Check `.env` file has valid API key
- Check internet connection
- The system uses fallback questions when API fails

### Issue: Port 5000 already in use
**Solution:** 
- Stop other applications using port 5000
- Or change the port in `app.py`:
```python
app.run(debug=Config.DEBUG, host='0.0.0.0', port=5001)
```

## 📁 Project Structure

```
Skill Mind AI Antigravity/
├── backend/
│   ├── app.py                 # Main Flask application
│   ├── config.py              # Configuration settings
│   ├── .env                   # Environment variables
│   ├── requirements.txt       # Python dependencies
│   ├── modules/
│   │   ├── resume_parser.py   # Resume parsing logic
│   │   ├── skill_analyzer.py  # Skill analysis
│   │   ├── question_generator.py  # Quiz & coding generation
│   │   ├── evaluator.py       # Answer evaluation
│   │   ├── hr_interviewer.py  # HR interview logic
│   │   └── report_generator.py    # Final report
│   └── uploads/               # Uploaded resumes
└── frontend/
    ├── index.html             # Main page
    ├── css/
    │   └── styles.css         # Styling
    └── js/
        ├── quiz-interface.js  # Quiz UI logic
        └── ...                # Other JS files
```

## 🧪 Testing the System

### Test MCQ Generation
```bash
python test_enhancements.py
```

Expected output:
```
✓ PASSED: MCQ Generation (10 questions)
✓ PASSED: HackerRank-Style Coding
✓ PASSED: Weighted Scoring
```

### Manual Testing Flow

1. **Upload a sample resume** with skills like Python, JavaScript, CSS
2. **Verify quiz generation**: Should get 10 questions per skill
3. **Check coding challenges**: Should have detailed problem descriptions
4. **Complete HR interview**: Answer 5-7 questions
5. **Review final report**: Check weighted scoring (30-40-30)

## 🔐 Security Notes

- Never commit `.env` file to version control
- Keep your OpenAI API key secure
- Uploaded resumes are stored locally in `uploads/` folder
- Clear old resumes periodically to save space

## 📊 API Usage

The application uses OpenAI API for:
- Generating unique MCQ questions
- Creating coding challenges
- HR interview conversation
- Evaluating open-ended responses

**Estimated API costs per session:**
- MCQ generation: ~$0.02-0.05
- Coding challenges: ~$0.05-0.10
- HR interview: ~$0.10-0.20
- **Total per user: ~$0.20-0.40**

## 🆘 Support

If you encounter issues:

1. Check this documentation first
2. Review error messages in the terminal
3. Check browser console for frontend errors (F12)
4. Verify all dependencies are installed
5. Ensure `.env` file is properly configured

## 📝 Notes

- The application runs locally on your machine
- All data is stored locally (no cloud storage)
- Internet connection required for AI features
- Fallback questions available for offline use
- Session data is stored in memory (lost on server restart)

---

**Ready to start?** Run `python app.py` and open http://127.0.0.1:5000 in your browser!
