
import os
import sys
from dotenv import load_dotenv
sys.path.append(os.path.join(os.getcwd(), 'backend'))
from modules.hr_interviewer import HRInterviewer

# Load env in case it's not loaded
load_dotenv(os.path.join('backend', '.env'))
load_dotenv(os.path.join(os.getcwd(), 'backend', '.env'))

def verify():
    key = os.getenv('OPENAI_API_KEY')
    print(f"Checking API Key: {'Present' if key else 'MISSING'}")
    if key and len(key) > 5:
        print(f"Key preview: {key[:5]}...")
    
    # Try initializing interviewer
    try:
        hr = HRInterviewer()
        print("HRInterviewer initialized successfully.")
    except Exception as e:
        print(f"HRInterviewer init failed: {e}")
        return

    # Try a simple completion
    print("\nAttempting API call...")
    try:
        response = hr.client.chat.completions.create(
            model=hr.model,
            messages=[{"role": "user", "content": "Say hello"}],
            max_tokens=5
        )
        print(f"Success! Response: {response.choices[0].message.content}")
    except Exception as e:
        print(f"API Call Failed: {e}")

if __name__ == "__main__":
    verify()
