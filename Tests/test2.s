        .data
var1:   .word 10
var2:   .word 20
arr:    .word 6,7,8,9,10

        .text
_start:
        la x5,var1
        lw x6,0(x5)
        la x5,var2
        lw x7,0(x5)
        mul x8,x6,x7
        div x9,x7,x6
        rem x10,x7,x6
        andi x11,x6,3
        ori x12,x7,4
        sltu x13,x6,x7
        beq x6,x7,equal
        bne x6,x7,not_equal

equal:
        la x5,arr

not_equal:
        j end

end:
        ecall
