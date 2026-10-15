from pathlib import Path
from uuid import uuid4

import torch
from diffusers import StableDiffusionPipeline

MODEL_ID = "stable-diffusion-v1-5/stable-diffusion-v1-5"

pipeline = None

def get_pipeline():
    global pipeline

    if pipeline is None:
        pipeline = StableDiffusionPipeline.from_pretrained(
            MODEL_ID,
            dtype=torch.float16,
            use_safetensors=True,
            local_files_only=True,
        )
        pipeline = pipeline.to("mps")
        pipeline.enable_attention_slicing()

    return pipeline

def create_image(seed, prompt, steps=10):
    pipe = get_pipeline()

    generator = torch.Generator(device="cpu").manual_seed(seed)
    image = pipe(
        prompt=prompt,
        num_inference_steps=steps,
        generator=generator,
        height=512,
        width=512,
    ).images[0]

    Path("images").mkdir(parents=True, exist_ok=True)
    
    image_path = f"images/generated_{seed}_{uuid4().hex}.png"
    
    image.save(image_path)
    
    return image_path