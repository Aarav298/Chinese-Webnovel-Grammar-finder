from pathlib import Path
from dotenv import load_dotenv

load_dotenv(Path("backend/.env"))

from backend.app.services.gemini_service import generate_analysis

result = generate_analysis(
    "虽然今天下雨，但是我还是去学校了。"
)

print(result.model_dump_json(indent=2))