"""
Feature showcase and demo for RISC-V Simulator GUI
This script demonstrates the GUI can be used programmatically
"""
import os
import sys

def print_banner():
    """Print welcome banner"""
    print("="*70)
    print("  RISC-V SIMULATOR GUI - FEATURE SHOWCASE")
    print("="*70)
    print()

def show_features():
    """Display all GUI features"""
    features = [
        ("Code Editor", [
            "✓ Syntax highlighting for RISC-V assembly",
            "✓ Line numbers for easy navigation",
            "✓ Monospace font for clarity",
            "✓ Tab width set to 4 spaces",
            "✓ Smart indentation"
        ]),
        ("File Operations", [
            "✓ New file (Ctrl+N)",
            "✓ Open file (Ctrl+O)",
            "✓ Save file (Ctrl+S)",
            "✓ Save As (Ctrl+Shift+S)",
            "✓ Unsaved changes detection",
            "✓ File type filtering (.asm, .s)"
        ]),
        ("Simulation", [
            "✓ Run programs (F5)",
            "✓ Threaded execution (non-blocking UI)",
            "✓ Real-time output capture",
            "✓ Error detection and reporting",
            "✓ Maximum instruction limit protection",
            "✓ Status updates in status bar"
        ]),
        ("Register Display", [
            "✓ All 32 RISC-V registers (X0-X31)",
            "✓ ABI names (ra, sp, a0-a7, etc.)",
            "✓ Three formats: unsigned, hex, signed",
            "✓ Scrollable view",
            "✓ Monospace font alignment",
            "✓ Auto-update after simulation"
        ]),
        ("Output Console", [
            "✓ Execution logs",
            "✓ Error messages",
            "✓ Instruction tracing",
            "✓ Clear output button",
            "✓ Scrollable history",
            "✓ Monospace font for alignment"
        ]),
        ("Built-in Examples", [
            "✓ Basic Arithmetic - Learn math operations",
            "✓ Loops - Iteration and branching",
            "✓ Functions - Calls and returns",
            "✓ Memory Operations - Load/store examples"
        ]),
        ("User Experience", [
            "✓ Menu bar with keyboard shortcuts",
            "✓ Toolbar with common actions",
            "✓ Status bar with feedback",
            "✓ About dialog with info",
            "✓ Help dialog (F1)",
            "✓ Resizable panels",
            "✓ Professional layout"
        ])
    ]
    
    for category, items in features:
        print(f"\n{category}:")
        print("-" * 70)
        for item in items:
            print(f"  {item}")
    
    print()

def show_supported_instructions():
    """Show supported RISC-V instructions"""
    print("\nSupported RISC-V Instructions:")
    print("-" * 70)
    
    categories = {
        "Arithmetic": ["ADD", "ADDI", "SUB", "MUL", "DIV", "REM"],
        "Logical": ["AND", "ANDI", "OR", "ORI", "XOR", "XORI"],
        "Shift": ["SLL", "SLLI", "SRL", "SRLI", "SRA", "SRAI"],
        "Compare": ["SLT", "SLTI", "SLTU", "SLTIU"],
        "Branch": ["BEQ", "BNE", "BLT", "BLTU", "BGE", "BGEU"],
        "Jump": ["J", "JAL", "JALR"],
        "Load": ["LB", "LBU", "LH", "LHU", "LW"],
        "Store": ["SB", "SH", "SW"],
        "Upper": ["LUI", "AUIPC"],
        "Pseudo": ["LI", "LA", "MV", "NEG", "NOT", "RET"]
    }
    
    for category, instructions in categories.items():
        print(f"\n  {category:12} : {', '.join(instructions)}")
    
    print()

def show_usage():
    """Show usage instructions"""
    print("\nHow to Use:")
    print("-" * 70)
    print("""
1. Launch the GUI:
   Windows: Double-click run_gui.bat
   Command: python gui_simulator.py

2. Write your assembly code in the editor

3. Press F5 to run the simulation

4. View results:
   - Registers on the right side
   - Output at the bottom right

5. Save your work with Ctrl+S
""")

def show_example_code():
    """Show example assembly code"""
    print("\nExample Program:")
    print("-" * 70)
    print("""
# Calculate sum of 1 to 10
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
    
    # Result: x3 = 55 (1+2+3+...+10)
    addi x10, x0, 93
    ecall
""")

def show_keyboard_shortcuts():
    """Show keyboard shortcuts"""
    print("\nKeyboard Shortcuts:")
    print("-" * 70)
    shortcuts = [
        ("Ctrl+N", "New file"),
        ("Ctrl+O", "Open file"),
        ("Ctrl+S", "Save file"),
        ("Ctrl+Shift+S", "Save As"),
        ("F5", "Run simulation"),
        ("Shift+F5", "Stop simulation"),
        ("Ctrl+L", "Clear output"),
        ("F1", "Show help"),
        ("Ctrl+Q", "Exit application")
    ]
    
    for shortcut, description in shortcuts:
        print(f"  {shortcut:20} - {description}")
    print()

def check_installation():
    """Check if GUI can be launched"""
    print("\nChecking Installation:")
    print("-" * 70)
    
    try:
        import wx
        print("  ✓ wxPython installed")
        wx_version = wx.version()
        print(f"    Version: {wx_version}")
    except ImportError:
        print("  ✗ wxPython not installed")
        print("    Install with: pip install wxPython")
        return False
    
    try:
        import wx.stc
        print("  ✓ wx.stc available")
    except ImportError:
        print("  ✗ wx.stc not available")
        return False
    
    try:
        sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
        from src.main_real import RISCVSimulator
        print("  ✓ RISC-V Simulator core available")
    except ImportError as e:
        print(f"  ✗ Simulator core import failed: {e}")
        return False
    
    if os.path.exists("gui/gui_simulator.py"):
        print("  ✓ GUI script found")
    else:
        print("  ✗ GUI script not found")
        return False
    
    print("\n  ✓ All components ready!")
    return True

def main():
    """Main showcase function"""
    print_banner()
    
    # Show features
    show_features()
    
    # Show instructions
    show_supported_instructions()
    
    # Show keyboard shortcuts
    show_keyboard_shortcuts()
    
    # Show example
    show_example_code()
    
    # Show usage
    show_usage()
    
    # Check installation
    is_ready = check_installation()
    
    # Final message
    print("\n" + "="*70)
    if is_ready:
        print("  Ready to launch! Run: python gui_simulator.py")
    else:
        print("  Please install dependencies: pip install -r requirements.txt")
    print("="*70)
    print()

if __name__ == '__main__':
    main()
