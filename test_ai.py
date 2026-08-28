from ai_engine import ask_ai_json

print("Testing structured Gemini response...")
print()

prompt = """
Return ONLY a JSON object with these fields:

{
    "name": "CareerAI",
    "status": "working",
    "score": 95
}
"""

result = ask_ai_json(prompt)

print("Gemini response:")
print(result)