# RISC-V Simulator

A comprehensive RISC-V assembly simulator with both command-line interface and graphical user interface.

## 🌟 Features

### Graphical User Interface (NEW! ✨)
- **Code Editor**: Syntax highlighting for RISC-V assembly
- **Real-time Simulation**: Run programs and see results instantly
- **Register Visualization**: View all 32 registers with multiple formats
- **File Management**: Create, open, save assembly files
- **Built-in Examples**: Learn from pre-written examples
- **Output Console**: See detailed execution logs

### Core Simulator
- **Full RV32I Support**: Complete RISC-V 32-bit base instruction set
- **Memory Management**: Segmented memory (text, data, heap, stack)
- **System Calls**: Basic syscall support
- **Error Handling**: Comprehensive error detection and reporting
- **Automated Testing**: 10 comprehensive test cases with 100% pass rate

## 🚀 Quick Start

### GUI Mode (Recommended for Beginners)

1. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the GUI**:
   ```bash
   # Windows
   gui\run_gui.bat
   
   # Or manually
   python run_gui_main.py
   ```

3. **Write code** in the editor and press **F5** to run!

See [GUI_README.md](GUI_README.md) for detailed GUI documentation.

### Command-Line Mode

1. **Create an assembly file** (e.g., `program.asm`):
   ```assembly
   .data
       value: .word 42
   
   .text
   main:
       addi x1, x0, 10
       addi x2, x0, 20
       add x3, x1, x2
       
       addi x10, x0, 93
       ecall
   ```

2. **Run the simulator**:
   ```bash
   python simulator.py
   ```

3. **Enter filename** when prompted

## 📦 Installation

### Requirements
- Python 3.8+
- wxPython 4.2+ (for GUI)

### Setup

```bash
# Clone repository
git clone https://github.com/ahmedfarid59/risc-v-simulator.git
cd risc-v-simulator

# Create virtual environment (recommended)
python -m venv .venv

# Activate virtual environment
# Windows:
.venv\Scripts\activate
# Linux/Mac:
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

## 📚 Documentation

- **[GUI Guide](docs/GUI_README.md)**: Complete GUI documentation with screenshots and examples
- **[Quick Start](docs/QUICK_START.md)**: Get started quickly
- **[Package Summary](docs/PACKAGE_SUMMARY.md)**: Overview of all modules
- **Instruction Reference**: See supported instructions below
- **Examples**: Built-in examples in the GUI Examples menu

## 🎮 Usage Examples

### Example 1: Basic Arithmetic
```assembly
.text
main:
    addi x1, x0, 10      # x1 = 10
    addi x2, x0, 20      # x2 = 20
    add x3, x1, x2       # x3 = 30
    sub x4, x2, x1       # x4 = 10
    
    addi x10, x0, 93
    ecall
```

### Example 2: Loop (Sum 1 to 10)
```assembly
.text
main:
    addi x1, x0, 1       # counter = 1
    addi x2, x0, 10      # limit = 10
    addi x3, x0, 0       # sum = 0
    
loop:
    add x3, x3, x1       # sum += counter
    addi x1, x1, 1       # counter++
    blt x1, x2, loop     # if counter < limit, loop
    beq x1, x2, loop     # if counter == limit, loop once more
    
    # Result: x3 = 55
    addi x10, x0, 93
    ecall
```

### Example 3: Memory Operations
```assembly
.data
    array: .word 1, 2, 3, 4, 5

.text
main:
    lui x1, 0x10000      # Base address
    lw x2, 0(x1)         # Load first element
    lw x3, 4(x1)         # Load second element
    add x4, x2, x3       # Add them
    sw x4, 8(x1)         # Store result
    
    addi x10, x0, 93
    ecall
```

## 🔧 Supported Instructions

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
- `LB`, `LBU`, `LH`, `LHU`, `LW`
- `SB`, `SH`, `SW`

### Upper Immediate
- `LUI`, `AUIPC`

### Pseudo-instructions
- `LI`, `LA`, `MV`, `NEG`, `NOT`, `RET`

## 🧪 Testing

Run the automated test suite:

```bash
python scripts/test_runner.py
```

**Current Status**: ✅ 10/10 tests passing (100%)

Test categories:
- Arithmetic operations
- Logical operations
- Shift operations
- Branch instructions
- Jump instructions
- Memory operations
- Edge cases
- Upper immediate instructions
- Set-less-than operations
- Noisy input handling

## 🏗️ Project Structure

```
risc-v-simulator/
├── src/                 # Core simulator modules
│   ├── main_real.py    # Main simulator engine
│   ├── parse_real.py   # Assembly parser
│   ├── functions.py    # Instruction implementations
│   ├── registers.py    # Register file management
│   ├── memory.py       # Memory system
│   ├── csr.py          # Control & Status Registers
│   ├── syscall.py      # System call handler
│   ├── constants.py    # Constants and definitions
│   ├── utils.py        # Utility functions
│   └── logger.py       # Logging configuration
├── gui/                 # GUI application
│   ├── gui_simulator.py # Main GUI application
│   ├── run_gui.py      # GUI launcher script
│   └── run_gui.bat     # Windows GUI launcher
├── scripts/             # Utility scripts
│   ├── test_runner.py  # Automated test runner
│   ├── verify_gui.py   # GUI verification
│   └── showcase.py     # Feature showcase
├── tests/               # Test cases (10 .asm files)
├── docs/                # Documentation
│   ├── GUI_README.md   # GUI documentation
│   ├── QUICK_START.md  # Quick start guide
│   └── PACKAGE_SUMMARY.md # Package overview
├── logs/                # Log files (auto-generated)
├── simulator.py         # CLI entry point
├── run_gui_main.py      # GUI entry point
├── requirements.txt     # Python dependencies
└── README.md            # This file
```

## 💡 Tips

1. **Start with GUI**: If you're new to RISC-V, use the GUI for interactive learning
2. **Use Examples**: Load built-in examples from the Examples menu
3. **Check Registers**: Always verify register values after simulation
4. **Test Incrementally**: Write and test code in small chunks
5. **Read Output**: The output panel shows detailed execution logs

## 🐛 Troubleshooting

### Common Issues

**GUI won't start**:
```bash
pip install wxPython
```

**Import errors**:
```bash
# Make sure you're in the virtual environment
.venv\Scripts\activate  # Windows
source .venv/bin/activate  # Linux/Mac
```

**Simulation fails**:
- Check assembly syntax
- Ensure proper `.data` and `.text` sections
- Verify label names are correct

## 🤝 Contributing

Contributions are welcome! Areas for improvement:
- Additional instruction support
- Debugging features (breakpoints, step-through)
- Memory visualization
- Performance optimization
- More examples and tutorials

## 📝 License

This project is open source. See LICENSE file for details.

## 👨‍💻 Authors

- Ahmed Farid (@ahmedfarid59)
- Contributors welcome!

## 🙏 Acknowledgments

- RISC-V Foundation for the ISA specification
- wxPython team for the GUI framework

## 📞 Support

- **Issues**: Open an issue on GitHub
- **Documentation**: See GUI_README.md
- **Help**: Press F1 in the GUI for built-in help

---

**Start simulating RISC-V assembly today! 🚀**
