import customtkinter
import tkinter
from tkinter import ttk
from tkinter import filedialog
import os
from converter import convertimage
from converter import png_to_vga_raw
import pygame
import numpy as np

# VGA 256-color palette (needed for viewer)
VGA_PALETTE = [
    (0, 0, 0), (0, 0, 169), (0, 169, 0), (0, 169, 169),
    (169, 0, 0), (169, 0, 169), (169, 85, 0), (169, 169, 169),
    (85, 85, 85), (85, 85, 255), (85, 255, 85), (85, 255, 255),
    (255, 85, 85), (255, 85, 255), (255, 255, 85), (255, 255, 255),
] + [(r * 51, g * 51, b * 51) for r in range(6) for g in range(6) for b in range(6)] + [
    (i, i, i) for i in range(8, 248, 10)
]

# Window dimensions for viewer
WIDTH, HEIGHT = 320, 200
SCALE = 2
WINDOW_WIDTH = WIDTH * SCALE
WINDOW_HEIGHT = HEIGHT * SCALE

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
    
    indices = raw_data.reshape((height, width))
    indices = np.rot90(indices, k=1)
    indices = np.fliplr(indices)
    indices = np.rot90(indices, k=2)
    
    new_height, new_width = indices.shape
    rgb_array = np.zeros((new_height, new_width, 3), dtype=np.uint8)
    for y in range(new_height):
        for x in range(new_width):
            rgb_array[y, x] = VGA_PALETTE[indices[y, x]]
    
    surface = pygame.surfarray.make_surface(rgb_array)
    if SCALE > 1:
        surface = pygame.transform.scale(surface, (WINDOW_WIDTH, WINDOW_HEIGHT))
    return surface

def view_raw():
    """Open a .raw file in the viewer."""
    filetypes = [("RAW Files", "*.raw")]
    raw_file_path = filedialog.askopenfilename(filetypes=filetypes)
    if raw_file_path:
        pygame.init()
        screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("8bpp VGA Image Viewer")
        
        image_surface = load_raw_image(raw_file_path)
        
        running = True
        clock = pygame.time.Clock()
        
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    running = False
            
            screen.fill((50, 50, 50))
            if image_surface:
                screen.blit(image_surface, (0, 0))
            else:
                font = pygame.font.SysFont(None, 36)
                text = font.render("Failed to load image. Check console.", True, (255, 0, 0))
                screen.blit(text, (10, WINDOW_HEIGHT // 2 - 18))
            
            pygame.display.flip()
            clock.tick(60)
        
        pygame.quit()

def button_convert():
    convertimage(open_png(), getsavelocationRAW())

def open_png():
    filetypes = [("Image Files", "*.png *.jpg")]
    return filedialog.askopenfilename(filetypes=filetypes)

def getsavelocationRAW():
    filetypes = [("RAW Files", "*.raw")]
    return filedialog.asksaveasfilename(filetypes=filetypes)

# Create the main window
app = customtkinter.CTk()
app.title("Image Downgrader")
app.geometry("400x150")  # Increased height to accommodate second button

# Set the window icon
app.iconbitmap("converter/Icon.ico")

# Configure grid and add buttons
app.grid_columnconfigure(0, weight=1)
button_convert = customtkinter.CTkButton(app, text="Convert Image", command=button_convert)
button_convert.grid(row=0, column=0, padx=20, pady=20, sticky="ew")

button_view = customtkinter.CTkButton(app, text="View RAW File", command=view_raw)
button_view.grid(row=1, column=0, padx=20, pady=10, sticky="ew")

# Start the application
app.mainloop()