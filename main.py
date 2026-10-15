from fastapi import FastAPI
from pydantic import BaseModel, Field
from generator import create_image
from fastapi.staticfiles import StaticFiles
from database import init_db, save_generation_with_backup, get_postgres_generations
from pathlib import Path

app = FastAPI(title="Local AI Studio")
Path("images").mkdir(parents=True, exist_ok=True)
init_db()
app.mount("/images", StaticFiles(directory="images"), name="images")

class GenerateRequest(BaseModel):
    prompt: str = Field(min_length=10, max_length=1000)
    steps: int = Field(default=8, ge=1, le=30)
    seed: int = Field(default=42, ge=0)

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/generate")
def generate_image(request: GenerateRequest):
    image_path = create_image(
        seed=request.seed,
        prompt=request.prompt,
        steps=request.steps
    )
    save_generation_with_backup(
        prompt=request.prompt,
        steps=request.steps,
        seed=request.seed,
        image_path=image_path
    )
    
    return {
        "status": "completed",
        "prompt": request.prompt,
        "steps": request.steps,
        "seed": request.seed,
        "image_path": image_path
    }

@app.get("/history")
def get_history():
    generations = get_postgres_generations()

    return {
        "status": "ok",
        "count": len(generations),
        "generations": generations
    }