from PIL import Image
from tkinter import filedialog
import numpy as np
import os

# Full VGA 256-color palette (RGB values)
VGA_PALETTE = [
    # 0-15: Basic VGA colors
    (0, 0, 0),    (0, 0, 169),  (0, 169, 0),  (0, 169, 169),
    (169, 0, 0),  (169, 0, 169), (169, 85, 0), (169, 169, 169),
    (85, 85, 85), (85, 85, 255), (85, 255, 85), (85, 255, 255),
    (255, 85, 85), (255, 85, 255), (255, 255, 85), (255, 255, 255),
] + [
    # 16-231: 6x6x6 RGB cube (6 levels: 0, 51, 102, 153, 204, 255)
    (r * 51, g * 51, b * 51)
    for r in range(6)
    for g in range(6)
    for b in range(6)
] + [
    # 232-255: Grayscale ramp (24 steps from 8 to 238)
    (i, i, i)
    for i in range(8, 248, 10)  # Steps of ~10: 8, 18, 28, ..., 238
]

# Verify palette size
assert len(VGA_PALETTE) == 256, f"Palette size is {len(VGA_PALETTE)}, expected 256"

def convertimage(filepath, savepath):
    # Open the image
    image = Image.open(filepath)

    # Convert the image to RGB mode if it’s not already
    image = image.convert("RGB")

    # Resize the image to 320x200 pixels
    resized_image = image.resize((320, 200), Image.Resampling.LANCZOS)

    # Reduce the image to 16 colors (outputs in "P" mode)
    quantized_image = resized_image.quantize(colors=256, method=Image.Quantize.MEDIANCUT)

    quantized_image.save("temp.bmp")
    png_to_vga_raw("temp.bmp", savepath)

def png_to_vga_raw(input_path, output_path):
    if not output_path.lower().endswith(".raw"):
        output_path += ".raw"

    img = Image.open(input_path).convert("RGB")
    img = img.resize((320, 200), Image.NEAREST)
    img_array = np.array(img, dtype=np.uint8)
    
    # Reshape to (320*200, 3) for vectorized computation
    pixels = img_array.reshape(-1, 3).astype(np.float32)  # Cast to float32
    vga_array = np.array(VGA_PALETTE, dtype=np.float32)
    
    # Compute squared differences for all pixels and palette colors at once
    diff = pixels[:, np.newaxis, :] - vga_array[np.newaxis, :, :]
    dists = np.sum(diff ** 2, axis=2)  # Sum along RGB axis
    raw_data = np.argmin(dists, axis=1).reshape(200, 320).astype(np.uint8)
    
    with open(output_path, 'wb') as f:
        f.write(raw_data.tobytes())
    
    os.remove("temp.bmp") 
    
    print(f"Converted {input_path} to {output_path}")