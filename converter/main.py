import customtkinter
import tkinter
from tkinter import ttk
from tkinter import filedialog
import os
from converter import convertimage
from converter import png_to_vga_raw
import pygame
import numpy as np
import base64
import tempfile
from icon_base64 import ICON_BASE64
from palette import VGA_PALETTE

# Window dimensions for viewer
WIDTH, HEIGHT = 320, 200
SCALE = 2
WINDOW_WIDTH = WIDTH * SCALE
WINDOW_HEIGHT = HEIGHT * SCALE



# Create temporary icon file from Base64
def create_icon_file():
    try:
        # Decode Base64 data
        icon_data = base64.b64decode(ICON_BASE64)
        print("Base64 decoded successfully. Data length:", len(icon_data))
        
        # Create temporary file
        temp_file = tempfile.NamedTemporaryFile(suffix='.ico', delete=False)
        temp_file.write(icon_data)
        temp_file.close()
        print("Temporary file created at:", temp_file.name)
        return temp_file.name
    except base64.binascii.Error as e:
        print(f"Base64 decoding failed: {e}")
        return None
    except Exception as e:
        print(f"Error creating temporary file: {e}")
        return None

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
    """Convert multiple images to .raw format."""
    input_paths = open_png_multiple()
    if not input_paths:
        return
    
    for input_path in input_paths:
        # Suggest output filename based on input filename
        initial_file = os.path.splitext(os.path.basename(input_path))[0] + ".raw"
        save_path = getsavelocationRAW(initial_file)
        if save_path:  # Only convert if a save path was selected
            convertimage(input_path, save_path)

def open_png_multiple():
    """Open multiple image files."""
    filetypes = [("Image Files", "*.png *.jpg")]
    return filedialog.askopenfilenames(filetypes=filetypes)

def getsavelocationRAW(initial_file):
    """Get save location for a single .raw file."""
    filetypes = [("RAW Files", "*.raw")]
    return filedialog.asksaveasfilename(filetypes=filetypes, initialfile=initial_file)

import subprocess

def compile_binary():
    # Define file type filters
    filetypesraw = [("Raw image", "*.raw")]

    # Get raw image file
    rawimage = filedialog.askopenfilename(filetypes=filetypesraw)
    if not rawimage:
        print("No raw image file selected")
        exit(1)
    rawimage = os.path.normpath(rawimage)
    print(f"Selected raw image: {rawimage}")
    if not os.path.exists(rawimage):
        print(f"Error: Raw image file not found at {rawimage}")
        exit(1)

    # Ensure Loader.bin exists in the current directory
    loader_path = os.path.abspath("./Loader.bin")
    print(f"Loader path: {loader_path}")
    if not os.path.exists(loader_path):
        print(f"Error: Loader.bin not found at {loader_path}")
        return()

    # Use subprocess instead of os.system
    command = f'copy /b "{loader_path}"+"{rawimage}" "MemeOs.bin"'
    print(f"Executing: {command}")
    try:
        result = subprocess.run(command, shell=True, check=True, text=True, capture_output=True)
        print(result.stdout)
    except subprocess.CalledProcessError as e:
        print(e.stdout)
        print(f"Compilation failed with exit code {e.returncode}")
    else:
        print("MemeOs.bin compiled successfully")

def run_binary():
    filetypesbin = [("Compiled Binary", "*.bin")]

    binary = filedialog.askopenfilename(filetypes=filetypesbin)
    if not binary:
        print("No binary file selected")
        return

    import subprocess
    
    qemu_path = "C:\\Program Files\\qemu\\qemu-system-x86_64.exe"
    command = [qemu_path, "-drive", f"file={binary},format=raw", "-d", "int"]
    
    try:
        subprocess.run(command, check=True, shell=False)
    except subprocess.CalledProcessError as e:
        print(f"Could not run. Error {e.returncode}")
    except FileNotFoundError:
        print("Error: QEMU not found at specified path. Please ensure QEMU is installed at C:\\Program Files\\qemu\\")

# Create the main window
app = customtkinter.CTk()
app.title("Image Downgrader")
app.geometry("400x225")

# Set the window icon using the temporary file
icon_path = create_icon_file()
app.iconbitmap(icon_path)

# Configure grid and add buttons
app.grid_columnconfigure(0, weight=1)
button_convert = customtkinter.CTkButton(app, text="Convert Images", command=button_convert)
button_convert.grid(row=0, column=0, padx=20, pady=20, sticky="ew")

button_view = customtkinter.CTkButton(app, text="View RAW File", command=view_raw)
button_view.grid(row=1, column=0, padx=20, pady=10, sticky="ew")

button_view = customtkinter.CTkButton(app, text="Compile Image(s) + Source To Binary", command=compile_binary)
button_view.grid(row=2, column=0, padx=20, pady=10, sticky="ew")

button_view = customtkinter.CTkButton(app, text="Run Binary", command=run_binary)
button_view.grid(row=3, column=0, padx=20, pady=10, sticky="ew")

# Start the application
app.mainloop()

# Clean up temporary file after app closes
os.unlink(icon_path)