from PIL import Image

def convertimage(filepath, savepath):
    # Open the image
    image = Image.open(filepath)

    # Convert the image to RGB mode if it’s not already
    image = image.convert("RGB")

    # Resize the image to 320x200 pixels
    resized_image = image.resize((320, 200), Image.Resampling.LANCZOS)

    # Reduce the image to 16 colors (outputs in "P" mode)
    quantized_image = resized_image.quantize(colors=256, method=Image.Quantize.MEDIANCUT)

    # Save the result as BMP
    quantized_image.save(savepath)