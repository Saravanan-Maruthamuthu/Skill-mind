from openai import OpenAI
from typing import List, Dict
import json
from config import Config

class HRInterviewer:
    """AI-powered HR interview simulation"""
    
    def __init__(self, api_key: str = None):
        api_key = api_key or Config.OPENAI_API_KEY
        
        # Check if using OpenRouter (API key starts with 'sk-or-')
        if api_key and api_key.startswith('sk-or-'):
            self.client = OpenAI(
                api_key=api_key,
                base_url="https://openrouter.ai/api/v1"
            )
        else:
            self.client = OpenAI(api_key=api_key)
        
        self.model = Config.OPENAI_MODEL
        self.conversation_history = []
        self.candidate_info = {}
    
    def initialize_interview(self, resume_data: Dict) -> Dict:
        """
        Initialize the HR interview with candidate information
        
        Args:
            resume_data: Parsed resume data
            
        Returns:
            Initial greeting and first question
        """
        self.candidate_info = resume_data
        
        # Create system prompt
        system_prompt = f"""You are an experienced HR interviewer conducting a professional job interview. 

Candidate Information:
- Name: {resume_data.get('personal_info', {}).get('name', 'Candidate')}
- Skills: {', '.join(resume_data.get('skills', [])[:10])}
- Education: {resume_data.get('education', [])}
- Experience: {resume_data.get('experience', [])}

Your role:
1. Conduct a professional, friendly interview
2. Ask behavioral and situational questions
3. Ask about projects and experience mentioned in the resume
4. Assess communication skills, problem-solving ability, and cultural fit
5. Adapt follow-up questions based on responses
6. Keep questions relevant and professional
7. Provide a warm, encouraging atmosphere

Interview duration: approximately {Config.HR_INTERVIEW_DURATION} minutes
Start with a warm greeting and an opening question."""
        
        self.conversation_history = [
            {"role": "system", "content": system_prompt}
        ]
        
        # Get first question
        return self.get_next_question()
    
    def get_next_question(self, candidate_response: str = None) -> Dict:
        """
        Get the next interview question based on conversation flow
        
        Args:
            candidate_response: Candidate's response to previous question
            
        Returns:
            Next question from the interviewer
        """
        if candidate_response:
            self.conversation_history.append({
                "role": "user",
                "content": candidate_response
            })
        
        # Retry logic for transient API failures
        max_retries = 3
        retry_delay = 1
        
        for attempt in range(max_retries):
            try:
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=self.conversation_history,
                    temperature=0.7,
                    max_tokens=300
                )
                
                interviewer_message = response.choices[0].message.content
                
                self.conversation_history.append({
                    "role": "assistant",
                    "content": interviewer_message
                })
                
                return {
                    'success': True,
                    'message': interviewer_message,
                    'question_number': len([m for m in self.conversation_history if m['role'] == 'assistant'])
                }
                
            except Exception as e:
                print(f"Attempt {attempt + 1}/{max_retries} failed: {str(e)}")
                
                if attempt < max_retries - 1:
                    import time
                    time.sleep(retry_delay)
                    retry_delay *= 2  # Exponential backoff
                else:
                    # Final attempt failed, return user-friendly error
                    return {
                        'success': False,
                        'error': str(e),
                        'message': 'I apologize for the technical difficulty. Let me try to continue our conversation. Could you please tell me more about your experience with the skills mentioned in your resume?'
                    }
    
    def end_interview(self) -> Dict:
        """
        End the interview and get closing remarks
        
        Returns:
            Closing message from interviewer
        """
        closing_prompt = "Please provide a warm closing statement for the interview, thanking the candidate and explaining next steps."
        
        self.conversation_history.append({
            "role": "user",
            "content": closing_prompt
        })
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=self.conversation_history,
                temperature=0.7,
                max_tokens=200
            )
            
            closing_message = response.choices[0].message.content
            
            return {
                'success': True,
                'message': closing_message
            }
            
        except Exception as e:
            return {
                'success': False,
                'message': 'Thank you for your time today. We will be in touch soon regarding next steps.'
            }
    
    def evaluate_interview_performance(self) -> Dict:
        """
        Evaluate the candidate's interview performance
        
        Returns:
            Performance evaluation and feedback
        """
        # Extract candidate responses
        candidate_responses = [
            msg['content'] for msg in self.conversation_history 
            if msg['role'] == 'user' and len(msg['content']) > 20
        ]
        
        if not candidate_responses:
            return {
                'score': 0,
                'feedback': 'Insufficient responses to evaluate'
            }
        
        evaluation_prompt = f"""Based on this interview conversation, evaluate the candidate's performance on the following criteria (score each 0-100):

1. Communication Skills: Clarity, articulation, professionalism
2. Confidence: Self-assurance in responses
3. Relevance: How well responses address the questions
4. Depth: Quality and detail of answers
5. Cultural Fit: Alignment with professional values

Candidate responses:
{json.dumps(candidate_responses, indent=2)}

Provide evaluation as JSON:
{{
  "communication_skills": score,
  "confidence": score,
  "relevance": score,
  "depth": score,
  "cultural_fit": score,
  "overall_score": average_score,
  "strengths": ["strength 1", "strength 2"],
  "areas_for_improvement": ["area 1", "area 2"],
  "summary": "brief summary of performance"
}}"""
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are an expert HR evaluator."},
                    {"role": "user", "content": evaluation_prompt}
                ],
                temperature=0.5,
                response_format={"type": "json_object"}
            )
            
            evaluation = json.loads(response.choices[0].message.content)
            return evaluation
            
        except Exception as e:
            print(f"Error evaluating interview: {e}")
            return self._get_fallback_evaluation()
    
    def _get_fallback_evaluation(self) -> Dict:
        """Fallback evaluation if API fails"""
        return {
            'communication_skills': 70,
            'confidence': 70,
            'relevance': 70,
            'depth': 70,
            'cultural_fit': 70,
            'overall_score': 70,
            'strengths': ['Participated in the interview'],
            'areas_for_improvement': ['Continue practicing interview skills'],
            'summary': 'Good effort in the interview process.'
        }
    
    def get_conversation_summary(self) -> List[Dict]:
        """Get the full conversation history"""
        return [
            {
                'role': msg['role'],
                'content': msg['content']
            }
            for msg in self.conversation_history
            if msg['role'] in ['user', 'assistant']
        ]
