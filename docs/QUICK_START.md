# Quick Start Guide - RISC-V Simulator GUI

## First Time Setup

### 1. Install Python (if not already installed)
- Download Python 3.8 or higher from python.org
- Make sure to check "Add Python to PATH" during installation

### 2. Install Dependencies
Open a terminal in the project directory and run:
```bash
pip install -r requirements.txt
```

This will install wxPython (the GUI library).

## Launching the GUI

### Windows
**Option 1**: Double-click `run_gui.bat`

**Option 2**: Open terminal and run:
```bash
python gui_simulator.py
```

### Linux/Mac
Open terminal and run:
```bash
python gui_simulator.py
```

## Your First Program

1. **Start the GUI** using one of the methods above

2. **The editor opens with a template** - you'll see:
   ```assembly
   .data
   .text
   main:
   ```

3. **Write your first program**:
   ```assembly
   .text
   main:
       addi x1, x0, 5       # x1 = 5
       addi x2, x0, 10      # x2 = 10
       add x3, x1, x2       # x3 = x1 + x2 = 15
       
       addi x10, x0, 93     # Exit syscall
       ecall
   ```

4. **Press F5** (or click Simulate → Run)

5. **Check the results**:
   - **Right side - Register Panel**: Look for X1, X2, X3
   - **Bottom right - Output**: See execution logs

## Understanding the Interface

```
┌─────────────────────────────────────────────────────────────┐
│  File  Simulate  Examples  Help                    [X]      │
├───────────────────────────────────────────┬─────────────────┤
│                                           │  Register Panel │
│                                           │  ┌────────────┐ │
│                                           │  │ X0 = 0     │ │
│          Code Editor                      │  │ X1 = 5     │ │
│                                           │  │ X2 = 10    │ │
│  .text                                    │  │ X3 = 15    │ │
│  main:                                    │  └────────────┘ │
│      addi x1, x0, 5                       │                 │
│      addi x2, x0, 10                      ├─────────────────┤
│      add x3, x1, x2                       │  Output Panel   │
│                                           │  ┌────────────┐ │
│                                           │  │ INFO: ...  │ │
│                                           │  │ Execution  │ │
│                                           │  │ complete   │ │
│                                           │  └────────────┘ │
└───────────────────────────────────────────┴─────────────────┘
```

## Common Tasks

### Save Your Program
- **First time**: File → Save As (Ctrl+Shift+S)
- **After that**: File → Save (Ctrl+S)

### Open an Existing File
- File → Open (Ctrl+O)
- Navigate to your `.asm` file

### Load an Example
- Examples → Choose one:
  - Basic Arithmetic
  - Loops
  - Functions
  - Memory Operations

### Clear Output
- Simulate → Clear Output (Ctrl+L)

## Keyboard Shortcuts

| Key | Action |
|-----|--------|
| **F5** | Run simulation |
| **Ctrl+S** | Save file |
| **Ctrl+O** | Open file |
| **Ctrl+N** | New file |
| **Ctrl+L** | Clear output |
| **F1** | Help |

## Example Programs

### 1. Simple Addition
```assembly
.text
main:
    addi x1, x0, 42
    addi x2, x0, 58
    add x3, x1, x2      # x3 = 100
    
    addi x10, x0, 93
    ecall
```

### 2. Count to 10
```assembly
.text
main:
    addi x1, x0, 0      # counter
    addi x2, x0, 10     # limit
    
loop:
    addi x1, x1, 1      # counter++
    blt x1, x2, loop    # if counter < 10, loop
    
    # x1 will be 10
    addi x10, x0, 93
    ecall
```

### 3. Using Memory
```assembly
.data
    my_number: .word 777

.text
main:
    lui x1, 0x10000     # Data segment address
    lw x2, 0(x1)        # Load my_number
    addi x2, x2, 1      # Increment
    sw x2, 0(x1)        # Store back
    
    addi x10, x0, 93
    ecall
```

## Reading Register Values

The register panel shows three formats:
```
X1  (ra   ):        100 (0x00000064) [        100]
     ↑               ↑         ↑               ↑
     |               |         |               |
  ABI name     Unsigned    Hex         Signed decimal
```

## Common Mistakes to Avoid

1. **Forgetting the exit code**:
   ```assembly
   # WRONG - no exit
   main:
       addi x1, x0, 10
   
   # RIGHT - has exit
   main:
       addi x1, x0, 10
       addi x10, x0, 93
       ecall
   ```

2. **Missing sections**:
   ```assembly
   # WRONG
   addi x1, x0, 10
   
   # RIGHT
   .text
   main:
       addi x1, x0, 10
   ```

3. **Typos in register names**:
   ```assembly
   # WRONG
   addi x33, x0, 10    # Only x0-x31 exist
   
   # RIGHT
   addi x3, x0, 10
   ```

## Need Help?

1. **Press F1** in the GUI for built-in help
2. **Load Examples** from the Examples menu
3. **Check Output Panel** for error messages
4. **Read GUI_README.md** for detailed documentation

## Tips

- 💡 Start with examples to learn
- 💡 Save your work frequently (Ctrl+S)
- 💡 Check registers after each simulation
- 💡 Use comments (`#`) to document your code
- 💡 Test small pieces of code before combining

---

**You're ready to start! Press F5 to run your first program! 🚀**
