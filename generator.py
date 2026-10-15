import os
from pathlib import Path
from uuid import uuid4

MODEL_ID = "stable-diffusion-v1-5/stable-diffusion-v1-5"

pipeline = None

def get_pipeline():
    global pipeline

    if pipeline is None:
        import torch
        from diffusers import StableDiffusionPipeline
        
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
    Path("images").mkdir(parents=True, exist_ok=True)
    image_path = f"images/generated_{seed}_{uuid4().hex}.png"

    if os.getenv("CI_MOCK_GENERATION") == "1":
        from PIL import Image

        image = Image.new("RGB", (512, 512), (90, 45, 145))
        image.save(image_path)
        return image_path

    import torch

    pipe = get_pipeline()

    generator = torch.Generator(device="cpu").manual_seed(seed)
    image = pipe(
        prompt=prompt,
        num_inference_steps=steps,
        generator=generator,
        height=512,
        width=512,
    ).images[0]
    
    image.save(image_path)
    
    return image_path