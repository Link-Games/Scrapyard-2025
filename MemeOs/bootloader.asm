bits 16
org 0x7c00

mov [ BOOT_DRIVE ], dl ; BIOS stores our boot drive in dl
mov ah,0x0
mov al,0x13
int 0x10
jmp $

readdisk:
    pusha
    mov ah, 0x02
    mov al, 128
    mov ch, CYL_TO_READ
    mov dh, 0 
    mov cl, 0
    mov bx, 0x1000
    mov ds, bx
    mov dl, [ BOOT_DRIVE ]
    int 0x13
    mov ax,0x0000
    mov ds, ax
    inc ch
    popa
    ret

BOOT_DRIVE: db 0
CYL_TO_READ: db 1

times 510 - ($-$$) db 0
dw 0xAA55