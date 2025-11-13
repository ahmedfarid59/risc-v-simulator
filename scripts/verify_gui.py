#!/usr/bin/env python3
"""
Demo script to verify RISC-V Simulator GUI functionality
Tests basic features without launching full GUI
"""
import sys
import os

def test_imports():
    """Test that all required modules can be imported"""
    print("Testing imports...")
    
    try:
        import wx
        print("✓ wxPython imported successfully")
    except ImportError as e:
        print(f"✗ Failed to import wxPython: {e}")
        return False
    
    try:
        import wx.stc
        print("✓ wx.stc imported successfully")
    except ImportError as e:
        print(f"✗ Failed to import wx.stc: {e}")
        return False
    
    try:
        sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
        from src.main_real import RISCVSimulator
        print("✓ RISCVSimulator imported successfully")
    except ImportError as e:
        print(f"✗ Failed to import RISCVSimulator: {e}")
        return False
    
    return True

def test_simulator():
    """Test basic simulator functionality"""
    print("\nTesting simulator...")
    
    try:
        sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
        from src.main_real import RISCVSimulator
        import tempfile
        
        # Create a simple test program
        test_program = """
.text
main:
    addi x1, x0, 10
    addi x2, x0, 20
    add x3, x1, x2
    addi x10, x0, 93
    ecall
"""
        
        # Write to temp file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.asm', delete=False) as f:
            f.write(test_program)
            temp_file = f.name
        
        # Create simulator and run
        sim = RISCVSimulator()
        success = sim.load_program(temp_file)
        
        if not success:
            print("✗ Failed to load program")
            return False
        
        print("✓ Program loaded successfully")
        
        # Run simulation
        try:
            sim.run(max_instructions=100)
        except Exception as e:
            if "ECALL" not in str(e):
                print(f"✗ Simulation error: {e}")
                return False
        
        print("✓ Simulation completed")
        
        # Check results
        if sim.regs['X1'] == 10 and sim.regs['X2'] == 20 and sim.regs['X3'] == 30:
            print("✓ Register values correct (x1=10, x2=20, x3=30)")
        else:
            print(f"✗ Register values incorrect (x1={sim.regs['X1']}, x2={sim.regs['X2']}, x3={sim.regs['X3']})")
            return False
        
        # Cleanup
        os.unlink(temp_file)
        
        return True
        
    except Exception as e:
        print(f"✗ Simulator test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Run all tests"""
    print("="*60)
    print("RISC-V Simulator GUI - Verification Test")
    print("="*60)
    
    all_passed = True
    
    # Test imports
    if not test_imports():
        all_passed = False
    
    # Test simulator
    if not test_simulator():
        all_passed = False
    
    print("\n" + "="*60)
    if all_passed:
        print("✓ All tests passed! GUI is ready to use.")
        print("\nTo launch the GUI, run:")
        print("  python gui_simulator.py")
        print("  or")
        print("  run_gui.bat (Windows)")
    else:
        print("✗ Some tests failed. Please check the errors above.")
        print("\nTo install dependencies:")
        print("  pip install -r requirements.txt")
    print("="*60)
    
    return 0 if all_passed else 1

if __name__ == '__main__':
    sys.exit(main())
