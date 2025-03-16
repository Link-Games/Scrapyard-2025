import customtkinter
import tkinter
from tkinter import ttk
from tkinter import filedialog
import os
from converter import convertimage, png_to_vga_raw 
import pygame
import numpy as np
import base64
import tempfile
from icon_base64 import ICON_BASE64
from palette import VGA_PALETTE
import subprocess
from PIL import Image, ImageTk

# Window dimensions for viewer
WIDTH, HEIGHT = 320, 200
SCALE = 2
WINDOW_WIDTH = WIDTH * SCALE
WINDOW_HEIGHT = HEIGHT * SCALE

class PopupDialog:
    def __init__(self, parent, title, message, width=500, height=150):
        self.top = tkinter.Toplevel(parent)
        self.top.title(title)
        self.top.transient(parent)
        self.top.grab_set()
        
        # Create a main frame to hold all content
        main_frame = ttk.Frame(self.top)
        main_frame.pack(expand=True, fill='both')

        #Logo
        logo_path = create_icon_file()
        if logo_path:
            icon = Image.open(logo_path)
            photo = ImageTk.PhotoImage(icon)
            self.top.wm_iconphoto(True, photo)
        
        # Message label
        msg = ttk.Label(main_frame, text=message, wraplength=width-40, justify="center", font=("Arial", 10))
        msg.pack(padx=20, pady=10, expand=True)
        
        # Button frame at bottom
        btn_frame = ttk.Frame(main_frame)
        btn_frame.pack(side='bottom', pady=10)
        ok_button = ttk.Button(btn_frame, text="OK", command=self.close)
        ok_button.pack()
        
        # Center the dialog relative to parent window
        parent_x = parent.winfo_x()
        parent_y = parent.winfo_y()
        parent_width = parent.winfo_width()
        parent_height = parent.winfo_height()
        x = parent_x + (parent_width - width) // 2
        y = parent_y + (parent_height - height) // 2
        self.top.geometry(f"{width}x{height}+{x}+{y}")
    
    def close(self):
        self.top.grab_release()
        self.top.destroy()

def create_icon_file():
    try:
        icon_data = base64.b64decode(ICON_BASE64)
        print("Base64 decoded successfully. Data length:", len(icon_data))
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
    return surface

def view_raw():
    filetypes = [("RAW Files", "*.raw")]
    raw_file_path = filedialog.askopenfilename(filetypes=filetypes)
    if raw_file_path:
        pygame.init()
        screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
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
                screen_width, screen_height = screen.get_size()
                scaled_image = pygame.transform.scale(image_surface, (screen_width, screen_height))
                screen.blit(scaled_image, (0, 0))
            else:
                font = pygame.font.SysFont(None, 36)
                text = font.render("Failed to load image. Check console.", True, (255, 0, 0))
                screen.blit(text, (10, screen_height // 2 - 18))
            pygame.display.flip()
            clock.tick(60)
        pygame.quit()

def button_convert():
    input_paths = open_png_multiple()
    if not input_paths:
        return
    for input_path in input_paths:
        initial_file = os.path.splitext(os.path.basename(input_path))[0] + ".raw"
        save_path = getsavelocationRAW(initial_file)
        if save_path:
            convertimage(input_path, save_path)

def open_png_multiple():
    filetypes = [("Image Files", "*.png *.jpg")]
    return filedialog.askopenfilenames(filetypes=filetypes)

def getsavelocationRAW(initial_file):
    filetypes = [("RAW Files", "*.raw")]
    return filedialog.asksaveasfilename(filetypes=filetypes, initialfile=initial_file)

def compile_binary():
    filetypesraw = [("Raw image", "*.raw")]
    rawimage = filedialog.askopenfilename(filetypes=filetypesraw)
    if not rawimage:
        print("No raw image file selected")
        return
    rawimage = os.path.normpath(rawimage)
    print(f"Selected raw image: {rawimage}")
    if not os.path.exists(rawimage):
        print(f"Error: Raw image file not found at {rawimage}")
        return
    loader_path = os.path.abspath("./Loader.bin")
    print(f"Loader path: {loader_path}")
    if not os.path.exists(loader_path):
        print(f"Error: Loader.bin not found at {loader_path}")
        PopupDialog(app, "Warning", f"Error: Loader.bin not found at {loader_path}")
        return
    command = [
        "powershell.exe", "-Command",
        f'Get-Content "{loader_path}", "{rawimage}" -Encoding Byte | Set-Content "MemeOs.img" -Encoding Byte'
    ]
    print(f"Executing: {' '.join(command)}")
    try:
        result = subprocess.run(command, check=True, text=True, capture_output=True)
        print(result.stdout)
        print("MemeOs.bin compiled successfully")
    except subprocess.CalledProcessError as e:
        print(f"Compilation failed with exit code {e.returncode}")
        print(f"Error output: {e.stderr}")
    except FileNotFoundError:
        print("Error: PowerShell not found. Ensure you're running on Windows with PowerShell installed.")

# Define run_binary as a standalone function
def run_binary(app):
    """Run a compiled binary in QEMU."""
    binary_path = os.path.abspath("./MemeOS.img")
    print(f"MemeOS path: {binary_path}")
    if not os.path.exists(binary_path):
        print(f"Error: MemeOS.img not found at {binary_path}")
        PopupDialog(app, "Warning", f"Error: MemeOS.bin not found at {binary_path}")
        return
    qemu_path = "C:\\Program Files\\qemu\\qemu-system-x86_64.exe"
    command = [qemu_path, "-drive", f"file={binary_path},format=raw"]
    try:
        subprocess.run(command, check=True, shell=False)
        print("Binary ran successfully in QEMU")
    except subprocess.CalledProcessError as e:
        print(f"Could not run. Error {e.returncode}")
    except FileNotFoundError:
        print("Error: QEMU not found at specified path. Ensure QEMU is installed at C:\\Program Files\\qemu\\")

# Create the main window
app = customtkinter.CTk()
app.title("Image Downgrader")
app.geometry("400x225")

# Set the window icon
icon_path = create_icon_file()
if icon_path:
    app.iconbitmap(icon_path)

# Configure grid and add buttons
app.grid_columnconfigure(0, weight=1)
button_convert = customtkinter.CTkButton(app, text="Convert Images", command=button_convert)
button_convert.grid(row=0, column=0, padx=20, pady=20, sticky="ew")

button_view = customtkinter.CTkButton(app, text="View RAW File", command=view_raw)
button_view.grid(row=1, column=0, padx=20, pady=10, sticky="ew")

button_compile = customtkinter.CTkButton(app, text="Compile Image + Source To Image", command=compile_binary)
button_compile.grid(row=2, column=0, padx=20, pady=10, sticky="ew")

button_run = customtkinter.CTkButton(app, text="Run MemeOS In QEMU", command=lambda: run_binary(app))
button_run.grid(row=3, column=0, padx=20, pady=10, sticky="ew")

# Start the application
app.mainloop()

# Clean up temporary file
if icon_path and os.path.exists(icon_path):
    os.unlink(icon_path)
    print("Temporary icon file deleted:", icon_path)