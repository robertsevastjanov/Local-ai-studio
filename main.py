from fastapi import FastAPI
from pydantic import BaseModel, Field
from generator import create_image
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

app = FastAPI(title="Local AI Studio")
app.mount("/images", StaticFiles(directory="images"), name="images")
@app.get("/")
def home():
    return FileResponse("templates/index.html")

class GenerateRequest(BaseModel):
    prompt: str = Field(min_length=10, max_length=1000)
    steps: int = Field(default=8, ge=1, le=30)
    seed: int = Field(default=42, ge=0)

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/generate")
def generate_image(request: GenerateRequest):
    image_path = create_image(request.seed)
    
    return {
        "status": "completed",
        "prompt": request.prompt,
        "steps": request.steps,
        "seed": request.seed,
        "image_path": image_path
    }