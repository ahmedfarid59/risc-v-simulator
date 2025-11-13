# RISC-V Simulator GUI - Complete Package

## 🎉 What You Have

A **complete RISC-V assembly simulator** with a professional graphical user interface!

### Files Created:
- ✅ `gui_simulator.py` - Main GUI application (700+ lines)
- ✅ `run_gui.bat` - Windows launcher
- ✅ `run_gui.py` - Cross-platform launcher
- ✅ `verify_gui.py` - Installation verification script
- ✅ `showcase.py` - Feature showcase script
- ✅ `requirements.txt` - Python dependencies
- ✅ `README.md` - Main documentation
- ✅ `GUI_README.md` - Detailed GUI guide
- ✅ `QUICK_START.md` - Quick start tutorial

## 🚀 Quick Start (3 Steps)

### Step 1: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 2: Launch the GUI
**Windows**: Double-click `run_gui.bat`

**Command Line**: 
```bash
python gui_simulator.py
```

### Step 3: Write and Run Code
1. Type your assembly code in the editor
2. Press **F5** to run
3. See results in registers panel and output

## 📋 GUI Features

### Editor Features
- ✅ **Syntax Highlighting** for RISC-V assembly
- ✅ **Line Numbers** for navigation
- ✅ **Auto-indentation** and smart formatting
- ✅ **Large editing area** for complex programs

### Simulation Features
- ✅ **One-click execution** (F5 key)
- ✅ **Real-time output** capture
- ✅ **Threaded execution** (UI stays responsive)
- ✅ **Error detection** and reporting
- ✅ **Status updates** in status bar

### Visualization
- ✅ **All 32 registers** displayed
- ✅ **Three number formats**: Unsigned, Hex, Signed
- ✅ **ABI names** (ra, sp, a0, etc.)
- ✅ **Auto-update** after each run
- ✅ **Scrollable panels** for easy viewing

### File Management
- ✅ **New/Open/Save/Save As** operations
- ✅ **Unsaved changes** detection
- ✅ **File type filtering** (.asm, .s)
- ✅ **Keyboard shortcuts** (Ctrl+N, Ctrl+O, etc.)

### Built-in Examples
- ✅ **Arithmetic** - Basic math operations
- ✅ **Loops** - Iteration examples
- ✅ **Functions** - Call/return examples
- ✅ **Memory** - Load/store operations

### Help & Documentation
- ✅ **Help dialog** (F1 key)
- ✅ **About dialog** with version info
- ✅ **Keyboard shortcuts** reference
- ✅ **Status bar** with tips

## 🎯 What You Can Do

### 1. Learn RISC-V Assembly
- Start with built-in examples
- Modify examples to experiment
- See immediate results

### 2. Write Programs
- Arithmetic calculations
- Loops and conditionals
- Function calls
- Memory operations
- Complex algorithms

### 3. Debug Code
- View register values after execution
- Read execution logs
- Identify errors quickly
- Test incrementally

### 4. Teach RISC-V
- Perfect for education
- Interactive learning
- Visual feedback
- Professional interface

## 📊 Technical Specifications

### Supported Instructions (47 total)
- **Arithmetic**: ADD, ADDI, SUB, MUL, DIV, REM
- **Logical**: AND, ANDI, OR, ORI, XOR, XORI
- **Shift**: SLL, SLLI, SRL, SRLI, SRA, SRAI
- **Compare**: SLT, SLTI, SLTU, SLTIU
- **Branch**: BEQ, BNE, BLT, BLTU, BGE, BGEU
- **Jump**: J, JAL, JALR
- **Load**: LB, LBU, LH, LHU, LW
- **Store**: SB, SH, SW
- **Upper**: LUI, AUIPC
- **Pseudo**: LI, LA, MV, NEG, NOT, RET

### Memory Layout
- **Text**: 0x00010000 - 0x00110000 (Code segment)
- **Data**: 0x10000000 - 0x10100000 (Variables)
- **Heap**: 0x10100000 - 0x10200000 (Dynamic allocation)
- **Stack**: 0x7FEFF000 - 0x7FFFF000 (Function calls)

### Directives
- `.data` - Data section
- `.text` - Code section
- `.word` - 32-bit value(s)
- `.half` - 16-bit value
- `.byte` - 8-bit value
- `.asciz` / `.ascii` - Strings
- `.space` - Reserve space

## 🎨 User Interface Layout

