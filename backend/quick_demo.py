"""
Quick Demo: Generate a Single Challenge
Run this to see a complete challenge generated instantly!
"""

from modules.dynamic_challenge_generator import DynamicChallengeGenerator
import json

# Create generator
generator = DynamicChallengeGenerator()

print("🎯 DYNAMIC CODING CHALLENGE GENERATOR")
print("=" * 70)
print("\nGenerating a challenge...\n")

# Generate a challenge
challenge = generator.generate_challenge(
    language="Python",
    difficulty="Intermediate",
    topic="Arrays"
)

# Display the challenge
print(f"📌 TITLE: {challenge['title']}\n")
print(f"🎚️  DIFFICULTY: {challenge['difficulty']}")
print(f"💻 LANGUAGE: {challenge['language']}")
print(f"📚 TOPIC: {challenge['topic']}\n")

print("=" * 70)
print("📝 DESCRIPTION:")
print("=" * 70)
print(challenge['description'])
print()

print("=" * 70)
print("⚙️  CONSTRAINTS:")
print("=" * 70)
for constraint in challenge['constraints']:
    print(f"  • {constraint}")
print()

print("=" * 70)
print("💡 HINTS:")
print("=" * 70)
for i, hint in enumerate(challenge['hints'], 1):
    print(f"  {i}. {hint}")
print()

print("=" * 70)
print("🧪 TEST CASES:")
print("=" * 70)
for i, tc in enumerate(challenge['test_cases'], 1):
    print(f"\n  Test Case {i}:")
    print(f"    Input: {tc['input']}")
    print(f"    Expected Output: {tc['expected_output']}")
    print(f"    Explanation: {tc['explanation']}")
print()

print("=" * 70)
print("💻 STARTER CODE:")
print("=" * 70)
print(challenge['starter_code'])
print()

print("=" * 70)
print("✅ Challenge generated successfully!")
print("=" * 70)
print(f"\n⏱️  Time Limit: {challenge['time_limit']} second(s)")
print(f"📊 Total Test Cases: {len(challenge['test_cases'])}")
print(f"🔄 Run this script again to get a DIFFERENT challenge!\n")

# Save to JSON file
with open("latest_challenge.json", "w") as f:
    json.dump(challenge, f, indent=2)

print("💾 Challenge saved to: latest_challenge.json")
