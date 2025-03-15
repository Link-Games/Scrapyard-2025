bits 16
org 0x7c00

mov [ BOOT_DRIVE ], dl ; BIOS stores our boot drive in dl
mov al, 'k'
mov ah, 0x0e
int 0x10
call readdisk
jmp $

readdisk:
    pusha
    mov ah, 0x02
    mov al, 128
    mov ch, 0
    mov dh, 0 
    mov cl, SECT_TO_READ
    mov bx, ADD_TO_WRITE
    mov ds, bx
    mov dl, [ BOOT_DRIVE ]
    int 0x13
    add cl, 128
    popa
    ret

BOOT_DRIVE: db 0
SECT_TO_READ: db 2
ADD_TO_WRITE: dw 0x1000
TEST_MESSAGE: db 'Hello World', 13, 10, 0

times 510 - ($-$$) db 0
dw 0xaa55