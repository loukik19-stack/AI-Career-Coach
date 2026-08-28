import os
import json

from dotenv import load_dotenv
from google import genai


# Load environment variables
load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    raise ValueError(
        "GEMINI_API_KEY was not found. "
        "Please check your .env file."
    )


# Create Gemini client
client = genai.Client(api_key=API_KEY)

MODEL_NAME = "gemini-3.6-flash"


def ask_ai(prompt):
    """Send a normal text prompt to Gemini."""

    try:
        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=prompt
        )

        return response.text

    except Exception as e:
        return f"AI Error: {str(e)}"


def ask_ai_json(prompt):
    """Send a prompt to Gemini and return JSON."""

    try:
        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=prompt,
            config={
                "response_mime_type": "application/json"
            }
        )

        return json.loads(response.text)

    except Exception as e:
        return {
            "error": str(e)
        }