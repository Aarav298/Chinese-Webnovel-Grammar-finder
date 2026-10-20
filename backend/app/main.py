from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from starlette.concurrency import run_in_threadpool
from app.models.analysis import AnalyzeRequest, AnalyzeResponse, AnalyzeUrlRequest
from app.services.gemini_service import generate_analysis, AnalysisUnavailableError
from app.services.extraction_service import extract_chapter_text, ChapterExtractionError, UnsupportedChapterUrlError

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
    try:
        return generate_analysis(request.text)
    except AnalysisUnavailableError:
        raise HTTPException(
            status_code=503,
            detail="Analysis service is temporarily unavailable"
        )

@app.post("/analyze-url", response_model=AnalyzeResponse)
async def analyze_url(request: AnalyzeUrlRequest):
    try:
        text = await extract_chapter_text(str(request.url))
        return await run_in_threadpool(generate_analysis, text)
    
    except UnsupportedChapterUrlError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc)
        )

    except ChapterExtractionError as exc:
        raise HTTPException(
            status_code=502,
            detail=str(exc)
        )

    except AnalysisUnavailableError:
        raise HTTPException(
            status_code=503,
            detail="Analysis service is temporarily unavailable"
        )