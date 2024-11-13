        .data                   # Start of the data section

# Integer variable initialization
var1:   .word  10              # Define a word and initialize it to 10
var2:   .word  20              # Define another word and initialize it to 20
msg:    .asciz "Hello, RISC-V!" # Null-terminated string

arr:    .word 1, 2, 3, 4, 5    # Array of integers

MAX_VAL: .word 100             # A constant with value 100

        .text                   # Start of the code section

_start:
        la   x5, var1           # Load address of var1 into x5
        lw   x6, 0(x5)          # Load the value of var1 (10) into x6
        la   x5, var2           # Load address of var2 into x5
        lw   x7, 0(x5)          # Load the value of var2 (20) into x7

        # Arithmetic operations
        add  x8, x6, x7         # x8 = var1 + var2 (30)
        sub  x9, x7, x6         # x9 = var2 - var1 (10)

        # Logical operations
        and  x10, x6, x7        # x10 = var1 & var2
        or   x11, x6, x7        # x11 = var1 | var2
        xor  x12, x6, x7        # x12 = var1 ^ var2
        not  x13, x6            # x13 = ~var1

        # Comparison operations
        slt  x14, x6, x7        # x14 = (var1 < var2) (1 if true, 0 if false)
        sltu x15, x6, x7        # x15 = (unsigned var1 < var2)
        slti x16, x6, 15         # x16 = (var1 < 15) (1 if true)
        sltiu x17, x6, 15        # x17 = (unsigned var1 < 15) (1 if true)

        # Load instructions
        la   x5, arr            # Load address of the array into x5
        lw   x18, 0(x5)         # Load the first element of the array (1)
        lw   x19, 4(x5)         # Load the second element of the array (2)

        # Store instructions
        la   x5, arr            # Load the address of the array into x5
        sw   x8, 8(x5)          # Store the result of addition (30) in arr[2]

        # Branching (conditional jumps)
        beq  x6, x7, equal      # If var1 == var2, jump to 'equal'
        bne  x6, x7, not_equal  # If var1 != var2, jump to 'not_equal'

equal:
        # Code if var1 == var2
        la   x5, msg            # Load address of msg
        # Normally, you would print the string here, but for now just return

not_equal:
        # Code if var1 != var2
        # Again, we do nothing for now

        # Jump instruction
        j   end                  # Jump to end

end:
        # Exit system call
        li   a7, 93              # Syscall number for exit
        ecall                    # Make the system call to exit
