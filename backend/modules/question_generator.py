import traceback
from openai import OpenAI
from typing import List, Dict
import json
import random
from config import Config

class QuestionGenerator:
    """Generate dynamic MCQ and coding questions using AI"""
    
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
            
            return questions
            
        except Exception as e:
            error_msg = str(e)
            print(f"Error generating MCQ questions: {error_msg}")
            
            # Check for specific API errors
            if "402" in error_msg:
                print("OpenAI API Quota Exceeded. Using fallback questions.")
                return self._get_fallback_mcq(skill, proficiency, num_questions)
            if "401" in error_msg:
                print("Invalid OpenAI API Key. Using fallback questions.")
                return self._get_fallback_mcq(skill, proficiency, num_questions)
                
            traceback.print_exc()
            return self._get_fallback_mcq(skill, proficiency, num_questions)
    
    def generate_coding_challenge(self, skill: str, proficiency: str) -> Dict:
        """
        Generate a HackerRank-style coding challenge for a specific skill
        
        Args:
            skill: The programming language or technology
            proficiency: Skill level (beginner/intermediate/advanced)
            
        Returns:
            Coding challenge with comprehensive test cases and details
        """
        prompt = f"""Create a HackerRank-style coding challenge to test {proficiency} level skills in {skill}.

The problem should be well-structured and professional, similar to problems on HackerRank or LeetCode.

Provide:
1. **Problem Title**: A clear, descriptive title
2. **Problem Statement**: Detailed description with context and requirements
3. **Input Format**: Precise specification of input format
4. **Output Format**: Precise specification of expected output
5. **Constraints**: Clear constraints on input size and values
6. **Sample Test Cases**: At least 3 example test cases with explanations
7. **Hidden Test Cases**: At least 2 additional test cases for validation
8. **Hints/Approach**: Brief hints on how to approach the problem
9. **Time Complexity**: Expected time complexity
10. **Space Complexity**: Expected space complexity

Difficulty Level: {proficiency}

Return as JSON with this exact structure:
{{
  "title": "Problem Title",
  "description": "Detailed problem statement with context. Explain what needs to be solved and why.",
  "input_format": "Detailed input format specification",
  "output_format": "Detailed output format specification",
  "constraints": [
    "Constraint 1 with specific bounds",
    "Constraint 2 with specific bounds",
    "Time limit: X seconds"
  ],
  "sample_test_cases": [
    {{
      "input": "sample input",
      "expected_output": "expected output",
      "explanation": "Why this is the correct output"
    }}
  ],
  "hidden_test_cases": [
    {{
      "input": "test input",
      "expected_output": "expected output",
      "explanation": "Test case purpose"
    }}
  ],
  "hints": [
    "Hint 1 about approach",
    "Hint 2 about optimization"
  ],
  "time_complexity": "O(n) or O(n log n) etc",
  "space_complexity": "O(1) or O(n) etc",
  "difficulty": "{proficiency}",
  "tags": ["array", "string", "dynamic programming", etc],
  "sample_solution": "Complete working solution code",
  "time_limit": 30
}}"""
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are an expert competitive programming instructor creating high-quality coding challenges similar to HackerRank, LeetCode, and Codeforces. Create problems that are clear, well-structured, and test real programming skills."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
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
            
            return challenge
            
        except Exception as e:
            error_msg = str(e)
            print(f"Error generating coding challenge: {error_msg}")
            
            if "402" in error_msg:
                print("OpenAI API Quota Exceeded. Using fallback coding challenge.")
                return self._get_fallback_coding(skill, proficiency)
            if "401" in error_msg:
                print("Invalid OpenAI API Key. Using fallback coding challenge.")
                return self._get_fallback_coding(skill, proficiency)
                
            return self._get_fallback_coding(skill, proficiency)
    
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
                # Generate multiple challenges as per config (default 3)
                num_challenges = getattr(Config, 'CODING_CHALLENGES_PER_SKILL', 1)
                for _ in range(num_challenges):
                    coding = self.generate_coding_challenge(skill, proficiency)
                    if coding:
                        all_coding.append(coding)
        
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
        while len(questions) < num:
            questions.append(questions[0].copy()) # Duplicate if not enough
            
        return questions[:num]
    
    def _get_fallback_coding(self, skill: str, proficiency: str) -> Dict:
        """Fallback coding challenges if API fails - HackerRank/LeetCode style"""
        
        # Skill-specific coding challenges with comprehensive details
        coding_challenges = {
            'Python': [
                {
                    'title': 'Two Sum',
                    'description': '''Given an array of integers nums and an integer target, return indices of the two numbers such that they add up to target.

You may assume that each input would have exactly one solution, and you may not use the same element twice.

You can return the answer in any order.

Example:
Input: nums = [2,7,11,15], target = 9
Output: [0,1]
Explanation: Because nums[0] + nums[1] == 9, we return [0, 1].''',
                    'input_format': 'First line contains space-separated integers (the array)\nSecond line contains the target integer',
                    'output_format': 'Two space-separated integers representing the indices',
                    'constraints': [
                        '2 <= nums.length <= 10^4',
                        '-10^9 <= nums[i] <= 10^9',
                        '-10^9 <= target <= 10^9',
                        'Only one valid answer exists',
                        'Time limit: 2 seconds'
                    ],
                    'test_cases': [
                        {
                            'input': '2 7 11 15\n9',
                            'expected_output': '0 1',
                            'explanation': 'Because nums[0] + nums[1] == 9, we return [0, 1]'
                        },
                        {
                            'input': '3 2 4\n6',
                            'expected_output': '1 2',
                            'explanation': 'Because nums[1] + nums[2] == 6, we return [1, 2]'
                        },
                        {
                            'input': '3 3\n6',
                            'expected_output': '0 1',
                            'explanation': 'Because nums[0] + nums[1] == 6, we return [0, 1]'
                        }
                    ],
                    'hints': [
                        'Use a hash map to store numbers you\'ve seen',
                        'For each number, check if its complement (target - num) exists in the hash map'
                    ],
                    'time_complexity': 'O(n)',
                    'space_complexity': 'O(n)',
                    'tags': ['array', 'hash-table'],
                    'sample_solution': '''nums = list(map(int, input().split()))
target = int(input())
seen = {}
for i, num in enumerate(nums):
    complement = target - num
    if complement in seen:
        print(seen[complement], i)
        break
    seen[num] = i'''
                },
                {
                    'title': 'Palindrome Check',
                    'description': '''Given a string s, determine if it is a palindrome, considering only alphanumeric characters and ignoring cases.

A palindrome is a word, phrase, number, or other sequence of characters that reads the same forward and backward (ignoring spaces, punctuation, and capitalization).

Example:
Input: "A man, a plan, a canal: Panama"
Output: True
Explanation: "amanaplanacanalpanama" is a palindrome.''',
                    'input_format': 'A single line containing the string to check',
                    'output_format': 'Print "True" if palindrome, "False" otherwise',
                    'constraints': [
                        '1 <= s.length <= 1000',
                        's consists only of printable ASCII characters',
                        'Time limit: 1 second'
                    ],
                    'test_cases': [
                        {
                            'input': 'racecar',
                            'expected_output': 'True',
                            'explanation': 'racecar reads the same forwards and backwards'
                        },
                        {
                            'input': 'hello',
                            'expected_output': 'False',
                            'explanation': 'hello is not the same when reversed'
                        },
                        {
                            'input': 'A man, a plan, a canal: Panama',
                            'expected_output': 'True',
                            'explanation': 'Ignoring non-alphanumeric characters and case, it is a palindrome'
                        }
                    ],
                    'hints': [
                        'Remove all non-alphanumeric characters first',
                        'Convert to lowercase for case-insensitive comparison',
                        'Compare the string with its reverse'
                    ],
                    'time_complexity': 'O(n)',
                    'space_complexity': 'O(n)',
                    'tags': ['string', 'two-pointers'],
                    'sample_solution': '''s = input()
cleaned = ''.join(c.lower() for c in s if c.isalnum())
print(cleaned == cleaned[::-1])'''
                },
                {
                    'title': 'Reverse Integer',
                    'description': '''Given a signed 32-bit integer x, return x with its digits reversed. If reversing x causes the value to go outside the signed 32-bit integer range [-2^31, 2^31 - 1], then return 0.

Assume the environment does not allow you to store 64-bit integers (signed or unsigned).

Example:
Input: x = 123
Output: 321

Example:
Input: x = -123
Output: -321''',
                    'input_format': 'A single integer x',
                    'output_format': 'The reversed integer, or 0 if it overflows',
                    'constraints': [
                        '-2^31 <= x <= 2^31 - 1',
                        'Time limit: 1 second'
                    ],
                    'test_cases': [
                        {
                            'input': '123',
                            'expected_output': '321',
                            'explanation': 'Reverse of 123 is 321'
                        },
                        {
                            'input': '-123',
                            'expected_output': '-321',
                            'explanation': 'Reverse of -123 is -321'
                        },
                        {
                            'input': '120',
                            'expected_output': '21',
                            'explanation': 'Reverse of 120 is 021, which is 21'
                        }
                    ],
                    'hints': [
                        'Handle negative numbers by storing the sign separately',
                        'Convert to string, reverse it, then convert back to integer',
                        'Check for overflow before returning'
                    ],
                    'time_complexity': 'O(log n)',
                    'space_complexity': 'O(1)',
                    'tags': ['math'],
                    'sample_solution': '''x = int(input())
sign = -1 if x < 0 else 1
x = abs(x)
reversed_x = int(str(x)[::-1]) * sign
if reversed_x < -2**31 or reversed_x > 2**31 - 1:
    print(0)
else:
    print(reversed_x)'''
                }
            ],
            'JavaScript': [
                {
                    'title': 'Valid Anagram',
                    'description': '''Given two strings s and t, return true if t is an anagram of s, and false otherwise.

An Anagram is a word or phrase formed by rearranging the letters of a different word or phrase, typically using all the original letters exactly once.

Example:
Input: s = "anagram", t = "nagaram"
Output: true

Example:
Input: s = "rat", t = "car"
Output: false''',
                    'input_format': 'Two lines, each containing a string',
                    'output_format': 'Print "true" if anagram, "false" otherwise',
                    'constraints': [
                        '1 <= s.length, t.length <= 5 * 10^4',
                        's and t consist of lowercase English letters',
                        'Time limit: 1 second'
                    ],
                    'test_cases': [
                        {
                            'input': 'anagram\\nnagaram',
                            'expected_output': 'true',
                            'explanation': 'Both strings have the same characters'
                        },
                        {
                            'input': 'rat\\ncar',
                            'expected_output': 'false',
                            'explanation': 'Different characters'
                        }
                    ],
                    'hints': [
                        'Sort both strings and compare',
                        'Or use a hash map to count character frequencies'
                    ],
                    'time_complexity': 'O(n log n) or O(n)',
                    'space_complexity': 'O(1) or O(n)',
                    'tags': ['string', 'hash-table', 'sorting'],
                    'sample_solution': '''const readline = require('readline');
const rl = readline.createInterface({input: process.stdin});
let lines = [];
rl.on('line', (line) => lines.push(line));
rl.on('close', () => {
    const s = lines[0].split('').sort().join('');
    const t = lines[1].split('').sort().join('');
    console.log(s === t);
});'''
                }
            ],
            'Java': [
                {
                    'title': 'Reverse String',
                    'description': '''Write a function that reverses a string. The input string is given as an array of characters s.

You must do this by modifying the input array in-place with O(1) extra memory.

Example:
Input: s = ["h","e","l","l","o"]
Output: ["o","l","l","e","h"]''',
                    'input_format': 'A single line containing the string',
                    'output_format': 'The reversed string',
                    'constraints': [
                        '1 <= s.length <= 10^5',
                        's[i] is a printable ASCII character',
                        'Time limit: 1 second'
                    ],
                    'test_cases': [
                        {
                            'input': 'hello',
                            'expected_output': 'olleh',
                            'explanation': 'Reverse of hello'
                        },
                        {
                            'input': 'Java',
                            'expected_output': 'avaJ',
                            'explanation': 'Reverse of Java'
                        }
                    ],
                    'hints': [
                        'Use two pointers, one at start and one at end',
                        'Swap characters and move pointers towards center'
                    ],
                    'time_complexity': 'O(n)',
                    'space_complexity': 'O(1)',
                    'tags': ['string', 'two-pointers'],
                    'sample_solution': '''import java.util.Scanner;

public class Main {
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        if (scanner.hasNextLine()) {
            String s = scanner.nextLine();
            System.out.println(new StringBuilder(s).reverse().toString());
        }
    }
}'''
                }
            ],
            'C++': [
                {
                    'title': 'Sum of Array',
                    'description': '''Given an array of integers, find the sum of its elements.

Example:
Input: 1 2 3
Output: 6''',
                    'input_format': 'Space-separated integers',
                    'output_format': 'The sum of the integers',
                    'constraints': [
                        '1 <= n <= 1000',
                        '-1000 <= arr[i] <= 1000',
                        'Time limit: 1 second'
                    ],
                    'test_cases': [
                        {
                            'input': '1 2 3',
                            'expected_output': '6',
                            'explanation': '1+2+3 = 6'
                        },
                        {
                            'input': '10 -5 20',
                            'expected_output': '25',
                            'explanation': '10-5+20 = 25'
                        }
                    ],
                    'hints': ['Use a loop or std::accumulate'],
                    'time_complexity': 'O(n)',
                    'space_complexity': 'O(1)',
                    'tags': ['array', 'math'],
                    'sample_solution': '''#include <iostream>
#include <vector>
#include <sstream>

using namespace std;

int main() {
    string line;
    getline(cin, line);
    stringstream ss(line);
    int num, sum = 0;
    while (ss >> num) {
        sum += num;
    }
    cout << sum << endl;
    return 0;
}'''
                }
            ],
            'C': [
                 {
                    'title': 'Factorial',
                    'description': '''Write a program to calculate the factorial of a number N.
Factorial of N = 1 * 2 * ... * N.
Factorial of 0 is 1.

Example:
Input: 5
Output: 120''',
                    'input_format': 'A single integer N',
                    'output_format': 'The factorial of N',
                    'constraints': [
                        '0 <= N <= 12',
                        'Time limit: 1 second'
                    ],
                    'test_cases': [
                        {
                            'input': '5',
                            'expected_output': '120',
                            'explanation': '5! = 120'
                        },
                        {
                            'input': '0',
                            'expected_output': '1',
                            'explanation': '0! = 1'
                        }
                    ],
                    'hints': ['Use recursion or a loop'],
                    'time_complexity': 'O(n)',
                    'space_complexity': 'O(1)',
                    'tags': ['math', 'recursion'],
                    'sample_solution': '''#include <stdio.h>

int main() {
    int n;
    if (scanf("%d", &n) != 1) return 0;
    
    long long fact = 1;
    for (int i = 1; i <= n; i++) {
        fact *= i;
    }
    printf("%lld\\n", fact);
    return 0;
}'''
                }
            ],
            'SQL': [
                {
                    'title': 'Hello World SQL',
                    'description': '''Write a query to return the string "Hello World".''',
                    'input_format': 'N/A',
                    'output_format': 'The string "Hello World"',
                    'constraints': [],
                    'test_cases': [
                        {
                            'input': '',
                            'expected_output': 'Hello World',
                            'explanation': 'Select string literal'
                        }
                    ],
                    'hints': ['Use SELECT'],
                    'time_complexity': 'O(1)',
                    'space_complexity': 'O(1)',
                    'tags': ['sql', 'basics'],
                    'sample_solution': "SELECT 'Hello World';"
                }
            ]
        }
        
        # Default coding challenge with HackerRank style
        default_challenge = {
            'title': f'{skill} - Hello World',
            'description': f'''Write a program in {skill} that prints "Hello World" to the console.

This is a basic warm-up challenge to verify your environment is set up correctly.

Example:
Output: Hello World''',
            'input_format': 'No input required',
            'output_format': 'Print "Hello World" (without quotes)',
            'constraints': [
                'Output must match exactly: Hello World',
                'Time limit: 1 second'
            ],
            'test_cases': [
                {
                    'input': '',
                    'expected_output': 'Hello World',
                    'explanation': 'Simple Hello World output'
                }
            ],
            'hints': [
                'Use the standard output function for your language',
                'Make sure the output matches exactly, including capitalization'
            ],
            'time_complexity': 'O(1)',
            'space_complexity': 'O(1)',
            'tags': ['basics'],
            'sample_solution': 'print("Hello World")',
            'difficulty': proficiency,
            'skill': skill,
            'type': 'coding',
            'time_limit': 30
        }
        
        # Get skill-specific challenges or use default
        challenges = coding_challenges.get(skill, [default_challenge])
        
        # Select a random challenge
        selected = random.choice(challenges) if isinstance(challenges, list) else default_challenge
        selected['difficulty'] = proficiency
        selected['skill'] = skill
        selected['type'] = 'coding'
        selected['time_limit'] = 30
        
        return selected
