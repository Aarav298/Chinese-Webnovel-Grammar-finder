import os
from google import genai
from google.genai import types
from ..models.analysis import AnalyzeResponse

client = genai.Client(
    api_key = os.environ["GEMINI_API_KEY"]
)

def generate_analysis(text: str) -> AnalyzeResponse:
    prompt = f"""
You are a Chinese language tutor. Analyze the following Chinese passage sentence by sentence.
Only analyze the exact sentences that are in the passage.

Chinese passage:
{text}
"""

    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=prompt,
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
            response_schema=AnalyzeResponse,
        ),
    )

    if not response.text:
        raise RuntimeError("Gemini returned an empty response.")

    return AnalyzeResponse.model_validate_json(response.text)