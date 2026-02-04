import os
from google import genai


def generate_content(prompt: str, model: str = "gemini-2.5-flash"):
    api_key = os.getenv("GENAI_API_KEY")
    if not api_key:
        raise RuntimeError("GENAI_API_KEY is not set")

    client = genai.Client(api_key=api_key)
    return client.models.generate_content(model=model, contents=prompt)
