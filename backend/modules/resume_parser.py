import PyPDF2
import docx
import re
from typing import Dict, List, Optional

class ResumeParser:
    """Parse resumes and extract relevant information"""
    
    def __init__(self):
        # Using regex-based extraction (spaCy optional)
        self.nlp = None
    
    def parse_resume(self, file_path: str) -> Dict:
        """
        Parse resume and extract all information
        
        Args:
            file_path: Path to resume file (PDF or DOC/DOCX)
            
        Returns:
            Dictionary containing extracted information
        """
        # Extract text from file
        text = self._extract_text(file_path)
        
        # Extract various components
        personal_info = self._extract_personal_info(text)
        education = self._extract_education(text)
        skills = self._extract_skills(text)
        projects = self._extract_projects(text)
        experience = self._extract_experience(text)
        
        return {
            'personal_info': personal_info,
            'education': education,
            'skills': skills,
            'projects': projects,
            'experience': experience,
            'raw_text': text
        }
    
    def _extract_text(self, file_path: str) -> str:
        """Extract text from PDF or DOCX file"""
        if file_path.endswith('.pdf'):
            return self._extract_from_pdf(file_path)
        elif file_path.endswith('.docx') or file_path.endswith('.doc'):
            return self._extract_from_docx(file_path)
        else:
            raise ValueError("Unsupported file format. Use PDF or DOCX.")
    
    def _extract_from_pdf(self, file_path: str) -> str:
        """Extract text from PDF"""
        text = ""
        try:
            with open(file_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                for page in pdf_reader.pages:
                    text += page.extract_text()
        except Exception as e:
            print(f"Error extracting PDF: {e}")
        return text
    
    def _extract_from_docx(self, file_path: str) -> str:
        """Extract text from DOCX"""
        text = ""
        try:
            doc = docx.Document(file_path)
            for paragraph in doc.paragraphs:
                text += paragraph.text + "\n"
        except Exception as e:
            print(f"Error extracting DOCX: {e}")
        return text
    
    def _extract_personal_info(self, text: str) -> Dict:
        """Extract personal information like name, email, phone"""
        info = {}
        
        # Extract email
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        emails = re.findall(email_pattern, text)
        info['email'] = emails[0] if emails else None
        
        # Extract phone
        phone_pattern = r'[\+\(]?[1-9][0-9 .\-\(\)]{8,}[0-9]'
        phones = re.findall(phone_pattern, text)
        info['phone'] = phones[0] if phones else None
        
        # Extract name (usually first line or before email)
        lines = text.split('\n')
        for line in lines[:5]:  # Check first 5 lines
            line = line.strip()
            if line and len(line.split()) <= 4 and len(line) < 50:
                # Likely a name
                if self.nlp:
                    doc = self.nlp(line)
                    if any(ent.label_ == "PERSON" for ent in doc.ents):
                        info['name'] = line
                        break
                else:
                    # Without spaCy, just use the first reasonable line
                    info['name'] = line
                    break
        
        if 'name' not in info and lines:
            info['name'] = lines[0].strip()
        
        return info
    
    def _extract_education(self, text: str) -> List[Dict]:
        """Extract education information"""
        education = []
        
        # Common education keywords
        edu_keywords = ['education', 'academic', 'qualification', 'degree']
        
        # Degree patterns
        degree_patterns = [
            r'(B\.?Tech|Bachelor|B\.?E\.?|B\.?S\.?|M\.?Tech|Master|M\.?E\.?|M\.?S\.?|PhD|Ph\.?D\.?)',
            r'(Computer Science|Information Technology|Engineering|Science)',
            r'(\d{4})\s*-\s*(\d{4}|\bpresent\b|\bcurrent\b)'
        ]
        
        lines = text.split('\n')
        in_education_section = False
        
        for i, line in enumerate(lines):
            line_lower = line.lower()
            
            # Check if we're in education section
            if any(keyword in line_lower for keyword in edu_keywords):
                in_education_section = True
                continue
            
            # Stop if we hit another section
            if in_education_section and any(keyword in line_lower for keyword in ['experience', 'project', 'skill', 'certification']):
                break
            
            # Extract degree information
            if in_education_section:
                for pattern in degree_patterns:
                    matches = re.findall(pattern, line, re.IGNORECASE)
                    if matches:
                        education.append({
                            'degree': line.strip(),
                            'institution': lines[i+1].strip() if i+1 < len(lines) else ''
                        })
                        break
        
        return education
    
    def _extract_skills(self, text: str) -> List[str]:
        """Extract technical skills"""
        # Comprehensive skill database
        skill_database = {
            'programming_languages': [
                'Python', 'Java', 'JavaScript', 'C++', 'C#', 'C', 'Ruby', 'Go', 'Rust',
                'PHP', 'Swift', 'Kotlin', 'TypeScript', 'Scala', 'R', 'MATLAB', 'Perl'
            ],
            'web_technologies': [
                'HTML', 'CSS', 'React', 'Angular', 'Vue.js', 'Node.js', 'Express',
                'Django', 'Flask', 'FastAPI', 'Spring', 'ASP.NET', 'jQuery', 'Bootstrap',
                'Tailwind', 'Next.js', 'Nuxt.js', 'Svelte'
            ],
            'databases': [
                'MySQL', 'PostgreSQL', 'MongoDB', 'SQLite', 'Oracle', 'SQL Server',
                'Redis', 'Cassandra', 'DynamoDB', 'Firebase', 'MariaDB', 'Neo4j'
            ],
            'cloud_devops': [
                'AWS', 'Azure', 'GCP', 'Docker', 'Kubernetes', 'Jenkins', 'Git',
                'GitHub', 'GitLab', 'CI/CD', 'Terraform', 'Ansible', 'Linux'
            ],
            'data_science_ml': [
                'Machine Learning', 'Deep Learning', 'TensorFlow', 'PyTorch', 'Keras',
                'Scikit-learn', 'Pandas', 'NumPy', 'NLP', 'Computer Vision', 'OpenCV'
            ],
            'mobile': [
                'Android', 'iOS', 'React Native', 'Flutter', 'Xamarin'
            ],
            'other': [
                'REST API', 'GraphQL', 'Microservices', 'Agile', 'Scrum', 'JIRA',
                'Data Structures', 'Algorithms', 'OOP', 'Design Patterns'
            ]
        }
        
        # Flatten all skills
        all_skills = []
        for category in skill_database.values():
            all_skills.extend(category)
        
        # Find skills in text (case-insensitive)
        found_skills = []
        text_lower = text.lower()
        
        for skill in all_skills:
            # Use word boundaries to avoid partial matches
            pattern = r'\b' + re.escape(skill.lower()) + r'\b'
            if re.search(pattern, text_lower):
                found_skills.append(skill)
        
        return list(set(found_skills))  # Remove duplicates
    
    def _extract_projects(self, text: str) -> List[Dict]:
        """Extract project information"""
        projects = []
        
        # Project section keywords
        project_keywords = ['project', 'work', 'portfolio']
        
        lines = text.split('\n')
        in_project_section = False
        current_project = None
        
        for i, line in enumerate(lines):
            line_lower = line.lower()
            
            # Check if we're in project section
            if any(keyword in line_lower for keyword in project_keywords):
                in_project_section = True
                continue
            
            # Stop if we hit another section
            if in_project_section and any(keyword in line_lower for keyword in ['education', 'experience', 'skill', 'certification']):
                if current_project:
                    projects.append(current_project)
                break
            
            # Extract project details
            if in_project_section and line.strip():
                if current_project is None:
                    current_project = {
                        'title': line.strip(),
                        'description': ''
                    }
                else:
                    # Check if this is a new project (usually bold or has bullet)
                    if line.startswith('•') or line.startswith('-') or line.startswith('*'):
                        if current_project['description']:
                            projects.append(current_project)
                        current_project = {
                            'title': line.strip(),
                            'description': ''
                        }
                    else:
                        current_project['description'] += ' ' + line.strip()
        
        if current_project:
            projects.append(current_project)
        
        return projects
    
    def _extract_experience(self, text: str) -> List[Dict]:
        """Extract work experience"""
        experience = []
        
        # Experience section keywords
        exp_keywords = ['experience', 'employment', 'work history', 'professional']
        
        lines = text.split('\n')
        in_exp_section = False
        
        for i, line in enumerate(lines):
            line_lower = line.lower()
            
            # Check if we're in experience section
            if any(keyword in line_lower for keyword in exp_keywords):
                in_exp_section = True
                continue
            
            # Stop if we hit another section
            if in_exp_section and any(keyword in line_lower for keyword in ['education', 'project', 'skill', 'certification']):
                break
            
            # Extract experience details
            if in_exp_section and line.strip():
                # Look for date patterns
                date_pattern = r'(\d{4})\s*-\s*(\d{4}|\bpresent\b|\bcurrent\b)'
                if re.search(date_pattern, line, re.IGNORECASE):
                    experience.append({
                        'position': line.strip(),
                        'company': lines[i+1].strip() if i+1 < len(lines) else '',
                        'duration': re.search(date_pattern, line, re.IGNORECASE).group()
                    })
        
        return experience
