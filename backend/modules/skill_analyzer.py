from typing import Dict, List
import re

class SkillAnalyzer:
    """Analyze and classify skills from resume"""
    
    def __init__(self):
        # Skill categories and their associated keywords
        self.skill_categories = {
            'Programming Languages': [
                'Python', 'Java', 'JavaScript', 'C++', 'C#', 'C', 'Ruby', 'Go', 'Rust',
                'PHP', 'Swift', 'Kotlin', 'TypeScript', 'Scala', 'R', 'MATLAB', 'Perl'
            ],
            'Web Development': [
                'HTML', 'CSS', 'React', 'Angular', 'Vue.js', 'Node.js', 'Express',
                'Django', 'Flask', 'FastAPI', 'Spring', 'ASP.NET', 'jQuery', 'Bootstrap',
                'Tailwind', 'Next.js', 'Nuxt.js', 'Svelte', 'REST API', 'GraphQL'
            ],
            'Databases': [
                'MySQL', 'PostgreSQL', 'MongoDB', 'SQLite', 'Oracle', 'SQL Server',
                'Redis', 'Cassandra', 'DynamoDB', 'Firebase', 'MariaDB', 'Neo4j', 'SQL'
            ],
            'Cloud & DevOps': [
                'AWS', 'Azure', 'GCP', 'Docker', 'Kubernetes', 'Jenkins', 'Git',
                'GitHub', 'GitLab', 'CI/CD', 'Terraform', 'Ansible', 'Linux', 'DevOps'
            ],
            'Data Science & ML': [
                'Machine Learning', 'Deep Learning', 'TensorFlow', 'PyTorch', 'Keras',
                'Scikit-learn', 'Pandas', 'NumPy', 'NLP', 'Computer Vision', 'OpenCV',
                'Data Analysis', 'Statistics', 'AI'
            ],
            'Mobile Development': [
                'Android', 'iOS', 'React Native', 'Flutter', 'Xamarin', 'Swift', 'Kotlin'
            ],
            'Software Engineering': [
                'Data Structures', 'Algorithms', 'OOP', 'Design Patterns', 'Microservices',
                'Agile', 'Scrum', 'Testing', 'Unit Testing', 'TDD'
            ]
        }
        
        # Proficiency indicators
        self.proficiency_keywords = {
            'beginner': ['basic', 'beginner', 'learning', 'familiar', 'exposure'],
            'intermediate': ['intermediate', 'working knowledge', 'proficient', 'experienced'],
            'advanced': ['advanced', 'expert', 'mastery', 'extensive', 'senior', 'lead']
        }
    
    def analyze_skills(self, skills: List[str], resume_text: str = "") -> Dict:
        """
        Analyze skills and classify them by category and proficiency
        
        Args:
            skills: List of extracted skills
            resume_text: Full resume text for context analysis
            
        Returns:
            Dictionary with categorized and classified skills
        """
        categorized_skills = self._categorize_skills(skills)
        skills_with_proficiency = self._assess_proficiency(skills, resume_text)
        
        return {
            'categorized': categorized_skills,
            'with_proficiency': skills_with_proficiency,
            'summary': self._generate_summary(categorized_skills, skills_with_proficiency)
        }
    
    def _categorize_skills(self, skills: List[str]) -> Dict[str, List[str]]:
        """Categorize skills into different domains"""
        categorized = {category: [] for category in self.skill_categories.keys()}
        categorized['Other'] = []
        
        for skill in skills:
            categorized_flag = False
            for category, category_skills in self.skill_categories.items():
                if skill in category_skills:
                    categorized[category].append(skill)
                    categorized_flag = True
                    break
            
            if not categorized_flag:
                categorized['Other'].append(skill)
        
        # Remove empty categories
        return {k: v for k, v in categorized.items() if v}
    
    def _assess_proficiency(self, skills: List[str], resume_text: str) -> List[Dict]:
        """
        Assess proficiency level for each skill
        
        Uses context from resume to determine proficiency:
        - Beginner: Mentioned once, no projects/experience
        - Intermediate: Used in projects or has some experience
        - Advanced: Multiple projects, years of experience, leadership
        """
        skills_with_level = []
        resume_lower = resume_text.lower()
        
        for skill in skills:
            skill_lower = skill.lower()
            
            # Count mentions
            mention_count = len(re.findall(r'\b' + re.escape(skill_lower) + r'\b', resume_lower))
            
            # Check for proficiency keywords near the skill
            context_window = 100  # characters before and after
            proficiency = 'intermediate'  # default
            
            # Find all occurrences
            for match in re.finditer(r'\b' + re.escape(skill_lower) + r'\b', resume_lower):
                start = max(0, match.start() - context_window)
                end = min(len(resume_lower), match.end() + context_window)
                context = resume_lower[start:end]
                
                # Check for proficiency keywords
                for level, keywords in self.proficiency_keywords.items():
                    if any(keyword in context for keyword in keywords):
                        proficiency = level
                        break
            
            # Heuristic based on mention count
            if mention_count == 1:
                proficiency = 'beginner'
            elif mention_count >= 5:
                proficiency = 'advanced'
            
            # Check for years of experience
            years_pattern = r'(\d+)\+?\s*(?:years?|yrs?)'
            years_matches = re.findall(years_pattern, resume_lower)
            if years_matches:
                max_years = max(int(y) for y in years_matches)
                if max_years >= 3:
                    proficiency = 'advanced'
                elif max_years >= 1:
                    proficiency = 'intermediate'
            
            skills_with_level.append({
                'skill': skill,
                'proficiency': proficiency,
                'mentions': mention_count
            })
        
        return skills_with_level
    
    def _generate_summary(self, categorized: Dict, with_proficiency: List[Dict]) -> Dict:
        """Generate a summary of the skill analysis"""
        total_skills = sum(len(skills) for skills in categorized.values())
        
        proficiency_counts = {
            'beginner': 0,
            'intermediate': 0,
            'advanced': 0
        }
        
        for skill_info in with_proficiency:
            proficiency_counts[skill_info['proficiency']] += 1
        
        # Identify top skills (advanced level)
        top_skills = [s['skill'] for s in with_proficiency if s['proficiency'] == 'advanced']
        
        # Identify areas for improvement (beginner level)
        improvement_areas = [s['skill'] for s in with_proficiency if s['proficiency'] == 'beginner']
        
        return {
            'total_skills': total_skills,
            'proficiency_distribution': proficiency_counts,
            'top_skills': top_skills,
            'improvement_areas': improvement_areas,
            'strongest_category': max(categorized.items(), key=lambda x: len(x[1]))[0] if categorized else None
        }
    
    def get_skills_for_assessment(self, skills_with_proficiency: List[Dict], max_skills: int = 5) -> List[Dict]:
        """
        Select skills for assessment based on proficiency
        Prioritizes intermediate and advanced skills
        
        Args:
            skills_with_proficiency: List of skills with proficiency levels
            max_skills: Maximum number of skills to assess
            
        Returns:
            List of selected skills for assessment
        """
        # Sort by proficiency (advanced first) and mentions
        sorted_skills = sorted(
            skills_with_proficiency,
            key=lambda x: (
                {'advanced': 3, 'intermediate': 2, 'beginner': 1}[x['proficiency']],
                x['mentions']
            ),
            reverse=True
        )
        
        return sorted_skills[:max_skills]

    def get_best_programming_languages(self, skills_with_proficiency: List[Dict], count: int = 2) -> List[Dict]:
        """
        Get the top programming languages from the identified skills
        
        Args:
            skills_with_proficiency: List of skills with proficiency levels
            count: Number of languages to return
            
        Returns:
            List of selected programming language skills
        """
        programming_langs = self.skill_categories.get('Programming Languages', [])
        
        # Filter for programming languages only
        lang_skills = [
            s for s in skills_with_proficiency 
            if any(lang.lower() == s['skill'].lower() or 
                   (lang.lower() in s['skill'].lower() and len(s['skill']) < len(lang) + 5) # Fuzzy match safely
                   for lang in programming_langs)
        ]
        
        # Sort by proficiency and mentions
        sorted_langs = sorted(
            lang_skills,
            key=lambda x: (
                {'advanced': 3, 'intermediate': 2, 'beginner': 1}[x['proficiency']],
                x['mentions']
            ),
            reverse=True
        )
        
        return sorted_langs[:count]

    def calculate_total_experience(self, experience_list: List[Dict]) -> int:
        """
        Calculate total years of experience based on experience entries
        
        Args:
            experience_list: List of experience dictionaries
            
        Returns:
            Total years of experience (integer)
        """
        total_months = 0
        from datetime import datetime
        import re

        for exp in experience_list:
            duration_str = exp.get('duration', '')
            if not duration_str:
                continue
                
            # Parse dates (simplified)
            # Expecting format "YYYY - YYYY" or "YYYY - Present"
            # Or "Mon YYYY - Mon YYYY"
            
            try:
                # Find all year-like patterns or 'present'
                dates = re.findall(r'([A-Za-z]+ \d{4}|\d{4}|present|current)', duration_str, re.IGNORECASE)
                
                if len(dates) >= 2:
                    start_str = dates[0]
                    end_str = dates[1]
                    
                    start_date = None
                    end_date = None
                    
                    # Parse start
                    if re.match(r'^\d{4}$', start_str):
                        start_date = datetime.strptime(start_str, "%Y")
                    else:
                        try:
                            start_date = datetime.strptime(start_str, "%b %Y")
                        except:
                            # Fallback to year extraction
                            year_match = re.search(r'\d{4}', start_str)
                            if year_match:
                                start_date = datetime.strptime(year_match.group(), "%Y")
                            
                    if not start_date:
                        continue

                    # Parse end
                    if end_str.lower() in ['present', 'current']:
                        end_date = datetime.now()
                    elif re.match(r'^\d{4}$', end_str):
                        end_date = datetime.strptime(end_str, "%Y")
                    else:
                        try:
                            # Try with month first
                            end_date = datetime.strptime(end_str, "%b %Y")
                        except:
                             # Fallback to year
                            year_match = re.search(r'\d{4}', end_str)
                            if year_match:
                                end_date = datetime.strptime(year_match.group(), "%Y")
                    
                    if not end_date:
                        continue
                    
                    # Calculate months
                    months = (end_date.year - start_date.year) * 12 + (end_date.month - start_date.month)
                    # Add 1 month to include the end month partially
                    months += 1
                    
                    if months > 0:
                        total_months += months
            except Exception as e:
                print(f"Error parsing duration '{duration_str}': {e}")
                continue
        
        # Convert to years (rounded)
        if total_months == 0:
            return 0
            
        years = round(total_months / 12)
        # Ensure at least 1 year if there is some experience but less than 6 months rounded
        if years == 0 and total_months > 0:
            years = 1
            
        return years
