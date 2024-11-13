  .text
  .global _start

_start:
  ADDI x1, x0, 5          # x1 = 5
  ADDI x2, x0, 10         # x2 = 10
  BEQ x1, x2, target      # Branch if x1 == x2 (this won't be taken)
  BNE x1, x2, target      # Branch if x1 != x2 (this will be taken)
  
target:
  ADDI x3, x2, 15         # x3 = x2 + 15 (x3 = 25)

  FENCE.TS                # Synchronize store operations

  # Test Case Complete
  .end
