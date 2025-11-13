#!/usr/bin/env python3
"""
Main entry point for RISC-V Simulator GUI
"""
import sys
import os

# Add project root to path
sys.path.insert(0, os.path.dirname(__file__))

if __name__ == '__main__':
    from gui.gui_simulator import main
    main()
