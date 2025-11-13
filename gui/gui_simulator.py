"""
RISC-V Simulator GUI
A wxPython-based graphical interface for the RISC-V simulator
"""
import wx
import wx.stc as stc
import os
import sys
from pathlib import Path
import threading
import io
from contextlib import redirect_stdout, redirect_stderr

# Import simulator components
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from src.main_real import RISCVSimulator


class AssemblyEditor(stc.StyledTextCtrl):
    """Assembly code editor with syntax highlighting"""
    
    def __init__(self, parent):
        super().__init__(parent)
        
        # Set up the editor
        self.SetLexer(stc.STC_LEX_ASM)
        self.SetMarginType(1, stc.STC_MARGIN_NUMBER)
        self.SetMarginWidth(1, 40)
        
        # Set up syntax highlighting
        self.StyleSetSpec(stc.STC_STYLE_DEFAULT, "face:Courier New,size:10")
        self.StyleClearAll()
        
        # Comments
        self.StyleSetSpec(stc.STC_ASM_COMMENT, "fore:#008000,italic")
        self.StyleSetSpec(stc.STC_ASM_COMMENTBLOCK, "fore:#008000,italic")
        
        # Instructions
        self.StyleSetSpec(stc.STC_ASM_CPUINSTRUCTION, "fore:#0000FF,bold")
        
        # Directives
        self.StyleSetSpec(stc.STC_ASM_DIRECTIVE, "fore:#800080,bold")
        
        # Numbers
        self.StyleSetSpec(stc.STC_ASM_NUMBER, "fore:#FF0000")
        
        # Strings
        self.StyleSetSpec(stc.STC_ASM_STRING, "fore:#808000")
        
        # Registers
        self.StyleSetSpec(stc.STC_ASM_REGISTER, "fore:#008080,bold")
        
        # Keywords (instructions)
        instructions = " ".join([
            "add addi and andi auipc beq bge bgeu blt bltu bne div",
            "j jal jalr lb lbu lh lhu li lui lw mul mv neg not",
            "or ori rem ret sb sh sll slli slt slti sltiu sltu",
            "sra srai srl srli sub sw xor xori la ecall"
        ])
        self.SetKeyWords(0, instructions)
        
        # Set tab width
        self.SetTabWidth(4)
        self.SetUseTabs(False)
        
        # Enable line numbers
        self.SetMarginWidth(0, 5)


class RegisterPanel(wx.Panel):
    """Panel to display register values"""
    
    def __init__(self, parent):
        super().__init__(parent)
        
        # Create a grid for registers
        sizer = wx.BoxSizer(wx.VERTICAL)
        
        # Title
        title = wx.StaticText(self, label="Register Values")
        title_font = title.GetFont()
        title_font.PointSize += 2
        title_font = title_font.Bold()
        title.SetFont(title_font)
        sizer.Add(title, 0, wx.ALL | wx.ALIGN_CENTER, 5)
        
        # Create scrolled window for registers
        scroll = wx.ScrolledWindow(self)
        scroll.SetScrollRate(5, 5)
        scroll_sizer = wx.BoxSizer(wx.VERTICAL)
        
        # Create text control for register display
        self.register_text = wx.TextCtrl(
            scroll,
            style=wx.TE_MULTILINE | wx.TE_READONLY | wx.TE_RICH2,
            size=(300, 600)
        )
        font = wx.Font(9, wx.FONTFAMILY_TELETYPE, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL)
        self.register_text.SetFont(font)
        
        scroll_sizer.Add(self.register_text, 1, wx.EXPAND | wx.ALL, 5)
        scroll.SetSizer(scroll_sizer)
        
        sizer.Add(scroll, 1, wx.EXPAND | wx.ALL, 5)
        self.SetSizer(sizer)
        
    def update_registers(self, regs):
        """Update register display"""
        if not regs:
            self.register_text.SetValue("No simulation run yet")
            return
        
        text = ""
        for i in range(32):
            reg_name = f"X{i}"
            value = regs.get(reg_name, 0)
            
            # Also show ABI name
            abi_names = {
                0: "zero", 1: "ra", 2: "sp", 3: "gp", 4: "tp",
                5: "t0", 6: "t1", 7: "t2", 8: "s0/fp", 9: "s1",
                10: "a0", 11: "a1", 12: "a2", 13: "a3", 14: "a4",
                15: "a5", 16: "a6", 17: "a7", 18: "s2", 19: "s3",
                20: "s4", 21: "s5", 22: "s6", 23: "s7", 24: "s8",
                25: "s9", 26: "s10", 27: "s11", 28: "t3", 29: "t4",
                30: "t5", 31: "t6"
            }
            
            abi_name = abi_names.get(i, "")
            
            # Convert to signed for display
            signed_val = value if value < 0x80000000 else value - 0x100000000
            
            text += f"{reg_name:3} ({abi_name:5}): {value:10} (0x{value:08X}) [{signed_val:11}]\n"
        
        self.register_text.SetValue(text)


