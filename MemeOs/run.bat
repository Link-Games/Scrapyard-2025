nasm -f bin ./bootloader.asm -o Loader.bin
copy /b Loader.bin+"Gooderness.raw" MemeOs.bin
"C:\Program Files\qemu\qemu-system-x86_64.exe" -drive file=MemeOs.bin,format=raw 