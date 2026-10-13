from PIL import Image
from uuid import uuid4

def create_image(seed):
    image = Image.new("RGB", (512, 512), color="pink")
    
    unique_id = uuid4().hex
    
    image_path = f"images/generated_{seed}_{unique_id}.png"
    
    image.save(image_path)
    
    return image_path