from PIL import Image

def create_image():
    image = Image.new("RGB", (512, 512), color="pink")
    image.save("images/generated.png")
    return "images/generated.png"