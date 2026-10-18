from pydantic import BaseModel, Field, StringConstraints
from typing import Annotated

class AnalyzeRequest(BaseModel):
    text: Annotated[str, StringConstraints(pattern=r".*\S.*")]

class SentenceAnalysis(BaseModel):
    sentence: str = Field(description="The original sentence")
    pattern: str = Field(description="The grammatical pattern in the sentence")
    hsk_level: int = Field(ge=1, le=6, description="Approximate hsk level of the grammar point")
    explanation: str = Field(description="A concise explanation in english of the grammar pattern")

class AnalyzeResponse(BaseModel):
    analyses: list[SentenceAnalysis] = Field(description="A list of all the sentences and the grammar points in them")