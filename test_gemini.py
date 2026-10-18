import os
from pathlib import Path
from dotenv import load_dotenv
from google import genai

env_path = Path("backend/.env")
load_dotenv(env_path)

if not os.getenv("GEMINI_API_KEY"):
    raise RuntimeError("GEMINI_API_KEY is missing from backend/.env")

client = genai.Client()

response = client.models.generate_content(
    model="gemini-3.6-flash",
    contents="Reply with exactly: GEMINI_CONNECTION_OK",
)

print(response.text)
