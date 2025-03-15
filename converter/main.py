from PIL import Image

images = ["MOUGGER", "What She Sees VS What I See"]
i = 0
while i < len(images):
    # Open the image
    image = Image.open("converter/input/" + images[i] + ".png")

    # Convert the image to RGB mode if it’s not already
    image = image.convert("RGB")

    # Resize the image to 320x200 pixels
    resized_image = image.resize((320, 200), Image.Resampling.LANCZOS)

    # Reduce the image to 256 colors (outputs in "P" mode)
    quantized_image = resized_image.quantize(colors=256, method=Image.Quantize.MEDIANCUT)

    # Save the result as PNG
    quantized_image.save("converter/output/" + images[i] + ".bmp", optimize=True)
    i+=1