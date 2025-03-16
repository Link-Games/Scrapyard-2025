bits 16
org 0x7c00

mov al,'k'
mov ah,0x0e
int 0x10
mov ah,0x0
mov al,0x13
int 0x10
call readdisk
;call write_screen
jmp $

readdisk:
    mov ah, 0x02
    mov al, 125
    mov ch, 0
    mov dh, 0 
    mov cl, 2
    mov bx, 0xa000
    mov es, bx
    mov bx, 0x0000
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

times 510 - ($-$$) db 0
dw 0xAA55

;image gets added at compile
