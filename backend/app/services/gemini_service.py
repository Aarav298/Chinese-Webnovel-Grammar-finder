import os
from google import genai
from google.genai import types
from google.genai import errors
from ..models.analysis import AnalyzeResponse
from dotenv import load_dotenv
from pathlib import Path

class AnalysisUnavailableError(Exception):
    """Raised when the analysis service is temporarily unavailable."""
    pass

load_dotenv(Path(__file__).resolve().parents[2]/".env")

client = genai.Client(
    api_key = os.environ["GEMINI_API_KEY"]
)

def generate_analysis(text: str) -> AnalyzeResponse:
    prompt = f"""
You are a Chinese language tutor. Analyze the following Chinese passage sentence by sentence.
Only analyze the exact sentences that are in the passage.

Follow these instructions:
- Analyze the passage sentence by sentence.
- Return exactly one analysis for each sentence.
- Select the single most educationally useful grammar pattern in that sentence.
- Prefer meaningful grammatical constructions over trivial observations.
- Preserve each original Chinese sentence.
- Estimate the grammar point's HSK level from 1 to 6.
- Give a concise explanation of its meaning and usage.
- Do not return multiple analyses for the same sentence.

Chinese passage:
{text}
"""
    try:
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
    except errors.ServerError as e:
        if e.code == 503:
            raise AnalysisUnavailableError() from e
        raise