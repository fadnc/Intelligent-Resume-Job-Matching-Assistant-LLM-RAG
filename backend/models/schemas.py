from pydantic import BaseModel
from typing import List

class AnalyzeResponse(BaseModel):
    score: int
    missing_skills : List[str]
    suggestions : List[str]
    rewritten_bullets : List[str]
    