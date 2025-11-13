#!/usr/bin/env python3
"""
Main entry point for RISC-V Simulator CLI
"""
import sys
import os

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

if __name__ == '__main__':
    from src.main_real import main
    main()
