import traceback
from openai import OpenAI
from typing import List, Dict
import json
import random
from config import Config

class QuestionGenerator:
    """Generate dynamic MCQ and coding questions using AI"""
    
    # Real-world scenario templates for unique challenge generation
    SCENARIO_TEMPLATES = [
        "smart_city_infrastructure", "healthcare_monitoring", "e_commerce_optimization",
        "logistics_routing", "social_media_analytics", "financial_fraud_detection",
        "gaming_matchmaking", "iot_sensor_networks", "food_delivery_optimization",
        "video_streaming_cdn", "autonomous_vehicle_coordination", "energy_grid_management",
        "warehouse_robotics", "agricultural_automation", "cybersecurity_threat_detection",
        "real_estate_pricing", "event_ticketing", "airline_seat_allocation",
        "music_recommendation", "sports_analytics", "supply_chain_optimization",
        "smart_parking_systems", "traffic_management", "inventory_management"
    ]
    
    # Common problems to avoid (anti-patterns)
    COMMON_PROBLEMS_TO_AVOID = [
        "Two Sum", "Palindrome", "Reverse String", "Fizz Buzz", "Fibonacci",
        "Valid Anagram", "Merge Intervals", "Longest Substring", "Binary Search",
        "Climbing Stairs", "Maximum Subarray", "House Robber", "Coin Change"
    ]
    
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
    
    def _clean_json_string(self, content: str) -> str:
        """Clean JSON string by removing markdown code blocks"""
        content = content.strip()
        if content.startswith("```json"):
            content = content[7:]
        elif content.startswith("```"):
            content = content[3:]
        
        if content.endswith("```"):
            content = content[:-3]
            
        return content.strip()

    def generate_mcq_questions(self, skill: str, proficiency: str, num_questions: int = 5) -> List[Dict]:
        """
        Generate MCQ questions for a specific skill
        
        Args:
            skill: The technical skill to test
            proficiency: Skill level (beginner/intermediate/advanced)
            num_questions: Number of questions to generate
            
        Returns:
            List of MCQ questions with answers
        """
        prompt = f"""Generate {num_questions} multiple-choice questions to test {proficiency} level knowledge of {skill}.

For each question, provide:
1. A clear, specific question
2. Four options (A, B, C, D)
3. The correct answer (letter)
4. A brief explanation of why the answer is correct

Make questions practical and relevant to real-world scenarios.
Difficulty level: {proficiency}

Return the response as a JSON array with this structure:
[
  {{
    "question": "question text",
    "options": {{
      "A": "option A text",
      "B": "option B text",
      "C": "option C text",
      "D": "option D text"
    }},
    "correct_answer": "A",
    "explanation": "explanation text",
    "difficulty": "{proficiency}"
  }}
]"""
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are an expert technical interviewer creating assessment questions."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.8,
                response_format={"type": "json_object"}
            )
            
            content = response.choices[0].message.content
            
            # Clean content to handle markdown code blocks
            content = self._clean_json_string(content)
            
            try:
                questions_data = json.loads(content)
            except json.JSONDecodeError as je:
                print(f"JSON Parsing Error: {je}")
                print(f"Raw content: {content}")
                raise je
            
            # Handle both direct array and object with questions key
            if isinstance(questions_data, dict) and 'questions' in questions_data:
                questions = questions_data['questions']
            elif isinstance(questions_data, list):
                questions = questions_data
            else:
                questions = [questions_data]
            
            # Add metadata
            for q in questions:
                q['skill'] = skill
                q['type'] = 'mcq'
            
            # Validate options
            valid_questions = []
            for q in questions:
                # Normalize keys to uppercase
                if 'options' in q and isinstance(q['options'], dict):
                    # Ensure A, B, C, D exist
                    normalized_options = {}
                    for k, v in q['options'].items():
                        # specific handle for 'a', 'b' etc
                        key = k.upper().strip()
                        if key in ['A', 'B', 'C', 'D']:
                            normalized_options[key] = str(v).strip()
                    
                    # Fill missing keys if needed or skip
                    if len(normalized_options) >= 2: # At least 2 options needed
                        q['options'] = normalized_options
                        
                        # Ensure correct answer is uppercase
                        if 'correct_answer' in q:
                            q['correct_answer'] = q['correct_answer'].upper().strip()
                        
                        valid_questions.append(q)
            
            return valid_questions[:num_questions]
            
        except Exception as e:
            error_msg = str(e)
            
            # Check for specific API errors to handle gracefully without full traceback
            if any(code in error_msg for code in ["402", "401", "429", "500", "503"]):
                print(f"OpenAI API Error ({error_msg}). Using fallback questions.")
                return self._get_fallback_mcq(skill, proficiency, num_questions)
                
            print(f"Error generating MCQ questions: {error_msg}")
            traceback.print_exc()
            return self._get_fallback_mcq(skill, proficiency, num_questions)
    

    
    def generate_coding_challenges_for_candidate(self, skills: List[str], years_of_experience: int = 1) -> List[Dict]:
        """
        Generate 3 coding challenges based on candidate's skill profile using specific prompt.
        
        Args:
            skills: List of candidate's technical skills
            years_of_experience: Candidate's years of experience
            
        Returns:
            List of 3 coding challenges
        """
        skills_str = ", ".join(skills)
        
        # User defined prompt
        prompt = f"""You are a coding interview question generator.

Generate 3 coding challenges for a candidate who has skills in:
{skills_str}

Candidate Experience: {years_of_experience} years.

Each question should include:
- Problem statement
- Input format
- Output format
- Difficulty level (Easy/Medium/Hard)
- Sample input and output

RETURN JSON ONLY.
The response must be a JSON object with a key "challenges" containing an array of 3 challenge objects.
Each challenge object MUST have these exact keys:
- title: string
- description: string (Problem statement)
- input_format: string
- output_format: string
- difficulty: string (Easy/Medium/Hard)
- sample_input: string
- sample_output: string
- skill: string (The specific skill this challenge tests)
- starter_code: string (valid starter code for the language)
- solution_code: string (valid solution code)
- test_cases: array of objects with "input" and "expected_output" keys
"""

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are an expert technical interviewer. You MUST return valid JSON only. No markdown formatting."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                response_format={"type": "json_object"}
            )
            
            content = response.choices[0].message.content
            content = self._clean_json_string(content)
            
            data = json.loads(content)
            challenges = data.get('challenges', [])
            
            # Post-processing to ensure all fields are present for the frontend
            valid_challenges = []
            for i, ch in enumerate(challenges):
                # Ensure essential fields
                if 'title' not in ch or 'description' not in ch:
                    continue
                    
                # Add metadata if missing
                if 'test_cases' not in ch:
                    ch['test_cases'] = [
                        {'input': ch.get('sample_input', ''), 'expected_output': ch.get('sample_output', ''), 'explanation': 'Sample case'}
                    ]
                
                # Ensure type is set
                ch['type'] = 'coding'
                
                # Normalize difficulty
                diff = ch.get('difficulty', 'Medium').lower()
                if 'easy' in diff: ch['difficulty'] = 'beginner'
                elif 'hard' in diff: ch['difficulty'] = 'advanced'
                else: ch['difficulty'] = 'intermediate'
                
                valid_challenges.append(ch)
                
            return valid_challenges[:3]
            
        except Exception as e:
            print(f"Error generating batch challenges: {e}")
            # Fallback to mock data for demonstration if API fails (e.g. no key)
            print("Using fallback mock challenges for demonstration.")
            return [
                {
                    "title": "Config Parsing Module",
                    "description": "Implement a parser for a custom configuration format used in a distributed system. The format consists of key-value pairs separated by specific delimiters.",
                    "input_format": "A string containing the configuration data.",
                    "output_format": "A JSON string representing the parsed configuration.",
                    "difficulty": "intermediate",
                    "skill": "Python",
                    "starter_code": "def parse_config(config_str):\n    # TODO: Implement parser\n    pass",
                    "test_cases": [
                        {"input": "key1=value1;key2=value2", "expected_output": "{\"key1\": \"value1\", \"key2\": \"value2\"}"}
                    ]
                },
                {
                    "title": "Log Analysis Tool",
                    "description": "Create a tool to analyze server logs and identify IP addresses with excessive request rates within a sliding window.",
                    "input_format": "A list of log entries with timestamp and IP.",
                    "output_format": "A list of flagged IP addresses.",
                    "difficulty": "advanced",
                    "skill": "Python",
                    "starter_code": "def analyze_logs(logs, window_size, limit):\n    # TODO: Implement analysis logic\n    pass",
                    "test_cases": [
                        {"input": "[{\"time\": 1, \"ip\": \"1.1.1.1\"}, ...]", "expected_output": "[\"1.1.1.1\"]"}
                    ]
                },
                {
                    "title": "Database Query Optimizer",
                    "description": "Simulate a query optimizer that reorders operations in a query plan to minimize estimated cost based on table statistics.",
                    "input_format": "A query plan structure and table statistics.",
                    "output_format": "Optimized query plan.",
                    "difficulty": "intermediate",
                    "skill": "Python",
                    "starter_code": "def optimize_query(plan, stats):\n    # TODO: Implement optimization\n    pass",
                    "test_cases": [
                        {"input": "{...}", "expected_output": "{...}"}
                    ]
                }
            ]

    def generate_coding_challenge(self, skill: str, proficiency: str, avoid_topics: List[str] = None, years_of_experience: int = 1) -> Dict:
        """
        Generate a dynamic, skill-adapted coding challenge using Instruction-Tuned Transformer models
        
        Args:
            skill: The programming language or technology
            proficiency: Skill level (beginner/intermediate/advanced)
            avoid_topics: List of topics/titles to avoid (to ensure variety)
            years_of_experience: Candidate's years of experience (for difficulty calibration)
            
        Returns:
            Coding challenge with comprehensive test cases and details
        """
        avoid_topics = avoid_topics or []
        
        # Select random scenario template for uniqueness
        selected_scenario = random.choice(self.SCENARIO_TEMPLATES)
        
        # Build avoid instruction with both user-provided and common problems
        all_avoided = avoid_topics + self.COMMON_PROBLEMS_TO_AVOID
        avoid_instruction = f"""CRITICAL UNIQUENESS REQUIREMENTS:
- Do NOT generate problems similar to: {', '.join(all_avoided[:15])}
- Do NOT create variations of common LeetCode/HackerRank problems
- MUST base the problem on the scenario: "{selected_scenario.replace('_', ' ')}"
- Problem MUST have real-world context and practical application
- Use creative combinations of data structures and algorithms"""

        # Map proficiency to experience-based difficulty
        difficulty_map = {
            'beginner': 'entry-level developer (0-2 years)',
            'intermediate': 'mid-level developer with production experience (2-5 years)',
            'advanced': 'senior developer capable of complex system design (5+ years)'
        }
        
        experience_context = difficulty_map.get(proficiency, 'developer')

        prompt = f"""You are an expert coding challenge architect creating UNIQUE technical assessments.

CONTEXT:
- Programming Language/Skill: {skill}
- Difficulty Level: {proficiency}
- Candidate Experience: {years_of_experience} year(s) - {experience_context}
- Scenario Theme: {selected_scenario.replace('_', ' ').title()}

{avoid_instruction}

YOUR TASK:
Create a COMPLETELY ORIGINAL coding problem that:

1. **Real-World Scenario**: Base the problem on "{selected_scenario.replace('_', ' ')}" - make it feel like solving an actual industry challenge
2. **Practical Application**: The solution should be something an {experience_context} would encounter in production systems
3. **Unique Constraints**: Add specific business rules or edge cases that make this problem distinct
4. **Appropriate Complexity**: Match difficulty to {proficiency} level and {years_of_experience} years of experience
5. **Testable & Clear**: Include comprehensive test cases that validate correctness

REQUIRED JSON STRUCTURE:
{{
  "title": "Descriptive title reflecting the real-world scenario (NOT generic algorithm names)",
  "description": "Detailed problem statement with:
    - Real-world context explaining WHY this matters
    - Business scenario setup (who, what, where)
    - Clear requirements and objectives
    - Practical constraints from the domain
    Make it engaging and scenario-driven, minimum 150 words.",
  
  "input_format": "Precise specification of input structure. Example: 'First line contains N (number of items). Next N lines contain...'",
  
  "output_format": "Exact expected output specification with format details and examples",
  
  "constraints": [
    "Numerical/size constraints (e.g., 1 <= n <= 10^5)",
    "Data type constraints (e.g., valid IPv4 addresses)",
    "Business rule constraints (e.g., prices must be positive)",
    "Time/space limits (e.g., Time limit: 2 seconds)"
  ],
  
  "sample_test_cases": [
    {{
      "input": "Concrete example input matching input_format",
      "expected_output": "Exact expected output for this input",
      "explanation": "Walk through WHY this is the correct output, explaining the logic"
    }},
    {{
      "input": "Second example with different scenario",
      "expected_output": "Expected output",
      "explanation": "Explanation of reasoning"
    }}
  ],
  
  "hidden_test_cases": [
    {{
      "input": "Edge case or complex scenario not shown to candidate",
      "expected_output": "Expected output",
      "explanation": "What this test validates (e.g., handles overflow, empty input, etc.)"
    }},
    {{
      "input": "Another edge case",
      "expected_output": "Expected output",
      "explanation": "Validation purpose"
    }}
  ],
  
  "hints": [
    "High-level approach hint (no code)",
    "Data structure suggestion",
    "Algorithm optimization hint"
  ],
  
  "time_complexity": "Expected optimal time complexity in Big-O notation",
  "space_complexity": "Expected space complexity in Big-O notation",
  "difficulty": "{proficiency}",
  "tags": ["relevant", "algorithm", "data_structure", "tags"],
  
  "sample_solution": "Complete, working, EXECUTABLE solution in {skill} with:
    - Proper input reading (stdin)
    - Full implementation of the algorithm
    - Output to stdout
    - Comments explaining key logic
    ENSURE THIS IS VALID {skill} CODE THAT WILL RUN.",
  
  "starter_code": "Starter template in {skill} with:
    - Input reading scaffolding
    - Function signature or main structure
    - TODO comments where logic goes
    - Output structure",
  
  "time_limit": 30,
  
  "solution_approach": "Brief text explanation (NO code) of:
    - Recommended algorithm or approach
    - Key insights needed to solve it
    - Optimization strategies
    - Common pitfalls to avoid"
}}

CRITICAL RULES:
✅ Problem MUST be unique and scenario-driven from "{selected_scenario.replace('_', ' ')}"
✅ Title should describe the scenario, NOT the algorithm (e.g., "Traffic Signal Optimizer", not "Greedy Algorithm")
✅ Include at least 2 sample test cases and 2 hidden test cases
✅ 'sample_solution' must be VALID, EXECUTABLE {skill} code
✅ 'starter_code' should help candidate get started
✅ Return ONLY valid JSON, no markdown formatting

Generate a problem that will make the candidate think: "This is a real system I might build!"
"""
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are an expert competitive programming instructor and software architect. You create high-quality, unique coding challenges that mirror real-world engineering problems. Your challenges are known for being creative, practical, and different from typical platforms."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.85,  # Increased for more creativity
                top_p=0.92,  # Nucleus sampling for diversity
                response_format={"type": "json_object"}
            )
            
            content = response.choices[0].message.content
            content = self._clean_json_string(content)
            
            try:
                challenge = json.loads(content)
            except json.JSONDecodeError as je:
                print(f"JSON Parsing Error in Coding Challenge: {je}")
                print(f"Raw content: {content}")
                raise je
            
            # Combine all test cases for evaluation
            all_test_cases = challenge.get('sample_test_cases', []) + challenge.get('hidden_test_cases', [])
            challenge['test_cases'] = all_test_cases
            
            # Add metadata
            challenge['skill'] = skill
            challenge['type'] = 'coding'
            challenge['scenario'] = selected_scenario
            
            return challenge
            
        except Exception as e:
            error_msg = str(e)
            
            # Check for specific API errors
            if any(code in error_msg for code in ["402", "401", "429", "500", "503"]):
                 print(f"OpenAI API Error ({error_msg}). Using fallback coding challenge.")
                 return self._get_fallback_coding(skill, proficiency, avoid_topics)
            
            print(f"Error generating coding challenge: {error_msg}")
            return self._get_fallback_coding(skill, proficiency, avoid_topics)
    
    def generate_quiz_for_skills(self, skills_with_proficiency: List[Dict]) -> Dict:
        """
        Generate a complete quiz for multiple skills
        
        Args:
            skills_with_proficiency: List of skills with proficiency levels
            
        Returns:
            Complete quiz with MCQs and coding challenges
        """
        all_mcqs = []
        all_coding = []
        
        for skill_info in skills_with_proficiency:
            skill = skill_info['skill']
            proficiency = skill_info['proficiency']
            
            # Generate MCQs
            mcqs = self.generate_mcq_questions(skill, proficiency, Config.MCQ_PER_SKILL)
            all_mcqs.extend(mcqs)
            
            # Generate coding challenges for programming languages only (12 essential languages)
            programming_langs = ['Python', 'Java', 'JavaScript', 'C++', 'C', 'SQL', 'Kotlin', 'Go', 'Rust', 'Swift', 'R']
            if skill in programming_langs:
                # Generate 3 distinct challenges
                num_challenges = getattr(Config, 'CODING_CHALLENGES_PER_SKILL', 3)
                generated_topics = []
                
                for _ in range(num_challenges):
                    # Pass previously generated topics to avoid duplication
                    coding = self.generate_coding_challenge(skill, proficiency, generated_topics)
                    if coding:
                        all_coding.append(coding)
                        generated_topics.append(coding.get('title', 'Unknown'))
                        print(f"Generated coding challenge: {coding.get('title')}")
        
        # Shuffle questions
        random.shuffle(all_mcqs)
        
        return {
            'mcq_questions': all_mcqs,
            'coding_challenges': all_coding,
            'total_mcqs': len(all_mcqs),
            'total_coding': len(all_coding),
            'time_limit_mcq': Config.QUIZ_TIME_LIMIT,
            'time_limit_coding': Config.CODING_TIME_LIMIT
        }
    
    def _get_fallback_mcq(self, skill: str, proficiency: str, num: int) -> List[Dict]:
        """Fallback MCQ questions if API fails"""
        print(f"Using fallback MCQs for {skill}")
        
        # Static question bank for common skills
        question_bank = {
            'Python': [
                {
                    "question": "What is the output of print(2 ** 3)?",
                    "options": {"A": "6", "B": "8", "C": "9", "D": "5"},
                    "correct_answer": "B",
                    "explanation": "** is the exponentiation operator in Python."
                },
                {
                    "question": "Which of the following is immutable?",
                    "options": {"A": "List", "B": "Dictionary", "C": "Set", "D": "Tuple"},
                    "correct_answer": "D",
                    "explanation": "Tuples are immutable sequences in Python."
                },
                {
                    "question": "How do you start a comment in Python?",
                    "options": {"A": "//", "B": "/*", "C": "#", "D": "<!--"},
                    "correct_answer": "C",
                    "explanation": "Python uses # for single-line comments."
                },
                {
                    "question": "What is the correct file extension for Python files?",
                    "options": {"A": ".pt", "B": ".pyt", "C": ".py", "D": ".python"},
                    "correct_answer": "C",
                    "explanation": "Python files save with the .py extension."
                },
                {
                    "question": "Which keyword is used to define a function?",
                    "options": {"A": "func", "B": "def", "C": "function", "D": "define"},
                    "correct_answer": "B",
                    "explanation": "def is used to define functions in Python."
                }
            ],
            'Java': [
                {
                    "question": "Which data type is used to create a variable that should store text?",
                    "options": {"A": "String", "B": "txt", "C": "string", "D": "Text"},
                    "correct_answer": "A",
                    "explanation": "String is the class used to store text in Java."
                },
                {
                    "question": "How do you insert COMMENTS in Java code?",
                    "options": {"A": "#", "B": "//", "C": "<!--", "D": "/*"},
                    "correct_answer": "B",
                    "explanation": "// is used for single-line comments in Java."
                }
            ],
            'JavaScript': [
                {
                    "question": "Inside which HTML element do we put the JavaScript?",
                    "options": {"A": "<script>", "B": "<js>", "C": "<javascript>", "D": "<scripting>"},
                    "correct_answer": "A",
                    "explanation": "JavaScript is placed inside the <script> tag."
                },
                {
                    "question": "How do you declare a variable in JavaScript?",
                    "options": {"A": "v carName;", "B": "var carName;", "C": "variable carName;", "D": "val carName;"},
                    "correct_answer": "B",
                    "explanation": "var, let, or const are used to declare variables."
                }
            ]
        }
        
        # Get specific questions or default to generic ones
        questions = question_bank.get(skill, [])
        
        # If no specific questions, key mapping might be needed or return generic
        if not questions:
            # Try partial match or return generic
            questions = [
                {
                    "question": f"What is a key feature of {skill}?",
                    "options": {"A": "Compiled", "B": "Interpreted", "C": "Object-Oriented", "D": "Functional"},
                    "correct_answer": "C",
                    "explanation": f"Most modern usages of {skill} involve object-oriented concepts."
                },
                {
                    "question": f"Which is NOT a valid concept in {skill}?",
                    "options": {"A": "Variables", "B": "Loops", "C": "Flux Capacitor", "D": "Functions"},
                    "correct_answer": "C",
                    "explanation": "Flux Capacitor is from Back to the Future, not programming."
                }
            ]
            
        # Add metadata
        for q in questions:
            q['skill'] = skill
            q['type'] = 'mcq'
            q['difficulty'] = proficiency
            
        # Ensure we return the requested number
        # Ensure we return the requested number
        initial_count = len(questions)
        if initial_count > 0:
            while len(questions) < num:
                # Cycle through existing questions instead of just repeating the first one
                # Add a marker to differentiate if strict uniqueness isn't possible
                base_q = questions[len(questions) % initial_count]
                new_q = base_q.copy()
                # Optionally add a suffix to title if it helps, but for MCQs, exact duplicate is better than broken
                questions.append(new_q)
            
        return questions[:num]
    
    def _get_fallback_coding(self, skill: str, proficiency: str, avoid_topics: List[str] = None) -> Dict:
        """
        Dynamic fallback coding challenges using template-based generation
        Works offline without API - generates unique challenges from combinations
        """
        avoid_topics = avoid_topics or []
        
        # Select random scenario for uniqueness
        selected_scenario = random.choice(self.SCENARIO_TEMPLATES)
        
        # Challenge templates with variable components
        challenge_templates = [
            {
                'title_pattern': '{context} {operation} Optimizer',
                'description_pattern': '''You're building a {scenario_desc} system. {business_context}

Your task is to implement an efficient algorithm that {objective}.

The system needs to handle {data_type} and optimize for {optimization_goal}.

Example Scenario:
{example_scenario}''',
                'contexts': ['Resource', 'Task', 'Data', 'Process', 'Queue', 'Schedule'],
                'operations': ['Allocation', 'Distribution', 'Management', 'Scheduling', 'Routing'],
                'data_types': ['collections of items',  'time-series data', 'hierarchical structures', 'network connections'],
                'optimization_goals': ['minimum cost', 'maximum efficiency', 'balanced load', 'fastest processing']
            },
            {
                'title_pattern': '{system} {analyzer} System',
                'description_pattern': '''Design a {system} that {action} based on {criteria}.

Business Requirements:
- {requirement1}
- {requirement2}
- {requirement3}

Your solution should {solution_approach}.

Input consists of {input_desc}.
Output should provide {output_desc}.''',
                'systems': ['Monitoring', 'Analytics', 'Tracking', 'Detection', 'Validation'],
                'analyzers': ['Pattern', 'Anomaly', 'Trend', 'Performance', 'Quality'],
                'actions': ['identifies patterns', 'detects anomalies', 'analyzes trends', 'validates data'],
                'criteria': ['predefined rules', 'statistical thresholds', 'historical patterns', 'business constraints']
            },
            {
                'title_pattern': 'Smart {domain} {function}',
                'description_pattern': '''You're developing a smart {domain} application that helps users {user_goal}.

The system receives {input_type} and must {processing_task}.

Constraints:
- {constraint1}
- {constraint2}
- Real-time processing required

Your algorithm should {algorithm_goal}.''',
                'domains': ['City', 'Home', 'Office', 'Factory', 'Campus', 'Hospital'],
                'functions': ['Controller', 'Manager', 'Coordinator', 'Planner', 'Optimizer'],
                'user_goals': ['optimize resource usage', 'improve efficiency', 'reduce costs', 'enhance experience'],
                'processing_tasks': ['process inputs in real-time', 'make intelligent decisions', 'predict outcomes', 'optimize operations']
            }
        ]
        
        # Select random template
        template = random.choice(challenge_templates)
        
        # Generate title based on pattern
        title_vars = {}
        for key in template.keys():
            if isinstance(template[key], list) and key not in ['title_pattern', 'description_pattern']:
                # Properly singularize by removing trailing 's' only
                singular_key = key[:-1] if key.endswith('s') else key
                title_vars[singular_key] = random.choice(template[key])
        
        # Create title
        title = template['title_pattern'].format(**title_vars)
        
        # Avoid repeated titles
        if title in avoid_topics:
            # Try different combination
            title = f"{selected_scenario.replace('_', ' ').title()} Challenge"
        
        # Map proficiency to difficulty parameters
        difficulty_params = {
            'beginner': {
                'constraints': ['1 <= n <= 100', 'Simple data types', 'Time limit: 2 seconds'],
                'complexity': 'O(n)',
                'description_length': 'concise'
            },
            'intermediate': {
                'constraints': ['1 <= n <= 10^4', 'Mixed data structures', 'Time limit: 1 second'],
                'complexity': 'O(n log n)',
                'description_length': 'detailed'
            },
            'advanced': {
                'constraints': ['1 <= n <= 10^6', 'Complex nested structures', 'Time limit: 1 second', 'Space limit: O(n)'],
                'complexity': 'O(n) or O(n log n)',
                'description_length': 'comprehensive'
            }
        }
        
        params = difficulty_params.get(proficiency, difficulty_params['beginner'])
        
        # Generate description based on scenario
        scenario_descriptions = {
            'smart_city_infrastructure': 'smart city infrastructure',
            'healthcare_monitoring': 'healthcare patient monitoring',
            'e_commerce_optimization': 'e-commerce recommendation',
            'logistics_routing': 'logistics and delivery routing',
            'social_media_analytics': 'social media content analytics',
            'financial_fraud_detection': 'financial fraud detection',
            'gaming_matchmaking': 'gaming matchmaking',
            'iot_sensor_networks': 'IoT sensor network',
            'food_delivery_optimization': 'food delivery optimization',
            'video_streaming_cdn': 'video streaming CDN',
            'warehouse_robotics': 'warehouse robotics coordination',
            'agricultural_automation': 'agricultural automation',
            'smart_parking_systems': 'smart parking management',
            'traffic_management': 'traffic signal coordination',
            'inventory_management': 'inventory stock management'
        }
        
        scenario_desc = scenario_descriptions.get(selected_scenario, 'system automation')
        
        # Generate sample code based on language
        sample_solutions = {
            'Python': f'''import sys

def process_data(items):
    """
    Implement your algorithm here
    """
    # TODO: Write your logic here
    return sum(items)

if __name__ == "__main__":
    # Read all input from stdin
    input_data = sys.stdin.read().split()
    
    if not input_data:
        print(0)
    else:
        # Convert to integers
        data = [int(x) for x in input_data]
        
        # Process and print result
        result = process_data(data)
        print(result)
''',
            'JavaScript': f'''// Node.js stdin reading
const readline = require('readline');
const rl = readline.createInterface({{input: process.stdin}});

let lines = [];
rl.on('line', (line) => {{
    lines.push(line);
}});

rl.on('close', () => {{
    // Process input
    const data = lines[0].split(' ').map(Number);
    
    // Your algorithm here ({proficiency} level)
    const result = processData(data);
    
    console.log(result);
}});

function processData(items) {{
    // Implement {params['complexity']} solution
    return items.reduce((a, b) => a + b, 0);
}}
''',
            'Java': f'''import java.util.*;

public class Main {{
    public static void main(String[] args) {{
        Scanner scanner = new Scanner(System.in);
        
        // Read input
        String[] input = scanner.nextLine().split(" ");
        int[] data = new int[input.length];
        for (int i = 0; i < input.length; i++) {{
            data[i] = Integer.parseInt(input[i]);
        }}
        
        // Process - implement {params['complexity']} algorithm
        int result = processData(data);
        
        System.out.println(result);
    }}
    
    static int processData(int[] items) {{
        // Your {proficiency} level solution here
        int sum = 0;
        for (int item : items) sum += item;
        return sum;
    }}
}}
''',
            'C++': f'''#include <iostream>
#include <vector>
#include <sstream>
using namespace std;

int processData(vector<int>& data) {{
    // Implement {params['complexity']} algorithm
    // {proficiency} level solution
    int sum = 0;
    for (int val : data) sum += val;
    return sum;
}}

int main() {{
    string line;
    getline(cin, line);
    stringstream ss(line);
    
    vector<int> data;
    int num;
    while (ss >> num) {{
        data.push_back(num);
    }}
    
    cout << processData(data) << endl;
    return 0;
}}
''',
            'C': f'''#include <stdio.h>

int main() {{
    int num;
    long long sum = 0;
    
    // Read integers until end of input
    while (scanf("%d", &num) == 1) {{
        // TODO: Implement your logic here
        sum += num;
    }}
    
    // Output the result
    printf("%lld\\n", sum);
    
    return 0;
}}
'''
        }
        
        # Get language-specific solution or use Python as default
        sample_solution = sample_solutions.get(skill, sample_solutions['Python'])
        
        # Build complete challenge
        challenge = {
            'title': title,
            'description': f'''You are building a {scenario_desc} system for a real-world application.

Problem Context:
The system needs to efficiently process incoming data according to specific business rules and constraints.

Task:
Implement an algorithm that processes the input data and produces the required output according to the specifications below.

This problem tests your understanding of:
- Efficient data processing
- Algorithm optimization for {proficiency} level
- {params['complexity']} time complexity solutions
''',
            'input_format': 'First line contains space-separated integers representing the data to process',
            'output_format': 'Output a single line with the processed result',
            'constraints': params['constraints'],
            'test_cases': [
                {
                    'input': '1 2 3 4 5',
                    'expected_output': '15',
                    'explanation': 'Process the input according to the algorithm'
                },
                {
                    'input': '10 20 30',
                    'expected_output': '60',
                    'explanation': 'Example with different input size'
                }
            ],
            'hints': [
                f'Consider using appropriate data structures for {proficiency} level',
                f'Aim for {params["complexity"]} time complexity',
                'Think about edge cases: empty input, single element, large datasets'
            ],
            'time_complexity': params['complexity'],
            'space_complexity': 'O(n)',
            'tags': ['algorithm', selected_scenario, proficiency],
            'sample_solution': sample_solution,
            'starter_code': f'# Starter code for {skill}\n# Read input, process, and output result\n',
            'difficulty': proficiency,
            'skill': skill,
            'type': 'coding',
            'time_limit': 30,
            'scenario': selected_scenario
        }
        
        print(f"Generated dynamic fallback challenge: {title} (scenario: {selected_scenario})")
        return challenge

