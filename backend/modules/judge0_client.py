import requests
import time
from typing import Dict, Optional
from config import Config
import logging

logger = logging.getLogger(__name__)


class Judge0Client:
    """Client for Judge0 CE API - Online code execution service"""
    
    # Judge0 Language ID Mappings - Only Essential Languages
    LANGUAGE_IDS = {
        # Core Languages
        'c': 50,           # C (GCC 9.2.0)
        
        'cpp': 54,         # C++ (GCC 9.2.0)
        'c++': 54,
        'cpp14': 54,
        'cpp17': 54,
        'cpp20': 54,
        
        'python': 71,      # Python 3.8.1
        'python3': 71,
        'py': 71,
        
        'java': 62,        # Java (OpenJDK 13.0.1)
        
        'javascript': 63,  # JavaScript (Node.js 12.14.0)
        'js': 63,
        'node': 63,
        'nodejs': 63,
        
        'sql': 82,         # SQL (SQLite 3.27.2)
        'sqlite': 82,
        
        # Modern Languages
        'kotlin': 78,      # Kotlin (1.3.70)
        'go': 60,          # Go (1.13.5)
        'golang': 60,
        'rust': 73,        # Rust (1.40.0)
        'swift': 83,       # Swift (5.2.3)
        
        # Data Science
        'r': 80,           # R (4.0.0)
    }
    
    def __init__(self):
        self.api_url = Config.JUDGE0_API_URL
        self.api_key = Config.JUDGE0_API_KEY
        self.api_host = Config.JUDGE0_API_HOST
        self.timeout = Config.JUDGE0_TIMEOUT
        
    def get_headers(self) -> Dict[str, str]:
        """Get headers for API requests"""
        return {
            'Content-Type': 'application/json'
        }
    
    def get_language_id(self, language: str) -> Optional[int]:
        """Get Judge0 language ID from language name"""
        lang_lower = language.lower().strip()
        return self.LANGUAGE_IDS.get(lang_lower)
    
    def execute_code(self, code: str, language: str, stdin: str = '', expected_output: str = '') -> Dict:
        """
        Execute code using Judge0 API
        
        Args:
            code: Source code to execute
            language: Programming language
            stdin: Standard input for the program
            expected_output: Expected output for comparison
            
        Returns:
            Dictionary with execution results
        """
        language_id = self.get_language_id(language)
        
        if not language_id:
            return {
                'success': False,
                'error': f'Language "{language}" is not supported by Judge0',
                'passed': False
            }
        
        try:
            # Create submission
            submission_data = {
                'source_code': code,
                'language_id': language_id,
                'stdin': stdin if stdin else '',
                'expected_output': expected_output if expected_output else None
            }
            
            # Submit code for execution
            response = requests.post(
                f'{self.api_url}/submissions?base64_encoded=false&wait=true',
                json=submission_data,
                headers=self.get_headers(),
                timeout=self.timeout
            )
            
            if response.status_code not in [200, 201]:
                logger.error(f'Judge0 submission failed: {response.status_code} - {response.text}')
                return {
                    'success': False,
                    'error': f'Code execution service returned error: {response.status_code}',
                    'passed': False
                }
            
            result = response.json()
            
            # Parse result
            return self._parse_result(result, expected_output)
            
        except requests.exceptions.Timeout:
            return {
                'success': False,
                'error': 'Code execution timed out',
                'passed': False
            }
        except requests.exceptions.RequestException as e:
            logger.error(f'Judge0 API error: {str(e)}')
            return {
                'success': False,
                'error': f'Code execution service error: {str(e)}',
                'passed': False
            }
        except Exception as e:
            logger.error(f'Unexpected error in Judge0 execution: {str(e)}')
            return {
                'success': False,
                'error': f'Unexpected error: {str(e)}',
                'passed': False
            }
    
    def _parse_result(self, result: Dict, expected_output: str) -> Dict:
        """Parse Judge0 execution result"""
        status = result.get('status', {})
        status_id = status.get('id', 0)
        status_desc = status.get('description', 'Unknown')
        
        stdout = (result.get('stdout') or '').strip()
        stderr = (result.get('stderr') or '').strip()
        compile_output = (result.get('compile_output') or '').strip()
        
        execution_time = result.get('time')  # in seconds
        memory = result.get('memory')  # in KB
        
        # Status codes:
        # 3 = Accepted
        # 4 = Wrong Answer
        # 5 = Time Limit Exceeded
        # 6 = Compilation Error
        # 7 = Runtime Error (SIGSEGV)
        # 8 = Runtime Error (SIGXFSZ)
        # 9 = Runtime Error (SIGFPE)
        # 10 = Runtime Error (SIGABRT)
        # 11 = Runtime Error (NZEC)
        # 12 = Runtime Error (Other)
        # 13 = Internal Error
        # 14 = Exec Format Error
        
        if status_id == 6:  # Compilation Error
            return {
                'success': False,
                'error': f'Compilation Error:\n{compile_output or stderr}',
                'stdout': '',
                'stderr': compile_output or stderr,
                'passed': False,
                'time': execution_time
            }
        
        if status_id == 5:  # Time Limit Exceeded
            return {
                'success': False,
                'error': 'Time Limit Exceeded',
                'stdout': stdout,
                'stderr': stderr,
                'passed': False,
                'time': execution_time
            }
        
        if status_id in [7, 8, 9, 10, 11, 12]:  # Runtime Errors
            return {
                'success': False,
                'error': f'Runtime Error: {status_desc}',
                'stdout': stdout,
                'stderr': stderr,
                'passed': False,
                'time': execution_time
            }
        
        # Check if output matches expected
        if expected_output:
            passed = self._compare_outputs(stdout, expected_output)
        else:
            # If no expected output provided, consider it passed if no errors
            passed = status_id == 3
        
        return {
            'success': True,
            'stdout': stdout,
            'stderr': stderr,
            'passed': passed,
            'time': execution_time,
            'memory': memory,
            'status': status_desc
        }
    
    def _compare_outputs(self, actual: str, expected: str) -> bool:
        """Compare actual and expected outputs"""
        # Direct comparison
        if actual == expected:
            return True
        
        # Try comparing as numbers
        try:
            return float(actual) == float(expected)
        except (ValueError, TypeError):
            pass
        
        # Case-insensitive comparison
        if actual.lower() == expected.lower():
            return True
        
        return False
