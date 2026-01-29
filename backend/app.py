from fastapi import FastAPI
from backend.routes.analyze import router as analyze_router
from backend.routes.health import router as health_router
from fastapi import APIRouter

app = FastAPI(title="Resume LLM Assistant")
router = APIRouter()

@router.get("/")
def show():
    return {"message": "API is running"}

@app.get("/")
def root():
    return {"message": "Welcome to the Resume LLM Assistant API"}

app.include_router(analyze_router)
app.include_router(health_router)