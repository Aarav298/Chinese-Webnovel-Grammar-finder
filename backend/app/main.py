from fastapi import FastAPI
from pydantic import BaseModel, Field, StringConstraints
from typing import Annotated
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get('/health')
def health():
    return {'status':'OK'}

class AnalyzeRequest(BaseModel):
    text: Annotated[str, StringConstraints(pattern=r".*\S.*")]

class SentenceAnalysis(BaseModel):
    sentence: str
    pattern: str
    hsk_level: int = Field(ge=1, le=6)
    explanation: str

class AnalyzeResponse(BaseModel):
    analyses: list[SentenceAnalysis]

@app.post("/analyze", response_model= AnalyzeResponse)
def analyze(request: AnalyzeRequest):
    return {"analyses" : [{
        "sentence": request.text,
        "pattern": "pattern works",
        "hsk_level": 3,
        "explanation": "explanation works"
    }]}