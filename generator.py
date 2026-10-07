from PIL import Image

def create_image(seed):
    image = Image.new("RGB", (512, 512), color="pink")
    image_path = f"images/generated_{seed}.png"
    image.save(image_path)
    return image_path