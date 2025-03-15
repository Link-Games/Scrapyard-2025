import customtkinter
from tkinter import ttk
from tkinter import filedialog
import tkinter
from converter import convertimage

popup = None
textbox = None

def button_addimage():
    global popup, textbox
    if popup is None or not popup.winfo_exists():
        popup = customtkinter.CTkToplevel(app)
        popup.title("Text Input")
        popup.geometry("300x250")
        popup.attributes('-topmost', True)
        
        screen_width = app.winfo_screenwidth()
        popup_width = 300
        popup_x = (screen_width - popup_width) // 2
        popup_y = 20
        popup.geometry(f"300x250+{popup_x}+{popup_y}")
        
        textbox = customtkinter.CTkTextbox(popup, width=250, height=150)
        textbox.pack(padx=20, pady=(20, 10))
        
        done_button = customtkinter.CTkButton(popup, text="Done", command=lambda: on_popup_close_with_text())
        done_button.pack(pady=10)
        
        popup.protocol("WM_DELETE_WINDOW", lambda: on_popup_close_with_text())
        print("button Add Image pressed")
    else:
        print("Popup already exists")

def on_popup_close_with_text():
    global popup, textbox
    if popup is not None and textbox is not None:
        # Print the textbox content before closing
        text_content = textbox.get("1.0", "end").strip()
        imagelocationsfile = open("converter/Files.meme", "w")
        imagelocationsfile.write(text_content)
        imagelocationsfile.close()
        print("Textbox content:", text_content)
        popup.destroy()
        popup = None
        textbox = text_content

def button_convert():
    convertimage(open_file(), getsavelocation())

def open_file():
    filetypes = [("Image Files", "*.png *.jpg")]
    return filedialog.askopenfilename(filetypes = filetypes)

def getsavelocation():
    filetypes = [("Bitmap File", "*.bmp")]
    return filedialog.asksaveasfilename(filetypes = filetypes)

app = customtkinter.CTk()
app.title("Image Downgrader")
app.geometry("400x100")

app.grid_columnconfigure(0, weight=1)
button = customtkinter.CTkButton(app, text="Convert Image", command=button_convert)
button.grid(row=0, column=0, padx=20, pady=20, sticky="ew")

app.mainloop()