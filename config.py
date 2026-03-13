"""
Configuration settings for the Library Management System
"""

# Database Configuration
DATABASE_FILE = "bci_library_data.json"

# UI Configuration
WINDOW_TITLE = "BCI Campus - Library Management System"
WINDOW_WIDTH = 900
WINDOW_HEIGHT = 700
WINDOW_MIN_WIDTH = 800
WINDOW_MIN_HEIGHT = 600

# Color Scheme
COLOR_BG = "#1e1e2f"
COLOR_ACCENT = "#3d3d5c"
COLOR_TEXT = "#ffffff"
COLOR_BTN = "#ff4757"
COLOR_HIGHLIGHT = "#2ed573"
COLOR_ERROR = "#e74c3c"

# Animation Configuration
ANIMATION_FRAME_RATE = 30  # milliseconds
NUM_FLYING_BOOKS = 8
BOOK_COLORS = ["#ff6b6b", "#4ecdc4", "#ffe66d", "#1a5f7a", "#ff9ff3", "#00d2d3"]

# Default Users
DEFAULT_ADMIN_USER = {
    "username": "admin",
    "password": "123",
    "role": "Librarian",
    "member_id": "STAFF-001"
}

DEFAULT_TEST_USER = {
    "username": "dinith",
    "password": "2002",
    "role": "Student",
    "member_id": "BCI-2026-0001",
    "borrowed_books": []
}

# Default Books
DEFAULT_BOOKS = [
    {
        "isbn": "101",
        "title": "Python for Beginners",
        "author": "Guido van Rossum",
        "available": True
    },
    {
        "isbn": "102",
        "title": "Data Science 101",
        "author": "BCI Faculty",
        "available": True
    },
    {
        "isbn": "103",
        "title": "History of Sri Lanka",
        "author": "Anonymous",
        "available": True
    }
]

# ID Generation
INSTITUTION_CODE = "BCI"
YEAR = "2026"