```
┌──────────────────────────────────────────────────────────────┐
│ File  Simulate  Examples  Help                    □ ─ ×     │
├──────────────────────────────────────────────────────────────┤
│ 📄 📂 💾   ▶️ ⏹                                             │ Toolbar
├────────────────────────────────────┬─────────────────────────┤
│                                    │ 📊 Register Values      │
│   📝 Assembly Code Editor          │ ┌─────────────────────┐ │
│   ┌────────────────────────────┐   │ │X0  (zero):  0       │ │
│  1│ .text                      │   │ │X1  (ra  ):  10      │ │
│  2│ main:                      │   │ │X2  (sp  ):  20      │ │
│  3│     addi x1, x0, 10        │   │ │X3  (gp  ):  30      │ │
│  4│     addi x2, x0, 20        │   │ │...                  │ │
│  5│     add x3, x1, x2         │   │ └─────────────────────┘ │
│  6│                            │   ├─────────────────────────┤
│  7│     addi x10, x0, 93       │   │ 📤 Simulation Output    │
│  8│     ecall                  │   │ ┌─────────────────────┐ │
│   │                            │   │ │INFO: Starting...    │ │
│   │                            │   │ │INFO: ADDI x1...     │ │
│   │                            │   │ │Execution complete!  │ │
│   └────────────────────────────┘   │ └─────────────────────┘ │
├────────────────────────────────────┴─────────────────────────┤
│ Ready                                                         │ Status
└──────────────────────────────────────────────────────────────┘
```

## 🔑 Essential Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| **F5** | ▶️ Run simulation |
| **Ctrl+S** | 💾 Save file |
| **Ctrl+O** | 📂 Open file |
| **Ctrl+N** | 📄 New file |
| **F1** | ❓ Help |

## 📖 Example Session

### 1. Launch GUI
```bash
python gui_simulator.py
```

### 2. Load Example
- Click **Examples** → **Basic Arithmetic**

### 3. Run It
- Press **F5**

### 4. See Results
- **Right panel**: X1=10, X2=20, X3=30
- **Output**: Execution logs

### 5. Modify Code
- Change `10` to `15`
- Press **F5** again
- See updated results!

## 🎓 Learning Path

### Beginner
1. Start with **Examples → Basic Arithmetic**
2. Modify values and re-run
3. Try **Examples → Loops**
4. Understand branching

### Intermediate
1. Write simple algorithms (factorial, fibonacci)
2. Use **Examples → Functions**
3. Practice with memory operations
4. Combine multiple instructions

### Advanced
1. Implement sorting algorithms
2. Write recursive functions
3. Use stack operations
4. Create complex data structures

## 🐛 Troubleshooting

### Issue: GUI won't start
**Solution**: Install wxPython
```bash
pip install wxPython
```

### Issue: Module not found
**Solution**: Activate virtual environment
```bash
.venv\Scripts\activate    # Windows
source .venv/bin/activate # Linux/Mac
```

### Issue: Simulation fails
**Check**:
- Syntax errors in code
- Missing `.text` or `.data` sections
- Proper `main:` label
- Exit code (`addi x10, x0, 93` + `ecall`)

### Issue: Registers all zero
**Check**:
- Code is in `.text` section
- Instructions executed before exit
- No errors in output panel

## 🎁 Bonus Features

- ✅ **Auto-save prompts** prevent data loss
- ✅ **Monospace fonts** for perfect alignment
- ✅ **Resizable panels** for your preference
- ✅ **Professional icons** from wxPython
- ✅ **Status bar** with helpful messages
- ✅ **Error highlighting** in output
- ✅ **Cross-platform** (Windows, Linux, Mac)

## 📚 Documentation Files

1. **README.md** - Project overview and features
2. **GUI_README.md** - Complete GUI guide (detailed!)
3. **QUICK_START.md** - Get started in 5 minutes
4. **This file** - Complete package summary

## 🔍 Verification

Run the verification script:
```bash
python verify_gui.py
```

Expected output:
```
✓ wxPython imported successfully
✓ wx.stc imported successfully
✓ RISCVSimulator imported successfully
✓ Program loaded successfully
✓ Simulation completed
✓ Register values correct
✓ All tests passed! GUI is ready to use.
```

## 🎉 Success!

You now have a **fully functional RISC-V simulator** with a professional GUI!

### What's Working:
✅ Text editor with syntax highlighting  
✅ File operations (new, open, save, save as)  
✅ Simulation execution (F5)  
✅ Register visualization (all 32 registers)  
✅ Output console with logs  
✅ Built-in examples  
✅ Help system  
✅ Keyboard shortcuts  
✅ Error handling  
✅ Status updates  

### Ready to Use:
```bash
python gui_simulator.py
```

### Start Learning:
1. Press F1 for help
2. Load an example from Examples menu
3. Press F5 to run
4. Watch the magic happen! ✨

---

**Enjoy your RISC-V Simulator GUI! Happy coding! 🚀**
