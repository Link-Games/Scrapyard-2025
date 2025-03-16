import pygame
import numpy as np
import os
from tkinter import filedialog
from main import create_icon_file, ICON_BASE64  # Assuming these are defined in main.py

# Initialize Pygame
pygame.init()

# VGA 256-color palette
VGA_PALETTE = [
    (0, 0, 0), (0, 2, 170), (20, 170, 0), (0, 170, 170), (170, 0, 3), (170, 0, 170), (170, 85, 0), (170, 170, 170),
    (85, 85, 85), (85, 85, 255), (85, 255, 85), (85, 255, 255), (255, 85, 85), (253, 85, 255), (255, 255, 85), (255, 255, 255),
    (0, 0, 0), (16, 16, 16), (32, 32, 32), (53, 53, 53), (69, 69, 69), (85, 85, 85), (101, 101, 101), (117, 117, 117),
    (138, 138, 138), (154, 154, 154), (170, 170, 170), (186, 186, 186), (202, 202, 202), (223, 223, 223), (239, 239, 239), (255, 255, 255),
    (0, 4, 255), (65, 4, 255), (130, 3, 255), (190, 2, 255), (253, 0, 255), (254, 0, 190), (255, 0, 130), (255, 0, 65),
    (255, 0, 8), (255, 65, 5), (255, 130, 0), (255, 190, 0), (255, 255, 0), (190, 255, 0), (130, 255, 0), (65, 255, 1),
    (36, 255, 0), (34, 255, 66), (29, 255, 130), (18, 255, 190), (0, 255, 255), (0, 190, 255), (1, 130, 255), (0, 65, 255),
    (130, 130, 255), (158, 130, 255), (190, 130, 255), (223, 130, 255), (253, 130, 255), (254, 130, 223), (255, 130, 190), (255, 130, 158),
    (255, 130, 130), (255, 158, 130), (255, 190, 130), (255, 223, 130), (255, 255, 130), (223, 255, 130), (190, 255, 130), (158, 255, 130),
    (130, 255, 130), (130, 255, 158), (130, 255, 190), (130, 255, 223), (130, 255, 255), (130, 223, 255), (130, 190, 255), (130, 158, 255),
    (186, 186, 255), (202, 186, 255), (223, 186, 255), (239, 186, 255), (254, 186, 255), (254, 186, 239), (255, 186, 223), (255, 186, 202),
    (255, 186, 186), (255, 202, 186), (255, 223, 186), (255, 239, 186), (255, 255, 186), (239, 255, 186), (223, 255, 186), (202, 255, 187),
    (186, 255, 186), (186, 255, 202), (186, 255, 223), (186, 255, 239), (186, 255, 255), (186, 239, 255), (186, 223, 255), (186, 202, 255),
    (1, 1, 113), (28, 1, 113), (57, 1, 113), (85, 0, 113), (113, 0, 113), (113, 0, 85), (113, 0, 57), (113, 0, 28),
    (113, 0, 1), (113, 28, 1), (113, 57, 0), (113, 85, 0), (113, 113, 0), (85, 113, 0), (57, 113, 0), (28, 113, 0),
    (9, 113, 0), (9, 113, 28), (6, 113, 57), (3, 113, 85), (0, 113, 113), (0, 85, 113), (0, 57, 113), (0, 28, 113),
    (57, 57, 113), (69, 57, 113), (85, 57, 113), (97, 57, 113), (113, 57, 113), (113, 57, 97), (113, 57, 85), (113, 57, 69),
    (113, 57, 57), (113, 69, 57), (113, 85, 57), (113, 97, 57), (113, 113, 57), (97, 113, 57), (85, 113, 57), (69, 113, 58),
    (57, 113, 57), (57, 113, 69), (57, 113, 85), (57, 113, 97), (57, 113, 113), (57, 97, 113), (57, 85, 113), (57, 69, 114),
    (81, 81, 113), (89, 81, 113), (97, 81, 113), (105, 81, 113), (113, 81, 113), (113, 81, 105), (113, 81, 97), (113, 81, 89),
    (113, 81, 81), (113, 89, 81), (113, 97, 81), (113, 105, 81), (113, 113, 81), (105, 113, 81), (97, 113, 81), (89, 113, 81),
    (81, 113, 81), (81, 113, 90), (81, 113, 97), (81, 113, 105), (81, 113, 113), (81, 105, 113), (81, 97, 113), (81, 89, 113),
    (0, 0, 66), (17, 0, 65), (32, 0, 65), (49, 0, 65), (65, 0, 65), (65, 0, 50), (65, 0, 32), (65, 0, 16),
    (65, 0, 0), (65, 16, 0), (65, 32, 0), (65, 49, 0), (65, 65, 0), (49, 65, 0), (32, 65, 0), (16, 65, 0),
    (3, 65, 0), (3, 65, 16), (2, 65, 32), (1, 65, 49), (0, 65, 65), (0, 49, 65), (0, 32, 65), (0, 16, 65),
    (32, 32, 65), (40, 32, 65), (49, 32, 65), (57, 32, 65), (65, 32, 65), (65, 32, 57), (65, 32, 49), (65, 32, 40),
    (65, 32, 32), (65, 40, 32), (65, 49, 32), (65, 57, 33), (65, 65, 32), (57, 65, 32), (49, 65, 32), (40, 65, 32),
    (32, 65, 32), (32, 65, 40), (32, 65, 49), (32, 65, 57), (32, 65, 65), (32, 57, 65), (32, 49, 65), (32, 40, 65),
    (45, 45, 65), (49, 45, 65), (53, 45, 65), (61, 45, 65), (65, 45, 65), (65, 45, 61), (65, 45, 53), (65, 45, 49),
    (65, 45, 45), (65, 49, 45), (65, 53, 45), (65, 61, 45), (65, 65, 45), (61, 65, 45), (53, 65, 45), (49, 65, 45),
    (45, 65, 45), (45, 65, 49), (45, 65, 53), (45, 65, 61), (45, 65, 65), (45, 61, 65), (45, 53, 65), (45, 49, 65),
    (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0)
]

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