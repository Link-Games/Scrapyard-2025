![Untitled](https://github.com/user-attachments/assets/cb173c57-770d-465b-a3b5-d93a22ece17c)

# Scrapyard-2025<br>
This is an OS that makes your computer completely useless. All it does is show images (preferably memes) you downscaled to 320x200 @ 8bpp beforehand using the converter program.
## Converter
### Depencencies:<br>
#### Compile:<br>
Python 3.13.2:<br>
[Python Downloads](https://www.python.org/downloads/) <br>
CustomTKInter, python-resize-image, Pillow, numpy, pygame<br>
`pip install customtkinter python-resize-image Pillow numpy pygame`<br>
nasm 2.16.03<br>
[Nasm Downloads](https://www.nasm.us/pub/nasm/releasebuilds/2.16.03/)<br>
QEMU<br>
[QEMU Downloads](https://www.qemu.org/download/)<br>
#### Run: ([Video Tutorial](https://youtu.be/9WA77e_jNv0)) <br>
`python converter/main.py`<br>
Press "Convert Images" to convert .png's an .jpg's to a custom .raw format.<br>
Press "Compile Image + Source To Binary" and choose a .raw file to include with it. It will give you MemOS.img This file is the image that you would put on the OS or run in the emulator.<br>
Optional: Press "Run MemeOS In QEMU" to run MemeOS in an emulator with your newly compiled .img file.<br>
## Run On Real Hardware
Take MemeOS.img and burn it to a USB using [Rufus](https://rufus.ie/en/)<br>
1. Choose your device
2. Press the "Select" button and choose MemeOS.img (it is where you downloaded MemeOS)
3. Press "Start". WARNING!!! IT WILL ERASE YOUR DRIVE!!!!
4. Reboot your computer and get in the BIOS.
5. Turn on legacy boot
6. Change boot order to boot off the USB.
7. Save and exit BIOS.
8. When you are done, make sure to turn UEFI boot back on.

# Credits  
Benjamin Zdunich  
Justin Wendt
