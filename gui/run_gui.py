#!/usr/bin/env python3
"""
Simple launcher script for RISC-V Simulator GUI
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from gui.gui_simulator import main

if __name__ == '__main__':
    main()
