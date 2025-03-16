bits 16
org 0x7c00

mov al,'k'
mov ah,0x0e
int 0x10
call readdisk
mov ah,0x0
mov al,0x13
int 0x10
call write_screen
jmp $

readdisk:
    mov ah, 0x02
    mov al, 125
    mov ch, 0
    mov dh, 0 
    mov cl, 1
    mov bx, 0xb000
    mov ds, bx
    mov dl, 0x80
    int 0x13
    jc disk_error ; Jump if error ( if carry flag set )
    ;mov bx,0x0000
    ;mov ds,bx
    ret
disk_error:
    mov ah, 0x01
    int 0x13
    mov al, ah
    add al, 32
    mov ah, 0x0e
    int 0x10
    jmp $
write_screen:
    pusha
    mov ah,0x0c
    mov bx,0xaa0 - 21
    mov ds,bx
    mov cx,0
    mov dx,0
write_pixel_loop:
    mov al,[bx]
    int 0x10
    cmp cx,64000
    je done_img_write
    inc cx
    add bx,1
    jmp write_pixel_loop
done_img_write:
    mov bx,0x0000
    mov ds,bx
    popa
    ret

times 510 - ($-$$) db 0
dw 0xAA55

;times 32768 db 0x0f
;times 32768 db 0x28
