import subprocess
import sys
import json
from typing import Dict, List
from config import Config
import time

class Evaluator:
    """Evaluate quiz answers and code submissions"""
    
    def __init__(self):
        self.timeout = Config.CODE_EXECUTION_TIMEOUT
        self.max_output = Config.MAX_OUTPUT_LENGTH
    
    def evaluate_mcq_quiz(self, questions: List[Dict], user_answers: Dict[int, str]) -> Dict:
        """
        Evaluate MCQ quiz answers
        
        Args:
            questions: List of MCQ questions
            user_answers: Dictionary mapping question index to selected answer
            
        Returns:
            Evaluation results with score and feedback
        """
        total_questions = len(questions)
        correct_answers = 0
        detailed_results = []
        
        for idx, question in enumerate(questions):
            user_answer = user_answers.get(idx, None)
            correct_answer = question['correct_answer']
            is_correct = user_answer == correct_answer
            
            if is_correct:
                correct_answers += 1
            
            detailed_results.append({
                'question_index': idx,
                'question': question['question'],
                'user_answer': user_answer,
                'correct_answer': correct_answer,
                'is_correct': is_correct,
                'explanation': question.get('explanation', ''),
                'skill': question.get('skill', '')
            })
        
        if total_questions > 0:
            score = (correct_answers / total_questions * 100)
        else:
            score = 0  # Handle case with no questions gracefully
        
        # Calculate skill-wise scores
        skill_scores = self._calculate_skill_scores(detailed_results)
        
        return {
            'total_questions': total_questions,
            'correct_answers': correct_answers,
            'score': round(score, 2),
            'percentage': round(score, 2),
            'detailed_results': detailed_results,
            'skill_scores': skill_scores,
            'performance_level': self._get_performance_level(score)
        }
    
    def evaluate_code(self, code: str, language: str, test_cases: List[Dict]) -> Dict:
        """
        Evaluate code submission against test cases
        
        Args:
            code: User's code submission
            language: Programming language
            test_cases: List of test cases with input and expected output
            
        Returns:
            Evaluation results
        """
        key = language.lower()
        
        # Map varying language codes to internal keys
        if key in ['js', 'node', 'javascript']: key = 'javascript'
        elif key in ['py', 'python3', 'python']: key = 'python'
        elif key in ['cpp', 'c++14', 'c++17', 'c++20', 'c++']: key = 'cpp'
        elif key in ['cs', 'csharp', 'dotnet']: key = 'csharp'
        elif key in ['ts', 'typescript']: key = 'typescript'
        
        # Python: Run locally (fast, no API limits, safe with exec)
        if key == 'python':
            return self._evaluate_python_code(code, test_cases)
        
        # All other languages: Use Judge0 API (no local installation needed)
        else:
            return self._evaluate_code_with_judge0(code, key, test_cases)
    
    def _evaluate_code_with_judge0(self, code: str, language: str, test_cases: List[Dict]) -> Dict:
        """
        Evaluate code using Judge0 API (for non-Python languages)
        
        Args:
            code: Source code
            language: Programming language  
            test_cases: List of test cases
            
        Returns:
            Evaluation results
        """
        from modules.judge0_client import Judge0Client
        import logging
        logger = logging.getLogger(__name__)
        
        try:
            client = Judge0Client()
            passed_tests = 0
            test_results = []
            
            for idx, test_case in enumerate(test_cases):
                test_input = str(test_case.get('input', '')).strip()
                expected_output = str(test_case.get('expected_output', '')).strip()
                
                # Execute code via Judge0
                result = client.execute_code(
                    code=code,
                    language=language,
                    stdin=test_input,
                    expected_output=expected_output
                )
                
                # Handle execution errors
                if not result.get('success', True):
                    test_results.append({
                        'test_case': idx + 1,
                        'input': test_input,
                        'expected_output': expected_output,
                        'actual_output': '',
                        'passed': False,
                        'error': result.get('error', 'Unknown error')
                    })
                    continue
                
                # Process successful execution
                is_passed = result.get('passed', False)
                if is_passed:
                    passed_tests += 1
                
                test_results.append({
                    'test_case': idx + 1,
                    'input': test_input,
                    'expected_output': expected_output,
                    'actual_output': result.get('stdout', ''),
                    'passed': is_passed,
                    'execution_time': result.get('time'),
                    'error': result.get('error') if not is_passed else None
                })
            
            total_tests = len(test_cases)
            score = (passed_tests / total_tests * 100) if total_tests > 0 else 0
            
            return {
                'success': True,
                'passed_tests': passed_tests,
                'total_tests': total_tests,
                'score': round(score, 2),
                'test_results': test_results,
                'performance_level': self._get_performance_level(score)
            }
            
        except Exception as e:
            logger.error(f'Judge0 evaluation error: {str(e)}', exc_info=True)
            return {
                'success': False,
                'error': f'Code execution service error: {str(e)}',
                'passed_tests': 0,
                'total_tests': len(test_cases)
            }

    # --- New Handlers ---
    
    def _evaluate_c_code(self, code: str, test_cases: List[Dict]) -> Dict:
        """Evaluate C code using GCC"""
        return self._evaluate_compiled_language(code, test_cases, 'c', 'gcc', ['.c'], lambda src, exe: ['gcc', src, '-o', exe])

    def _evaluate_csharp_code(self, code: str, test_cases: List[Dict]) -> Dict:
        """Evaluate C# code (Scripting mode / Mono)"""
        # Checks for 'csc' (Mono) or 'dotnet'
        # Simplified: Trying to run as single file (Mono style: mcs or csc)
        if self._is_command_available('csc'):
             return self._evaluate_compiled_language(code, test_cases, 'cs', 'csc', ['.cs'], lambda src, exe: ['csc', f'-out:{exe}', src])
        else:
             return self._create_missing_tool_result('C# Compiler (csc)', len(test_cases))

    def _evaluate_go_code(self, code: str, test_cases: List[Dict]) -> Dict:
        """Evaluate Go code"""
        if not self._is_command_available('go'):
            return self._create_missing_tool_result('Go', len(test_cases))
            
        return self._evaluate_interpreted_language(code, test_cases, 'go', lambda src: ['go', 'run', src])

    def _evaluate_rust_code(self, code: str, test_cases: List[Dict]) -> Dict:
        """Evaluate Rust code"""
        return self._evaluate_compiled_language(code, test_cases, 'rs', 'rustc', ['.rs'], lambda src, exe: ['rustc', src, '-o', exe])

    def _evaluate_ruby_code(self, code: str, test_cases: List[Dict]) -> Dict:
        return self._evaluate_interpreted_language(code, test_cases, 'rb', lambda src: ['ruby', src], 'ruby')

    def _evaluate_php_code(self, code: str, test_cases: List[Dict]) -> Dict:
        return self._evaluate_interpreted_language(code, test_cases, 'php', lambda src: ['php', src], 'php')
        
    def _evaluate_typescript_code(self, code: str, test_cases: List[Dict]) -> Dict:
        return self._evaluate_interpreted_language(code, test_cases, 'ts', lambda src: ['ts-node', src], 'ts-node')
        
    def _evaluate_bash_code(self, code: str, test_cases: List[Dict]) -> Dict:
        return self._evaluate_interpreted_language(code, test_cases, 'sh', lambda src: ['bash', src], 'bash')

    # --- Generic Helpers ---

    def _evaluate_interpreted_language(self, code: str, test_cases: List[Dict], ext: str, cmd_builder, tool_name: str = None) -> Dict:
        """Generic handler for interpreted languages"""
        import tempfile, os
        
        if tool_name and not self._is_command_available(tool_name):
            return self._create_missing_tool_result(tool_name, len(test_cases))

        passed_tests = 0
        test_results = []
        
        with tempfile.NamedTemporaryFile(suffix=f'.{ext}', delete=False, mode='w', encoding='utf-8') as f:
            f.write(code)
            src_file = f.name
            
        try:
            for idx, test_case in enumerate(test_cases):
                test_input = str(test_case.get('input', '')).strip()
                expected_output = str(test_case.get('expected_output', '')).strip()
                
                result = self._run_subprocess(cmd_builder(src_file), test_input)
                self._process_test_result(result, test_case, idx, test_input, expected_output, test_results)
                if test_results[-1]['passed']: passed_tests += 1
                
        finally:
            if os.path.exists(src_file): os.unlink(src_file)
            
        return self._compile_final_result(passed_tests, test_results, len(test_cases))

    def _evaluate_compiled_language(self, code: str, test_cases: List[Dict], ext: str, tool_name: str, temp_files_exts: List[str], compile_cmd_builder) -> Dict:
        """Generic handler for compiled languages"""
        import tempfile, os, platform
        
        if not self._is_command_available(tool_name):
             return self._create_missing_tool_result(tool_name, len(test_cases))

        with tempfile.NamedTemporaryFile(suffix=f'.{ext}', delete=False, mode='w', encoding='utf-8') as f:
            f.write(code)
            src_file = f.name
            
        exe_ext = '.exe' if platform.system() == 'Windows' else '.out'
        exe_file = src_file.replace(f'.{ext}', exe_ext)
        
        try:
            # Compile
            compile_res = self._run_subprocess(compile_cmd_builder(src_file, exe_file), '')
            if compile_res['return_code'] != 0:
                return {
                    'success': False,
                    'error': f"Compilation Error:\n{compile_res['stderr']}",
                    'passed_tests': 0,
                    'total_tests': len(test_cases)
                }
            
            # Execute
            passed_tests = 0
            test_results = []
            
            for idx, test_case in enumerate(test_cases):
                test_input = str(test_case.get('input', '')).strip()
                expected_output = str(test_case.get('expected_output', '')).strip()
                
                result = self._run_subprocess([exe_file], test_input)
                self._process_test_result(result, test_case, idx, test_input, expected_output, test_results)
                if test_results[-1]['passed']: passed_tests += 1
                
        finally:
            if os.path.exists(src_file): os.unlink(src_file)
            if os.path.exists(exe_file): os.unlink(exe_file)
            
        return self._compile_final_result(passed_tests, test_results, len(test_cases))

    def _process_test_result(self, result, test_case, idx, inp, expected, results_list):
        """Helper to process a subprocess result into the results list"""
        if result['timeout']:
            results_list.append({
                'test_case': idx + 1,
                'input': inp,
                'expected_output': expected,
                'actual_output': '',
                'passed': False,
                'error': 'Time limit exceeded',
                'execution_time': result['execution_time']
            })
            return

        if result['return_code'] != 0:
            results_list.append({
                'test_case': idx + 1,
                'input': inp,
                'expected_output': expected,
                'actual_output': result['stderr'],
                'passed': False,
                'error': 'Runtime Error'
            })
            return

        is_passed = self._compare_outputs(result['stdout'], expected)
        results_list.append({
            'test_case': idx + 1,
            'input': inp,
            'expected_output': expected,
            'actual_output': result['stdout'],
            'passed': is_passed,
            'execution_time': result['execution_time']
        })

    def _compile_final_result(self, passed, results, total):
        score = (passed / total * 100) if total > 0 else 0
        return {
            'success': True,
            'passed_tests': passed,
            'total_tests': total,
            'score': round(score, 2),
            'test_results': results,
            'performance_level': self._get_performance_level(score)
        }

    def _create_missing_tool_result(self, tool, total_tests):
        return {
            'success': False,
            'error': f'{tool} not found on server. Please install it to run this code.',
            'passed_tests': 0,
            'total_tests': total_tests
        }
    
    def _evaluate_python_code(self, code: str, test_cases: List[Dict]) -> Dict:
        """Evaluate Python code in a restricted environment"""
        import io
        import sys
        
        passed_tests = 0
        test_results = []
        
        for idx, test_case in enumerate(test_cases):
            try:
                # Prepare input and expected output
                test_input = str(test_case.get('input', '')).strip()
                expected_output = str(test_case.get('expected_output', '')).strip()
                
                # Execute code with timeout
                start_time = time.time()
                
                # Capture stdout
                old_stdout = sys.stdout
                sys.stdout = captured_output = io.StringIO()
                
                # Prepare input simulation
                old_stdin = sys.stdin
                sys.stdin = io.StringIO(test_input)
                
                try:
                    # Create execution environment
                    exec_globals = {
                        '__builtins__': __builtins__,
                        '__name__': '__main__',
                        'input': lambda prompt='': sys.stdin.readline().rstrip('\n')
                    }
                    
                    # Execute the code
                    exec(code, exec_globals)
                    
                    # Get the captured output
                    actual_output = captured_output.getvalue().strip()
                    
                    # If no output captured, try to get result from globals
                    if not actual_output:
                        if 'result' in exec_globals:
                            actual_output = str(exec_globals['result']).strip()
                        elif 'output' in exec_globals:
                            actual_output = str(exec_globals['output']).strip()
                    
                finally:
                    # Restore stdout and stdin
                    sys.stdout = old_stdout
                    sys.stdin = old_stdin
                
                execution_time = time.time() - start_time
                
                # Check timeout
                if execution_time > self.timeout:
                    test_results.append({
                        'test_case': idx + 1,
                        'input': test_input,
                        'expected_output': expected_output,
                        'actual_output': '',
                        'passed': False,
                        'error': 'Time limit exceeded',
                        'execution_time': execution_time
                    })
                    continue
                
                # Compare outputs (handle different types)
                is_passed = self._compare_outputs(actual_output, expected_output)
                
                if is_passed:
                    passed_tests += 1
                
                test_results.append({
                    'test_case': idx + 1,
                    'input': test_input,
                    'expected_output': expected_output,
                    'actual_output': actual_output,
                    'passed': is_passed,
                    'execution_time': round(execution_time, 3)
                })
                
            except Exception as e:
                test_results.append({
                    'test_case': idx + 1,
                    'input': test_input if 'test_input' in locals() else '',
                    'expected_output': expected_output if 'expected_output' in locals() else '',
                    'actual_output': '',
                    'passed': False,
                    'error': str(e)
                })
        
        total_tests = len(test_cases)
        score = (passed_tests / total_tests * 100) if total_tests > 0 else 0
        
        return {
            'success': True,
            'passed_tests': passed_tests,
            'total_tests': total_tests,
            'score': round(score, 2),
            'test_results': test_results,
            'performance_level': self._get_performance_level(score)
        }
    
    def _compare_outputs(self, actual: str, expected: str) -> bool:
        """Compare actual and expected outputs with flexible matching"""
        # Direct string comparison
        if actual == expected:
            return True
        
        # Try comparing as numbers
        try:
            return float(actual) == float(expected)
        except (ValueError, TypeError):
            pass
        
        # Try comparing as booleans
        if actual.lower() in ['true', 'false'] and expected.lower() in ['true', 'false']:
            return actual.lower() == expected.lower()
        
        # Case-insensitive comparison
        if actual.lower() == expected.lower():
            return True
        
        return False
    
    def _evaluate_javascript_code(self, code: str, test_cases: List[Dict]) -> Dict:
        """Evaluate JavaScript code using Node.js"""
        import tempfile
        import os
        
        # Check if node is installed
        if not self._is_command_available('node'):
             return {
                'success': False,
                'error': 'Node.js not found on server. Please install Node.js.',
                'passed_tests': 0,
                'total_tests': len(test_cases)
            }

        passed_tests = 0
        test_results = []
        
        for idx, test_case in enumerate(test_cases):
            # Create temporary JS file
            with tempfile.NamedTemporaryFile(suffix='.js', delete=False, mode='w', encoding='utf-8') as f:
                f.write(code)
                js_file = f.name
            
            try:
                test_input = str(test_case.get('input', '')).strip()
                expected_output = str(test_case.get('expected_output', '')).strip()
                
                # Execute
                result = self._run_subprocess(['node', js_file], test_input)
                
                if result['timeout']:
                    test_results.append({
                        'test_case': idx + 1,
                        'input': test_input,
                        'expected_output': expected_output,
                        'actual_output': '',
                        'passed': False,
                        'error': 'Time limit exceeded',
                        'execution_time': result['execution_time']
                    })
                    continue
                    
                if result['return_code'] != 0:
                     test_results.append({
                        'test_case': idx + 1,
                        'input': test_input,
                        'expected_output': expected_output,
                        'actual_output': result['stderr'],
                        'passed': False,
                        'error': 'Runtime Error'
                    })
                     continue

                is_passed = self._compare_outputs(result['stdout'], expected_output)
                if is_passed:
                    passed_tests += 1
                    
                test_results.append({
                    'test_case': idx + 1,
                    'input': test_input,
                    'expected_output': expected_output,
                    'actual_output': result['stdout'],
                    'passed': is_passed,
                    'execution_time': result['execution_time']
                })
                
            except Exception as e:
                 test_results.append({
                    'test_case': idx + 1,
                    'passed': False,
                    'error': str(e)
                })
            finally:
                if os.path.exists(js_file):
                    os.unlink(js_file)

        total_tests = len(test_cases)
        score = (passed_tests / total_tests * 100) if total_tests > 0 else 0
        
        return {
            'success': True,
            'passed_tests': passed_tests,
            'total_tests': total_tests,
            'score': round(score, 2),
            'test_results': test_results,
            'performance_level': self._get_performance_level(score)
        }
    
    def _evaluate_java_code(self, code: str, test_cases: List[Dict]) -> Dict:
        """Evaluate Java code"""
        import tempfile
        import os
        import shutil
        
        # Check for Java
        if not self._is_command_available('javac') or not self._is_command_available('java'):
             return {
                'success': False,
                'error': 'Java (JDK) not found on server.',
                'passed_tests': 0,
                'total_tests': len(test_cases)
            }

        # Create a temp directory for class files
        temp_dir = tempfile.mkdtemp()
        java_file = os.path.join(temp_dir, 'Main.java')
        
        try:
            with open(java_file, 'w', encoding='utf-8') as f:
                f.write(code)
            
            # Compile
            compile_result = self._run_subprocess(['javac', java_file], '')
            
            if compile_result['return_code'] != 0:
                return {
                    'success': False,
                    'error': f"Compilation Error:\n{compile_result['stderr']}",
                    'passed_tests': 0,
                    'total_tests': len(test_cases)
                }
                
            passed_tests = 0
            test_results = []
            
            for idx, test_case in enumerate(test_cases):
                test_input = str(test_case.get('input', '')).strip()
                expected_output = str(test_case.get('expected_output', '')).strip()
                
                # Run (classpath must be temp_dir)
                result = self._run_subprocess(['java', '-cp', temp_dir, 'Main'], test_input)
                
                if result['timeout']:
                    test_results.append({
                        'test_case': idx + 1,
                        'input': test_input,
                        'expected_output': expected_output,
                        'actual_output': '',
                        'passed': False,
                        'error': 'Time limit exceeded',
                        'execution_time': result['execution_time']
                    })
                    continue
                
                if result['return_code'] != 0:
                    test_results.append({
                        'test_case': idx + 1,
                        'input': test_input,
                        'expected_output': expected_output,
                        'actual_output': result['stderr'],
                        'passed': False,
                        'error': 'Runtime Error'
                    })
                    continue
                    
                is_passed = self._compare_outputs(result['stdout'], expected_output)
                if is_passed:
                    passed_tests += 1
                
                test_results.append({
                    'test_case': idx + 1,
                    'input': test_input,
                    'expected_output': expected_output,
                    'actual_output': result['stdout'],
                    'passed': is_passed,
                    'execution_time': result['execution_time']
                })
                
        finally:
            shutil.rmtree(temp_dir, ignore_errors=True)
            
        total_tests = len(test_cases)
        score = (passed_tests / total_tests * 100) if total_tests > 0 else 0
        
        return {
            'success': True,
            'passed_tests': passed_tests,
            'total_tests': total_tests,
            'score': round(score, 2),
            'test_results': test_results,
            'performance_level': self._get_performance_level(score)
        }

    def _evaluate_cpp_code(self, code: str, test_cases: List[Dict]) -> Dict:
        """Evaluate C++ code"""
        import tempfile
        import os
        import platform
        
        if not self._is_command_available('g++'):
             return {
                'success': False,
                'error': 'G++ compiler not found on server.',
                'passed_tests': 0,
                'total_tests': len(test_cases)
            }

        with tempfile.NamedTemporaryFile(suffix='.cpp', delete=False, mode='w', encoding='utf-8') as f:
            f.write(code)
            cpp_file = f.name
            
        exe_extension = '.exe' if platform.system() == 'Windows' else '.out'
        exe_file = cpp_file.replace('.cpp', exe_extension)
        
        try:
            # Compile
            compile_cmd = ['g++', cpp_file, '-o', exe_file]
            compile_result = self._run_subprocess(compile_cmd, '')
            
            if compile_result['return_code'] != 0:
                os.unlink(cpp_file) 
                return {
                    'success': False,
                    'error': f"Compilation Error:\n{compile_result['stderr']}",
                    'passed_tests': 0,
                    'total_tests': len(test_cases)
                }
            
            passed_tests = 0
            test_results = []
            
            for idx, test_case in enumerate(test_cases):
                test_input = str(test_case.get('input', '')).strip()
                expected_output = str(test_case.get('expected_output', '')).strip()
                
                result = self._run_subprocess([exe_file], test_input)
                
                if result['timeout']:
                    test_results.append({
                        'test_case': idx + 1,
                        'input': test_input,
                        'expected_output': expected_output,
                        'actual_output': '',
                        'passed': False,
                        'error': 'Time limit exceeded',
                        'execution_time': result['execution_time']
                    })
                    continue
                
                is_passed = self._compare_outputs(result['stdout'], expected_output)
                if is_passed:
                    passed_tests += 1
                
                test_results.append({
                    'test_case': idx + 1,
                    'input': test_input,
                    'expected_output': expected_output,
                    'actual_output': result['stdout'],
                    'passed': is_passed,
                    'execution_time': result['execution_time']
                })
                
        finally:
            if os.path.exists(cpp_file):
                os.unlink(cpp_file)
            if os.path.exists(exe_file):
                os.unlink(exe_file)
                
        total_tests = len(test_cases)
        score = (passed_tests / total_tests * 100) if total_tests > 0 else 0
        
        return {
            'success': True,
            'passed_tests': passed_tests,
            'total_tests': total_tests,
            'score': round(score, 2),
            'test_results': test_results,
            'performance_level': self._get_performance_level(score)
        }

    def _is_command_available(self, cmd: str) -> bool:
        """Check if a command is available in PATH"""
        import shutil
        return shutil.which(cmd) is not None

    def _run_subprocess(self, cmd: List[str], input_str: str) -> Dict:
        """Run a subprocess with input and capture output safely"""
        start_time = time.time()
        try:
            process = subprocess.run(
                cmd,
                input=input_str,
                capture_output=True,
                text=True,
                timeout=self.timeout
            )
            return {
                'stdout': process.stdout.strip(),
                'stderr': process.stderr.strip(),
                'return_code': process.returncode,
                'timeout': False,
                'execution_time': time.time() - start_time
            }
        except subprocess.TimeoutExpired:
            return {
                'stdout': '',
                'stderr': 'Timeout',
                'return_code': -1,
                'timeout': True,
                'execution_time': self.timeout
            }
        except Exception as e:
            return {
                'stdout': '',
                'stderr': str(e),
                'return_code': -1,
                'timeout': False,
                'execution_time': time.time() - start_time
            }
    
    def _calculate_skill_scores(self, detailed_results: List[Dict]) -> Dict[str, Dict]:
        """Calculate scores for each skill"""
        skill_data = {}
        
        for result in detailed_results:
            skill = result.get('skill', 'Unknown')
            if skill not in skill_data:
                skill_data[skill] = {'correct': 0, 'total': 0}
            
            skill_data[skill]['total'] += 1
            if result['is_correct']:
                skill_data[skill]['correct'] += 1
        
        # Calculate percentages
        skill_scores = {}
        for skill, data in skill_data.items():
            score = (data['correct'] / data['total'] * 100) if data['total'] > 0 else 0
            skill_scores[skill] = {
                'correct': data['correct'],
                'total': data['total'],
                'score': round(score, 2),
                'performance_level': self._get_performance_level(score)
            }
        
        return skill_scores
    
    def _get_performance_level(self, score: float) -> str:
        """Determine performance level based on score"""
        if score >= Config.SCORE_EXCELLENT:
            return 'Excellent'
        elif score >= Config.SCORE_GOOD:
            return 'Good'
        elif score >= Config.SCORE_AVERAGE:
            return 'Average'
        elif score >= Config.SCORE_NEEDS_IMPROVEMENT:
            return 'Needs Improvement'
        else:
            return 'Poor'
    
    def calculate_overall_score(self, mcq_result: Dict, coding_results: List[Dict], hr_evaluation: Dict = None) -> Dict:
        """
        Calculate overall assessment score using weighted evaluation
        
        Args:
            mcq_result: MCQ evaluation result
            coding_results: List of coding challenge results
            hr_evaluation: HR interview evaluation (optional)
            
        Returns:
            Overall score and detailed breakdown
        """
        # Get individual scores
        mcq_score = mcq_result.get('score', 0)
        
        # Calculate average coding score
        if coding_results:
            coding_score = sum(r.get('score', 0) for r in coding_results) / len(coding_results)
        else:
            coding_score = 0
        
        # Get HR interview score
        hr_score = hr_evaluation.get('overall_score', 0) if hr_evaluation else 0
        
        # Get weights from config
        weights = Config.SCORING_WEIGHTS
        
        # Calculate weighted overall score
        if hr_evaluation:
            # All three components available
            overall_score = (
                mcq_score * weights['mcq'] +
                coding_score * weights['coding'] +
                hr_score * weights['hr_interview']
            )
        elif coding_results:
            # Only MCQ and Coding available
            total_weight = weights['mcq'] + weights['coding']
            overall_score = (
                mcq_score * (weights['mcq'] / total_weight) +
                coding_score * (weights['coding'] / total_weight)
            )
        else:
            # Only MCQ available
            overall_score = mcq_score
        
        return {
            'mcq_score': round(mcq_score, 2),
            'mcq_weight': weights['mcq'] * 100,
            'coding_score': round(coding_score, 2),
            'coding_weight': weights['coding'] * 100,
            'hr_score': round(hr_score, 2),
            'hr_weight': weights['hr_interview'] * 100,
            'overall_score': round(overall_score, 2),
            'performance_level': self._get_performance_level(overall_score),
            'breakdown': {
                'mcq_contribution': round(mcq_score * weights['mcq'], 2),
                'coding_contribution': round(coding_score * weights['coding'], 2),
                'hr_contribution': round(hr_score * weights['hr_interview'], 2)
            }
        }
