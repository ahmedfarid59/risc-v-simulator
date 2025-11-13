# RISC-V Simulator GUI

A graphical user interface for the RISC-V assembly simulator built with wxPython.

## Features

### 📝 Code Editor
- **Syntax Highlighting**: Assembly syntax highlighting for better code readability
- **Line Numbers**: Easy navigation with line numbers
- **Multiple File Support**: Create, open, save, and manage assembly files
- **Auto-complete Ready**: Smart editor with monospace font

### 🎮 Simulation Controls
- **Run**: Execute your RISC-V assembly programs (F5)
- **Stop**: Stop running simulations
- **Real-time Output**: See simulation logs and messages as they happen

### 📊 Register Visualization
- **All 32 Registers**: View X0-X31 register values
- **ABI Names**: Shows both numeric (X10) and ABI names (a0)
- **Multiple Formats**: Unsigned, Hexadecimal, and Signed decimal
- **Auto-update**: Registers update automatically after simulation

### 📚 Built-in Examples
- **Arithmetic Operations**: Basic math operations
- **Loops**: Iteration examples
- **Functions**: Function calls and returns
- **Memory Operations**: Load/store examples

## Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package installer)

### Setup

1. **Clone or download the repository**
   ```bash
   git clone https://github.com/ahmedfarid59/risc-v-simulator.git
   cd risc-v-simulator
   ```

2. **Create virtual environment (recommended)**
   ```bash
   python -m venv .venv
   
   # Windows
   .venv\Scripts\activate
   
   # Linux/Mac
   source .venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

## Running the GUI

### Windows
Double-click `run_gui.bat` or run:
```cmd
.venv\Scripts\python.exe gui_simulator.py
```

### Linux/Mac
```bash
python gui_simulator.py
```

Or use the launcher:
```bash
python run_gui.py
```

## Usage Guide

### Creating a New Program

1. **Click File → New** (or Ctrl+N)
2. Write your assembly code in the editor
3. Use the template provided as a starting point

### Opening Existing Files

1. **Click File → Open** (or Ctrl+O)
2. Navigate to your `.asm` or `.s` file
3. The file will load in the editor

### Writing Assembly Code

Basic structure:
```assembly
.data
    # Define variables here
    my_value: .word 42
    my_string: .asciz "Hello"

.text
main:
    # Write your instructions here
    addi x1, x0, 10      # x1 = 10
    addi x2, x0, 20      # x2 = 20
    add x3, x1, x2       # x3 = x1 + x2
    
    # Exit program
    addi x10, x0, 93
    ecall
```

### Running Simulations

1. **Write or load your assembly code**
2. **Click Simulate → Run** (or press F5)
3. **View results**:
   - **Output Panel**: Shows execution logs
   - **Register Panel**: Shows register values after execution

### Saving Your Work

- **Save**: File → Save (Ctrl+S) - Saves to current file
- **Save As**: File → Save As (Ctrl+Shift+S) - Save with new name

### Loading Examples

1. **Click Examples menu**
2. **Choose an example**:
   - Basic Arithmetic
   - Loops
   - Functions
   - Memory Operations
3. The example code loads automatically

## Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| Ctrl+N | New file |
| Ctrl+O | Open file |
| Ctrl+S | Save file |
| Ctrl+Shift+S | Save As |
| F5 | Run simulation |
| Shift+F5 | Stop simulation |
| Ctrl+L | Clear output |
| F1 | Show help |
| Ctrl+Q | Exit application |

## Understanding the Output

### Register Display Format
```
X1  (ra   ):         10 (0x0000000A) [         10]
 ^    ^                ^       ^               ^
 |    |                |       |               |
 |    ABI name         |       Hexadecimal     Signed decimal
 Register number       Unsigned decimal