class OutputPanel(wx.Panel):
    """Panel to display simulation output"""
    
    def __init__(self, parent):
        super().__init__(parent)
        
        sizer = wx.BoxSizer(wx.VERTICAL)
        
        # Title
        title = wx.StaticText(self, label="Simulation Output")
        title_font = title.GetFont()
        title_font.PointSize += 2
        title_font = title_font.Bold()
        title.SetFont(title_font)
        sizer.Add(title, 0, wx.ALL | wx.ALIGN_CENTER, 5)
        
        # Output text
        self.output_text = wx.TextCtrl(
            self,
            style=wx.TE_MULTILINE | wx.TE_READONLY | wx.TE_RICH2
        )
        font = wx.Font(9, wx.FONTFAMILY_TELETYPE, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL)
        self.output_text.SetFont(font)
        
        sizer.Add(self.output_text, 1, wx.EXPAND | wx.ALL, 5)
        
        # Clear button
        clear_btn = wx.Button(self, label="Clear Output")
        clear_btn.Bind(wx.EVT_BUTTON, self.on_clear)
        sizer.Add(clear_btn, 0, wx.ALL | wx.ALIGN_RIGHT, 5)
        
        self.SetSizer(sizer)
        
    def append_text(self, text):
        """Append text to output"""
        self.output_text.AppendText(text)
        
    def clear(self):
        """Clear output"""
        self.output_text.Clear()
        
    def on_clear(self, event):
        """Clear button handler"""
        self.clear()


