from ai_engine import ask_ai

print("Testing Gemini connection...")
print()

response = ask_ai(
    "Reply with exactly: Gemini connection successful!"
)

print("Gemini response:")
print(response)