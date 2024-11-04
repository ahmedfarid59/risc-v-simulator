# Sample RISC-V Assembly Code

# Registers:
# x5: Holds the value 10
# x6: Holds the value 20
# x7: Result of addition (x5 + x6)
# x8: Result of subtraction (x6 - x5)
# x9: Loop counter

    .section .data        # Data section (if needed)

    .section .text        # Code section
    .globl _start         # Entry point

_start:

    # Load immediate values into registers
    li x5, 10             # Load 10 into register x5
    li x6, 20             # Load 20 into register x6

    # Perform addition
    add x7, x5, x6        # x7 = x5 + x6 (x7 = 10 + 20)

    # Perform subtraction
    sub x8, x6, x5        # x8 = x6 - x5 (x8 = 20 - 10)

    # Initialize loop counter
    li x9, 5              # Set the loop counter to 5

loop:
    beq x9, x0, end_loop  # If x9 == 0, exit the loop
    addi x9, x9, -1       # Decrement the loop counter by 1
    j loop                # Jump back to the start of the loop

end_loop:
    # Exit program (using ecall for testing purposes)
    li x10, 10            # Syscall code for exit
    ecall                 # Make the syscall (in real systems)