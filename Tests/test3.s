        .data                   # Start of the data section

var1:   .word  10              # Define a word and initialize it to 10
var2:   .word  20              # Define another word and initialize it to 20
arr:    .word  6, 7, 8, 9, 10  # Array of integers

        .text                   # Start of the code section

_start:
        la   x5, var1           # Load address of var1 into x5
        lw   x6, 0(x5)          # Load the value of var1 (10) into x6
        la   x5, var2           # Load address of var2 into x5
        lw   x7, 0(x5)          # Load the value of var2 (20) into x7

        # Arithmetic operations
        mul  x8, x6, x7         # x8 = var1 * var2
        div  x9, x7, x6         # x9 = var2 / var1
        rem  x10, x7, x6        # x10 = var2 % var1

        # Logical operations
        andi x11, x6, 3         # x11 = var1 & 3
        ori  x12, x7, 4         # x12 = var2 | 4
        sltu x13, x6, x7        # x13 = (unsigned var1 < var2)

        # Branching (conditional jumps)
        beq  x6, x7, equal      # If var1 == var2, jump to 'equal'
        bne  x6, x7, not_equal  # If var1 != var2, jump to 'not_equal'

equal:
        la   x5, arr            # Load address of arr

not_equal:
        j   end                 # Jump to end

end:
        ecall                   # Exit system call