class SimulatorFrame(wx.Frame):
    """Main application frame"""
    
    def __init__(self):
        super().__init__(None, title="RISC-V Simulator", size=(1200, 800))
        
        self.current_file = None
        self.simulator = None
        
        # Create menu bar
        self.create_menu_bar()
        
        # Create toolbar
        self.create_toolbar()
        
        # Create status bar
        self.CreateStatusBar()
        self.SetStatusText("Ready")
        
        # Create main panel
        panel = wx.Panel(self)
        main_sizer = wx.BoxSizer(wx.HORIZONTAL)
        
        # Left side: Editor
        left_panel = wx.Panel(panel)
        left_sizer = wx.BoxSizer(wx.VERTICAL)
        
        editor_label = wx.StaticText(left_panel, label="Assembly Code Editor")
        editor_font = editor_label.GetFont()
        editor_font.PointSize += 2
        editor_font = editor_font.Bold()
        editor_label.SetFont(editor_font)
        left_sizer.Add(editor_label, 0, wx.ALL | wx.ALIGN_CENTER, 5)
        
        self.editor = AssemblyEditor(left_panel)
        left_sizer.Add(self.editor, 1, wx.EXPAND | wx.ALL, 5)
        
        left_panel.SetSizer(left_sizer)
        main_sizer.Add(left_panel, 2, wx.EXPAND | wx.ALL, 5)
        
        # Right side: Split between registers and output
        right_panel = wx.Panel(panel)
        right_sizer = wx.BoxSizer(wx.VERTICAL)
        
        # Registers
        self.register_panel = RegisterPanel(right_panel)
        right_sizer.Add(self.register_panel, 1, wx.EXPAND | wx.ALL, 5)
        
        # Output
        self.output_panel = OutputPanel(right_panel)
        right_sizer.Add(self.output_panel, 1, wx.EXPAND | wx.ALL, 5)
        
        right_panel.SetSizer(right_sizer)
        main_sizer.Add(right_panel, 1, wx.EXPAND | wx.ALL, 5)
        
        panel.SetSizer(main_sizer)
        
        # Set default text
        self.editor.SetText(self.get_default_template())
        
        self.Centre()
        
    def create_menu_bar(self):
        """Create application menu bar"""
        menubar = wx.MenuBar()
        
        # File menu
        file_menu = wx.Menu()
        new_item = file_menu.Append(wx.ID_NEW, "&New\tCtrl+N", "Create new file")
        open_item = file_menu.Append(wx.ID_OPEN, "&Open\tCtrl+O", "Open file")
        save_item = file_menu.Append(wx.ID_SAVE, "&Save\tCtrl+S", "Save file")
        save_as_item = file_menu.Append(wx.ID_SAVEAS, "Save &As\tCtrl+Shift+S", "Save file as")
        file_menu.AppendSeparator()
        exit_item = file_menu.Append(wx.ID_EXIT, "E&xit\tCtrl+Q", "Exit application")
        
        # Bind file menu events
        self.Bind(wx.EVT_MENU, self.on_new, new_item)
        self.Bind(wx.EVT_MENU, self.on_open, open_item)
        self.Bind(wx.EVT_MENU, self.on_save, save_item)
        self.Bind(wx.EVT_MENU, self.on_save_as, save_as_item)
        self.Bind(wx.EVT_MENU, self.on_exit, exit_item)
        
        menubar.Append(file_menu, "&File")
        
        # Simulate menu
        sim_menu = wx.Menu()
        run_item = sim_menu.Append(wx.ID_ANY, "&Run\tF5", "Run simulation")
        stop_item = sim_menu.Append(wx.ID_ANY, "&Stop\tShift+F5", "Stop simulation")
        sim_menu.AppendSeparator()
        clear_item = sim_menu.Append(wx.ID_ANY, "&Clear Output\tCtrl+L", "Clear output")
        
        # Bind simulate menu events
        self.Bind(wx.EVT_MENU, self.on_run, run_item)
        self.Bind(wx.EVT_MENU, self.on_stop, stop_item)
        self.Bind(wx.EVT_MENU, self.on_clear_output, clear_item)
        
        menubar.Append(sim_menu, "&Simulate")
        
        # Examples menu
        examples_menu = wx.Menu()
        ex1 = examples_menu.Append(wx.ID_ANY, "Basic Arithmetic", "Load arithmetic example")
        ex2 = examples_menu.Append(wx.ID_ANY, "Loops", "Load loop example")
        ex3 = examples_menu.Append(wx.ID_ANY, "Functions", "Load function example")
        ex4 = examples_menu.Append(wx.ID_ANY, "Memory Operations", "Load memory example")
        
        self.Bind(wx.EVT_MENU, lambda e: self.load_example("arithmetic"), ex1)
        self.Bind(wx.EVT_MENU, lambda e: self.load_example("loops"), ex2)
        self.Bind(wx.EVT_MENU, lambda e: self.load_example("functions"), ex3)
        self.Bind(wx.EVT_MENU, lambda e: self.load_example("memory"), ex4)
        
        menubar.Append(examples_menu, "&Examples")
        
        # Help menu
        help_menu = wx.Menu()
        about_item = help_menu.Append(wx.ID_ABOUT, "&About", "About RISC-V Simulator")
        help_item = help_menu.Append(wx.ID_HELP, "&Help\tF1", "Show help")
        
        self.Bind(wx.EVT_MENU, self.on_about, about_item)
        self.Bind(wx.EVT_MENU, self.on_help, help_item)
        
        menubar.Append(help_menu, "&Help")
        
        self.SetMenuBar(menubar)
        
    def create_toolbar(self):
        """Create application toolbar"""
        toolbar = self.CreateToolBar()
        
        # Add tools
        new_tool = toolbar.AddTool(wx.ID_NEW, "New", 
                                    wx.ArtProvider.GetBitmap(wx.ART_NEW, wx.ART_TOOLBAR),
                                    "New file")
        open_tool = toolbar.AddTool(wx.ID_OPEN, "Open",
                                     wx.ArtProvider.GetBitmap(wx.ART_FILE_OPEN, wx.ART_TOOLBAR),
                                     "Open file")
        save_tool = toolbar.AddTool(wx.ID_SAVE, "Save",
                                     wx.ArtProvider.GetBitmap(wx.ART_FILE_SAVE, wx.ART_TOOLBAR),
                                     "Save file")
        
        toolbar.AddSeparator()
        
        run_tool = toolbar.AddTool(wx.ID_ANY, "Run",
                                    wx.ArtProvider.GetBitmap(wx.ART_GO_FORWARD, wx.ART_TOOLBAR),
                                    "Run simulation")
        stop_tool = toolbar.AddTool(wx.ID_ANY, "Stop",
                                     wx.ArtProvider.GetBitmap(wx.ART_QUIT, wx.ART_TOOLBAR),
                                     "Stop simulation")
        
        # Bind toolbar events
        self.Bind(wx.EVT_TOOL, self.on_new, new_tool)
        self.Bind(wx.EVT_TOOL, self.on_open, open_tool)
        self.Bind(wx.EVT_TOOL, self.on_save, save_tool)
        self.Bind(wx.EVT_TOOL, self.on_run, run_tool)
        self.Bind(wx.EVT_TOOL, self.on_stop, stop_tool)
        
        toolbar.Realize()
        
    def get_default_template(self):
        """Get default assembly template"""
        return """# RISC-V Assembly Program
# Write your assembly code here

.data
    # Data section - define your variables here
    # Example: value: .word 42

.text
main:
    # Text section - write your instructions here
    # Example:
    # addi x1, x0, 10    # x1 = 10
    # addi x2, x0, 20    # x2 = 20
    # add x3, x1, x2     # x3 = x1 + x2
    
    # Exit
    addi x10, x0, 93
    ecall
"""
    
    def on_new(self, event):
        """Create new file"""
        if self.editor.GetModify():
            dlg = wx.MessageDialog(self, "Save changes?", "Unsaved Changes",
                                  wx.YES_NO | wx.CANCEL | wx.ICON_QUESTION)
            result = dlg.ShowModal()
            dlg.Destroy()
            
            if result == wx.ID_YES:
                self.on_save(None)
            elif result == wx.ID_CANCEL:
                return
        
        self.editor.SetText(self.get_default_template())
        self.current_file = None
        self.SetTitle("RISC-V Simulator - Untitled")
        self.SetStatusText("New file created")
        
    def on_open(self, event):
        """Open file"""
        wildcard = "Assembly files (*.asm;*.s)|*.asm;*.s|All files (*.*)|*.*"
        dlg = wx.FileDialog(self, "Open Assembly File", wildcard=wildcard,
                           style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST)
        
        if dlg.ShowModal() == wx.ID_OK:
            path = dlg.GetPath()
            try:
                with open(path, 'r') as f:
                    content = f.read()
                self.editor.SetText(content)
                self.current_file = path
                self.SetTitle(f"RISC-V Simulator - {os.path.basename(path)}")
                self.SetStatusText(f"Opened: {path}")
            except Exception as e:
                wx.MessageBox(f"Error opening file: {e}", "Error", wx.OK | wx.ICON_ERROR)
        
        dlg.Destroy()
        
    def on_save(self, event):
        """Save file"""
        if self.current_file:
            try:
                with open(self.current_file, 'w') as f:
                    f.write(self.editor.GetText())
                self.editor.SetSavePoint()
                self.SetStatusText(f"Saved: {self.current_file}")
            except Exception as e:
                wx.MessageBox(f"Error saving file: {e}", "Error", wx.OK | wx.ICON_ERROR)
        else:
            self.on_save_as(None)
            
    def on_save_as(self, event):
        """Save file as"""
        wildcard = "Assembly files (*.asm)|*.asm|All files (*.*)|*.*"
        dlg = wx.FileDialog(self, "Save Assembly File", wildcard=wildcard,
                           style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT)
        
        if dlg.ShowModal() == wx.ID_OK:
            path = dlg.GetPath()
            try:
                with open(path, 'w') as f:
                    f.write(self.editor.GetText())
                self.current_file = path
                self.editor.SetSavePoint()
                self.SetTitle(f"RISC-V Simulator - {os.path.basename(path)}")
                self.SetStatusText(f"Saved: {path}")
            except Exception as e:
                wx.MessageBox(f"Error saving file: {e}", "Error", wx.OK | wx.ICON_ERROR)
        
        dlg.Destroy()
        
    def on_exit(self, event):
        """Exit application"""
        if self.editor.GetModify():
            dlg = wx.MessageDialog(self, "Save changes before exiting?", "Unsaved Changes",
                                  wx.YES_NO | wx.CANCEL | wx.ICON_QUESTION)
            result = dlg.ShowModal()
            dlg.Destroy()
            
            if result == wx.ID_YES:
                self.on_save(None)
            elif result == wx.ID_CANCEL:
                return
        
        self.Close()
        
    def on_run(self, event):
        """Run simulation"""
        # Save to temporary file
        temp_file = Path("temp_simulation.asm")
        try:
            with open(temp_file, 'w') as f:
                f.write(self.editor.GetText())
        except Exception as e:
            wx.MessageBox(f"Error creating temporary file: {e}", "Error", wx.OK | wx.ICON_ERROR)
            return
        
        # Clear output
        self.output_panel.clear()
        self.output_panel.append_text("="*80 + "\n")
        self.output_panel.append_text("Starting simulation...\n")
        self.output_panel.append_text("="*80 + "\n\n")
        
        # Run in thread to avoid blocking UI
        thread = threading.Thread(target=self.run_simulation, args=(temp_file,))
        thread.daemon = True
        thread.start()
        
        self.SetStatusText("Running simulation...")
        
    def run_simulation(self, asm_file):
        """Run the simulation (in separate thread)"""
        try:
            # Capture output
            output_buffer = io.StringIO()
            
            with redirect_stdout(output_buffer), redirect_stderr(output_buffer):
                # Create simulator
                sim = RISCVSimulator()
                
                # Load program
                success = sim.load_program(str(asm_file))
                if not success:
                    wx.CallAfter(self.output_panel.append_text, "\nError: Failed to load program\n")
                    wx.CallAfter(self.SetStatusText, "Simulation failed")
                    return
                
                # Run simulation
                try:
                    sim.run(max_instructions=10000)
                except Exception as e:
                    if "ECALL" not in str(e) and "HALT" not in str(e):
                        wx.CallAfter(self.output_panel.append_text, f"\nError during execution: {e}\n")
                
                # Store simulator reference
                self.simulator = sim
            
            # Get output
            output = output_buffer.getvalue()
            
            # Update UI in main thread
            wx.CallAfter(self.output_panel.append_text, output)
            wx.CallAfter(self.output_panel.append_text, "\n" + "="*80 + "\n")
            wx.CallAfter(self.output_panel.append_text, "Simulation complete!\n")
            wx.CallAfter(self.output_panel.append_text, "="*80 + "\n")
            
            # Update registers
            if sim.regs:
                registers = {}
                for i in range(32):
                    reg_name = f"X{i}"
                    registers[reg_name] = sim.regs[reg_name]
                wx.CallAfter(self.register_panel.update_registers, registers)
            
            wx.CallAfter(self.SetStatusText, "Simulation complete")
            
        except Exception as e:
            wx.CallAfter(self.output_panel.append_text, f"\nFatal error: {e}\n")
            wx.CallAfter(self.SetStatusText, "Simulation error")
        
    def on_stop(self, event):
        """Stop simulation (not implemented for now)"""
        wx.MessageBox("Stop functionality not yet implemented", "Info", wx.OK | wx.ICON_INFORMATION)
        
    def on_clear_output(self, event):
        """Clear output panel"""
        self.output_panel.clear()
        
    def load_example(self, example_type):
        """Load example code"""
        examples = {
            "arithmetic": """# Basic Arithmetic Example
.data

.text
main:
    # Load immediate values
    addi x1, x0, 10      # x1 = 10
    addi x2, x0, 20      # x2 = 20
    
    # Addition
    add x3, x1, x2       # x3 = x1 + x2 = 30
    
    # Subtraction
    sub x4, x2, x1       # x4 = x2 - x1 = 10
    
    # Multiplication (if MUL supported)
    mul x5, x1, x2       # x5 = x1 * x2 = 200
    
    # Division (if DIV supported)
    div x6, x2, x1       # x6 = x2 / x1 = 2
    
    # Exit
    addi x10, x0, 93
    ecall
""",
            "loops": """# Loop Example - Sum 1 to 10
.data

.text
main:
    addi x1, x0, 1       # counter = 1
    addi x2, x0, 10      # limit = 10
    addi x3, x0, 0       # sum = 0
    
loop:
    add x3, x3, x1       # sum += counter
    addi x1, x1, 1       # counter++
    
    # Check if counter <= limit
    blt x1, x2, loop     # if counter < limit, continue
    beq x1, x2, loop     # if counter == limit, do once more
    
    # Result in x3 should be 55 (1+2+3+...+10)
    
    # Exit
    addi x10, x0, 93
    ecall
""",
            "functions": """# Function Call Example
.data

.text
main:
    # Prepare arguments
    addi x10, x0, 5      # a0 = 5
    addi x11, x0, 7      # a1 = 7
    
    # Call function
    jal x1, add_function
    
    # Result in x10 (a0)
    
    # Exit
    addi x10, x0, 93
    ecall

add_function:
    # Add two numbers
    add x10, x10, x11    # a0 = a0 + a1
    
    # Return
    jalr x0, x1, 0
""",
            "memory": """# Memory Operations Example
.data
    value1: .word 42
    value2: .word 100
    array: .word 1, 2, 3, 4, 5

.text
main:
    # Load upper immediate to get data segment address
    lui x1, 0x10000
    
    # Load word from memory
    lw x2, 0(x1)         # Load value1 (42)
    lw x3, 4(x1)         # Load value2 (100)
    
    # Store to memory
    addi x4, x0, 999
    sw x4, 8(x1)         # Store 999 to array[0]
    
    # Load it back
    lw x5, 8(x1)         # Should be 999
    
    # Load byte
    lb x6, 0(x1)         # Load byte from value1
    
    # Exit
    addi x10, x0, 93
    ecall
"""
        }
        
        if example_type in examples:
            self.editor.SetText(examples[example_type])
            self.current_file = None
            self.SetTitle(f"RISC-V Simulator - {example_type.title()} Example")
            self.SetStatusText(f"Loaded {example_type} example")
        
    def on_about(self, event):
        """Show about dialog"""
        info = wx.adv.AboutDialogInfo()
        info.SetName("RISC-V Simulator")
        info.SetVersion("1.0")
        info.SetDescription("A graphical RISC-V assembly simulator with syntax highlighting\n"
                          "and register visualization.")
        info.SetWebSite("https://github.com/ahmedfarid59/risc-v-simulator")
        info.AddDeveloper("RISC-V Simulator Team")
        
        wx.adv.AboutBox(info)
        
    def on_help(self, event):
        """Show help dialog"""
        help_text = """RISC-V Simulator Help

SUPPORTED INSTRUCTIONS:
- Arithmetic: ADD, ADDI, SUB, MUL, DIV, REM
- Logical: AND, ANDI, OR, ORI, XOR, XORI
- Shift: SLL, SLLI, SRL, SRLI, SRA, SRAI
- Comparison: SLT, SLTI, SLTU, SLTIU
- Branch: BEQ, BNE, BLT, BLTU, BGE, BGEU
- Jump: J, JAL, JALR
- Load: LB, LBU, LH, LHU, LW
- Store: SB, SH, SW
- Upper Immediate: LUI, AUIPC
- Pseudo: LI, LA, MV, NEG, NOT, RET

ASSEMBLY FORMAT:
.data
    variable_name: .word value
    string_name: .asciz "text"
    
.text
main:
    instruction rd, rs1, rs2
    instruction rd, rs1, immediate
    
KEYBOARD SHORTCUTS:
- Ctrl+N: New file
- Ctrl+O: Open file
- Ctrl+S: Save file
- Ctrl+Shift+S: Save As
- F5: Run simulation
- Ctrl+L: Clear output
- F1: Show this help

REGISTER NAMES:
- x0-x31: General purpose registers
- ABI names: zero, ra, sp, gp, tp, t0-t6, s0-s11, a0-a7
"""
        
        dlg = wx.MessageDialog(self, help_text, "Help", wx.OK | wx.ICON_INFORMATION)
        dlg.ShowModal()
        dlg.Destroy()


class SimulatorApp(wx.App):
    """Main application class"""
    
    def OnInit(self):
        self.frame = SimulatorFrame()
        self.frame.Show()
        return True


def main():
    """Main entry point"""
    app = SimulatorApp()
    app.MainLoop()


if __name__ == '__main__':
    main()
