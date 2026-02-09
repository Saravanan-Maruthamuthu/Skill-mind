
import requests
import json
import sys
import os

# Add module path
sys.path.append(os.path.join(os.getcwd(), 'backend'))
sys.path.append(os.path.join(os.getcwd(), 'backend', 'modules'))

from modules.judge0_client import Judge0Client

def verify_fix():
    client = Judge0Client()
    
    # JavaScript solution (from fallback)
    code = """const readline = require('readline');
const rl = readline.createInterface({input: process.stdin});
let lines = [];
rl.on('line', (line) => lines.push(line));
rl.on('close', () => {
    if (lines.length < 2) return;
    const s = lines[0].split('').sort().join('');
    const t = lines[1].split('').sort().join('');
    console.log(s === t);
});"""

    # Correct input
    stdin = "anagram\nnagaram"
    expected = "true"
    
    print("Submitting code to Judge0...")
    result = client.execute_code(code, "javascript", stdin, expected)
    
    print("\nResult:")
    print(json.dumps(result, indent=2))
    
    if result['success'] and result['passed']:
        print("\nSUCCESS: Code executed successfully and passed.")
    else:
        print("\nFAILURE: Code execution failed or did not pass.")
        sys.exit(1)

if __name__ == "__main__":
    verify_fix()
