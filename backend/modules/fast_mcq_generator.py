"""
Fast Dynamic MCQ Generator
Generates MCQ questions INSTANTLY without API calls
Perfect for quick resume upload → quiz generation workflow
"""

import random
from typing import List, Dict


class FastMCQGenerator:
    """Generate MCQ questions dynamically using templates - NO API delays!"""
    
    # Dynamic question templates with randomizable values
    MCQ_TEMPLATES = {
        "Python": {
            "beginner": [
                {
                    "template": "What is the output of print({num1} {operator} {num2})?",
                    "generator": lambda: {
                        "num1": random.randint(2, 10),
                        "num2": random.randint(2, 5),
                        "operator": random.choice(["**", "//", "%", "*"])
                    },
                    "answer_calculator": lambda params: {
                        "**": params["num1"] ** params["num2"],
                        "//": params["num1"] // params["num2"],
                        "%": params["num1"] % params["num2"],
                        "*": params["num1"] * params["num2"]
                    }[params["operator"]],
                    "explanation": "Python arithmetic operators: ** (power), // (floor division), % (modulo), * (multiply)"
                },
                {
                    "template": "Which data type is {property}?",
                    "generator": lambda: {
                        "property": random.choice(["immutable", "mutable", "ordered", "unordered"])
                    },
                    "options_map": {
                        "immutable": {"correct": "Tuple", "wrong": ["List", "Dictionary", "Set"]},
                        "mutable": {"correct": "List", "wrong": ["Tuple", "String", "Integer"]},
                        "ordered": {"correct": "List", "wrong": ["Set", "Dictionary (Python 3.6-)", "Frozenset"]},
                        "unordered": {"correct": "Set", "wrong": ["List", "Tuple", "String"]}
                    },
                    "explanation": "Python data types have different properties: mutability, ordering, etc."
                },
                {
                    "template": "How do you create a list with {count} elements in Python?",
                    "generator": lambda: {"count": random.randint(3, 7)},
                    "options_map": {
                        "default": {
                            "correct": "[1, 2, 3, ...]",
                            "wrong": ["{1, 2, 3, ...}", "(1, 2, 3, ...)", "list(1, 2, 3, ...)"]
                        }
                    },
                    "explanation": "Lists in Python are created using square brackets []"
                },
            ],
            "intermediate": [
                {
                    "template": "What is the time complexity of accessing an element in a dictionary?",
                    "generator": lambda: {},
                    "options_map": {
                        "default": {
                            "correct": "O(1)",
                            "wrong": ["O(n)", "O(log n)", "O(n²)"]
                        }
                    },
                    "explanation": "Dictionary lookup in Python uses hash tables, providing O(1) average time complexity"
                },
                {
                    "template": "Which decorator is used to create a {decorator_type} in Python?",
                    "generator": lambda: {
                        "decorator_type": random.choice(["static method", "class method", "property"])
                    },
                    "options_map": {
                        "static method": {"correct": "@staticmethod", "wrong": ["@classmethod", "@property", "@abstractmethod"]},
                        "class method": {"correct": "@classmethod", "wrong": ["@staticmethod", "@property", "@method"]},
                        "property": {"correct": "@property", "wrong": ["@staticmethod", "@classmethod", "@getter"]}
                    },
                    "explanation": "Python decorators modify function/method behavior"
                },
            ],
            "advanced": [
                {
                    "template": "What is the GIL in Python?",
                    "generator": lambda: {},
                    "options_map": {
                        "default": {
                            "correct": "Global Interpreter Lock",
                            "wrong": ["General Interface Layer", "Garbage Iteration Loop", "Generic Input Loader"]
                        }
                    },
                    "explanation": "The GIL prevents multiple threads from executing Python bytecode simultaneously"
                },
                {
                    "template": "Which method is called when using 'with' statement?",
                    "generator": lambda: {},
                    "options_map": {
                        "default": {
                            "correct": "__enter__ and __exit__",
                            "wrong": ["__init__ and __del__", "__start__ and __stop__", "__open__ and __close__"]
                        }
                    },
                    "explanation": "Context managers use __enter__ and __exit__ for resource management"
                },
            ]
        },
        "Java": {
            "beginner": [
                {
                    "template": "Which keyword is used to inherit a class in Java?",
                    "generator": lambda: {},
                    "options_map": {
                        "default": {
                            "correct": "extends",
                            "wrong": ["implements", "inherits", "super"]
                        }
                    },
                    "explanation": "'extends' is used for class inheritance in Java"
                },
                {
                    "template": "What is the default value of a boolean variable in Java?",
                    "generator": lambda: {},
                    "options_map": {
                        "default": {
                            "correct": "false",
                            "wrong": ["true", "0", "null"]
                        }
                    },
                    "explanation": "Boolean variables default to false in Java"
                },
            ],
            "intermediate": [
                {
                    "template": "Which collection maintains insertion order in Java?",
                    "generator": lambda: {},
                    "options_map": {
                        "default": {
                            "correct": "LinkedHashMap",
                            "wrong": ["HashMap", "TreeMap", "HashSet"]
                        }
                    },
                    "explanation": "LinkedHashMap maintains insertion order unlike HashMap"
                },
            ],
            "advanced": [
                {
                    "template": "What is the purpose of volatile keyword in Java?",
                    "generator": lambda: {},
                    "options_map": {
                        "default": {
                            "correct": "Ensures visibility of changes across threads",
                            "wrong": ["Makes variable constant", "Increases performance", "Enables garbage collection"]
                        }
                    },
                    "explanation": "volatile ensures thread visibility but doesn't guarantee atomicity"
                },
            ]
        },
        "JavaScript": {
            "beginner": [
                {
                    "template": "What is the result of typeof null in JavaScript?",
                    "generator": lambda: {},
                    "options_map": {
                        "default": {
                            "correct": "object",
                            "wrong": ["null", "undefined", "number"]
                        }
                    },
                    "explanation": "This is a known JavaScript quirk - typeof null returns 'object'"
                },
                {
                    "template": "Which method adds an element to the end of an array?",
                    "generator": lambda: {},
                    "options_map": {
                        "default": {
                            "correct": "push()",
                            "wrong": ["pop()", "shift()", "unshift()"]
                        }
                    },
                    "explanation": "push() adds to end, pop() removes from end, shift() removes from start, unshift() adds to start"
                },
            ],
            "intermediate": [
                {
                    "template": "What does the '===' operator check in JavaScript?",
                    "generator": lambda: {},
                    "options_map": {
                        "default": {
                            "correct": "Value and type equality",
                            "wrong": ["Only value equality", "Only type equality", "Reference equality"]
                        }
                    },
                    "explanation": "=== checks both value and type (strict equality), == only checks value"
                },
            ],
            "advanced": [
                {
                    "template": "What is a closure in JavaScript?",
                    "generator": lambda: {},
                    "options_map": {
                        "default": {
                            "correct": "Function with access to outer scope variables",
                            "wrong": ["A closed function", "A private class", "An async function"]
                        }
                    },
                    "explanation": "Closures allow functions to access variables from their outer scope"
                },
            ]
        },
        # Add more languages as needed
        "C++": {
            "beginner": [
                {
                    "template": "Which operator is used for pointer dereferencing in C++?",
                    "generator": lambda: {},
                    "options_map": {
                        "default": {
                            "correct": "*",
                            "wrong": ["&", "->", "::"]
                        }
                    },
                    "explanation": "* dereferences a pointer, & gets address, -> accesses member through pointer"
                },
            ],
            "intermediate": [
                {
                    "template": "What is RAII in C++?",
                    "generator": lambda: {},
                    "options_map": {
                        "default": {
                            "correct": "Resource Acquisition Is Initialization",
                            "wrong": ["Random Access Iterator Interface", "Runtime Array Index Initialization", "Reference And Instance Inheritance"]
                        }
                    },
                    "explanation": "RAII ties resource lifetime to object lifetime for automatic cleanup"
                },
            ],
            "advanced": [
                {
                    "template": "What is move semantics in C++11?",
                    "generator": lambda: {},
                    "options_map": {
                        "default": {
                            "correct": "Transferring ownership of resources without copying",
                            "wrong": ["Moving objects in memory", "Changing variable scope", "Pointer arithmetic"]
                        }
                    },
                    "explanation": "Move semantics enable efficient transfer of resources using rvalue references"
                },
            ]
        }
    }
    
    def __init__(self):
        """Initialize fast MCQ generator"""
        pass
    
    def generate_mcq_questions(self, skill: str, proficiency: str, num_questions: int = 5) -> List[Dict]:
        """
        Generate MCQ questions INSTANTLY using templates
        
        Args:
            skill: Programming language or skill
            proficiency: beginner/intermediate/advanced
            num_questions: Number of questions to generate
            
        Returns:
            List of MCQ questions with randomized values
        """
        proficiency = proficiency.lower()
        
        # Get templates for this skill and proficiency
        if skill not in self.MCQ_TEMPLATES:
            # Fallback to generic questions
            return self._generate_generic_questions(skill, proficiency, num_questions)
        
        skill_templates = self.MCQ_TEMPLATES[skill]
        
        if proficiency not in skill_templates:
            proficiency = "beginner"  # Default fallback
        
        templates = skill_templates[proficiency]
        
        # Generate questions
        questions = []
        
        for i in range(num_questions):
            # Select template (cycle through if not enough)
            template_data = templates[i % len(templates)]
            
            # Generate random parameters
            params = template_data["generator"]()
            
            # Build question text
            question_text = template_data["template"].format(**params)
            
            # Generate options
            if "answer_calculator" in template_data:
                # Calculate correct answer
                correct_answer = str(template_data["answer_calculator"](params))
                
                # Generate wrong answers
                wrong_answers = []
                for _ in range(3):
                    wrong = str(random.randint(1, 100))
                    while wrong == correct_answer or wrong in wrong_answers:
                        wrong = str(random.randint(1, 100))
                    wrong_answers.append(wrong)
            else:
                # Use predefined options
                if params and list(params.keys()):
                    options_key = params.get(list(params.keys())[0])
                else:
                    options_key = "default"
                
                # Get options data with fallback
                if options_key in template_data["options_map"]:
                    options_data = template_data["options_map"][options_key]
                else:
                    options_data = template_data["options_map"].get("default", {
                        "correct": "Option A",
                        "wrong": ["Option B", "Option C", "Option D"]
                    })
                
                correct_answer = options_data["correct"]
                wrong_answers = options_data["wrong"][:3]  # Take first 3
            
            # Shuffle options
            all_options = [correct_answer] + wrong_answers
            random.shuffle(all_options)
            
            # Assign to A, B, C, D
            options = {
                "A": all_options[0],
                "B": all_options[1],
                "C": all_options[2],
                "D": all_options[3]
            }
            
            # Find correct letter
            correct_letter = [k for k, v in options.items() if v == correct_answer][0]
            
            # Build question
            question = {
                "question": question_text,
                "options": options,
                "correct_answer": correct_letter,
                "explanation": template_data["explanation"],
                "difficulty": proficiency,
                "skill": skill,
                "type": "mcq"
            }
            
            questions.append(question)
        
        return questions
    
    def _generate_generic_questions(self, skill: str, proficiency: str, num: int) -> List[Dict]:
        """Generate generic questions for unsupported skills"""
        questions = []
        
        generic_templates = [
            {
                "question": f"What is a key feature of {skill}?",
                "options": {"A": "Type Safety", "B": "Memory Management", "C": "Concurrency", "D": "All of the above"},
                "correct_answer": "D",
                "explanation": f"{skill} typically includes multiple important features"
            },
            {
                "question": f"Which is a common use case for {skill}?",
                "options": {"A": "Web Development", "B": "Data Analysis", "C": "System Programming", "D": "Mobile Apps"},
                "correct_answer": "A",
                "explanation": f"{skill} is commonly used in various development scenarios"
            },
        ]
        
        for i in range(num):
            q = generic_templates[i % len(generic_templates)].copy()
            q["skill"] = skill
            q["difficulty"] = proficiency
            q["type"] = "mcq"
            questions.append(q)
        
        return questions


# Quick test
if __name__ == "__main__":
    generator = FastMCQGenerator()
    
    print("⚡ FAST MCQ GENERATOR TEST\n")
    
    # Test Python questions
    questions = generator.generate_mcq_questions("Python", "beginner", 3)
    
    for i, q in enumerate(questions, 1):
        print(f"Q{i}: {q['question']}")
        for key, val in q['options'].items():
            marker = "✓" if key == q['correct_answer'] else " "
            print(f"  {marker} {key}. {val}")
        print(f"  Answer: {q['correct_answer']}")
        print()
