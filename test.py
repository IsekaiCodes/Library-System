#!/usr/bin/env python3
"""
Test script to verify the Library Management System is working correctly
"""

import sys
import os
import json
from pathlib import Path

def print_header(text):
    print()
    print("=" * 60)
    print(text)
    print("=" * 60)

def test_imports():
    """Test if all required modules can be imported"""
    print_header("Testing Imports")
    
    tests = [
        ("tkinter", "Window UI framework"),
        ("json", "Data serialization"),
        ("os", "Operating system interface"),
        ("random", "Random number generation"),
        ("time", "Time management"),
    ]
    
    all_passed = True
    for module, description in tests:
        try:
            __import__(module)
            print(f"✓ {module:12} - {description}")
        except ImportError as e:
            print(f"✗ {module:12} - {description}: {e}")
            all_passed = False
    
    return all_passed

def test_file_structure():
    """Test if all required files exist"""
    print_header("Testing File Structure")
    
    required_files = [
        "main.py",
        "config.py",
        "requirements.txt",
        "README.md",
        "LICENSE",
        ".gitignore",
    ]
    
    all_passed = True
    for filename in required_files:
        filepath = Path(filename)
        if filepath.exists():
            size = filepath.stat().st_size
            print(f"✓ {filename:20} ({size:,} bytes)")
        else:
            print(f"✗ {filename:20} - FILE NOT FOUND")
            all_passed = False
    
    return all_passed

def test_syntax():
    """Test if main.py has valid Python syntax"""
    print_header("Testing Python Syntax")
    
    try:
        with open("main.py", "r") as f:
            code = f.read()
        compile(code, "main.py", "exec")
        print("✓ main.py has valid Python syntax")
        return True
    except SyntaxError as e:
        print(f"✗ Syntax error in main.py: {e}")
        return False

def test_config():
    """Test if config.py can be imported"""
    print_header("Testing Configuration")
    
    try:
        import config
        
        # Check for important config properties
        properties = [
            "DATABASE_FILE",
            "WINDOW_TITLE",
            "COLOR_BG",
            "ANIMATION_FRAME_RATE",
            "DEFAULT_ADMIN_USER",
            "DEFAULT_BOOKS",
        ]
        
        all_passed = True
        for prop in properties:
            if hasattr(config, prop):
                value = getattr(config, prop)
                print(f"✓ config.{prop:30} = {str(value)[:30]}...")
            else:
                print(f"✗ config.{prop:30} - NOT FOUND")
                all_passed = False
        
        return all_passed
    except Exception as e:
        print(f"✗ Error loading config: {e}")
        return False

def test_database():
    """Test if database can be initialized"""
    print_header("Testing Database Initialization")
    
    try:
        from main import LibraryDatabase
        db = LibraryDatabase()
        
        print(f"✓ Database loaded successfully")
        print(f"  - Books in catalog: {len(db.data.get('books', []))}")
        print(f"  - Registered users: {len(db.data.get('users', []))}")
        print(f"  - Next member ID: {db.data.get('config', {}).get('next_id', 'N/A')}")
        
        # Verify database structure
        required_keys = ["books", "users", "config"]
        all_passed = True
        for key in required_keys:
            if key in db.data:
                print(f"✓ Database contains '{key}' section")
            else:
                print(f"✗ Database missing '{key}' section")
                all_passed = False
        
        return all_passed
    except Exception as e:
        print(f"✗ Error testing database: {e}")
        return False

def test_models():
    """Test if all model classes can be instantiated"""
    print_header("Testing Model Classes")
    
    try:
        from main import Book, User, Student, Librarian
        
        # Test Book
        book = Book("TEST-001", "Test Book", "Test Author")
        print(f"✓ Book model instantiated: {book.title}")
        
        # Test Student
        student = Student("testuser", "password", "BCI-2026-0001")
        print(f"✓ Student model instantiated: {student.username} ({student.role})")
        
        # Test Librarian
        librarian = Librarian("admin", "password")
        print(f"✓ Librarian model instantiated: {librarian.username} ({librarian.role})")
        
        return True
    except Exception as e:
        print(f"✗ Error testing models: {e}")
        return False

def main():
    """Run all tests"""
    print("\n")
    print("█" * 60)
    print("█  BCI LIBRARY MANAGEMENT SYSTEM - TEST SUITE           █")
    print("█" * 60)
    
    results = {
        "Imports": test_imports(),
        "File Structure": test_file_structure(),
        "Python Syntax": test_syntax(),
        "Configuration": test_config(),
        "Database": test_database(),
        "Models": test_models(),
    }
    
    # Summary
    print_header("Test Summary")
    
    passed = sum(1 for v in results.values() if v)
    total = len(results)
    
    for test_name, result in results.items():
        status = "✓ PASSED" if result else "✗ FAILED"
        print(f"{test_name:20} {status}")
    
    print()
    print(f"Overall: {passed}/{total} test groups passed")
    
    if passed == total:
        print()
        print("✓ All tests passed! The system is ready to use.")
        print()
        print("To run the application, execute:")
        print("  python main.py")
        print("  or")
        print("  python run.py")
        return 0
    else:
        print()
        print("✗ Some tests failed. Please fix the issues above.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
