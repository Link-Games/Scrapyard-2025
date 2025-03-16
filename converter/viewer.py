import pygame
import numpy as np
import os
from tkinter import filedialog

# Initialize Pygame
pygame.init()

# VGA 256-color palette
VGA_PALETTE = [
(0, 0, 0), (0, 0, 169), (0, 169, 0), (0, 169, 169), (169, 0, 0), (169, 0, 169), (169, 85, 0), (169, 169, 169),
(85, 85, 85), (85, 85, 255), (85, 255, 85), (85, 255, 255), (255, 85, 85), (255, 85, 255), (255, 255, 85), (255, 255, 255),
(0, 0, 0), (16, 16, 16), (32, 32, 32), (48, 48, 48), (64, 64, 64), (80, 80, 80), (96, 96, 96), (112, 112, 112),
(128, 128, 128), (144, 144, 144), (160, 160, 160), (176, 176, 176), (192, 192, 192), (208, 208, 208), (224, 224, 224), (240, 240, 240),
(0, 0, 255), (0, 0, 239), (0, 0, 223), (0, 0, 207), (0, 0, 191), (0, 0, 175), (0, 0, 159), (0, 0, 143),
(0, 0, 127), (0, 0, 111), (0, 0, 95), (0, 0, 79), (0, 0, 63), (0, 0, 47), (0, 0, 31), (0, 0, 15),
(0, 255, 0), (0, 239, 0), (0, 223, 0), (0, 207, 0), (0, 191, 0), (0, 175, 0), (0, 159, 0), (0, 143, 0),
(0, 127, 0), (0, 111, 0), (0, 95, 0), (0, 79, 0), (0, 63, 0), (0, 47, 0), (0, 31, 0), (0, 15, 0),
(255, 0, 0), (239, 0, 0), (223, 0, 0), (207, 0, 0), (191, 0, 0), (175, 0, 0), (159, 0, 0), (143, 0, 0),
(127, 0, 0), (111, 0, 0), (95, 0, 0), (79, 0, 0), (63, 0, 0), (47, 0, 0), (31, 0, 0), (15, 0, 0),
(255, 255, 0), (239, 239, 0), (223, 223, 0), (207, 207, 0), (191, 191, 0), (175, 175, 0), (159, 159, 0), (143, 143, 0),
(127, 127, 0), (111, 111, 0), (95, 95, 0), (79, 79, 0), (63, 63, 0), (47, 47, 0), (31, 31, 0), (15, 15, 0),
(0, 255, 255), (0, 239, 239), (0, 223, 223), (0, 207, 207), (0, 191, 191), (0, 175, 175), (0, 159, 159), (0, 143, 143),
(0, 127, 127), (0, 111, 111), (0, 95, 95), (0, 79, 79), (0, 63, 63), (0, 47, 47), (0, 31, 31), (0, 15, 15),
(255, 0, 255), (239, 0, 239), (223, 0, 223), (207, 0, 207), (191, 0, 191), (175, 0, 175), (159, 0, 159), (143, 0, 143),
(127, 0, 127), (111, 0, 111), (95, 0, 95), (79, 0, 79), (63, 0, 63), (47, 0, 47), (31, 0, 31), (15, 0, 15),
(127, 63, 0), (127, 79, 15), (127, 95, 31), (127, 111, 47), (127, 127, 63), (127, 143, 79), (127, 159, 95), (127, 175, 111),
(127, 191, 127), (127, 207, 143), (127, 223, 159), (127, 239, 175), (127, 255, 191), (143, 255, 207), (159, 255, 223), (175, 255, 239),
(63, 127, 0), (79, 127, 15), (95, 127, 31), (111, 127, 47), (127, 127, 63), (143, 127, 79), (159, 127, 95), (175, 127, 111),
(191, 127, 127), (207, 127, 143), (223, 127, 159), (239, 127, 175), (255, 127, 191), (255, 143, 207), (255, 159, 223), (255, 175, 239),
(0, 127, 63), (15, 127, 79), (31, 127, 95), (47, 127, 111), (63, 127, 127), (79, 127, 143), (95, 127, 159), (111, 127, 175),
(127, 127, 191), (143, 127, 207), (159, 127, 223), (175, 127, 239), (191, 127, 255), (207, 143, 255), (223, 159, 255), (239, 175, 255),
(0, 63, 127), (15, 79, 127), (31, 95, 127), (47, 111, 127), (63, 127, 127), (79, 143, 127), (95, 159, 127), (111, 175, 127),
(127, 191, 127), (143, 207, 127), (159, 223, 127), (175, 239, 127), (191, 255, 127), (207, 255, 143), (223, 255, 159), (239, 255, 175),
(63, 0, 127), (79, 15, 127), (95, 31, 127), (111, 47, 127), (127, 63, 127), (143, 79, 127), (159, 95, 127), (175, 111, 127),
(191, 127, 127), (207, 143, 127), (223, 159, 127), (239, 175, 127), (255, 191, 127), (255, 207, 143), (255, 223, 159), (255, 239, 175),
(127, 0, 63), (127, 15, 79), (127, 31, 95), (127, 47, 111), (127, 63, 127), (127, 79, 143), (127, 95, 159), (127, 111, 175),
(127, 127, 191), (127, 143, 207), (127, 159, 223), (127, 175, 239), (127, 191, 255), (143, 207, 255), (159, 223, 255), (175, 239, 255),
(191, 191, 191), (195, 195, 195), (199, 199, 199), (203, 203, 203), (207, 207, 207), (211, 211, 211), (215, 215, 215), (219, 219, 219),
(223, 223, 223), (227, 227, 227), (231, 231, 231), (235, 235, 235), (239, 239, 239), (243, 243, 243), (247, 247, 247), (251, 251, 251),
(255, 255, 255), (255, 251, 255), (255, 247, 255), (255, 243, 255), (255, 239, 255), (255, 235, 255), (255, 231, 255), (255, 227, 255),
(255, 223, 255), (255, 219, 255), (255, 215, 255), (255, 211, 255), (255, 207, 255), (255, 203, 255), (255, 199, 255), (255, 195, 255)
]

# Window dimensions
WIDTH, HEIGHT = 320, 200
SCALE = 2
WINDOW_WIDTH = WIDTH * SCALE
WINDOW_HEIGHT = HEIGHT * SCALE

# Set up the display
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("8bpp VGA Image Viewer")

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
    
    pygame.quit()

# Call the function
filetypes = [("RAW Files", "*.raw")]
raw_file_path = filedialog.askopenfilename(filetypes=filetypes)
print(f"Loading: {os.path.abspath(raw_file_path)}")
main(raw_file_path)