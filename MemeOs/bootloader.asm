bits 16
org 0x7c00

mov [ BOOT_DRIVE ], dl ; BIOS stores our boot drive in dl

jmp $    

readdisk:
    pusha
    mov ah, 0x02
    mov al, 128
    mov ch, 0
    mov dh, 0 
    mov cl, SECT_TO_READ
    mov bx, ADD_TO_WRITE
    mov dl, [ BOOT_DRIVE ]
    int 0x13
    add SECT_TO_READ, 128
    add ADD_TO_WRITE, 0x10000
    popa
    ret

BOOT_DRIVE: db 0
SECT_TO_READ: db 2
ADD_TO_WRITE: db 0x7e00
TEST_MESSAGE: db 'Hello World', 13, 10, 0
