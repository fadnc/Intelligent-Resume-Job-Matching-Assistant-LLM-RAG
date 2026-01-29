from pydantic import BaseModel
from typing import List

class AnalyzeResponse(BaseModel):
    score: int
    missing_skills : List[str]
    sugestions : List[str]
    rewritten_bullets : List[str]
    