```

### Simulation Output
- **INFO**: Normal execution messages
- **WARNING**: Non-critical issues
- **ERROR**: Execution errors

## Supported Instructions

### Arithmetic
- `ADD`, `ADDI`, `SUB`, `MUL`, `DIV`, `REM`

### Logical
- `AND`, `ANDI`, `OR`, `ORI`, `XOR`, `XORI`

### Shift
- `SLL`, `SLLI`, `SRL`, `SRLI`, `SRA`, `SRAI`

### Comparison
- `SLT`, `SLTI`, `SLTU`, `SLTIU`

### Branch
- `BEQ`, `BNE`, `BLT`, `BLTU`, `BGE`, `BGEU`

### Jump
- `J`, `JAL`, `JALR`

### Memory
- **Load**: `LB`, `LBU`, `LH`, `LHU`, `LW`
- **Store**: `SB`, `SH`, `SW`

### Upper Immediate
- `LUI`, `AUIPC`

### Pseudo-instructions
- `LI` (Load Immediate)
- `LA` (Load Address)
- `MV` (Move)
- `NEG` (Negate)
- `NOT` (Bitwise NOT)
- `RET` (Return)

## Troubleshooting

### GUI Won't Start

**Problem**: Error about wx module not found

**Solution**:
```bash
pip install wxPython
```

### Simulation Errors

**Problem**: "Failed to load program"

**Solutions**:
- Check for syntax errors in your assembly code
- Ensure `.data` and `.text` sections are properly defined
- Verify label and variable names don't have typos

### Register Values All Zero

**Problem**: Registers show 0 after simulation

**Solutions**:
- Ensure your code doesn't exit immediately
- Check that instructions are in the `.text` section
- Verify you have a `main:` label

### Output Not Showing

**Problem**: No output in output panel

**Solutions**:
- Click "Simulate → Clear Output" to refresh
- Check the status bar for error messages
- Look for ERROR messages in the output panel

## Tips and Best practices

1. **Always start with a template**: Use File → New to get the basic structure
2. **Test incrementally**: Run your code frequently as you write
3. **Use comments**: Document your code with `#` comments
4. **Check registers**: After simulation, verify register values match expectations
5. **Save regularly**: Use Ctrl+S frequently to save your work
6. **Try examples**: Learn from built-in examples before writing complex code

## Architecture Details

### Memory Layout
- **Text Segment**: 0x00010000 - 0x00110000 (Code)
- **Data Segment**: 0x10000000 - 0x10100000 (Variables)
- **Heap Segment**: 0x10100000 - 0x10200000
- **Stack Segment**: 0x7FEFF000 - 0x7FFFF000 (grows downward)

### Register Convention (ABI)
- **x0 (zero)**: Always zero
- **x1 (ra)**: Return address
- **x2 (sp)**: Stack pointer
- **x3 (gp)**: Global pointer
- **x4 (tp)**: Thread pointer
- **x5-x7 (t0-t2)**: Temporary registers
- **x8-x9 (s0-s1)**: Saved registers
- **x10-x17 (a0-a7)**: Argument registers
- **x18-x27 (s2-s11)**: Saved registers
- **x28-x31 (t3-t6)**: Temporary registers

## Advanced Features

### Custom Memory Initialization
```assembly
.data
    # Single values
    my_byte: .byte 0xFF
    my_half: .half 0x1234
    my_word: .word 0xDEADBEEF
    
    # Arrays
    array: .word 1, 2, 3, 4, 5
    
    # Strings
    message: .asciz "Hello, RISC-V!"
    
    # Reserved space
    buffer: .space 100
```

### System Calls
The simulator supports basic system calls via `ecall`:
- **Exit**: `addi x10, x0, 93` then `ecall`

## Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues.

## License

This project is open source. See LICENSE file for details.

## Support

For issues, questions, or suggestions:
- Open an issue on GitHub
- Check the Help menu (F1) in the GUI
- Review the examples provided

## Version History

### v1.0 (Current)
- Initial release with GUI
- Full RISC-V instruction support
- Syntax highlighting
- Register visualization
- Built-in examples
- File management

---

**Happy Coding! 🚀**
