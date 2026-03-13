#!/usr/bin/env python3
"""
Quick startup script for the BCI Library Management System
Run this script to launch the application with error handling
"""

import sys
import os
import traceback

try:
    print("=" * 60)
    print("BCI CAMPUS - LIBRARY MANAGEMENT SYSTEM")
    print("=" * 60)
    print()
    
    # Check Python version
    if sys.version_info < (3, 7):
        print("❌ Error: Python 3.7 or higher is required.")
        print(f"   Your version: {sys.version}")
        sys.exit(1)
    
    print(f"✓ Python version: {sys.version.split()[0]}")
    
    # Check for tkinter
    try:
        import tkinter as tk
        print("✓ Tkinter is available")
    except ImportError:
        print("❌ Error: Tkinter is not installed.")
        print("   Install it with: pip install tk")
        sys.exit(1)
    
    print()
    print("Starting application...")
    print()
    
    # Import and run the main application
    from main import LibraryApp
    
    root = tk.Tk()
    app = LibraryApp(root)
    root.mainloop()
    
except Exception as e:
    print()
    print("=" * 60)
    print("❌ ERROR OCCURRED")
    print("=" * 60)
    print()
    print(f"Error Type: {type(e).__name__}")
    print(f"Error Message: {str(e)}")
    print()
    print("Full Traceback:")
    print("-" * 60)
    traceback.print_exc()
    print("-" * 60)
    print()
    print("Please check the error above and ensure:")
    print("  1. All files are in the correct directory")
    print("  2. Python 3.7+ is installed")
    print("  3. Tkinter is available")
    print()
    sys.exit(1)
