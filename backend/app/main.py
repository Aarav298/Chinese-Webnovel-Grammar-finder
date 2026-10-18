from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.models.analysis import AnalyzeRequest, AnalyzeResponse
from app.services.gemini_service import generate_analysis

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

@app.post("/analyze", response_model= AnalyzeResponse)
def analyze(request: AnalyzeRequest):
    return generate_analysis(request.text)