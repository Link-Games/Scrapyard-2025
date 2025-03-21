import pygame
import numpy as np
import os
from tkinter import filedialog
from palette import VGA_PALETTE
from main import create_icon_file
from icon_base64 import ICON_BASE64

# Initialize Pygame
pygame.init()

# Window dimensions
WIDTH, HEIGHT = 320, 200
SCALE = 2
WINDOW_WIDTH = WIDTH * SCALE
WINDOW_HEIGHT = HEIGHT * SCALE

# Set up the display
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("8bpp VGA Image Viewer")

# Load and set the icon with debugging
icon_path = create_icon_file()
if icon_path:
    print("Attempting to load icon from:", icon_path)
    try:
        if not os.path.exists(icon_path):
            print("File does not exist at:", icon_path)
            raise FileNotFoundError("Temporary file missing")
        print("File size on disk:", os.path.getsize(icon_path), "bytes")
        icon = pygame.image.load(icon_path)
        print("Icon loaded successfully. Surface size:", icon.get_size())
        pygame.display.set_icon(icon)
        print("Icon set successfully")
    except pygame.error as e:
        print(f"Pygame error loading icon: {e}")
    except Exception as e:
        print(f"Unexpected error loading icon: {e}")
else:
    print("No icon path returned; skipping icon loading")

def load_raw_image(filepath, width=320, height=200):
    """Load a 320x200 8bpp raw image and convert to RGB using VGA palette."""
    if not os.path.exists(filepath):
        print(f"Error: File not found: {filepath}")
        return None
    
    with open(filepath, 'rb') as f:
        raw_data = np.fromfile(f, dtype=np.uint8)
    
    expected_size = width * height
    if len(raw_data) != expected_size:
        print(f"Error: File size ({len(raw_data)}) does not match {width}x{height} ({expected_size} bytes)")
        return None
    
    # Reshape to 2D array (height, width)
    indices = raw_data.reshape((height, width))
    
    # Correct orientation:
    # 1. Original: Rotate 90 degrees counterclockwise
    indices = np.rot90(indices, k=1)  # k=1 means 90° counterclockwise
    # 2. Original: Flip horizontally
    indices = np.fliplr(indices)
    # 3. New: Rotate 180 degrees
    indices = np.rot90(indices, k=2)  # k=2 means 180° rotation
    
    # After transformations, dimensions are swapped: (height, width) becomes (width, height)
    new_height, new_width = indices.shape  # Should still be (320, 200)
    
    # Create RGB surface array with new dimensions
    rgb_array = np.zeros((new_height, new_width, 3), dtype=np.uint8)
    for y in range(new_height):
        for x in range(new_width):
            rgb_array[y, x] = VGA_PALETTE[indices[y, x]]
    
    # Convert to Pygame surface
    surface = pygame.surfarray.make_surface(rgb_array)
    if SCALE > 1:
        surface = pygame.transform.scale(surface, (WINDOW_WIDTH, WINDOW_HEIGHT))
    return surface

def main(raw_filepath):
    """Display the raw image in a Pygame window."""
    image_surface = load_raw_image(raw_filepath)
    
    running = True
    clock = pygame.time.Clock()
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                running = False
        
        screen.fill((50, 50, 50))  # Dark gray background
        if image_surface:
            screen.blit(image_surface, (0, 0))
        else:
            font = pygame.font.SysFont(None, 36)
            text = font.render("Failed to load image. Check console.", True, (255, 0, 0))
            screen.blit(text, (10, WINDOW_HEIGHT // 2 - 18))
        
        pygame.display.flip()
        clock.tick(60)
    
    # Clean up the temporary icon file before quitting
    if icon_path and os.path.exists(icon_path):
        os.unlink(icon_path)
        print("Temporary file deleted:", icon_path)
    
    pygame.quit()

# Call the function
filetypes = [("RAW Files", "*.raw")]
raw_file_path = filedialog.askopenfilename(filetypes=filetypes)
print(f"Loading: {os.path.abspath(raw_file_path)}")
main(raw_file_path)