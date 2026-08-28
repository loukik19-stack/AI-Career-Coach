import os

from dotenv import load_dotenv
from openai import OpenAI


# Load the secret key from .env
load_dotenv()


# Create the OpenAI client
client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)


def ask_ai(question):

    response = client.responses.create(
        model="gpt-5.6-luna",
        input=question
    )

    return response.output_text