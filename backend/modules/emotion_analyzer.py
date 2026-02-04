from typing import List, Dict
import json
from datetime import datetime
from collections import Counter

class EmotionAnalyzer:
    """Analyze facial expressions and emotions during interview"""
    
    def __init__(self):
        self.emotion_data = []
        self.session_start = None
        self.session_end = None
    
    def start_session(self):
        """Start emotion tracking session"""
        self.emotion_data = []
        self.session_start = datetime.now()
    
    def add_emotion_data(self, emotion: str, confidence: float, timestamp: str = None):
        """
        Add emotion detection result
        
        Args:
            emotion: Detected emotion (happy, sad, angry, neutral, surprised, fearful, disgusted)
            confidence: Confidence score (0-1)
            timestamp: ISO timestamp of detection
        """
        if timestamp is None:
            timestamp = datetime.now().isoformat()
        
        self.emotion_data.append({
            'emotion': emotion,
            'confidence': confidence,
            'timestamp': timestamp
        })
    
    def end_session(self):
        """End emotion tracking session"""
        self.session_end = datetime.now()
    
    def get_emotion_summary(self) -> Dict:
        """
        Generate comprehensive emotion analysis summary
        
        Returns:
            Dictionary containing emotion metrics and insights
        """
        if not self.emotion_data:
            return self._get_default_summary()
        
        # Calculate emotion distribution
        emotions = [entry['emotion'] for entry in self.emotion_data]
        emotion_counts = Counter(emotions)
        total_detections = len(emotions)
        
        emotion_distribution = {
            emotion: (count / total_detections) * 100
            for emotion, count in emotion_counts.items()
        }
        
        # Determine dominant emotion
        dominant_emotion = emotion_counts.most_common(1)[0][0]
        
        # Calculate engagement score
        engagement_score = self._calculate_engagement_score(emotion_distribution)
        
        # Calculate confidence score
        confidence_score = self._calculate_confidence_score(emotion_distribution)
        
        # Calculate emotional consistency
        consistency_score = self._calculate_consistency_score()
        
        # Generate timeline data
        timeline = self._generate_timeline()
        
        # Generate feedback
        feedback = self._generate_feedback(
            emotion_distribution,
            engagement_score,
            confidence_score,
            consistency_score
        )
        
        return {
            'emotion_distribution': emotion_distribution,
            'dominant_emotion': dominant_emotion,
            'engagement_score': engagement_score,
            'confidence_score': confidence_score,
            'consistency_score': consistency_score,
            'timeline': timeline,
            'total_detections': total_detections,
            'session_duration': self._get_session_duration(),
            'feedback': feedback
        }
    
    def _calculate_engagement_score(self, emotion_distribution: Dict) -> float:
        """
        Calculate engagement score based on positive emotions
        
        Positive emotions: happy, surprised
        Neutral: neutral
        Negative: sad, angry, fearful, disgusted
        """
        positive_emotions = ['happy', 'surprised']
        neutral_emotions = ['neutral']
        
        positive_score = sum(
            emotion_distribution.get(emotion, 0)
            for emotion in positive_emotions
        )
        
        neutral_score = sum(
            emotion_distribution.get(emotion, 0)
            for emotion in neutral_emotions
        )
        
        # Engagement = 100% positive + 70% neutral
        engagement = (positive_score + (neutral_score * 0.7))
        
        return min(100, max(0, engagement))
    
    def _calculate_confidence_score(self, emotion_distribution: Dict) -> float:
        """
        Calculate confidence score based on emotion patterns
        
        High confidence: happy, neutral (stable emotions)
        Low confidence: fearful, sad (nervous emotions)
        """
        confident_emotions = ['happy', 'neutral']
        nervous_emotions = ['fearful', 'sad']
        
        confident_score = sum(
            emotion_distribution.get(emotion, 0)
            for emotion in confident_emotions
        )
        
        nervous_score = sum(
            emotion_distribution.get(emotion, 0)
            for emotion in nervous_emotions
        )
        
        # Confidence = confident emotions - nervous emotions
        confidence = confident_score - (nervous_score * 0.5)
        
        return min(100, max(0, confidence))
    
    def _calculate_consistency_score(self) -> float:
        """
        Calculate emotional consistency (less variation = more consistent)
        """
        if len(self.emotion_data) < 10:
            return 70  # Default for short sessions
        
        # Calculate emotion changes
        changes = 0
        for i in range(1, len(self.emotion_data)):
            if self.emotion_data[i]['emotion'] != self.emotion_data[i-1]['emotion']:
                changes += 1
        
        # Consistency = 100 - (change_rate * 100)
        change_rate = changes / len(self.emotion_data)
        consistency = 100 - (change_rate * 100)
        
        return min(100, max(0, consistency))
    
    def _generate_timeline(self) -> List[Dict]:
        """Generate emotion timeline for visualization"""
        if not self.emotion_data:
            return []
        
        # Sample data points for timeline (max 50 points)
        step = max(1, len(self.emotion_data) // 50)
        timeline = []
        
        for i in range(0, len(self.emotion_data), step):
            entry = self.emotion_data[i]
            timeline.append({
                'timestamp': entry['timestamp'],
                'emotion': entry['emotion'],
                'confidence': entry['confidence']
            })
        
        return timeline
    
    def _get_session_duration(self) -> float:
        """Get session duration in seconds"""
        if not self.session_start or not self.session_end:
            return 0
        
        duration = (self.session_end - self.session_start).total_seconds()
        return round(duration, 2)
    
    def _generate_feedback(
        self,
        emotion_distribution: Dict,
        engagement_score: float,
        confidence_score: float,
        consistency_score: float
    ) -> Dict:
        """Generate personalized feedback based on emotion analysis"""
        
        strengths = []
        improvements = []
        recommendations = []
        
        # Analyze engagement
        if engagement_score >= 75:
            strengths.append("High engagement and positive demeanor throughout the interview")
        elif engagement_score >= 50:
            strengths.append("Maintained good engagement during the interview")
        else:
            improvements.append("Show more enthusiasm and engagement during responses")
            recommendations.append("Practice maintaining a positive facial expression while speaking")
        
        # Analyze confidence
        if confidence_score >= 75:
            strengths.append("Displayed strong confidence and composure")
        elif confidence_score >= 50:
            strengths.append("Showed adequate confidence in responses")
        else:
            improvements.append("Work on projecting more confidence through facial expressions")
            recommendations.append("Practice relaxation techniques before interviews to reduce nervousness")
        
        # Analyze consistency
        if consistency_score >= 75:
            strengths.append("Maintained consistent emotional composure")
        elif consistency_score < 50:
            improvements.append("Emotional expressions varied significantly during the interview")
            recommendations.append("Practice maintaining steady composure when discussing different topics")
        
        # Analyze specific emotions
        if emotion_distribution.get('happy', 0) >= 30:
            strengths.append("Positive and friendly demeanor")
        
        if emotion_distribution.get('neutral', 0) >= 40:
            strengths.append("Professional and composed demeanor")
        
        if emotion_distribution.get('angry', 0) >= 10:
            improvements.append("Occasional signs of frustration detected")
            recommendations.append("Practice staying calm when discussing challenging topics")
        
        if emotion_distribution.get('fearful', 0) >= 15:
            improvements.append("Signs of nervousness detected")
            recommendations.append("Practice mock interviews to build confidence")
        
        # Ensure we have at least some feedback
        if not strengths:
            strengths.append("Completed the interview process")
        
        if not improvements:
            improvements.append("Continue practicing interview skills")
        
        if not recommendations:
            recommendations.append("Keep practicing to maintain your strong performance")
        
        return {
            'strengths': strengths,
            'areas_for_improvement': improvements,
            'recommendations': recommendations
        }
    
    def _get_default_summary(self) -> Dict:
        """Return default summary when no emotion data available"""
        return {
            'emotion_distribution': {},
            'dominant_emotion': 'neutral',
            'engagement_score': 70,
            'confidence_score': 70,
            'consistency_score': 70,
            'timeline': [],
            'total_detections': 0,
            'session_duration': 0,
            'feedback': {
                'strengths': ['Participated in the interview'],
                'areas_for_improvement': ['Enable video for more comprehensive feedback'],
                'recommendations': ['Consider using video interview mode for detailed facial expression analysis']
            }
        }
