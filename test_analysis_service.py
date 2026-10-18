from pathlib import Path
from dotenv import load_dotenv

load_dotenv(Path("backend/.env"))

from backend.app.services.gemini_service import generate_analysis

result = generate_analysis(
    "许多外国人发现，中国人非常喜欢喝热水。无论是在家里、办公室，还是在餐厅，人们总是拿着一个保温杯。在中医看来，喝热水对身体很好，可以帮助消化和促进血液循环。尤其是在感冒或者生病的时候，多喝热水是最好的照顾自己的方式。"
)

print(result.model_dump_json(indent=2))