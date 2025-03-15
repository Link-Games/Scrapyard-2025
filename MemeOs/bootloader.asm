bits 16
org 0x7c00

mov [ BOOT_DRIVE ], dl ; BIOS stores our boot drive in dl
call readdisk
mov ah,0x0
mov al,0x13
int 0x10
call write_screen
jmp $

readdisk:
    pusha
    mov ah, 0x02
    mov al, 128
    mov ch, 0
    mov dh, 0 
    mov cl, 0
    mov bx, 0x1000
    mov ds, bx
    mov bx, 0x0000
    mov dl, [ BOOT_DRIVE ]
    int 0x13
    jc disk_error ; Jump if error ( if carry flag set )
    mov ax,0x0000
    mov ds, ax
    popa
    ret
disk_error :
    
    jmp $
write_screen:
    pusha
    mov ah,0x0c
    mov bx,0x1000
    mov ds,bx
    mov bx,0x0000
    mov cx,0
    mov dx,0
write_pixel_loop:
    mov al,[bx]
    int 0x10
    cmp cx,64000
    je done_img_write
    add cx,1
    add bx,1
    jmp write_pixel_loop
done_img_write:
    mov bx,0x0000
    mov ds,bx
    popa
    ret


BOOT_DRIVE: db 0

times 510 - ($-$$) db 0
dw 0xAA55

times 32000 db 0x0f
times 32000 db 0x28
