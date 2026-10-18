from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.models.analysis import AnalyzeRequest, AnalyzeResponse

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
    return {"analyses" : [{
        "sentence": request.text,
        "pattern": "pattern works",
        "hsk_level": 3,
        "explanation": "explanation works"
    }]}