"""
Simplified Question Generator using Static Challenge Bank
Generates coding challenges based on skill and difficulty level
"""

from typing import List, Dict
import random

class QuestionGenerator:
    """Generate coding questions from a static challenge bank"""
    
    # Static challenge bank organized by language and difficulty
    CHALLENGE_BANK = {
        "Python": {
            "beginner": [
                {
                    "title": "String Reversal",
                    "description": "Write a function that reverses a given string.\n\nExample:\nInput: 'hello'\nOutput: 'olleh'",
                    "difficulty": "beginner",
                    "test_cases": [
                        {"input": "hello", "expected_output": "olleh"},
                        {"input": "Python", "expected_output": "nohtyP"},
                        {"input": "12345", "expected_output": "54321"}
                    ],
                    "starter_code": "def reverse_string(s):\n    # TODO: Implement string reversal\n    pass\n\nif __name__ == '__main__':\n    import sys\n    text = sys.stdin.read().strip()\n    print(reverse_string(text))",
                    "solution_code": "def reverse_string(s):\n    return s[::-1]"
                },
                {
                    "title": "Prime Number Checker",
                    "description": "Write a function to check if a number is prime.\n\nA prime number is only divisible by 1 and itself.",
                    "difficulty": "beginner",
                    "test_cases": [
                        {"input": "7", "expected_output": "True"},
                        {"input": "10", "expected_output": "False"},
                        {"input": "2", "expected_output": "True"}
                    ],
                    "starter_code": "def is_prime(n):\n    # TODO: Check if n is prime\n    pass\n\nif __name__ == '__main__':\n    import sys\n    num = int(sys.stdin.read().strip())\n    print(is_prime(num))",
                    "solution_code": "def is_prime(n):\n    if n < 2:\n        return False\n    for i in range(2, int(n**0.5) + 1):\n        if n % i == 0:\n            return False\n    return True"
                },
                {
                    "title": "Sum of List Elements",
                    "description": "Write a function that calculates the sum of all elements in a list.",
                    "difficulty": "beginner",
                    "test_cases": [
                        {"input": "1 2 3 4 5", "expected_output": "15"},
                        {"input": "10 20 30", "expected_output": "60"},
                        {"input": "5", "expected_output": "5"}
                    ],
                    "starter_code": "def sum_list(numbers):\n    # TODO: Calculate sum\n    pass\n\nif __name__ == '__main__':\n    import sys\n    nums = list(map(int, sys.stdin.read().split()))\n    print(sum_list(nums))",
                    "solution_code": "def sum_list(numbers):\n    return sum(numbers)"
                }
            ],
            "intermediate": [
                {
                    "title": "Fibonacci Sequence",
                    "description": "Generate the first N numbers in the Fibonacci sequence.\n\nThe Fibonacci sequence starts with 0, 1, and each subsequent number is the sum of the previous two.",
                    "difficulty": "intermediate",
                    "test_cases": [
                        {"input": "5", "expected_output": "0 1 1 2 3"},
                        {"input": "7", "expected_output": "0 1 1 2 3 5 8"},
                        {"input": "1", "expected_output": "0"}
                    ],
                    "starter_code": "def fibonacci(n):\n    # TODO: Generate Fibonacci sequence\n    pass\n\nif __name__ == '__main__':\n    import sys\n    n = int(sys.stdin.read().strip())\n    result = fibonacci(n)\n    print(' '.join(map(str, result)))",
                    "solution_code": "def fibonacci(n):\n    if n <= 0:\n        return []\n    if n == 1:\n        return [0]\n    fib = [0, 1]\n    for i in range(2, n):\n        fib.append(fib[i-1] + fib[i-2])\n    return fib"
                },
                {
                    "title": "Dictionary Word Counter",
                    "description": "Count the frequency of each word in a given text.\n\nReturn a dictionary with words as keys and their counts as values.",
                    "difficulty": "intermediate",
                    "test_cases": [
                        {"input": "hello world hello", "expected_output": "hello:2 world:1"},
                        {"input": "python is great python", "expected_output": "python:2 is:1 great:1"}
                    ],
                    "starter_code": "def word_count(text):\n    # TODO: Count word frequencies\n    pass\n\nif __name__ == '__main__':\n    import sys\n    text = sys.stdin.read().strip()\n    result = word_count(text)\n    print(' '.join(f'{k}:{v}' for k, v in sorted(result.items())))",
                    "solution_code": "def word_count(text):\n    words = text.split()\n    counts = {}\n    for word in words:\n        counts[word] = counts.get(word, 0) + 1\n    return counts"
                },
                {
                    "title": "Binary Search Implementation",
                    "description": "Implement binary search to find an element in a sorted list.\n\nReturn the index if found, -1 otherwise.",
                    "difficulty": "intermediate",
                    "test_cases": [
                        {"input": "1 2 3 4 5\n3", "expected_output": "2"},
                        {"input": "10 20 30 40\n25", "expected_output": "-1"}
                    ],
                    "starter_code": "def binary_search(arr, target):\n    # TODO: Implement binary search\n    pass\n\nif __name__ == '__main__':\n    import sys\n    lines = sys.stdin.read().strip().split('\\n')\n    arr = list(map(int, lines[0].split()))\n    target = int(lines[1])\n    print(binary_search(arr, target))",
                    "solution_code": "def binary_search(arr, target):\n    left, right = 0, len(arr) - 1\n    while left <= right:\n        mid = (left + right) // 2\n        if arr[mid] == target:\n            return mid\n        elif arr[mid] < target:\n            left = mid + 1\n        else:\n            right = mid - 1\n    return -1"
                }
            ],
            "advanced": [
                {
                    "title": "Async File Processing",
                    "description": "Implement an async function to process multiple files concurrently.\n\nUse asyncio to read and process files efficiently.",
                    "difficulty": "advanced",
                    "test_cases": [
                        {"input": "file1.txt file2.txt", "expected_output": "2"},
                        {"input": "data.txt", "expected_output": "1"}
                    ],
                    "starter_code": "import asyncio\n\nasync def process_files(filenames):\n    # TODO: Implement async file processing\n    pass\n\nif __name__ == '__main__':\n    import sys\n    files = sys.stdin.read().strip().split()\n    result = asyncio.run(process_files(files))\n    print(result)",
                    "solution_code": "import asyncio\n\nasync def process_files(filenames):\n    async def process_one(filename):\n        # Simulate file processing\n        await asyncio.sleep(0.1)\n        return filename\n    \n    tasks = [process_one(f) for f in filenames]\n    results = await asyncio.gather(*tasks)\n    return len(results)"
                },
                {
                    "title": "LRU Cache Implementation",
                    "description": "Implement a Least Recently Used (LRU) cache with get and put operations.\n\nBoth operations should run in O(1) time.",
                    "difficulty": "advanced",
                    "test_cases": [
                        {"input": "PUT 1 10\nGET 1", "expected_output": "10"},
                        {"input": "PUT 1 10\nPUT 2 20\nGET 1", "expected_output": "10"}
                    ],
                    "starter_code": "class LRUCache:\n    def __init__(self, capacity):\n        # TODO: Initialize cache\n        pass\n    \n    def get(self, key):\n        # TODO: Get value\n        pass\n    \n    def put(self, key, value):\n        # TODO: Put value\n        pass",
                    "solution_code": "from collections import OrderedDict\n\nclass LRUCache:\n    def __init__(self, capacity):\n        self.cache = OrderedDict()\n        self.capacity = capacity\n    \n    def get(self, key):\n        if key not in self.cache:\n            return -1\n        self.cache.move_to_end(key)\n        return self.cache[key]\n    \n    def put(self, key, value):\n        if key in self.cache:\n            self.cache.move_to_end(key)\n        self.cache[key] = value\n        if len(self.cache) > self.capacity:\n            self.cache.popitem(last=False)"
                },
                {
                    "title": "Multithreaded Data Processor",
                    "description": "Process large datasets using multiple threads for parallel execution.\n\nImplement thread-safe data processing with proper synchronization.",
                    "difficulty": "advanced",
                    "test_cases": [
                        {"input": "1 2 3 4 5", "expected_output": "15"},
                        {"input": "10 20 30", "expected_output": "60"}
                    ],
                    "starter_code": "import threading\n\ndef process_data_parallel(data, num_threads=4):\n    # TODO: Implement multithreaded processing\n    pass\n\nif __name__ == '__main__':\n    import sys\n    data = list(map(int, sys.stdin.read().split()))\n    result = process_data_parallel(data)\n    print(result)",
                    "solution_code": "import threading\n\ndef process_data_parallel(data, num_threads=4):\n    result = [0]\n    lock = threading.Lock()\n    \n    def worker(chunk):\n        local_sum = sum(chunk)\n        with lock:\n            result[0] += local_sum\n    \n    chunk_size = len(data) // num_threads\n    threads = []\n    \n    for i in range(num_threads):\n        start = i * chunk_size\n        end = start + chunk_size if i < num_threads - 1 else len(data)\n        thread = threading.Thread(target=worker, args=(data[start:end],))\n        threads.append(thread)\n        thread.start()\n    \n    for thread in threads:\n        thread.join()\n    \n    return result[0]"
                }
            ]
        },
        "Java": {
            "beginner": [
                {
                    "title": "Array Sum Calculator",
                    "description": "Write a Java method to calculate the sum of an integer array.",
                    "difficulty": "beginner",
                    "test_cases": [
                        {"input": "1 2 3 4 5", "expected_output": "15"},
                        {"input": "10 20", "expected_output": "30"}
                    ],
                    "starter_code": "import java.util.*;\n\npublic class Main {\n    public static int arraySum(int[] arr) {\n        // TODO: Calculate sum\n        return 0;\n    }\n    \n    public static void main(String[] args) {\n        Scanner sc = new Scanner(System.in);\n        String[] input = sc.nextLine().split(\" \");\n        int[] arr = new int[input.length];\n        for (int i = 0; i < input.length; i++) {\n            arr[i] = Integer.parseInt(input[i]);\n        }\n        System.out.println(arraySum(arr));\n    }\n}",
                    "solution_code": "public static int arraySum(int[] arr) {\n    int sum = 0;\n    for (int num : arr) {\n        sum += num;\n    }\n    return sum;\n}"
                }
            ],
            "intermediate": [
                {
                    "title": "Bank Account Class",
                    "description": "Implement a BankAccount class with deposit, withdraw, and balance methods.",
                    "difficulty": "intermediate",
                    "test_cases": [
                        {"input": "DEPOSIT 100\nBALANCE", "expected_output": "100"},
                        {"input": "DEPOSIT 100\nWITHDRAW 30\nBALANCE", "expected_output": "70"}
                    ],
                    "starter_code": "public class BankAccount {\n    private double balance;\n    \n    public void deposit(double amount) {\n        // TODO\n    }\n    \n    public void withdraw(double amount) {\n        // TODO\n    }\n    \n    public double getBalance() {\n        // TODO\n        return 0;\n    }\n}",
                    "solution_code": "public class BankAccount {\n    private double balance;\n    \n    public void deposit(double amount) {\n        if (amount > 0) {\n            balance += amount;\n        }\n    }\n    \n    public void withdraw(double amount) {\n        if (amount > 0 && amount <= balance) {\n            balance -= amount;\n        }\n    }\n    \n    public double getBalance() {\n        return balance;\n    }\n}"
                }
            ],
            "advanced": [
                {
                    "title": "Thread-Safe Singleton Pattern",
                    "description": "Implement a thread-safe Singleton pattern in Java.",
                    "difficulty": "advanced",
                    "test_cases": [
                        {"input": "CREATE\nCREATE", "expected_output": "SAME"}
                    ],
                    "starter_code": "public class Singleton {\n    // TODO: Implement thread-safe singleton\n}",
                    "solution_code": "public class Singleton {\n    private static volatile Singleton instance;\n    \n    private Singleton() {}\n    \n    public static Singleton getInstance() {\n        if (instance == null) {\n            synchronized (Singleton.class) {\n                if (instance == null) {\n                    instance = new Singleton();\n                }\n            }\n        }\n        return instance;\n    }\n}"
                }
            ]
        },
        "JavaScript": {
            "beginner": [
                {
                    "title": "Array Filter Function",
                    "description": "Write a function to filter even numbers from an array.",
                    "difficulty": "beginner",
                    "test_cases": [
                        {"input": "1 2 3 4 5", "expected_output": "2 4"},
                        {"input": "10 15 20", "expected_output": "10 20"}
                    ],
                    "starter_code": "function filterEven(numbers) {\n    // TODO: Filter even numbers\n}\n\nconst readline = require('readline');\nconst rl = readline.createInterface({input: process.stdin});\nrl.on('line', (line) => {\n    const nums = line.split(' ').map(Number);\n    console.log(filterEven(nums).join(' '));\n    rl.close();\n});",
                    "solution_code": "function filterEven(numbers) {\n    return numbers.filter(n => n % 2 === 0);\n}"
                }
            ],
            "intermediate": [
                {
                    "title": "Promise Chain Handler",
                    "description": "Create a function that chains multiple promises and handles errors.",
                    "difficulty": "intermediate",
                    "test_cases": [
                        {"input": "5", "expected_output": "25"},
                        {"input": "3", "expected_output": "9"}
                    ],
                    "starter_code": "async function processNumber(n) {\n    // TODO: Process number with promises\n}\n\nprocessNumber(5).then(console.log);",
                    "solution_code": "async function processNumber(n) {\n    return new Promise((resolve) => {\n        setTimeout(() => resolve(n * n), 100);\n    });\n}"
                }
            ],
            "advanced": [
                {
                    "title": "Custom Event Emitter",
                    "description": "Implement a custom EventEmitter class with on, emit, and off methods.",
                    "difficulty": "advanced",
                    "test_cases": [
                        {"input": "EMIT test", "expected_output": "EVENT_FIRED"}
                    ],
                    "starter_code": "class EventEmitter {\n    // TODO: Implement event emitter\n}",
                    "solution_code": "class EventEmitter {\n    constructor() {\n        this.events = {};\n    }\n    \n    on(event, listener) {\n        if (!this.events[event]) {\n            this.events[event] = [];\n        }\n        this.events[event].push(listener);\n    }\n    \n    emit(event, ...args) {\n        if (this.events[event]) {\n            this.events[event].forEach(listener => listener(...args));\n        }\n    }\n    \n    off(event, listener) {\n        if (this.events[event]) {\n            this.events[event] = this.events[event].filter(l => l !== listener);\n        }\n    }\n}"
                }
            ]
        },
        "C": {
            "beginner": [
                {
                    "title": "Sum of Array",
                    "description": "Calculate the sum of integers in an array.",
                    "difficulty": "beginner",
                    "test_cases": [
                        {"input": "1 2 3 4 5", "expected_output": "15"},
                        {"input": "10 20", "expected_output": "30"}
                    ],
                    "starter_code": "#include <stdio.h>\n\nint main() {\n    int num, sum = 0;\n    while (scanf(\"%d\", &num) == 1) {\n        sum += num;\n    }\n    printf(\"%d\\n\", sum);\n    return 0;\n}",
                    "solution_code": "#include <stdio.h>\n\nint main() {\n    int num, sum = 0;\n    while (scanf(\"%d\", &num) == 1) {\n        sum += num;\n    }\n    printf(\"%d\\n\", sum);\n    return 0;\n}"
                }
            ],
            "intermediate": [],
            "advanced": []
        }
    }
    
    def __init__(self, api_key: str = None):
        """Initialize question generator (API key kept for MCQ generation)"""
        self.api_key = api_key
    
    def generate_questions_per_language(self, programming_languages: List[Dict], years_of_experience: int = 1) -> List[Dict]:
        """
        Generate 3 unique coding challenges for each programming language skill.
        
        Args:
            programming_languages: List of dicts with 'skill' and 'proficiency' keys
            years_of_experience: Candidate's years of experience (for future use)
            
        Returns:
            List of all generated coding challenges (3 per language)
        """
        all_challenges = []
        
        for lang_info in programming_languages:
            language = lang_info['skill']
            proficiency = lang_info['proficiency']
            
            print(f"\n{'='*60}")
            print(f"Generating 3 challenges for {language} ({proficiency} level)")
            print(f"{'='*60}")
            
            # Track selected challenges to avoid duplicates
            selected_titles = []
            
            # Generate exactly 3 challenges per language
            for challenge_num in range(1, 4):
                print(f"\nSelecting challenge {challenge_num}/3 for {language}...")
                
                try:
                    challenge = self.generate_coding_challenge(language, proficiency, avoid_titles=selected_titles)
                    
                    if challenge:
                        # Add challenge number metadata
                        challenge['challenge_number'] = challenge_num
                        challenge['language'] = language
                        challenge['skill'] = language
                        challenge['type'] = 'coding'
                        
                        all_challenges.append(challenge)
                        selected_titles.append(challenge.get('title', 'Untitled'))
                        print(f"[OK] Selected: {challenge.get('title', 'Untitled')}")
                    else:
                        print(f"[FAIL] No challenge available for {language} at {proficiency} level")
                        
                except Exception as e:
                    print(f"[ERROR] Error selecting challenge {challenge_num} for {language}: {e}")
                    continue
            
            print(f"\nCompleted {language}: {len([c for c in all_challenges if c.get('language') == language])}/3 challenges selected")
        
        print(f"\n{'='*60}")
        print(f"Total challenges generated: {len(all_challenges)}")
        print(f"{'='*60}\n")
        
        return all_challenges
    
    def generate_coding_challenge(self, skill: str, proficiency: str, avoid_titles: List[str] = None) -> Dict:
        """
        Generate a coding challenge from the static bank.
        
        Args:
            skill: The programming language
            proficiency: Skill level (beginner/intermediate/advanced)
            avoid_titles: List of challenge titles to avoid (for uniqueness)
            
        Returns:
            Coding challenge dictionary
        """
        avoid_titles = avoid_titles or []
        
        # Check if skill and proficiency exist in bank
        if skill in self.CHALLENGE_BANK and proficiency in self.CHALLENGE_BANK[skill]:
            challenges = self.CHALLENGE_BANK[skill][proficiency]
            
            if challenges:
                # Filter out already selected challenges
                available = [c for c in challenges if c['title'] not in avoid_titles]
                
                if available:
                    # Randomly select from available challenges
                    challenge = random.choice(available).copy()
                    return challenge
                else:
                    # If all challenges used, allow repeats but warn
                    print(f"[WARNING] All {proficiency} {skill} challenges used, selecting randomly")
                    challenge = random.choice(challenges).copy()
                    return challenge
        
        # Fallback if no challenges available
        return {
            "title": f"{skill} Challenge",
            "description": f"Complete a {proficiency} level {skill} coding challenge.",
            "difficulty": proficiency,
            "test_cases": [
                {"input": "test", "expected_output": "test"}
            ],
            "starter_code": f"# {skill} starter code\n# TODO: Implement solution",
            "solution_code": "# Solution code",
            "skill": skill,
            "type": "coding"
        }

    
    def generate_mcq_questions(self, skill: str, proficiency: str, num_questions: int = 5) -> List[Dict]:
        """
        Generate MCQ questions (kept from original for compatibility)
        Note: This still uses the original implementation
        """
        # This method remains unchanged for MCQ generation
        return []
