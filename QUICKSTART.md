## 🚀 Quick Start Guide

### Quick Installation & Run

**Windows:**
```bash
python main.py
```

**Linux/Mac:**
```bash
python3 main.py
```

### Default Login Credentials

| Role | Username | Password |
|------|----------|----------|
| **Librarian** | `admin` | `123` |
| **Student** | `dinith` | `2002` |

---

## 📖 What You Can Do

### As a Librarian
1. Log in with `admin` / `123`
2. **Add Books:** Go to "Inventory Management" → Click "+ Add New Book"
3. **Delete Books:** Select book → Click "Delete Selected"
4. **Register Students:** Go to "Member Registration" → Enter name/password → "Generate Member Card"

### As a Student
1. Log in with `dinith` / `2002`
2. **Browse Books:** Left side shows available books
3. **Borrow:** Select book → "Borrow Selected Book"
4. **Return:** Select from "Your Borrowed Items" → "Return Selected"

---

## 🔧 Testing the System

To run the test suite:
```bash
python test.py
```

---

## 💾 Data

- Database file: `bci_library_data.json` (auto-created on first run)
- All data is automatically saved after each action
- To reset, delete `bci_library_data.json` and restart

---

## 📁 Project Files

```
Library-System/
├── main.py              Main application (run this!)
├── config.py            Configuration settings
├── run.py               Alternative launcher with error handling
├── test.py              Test suite
├── requirements.txt     Dependencies
├── README.md            Full documentation
├── QUICKSTART.md        This file
├── LICENSE              MIT License
└── .gitignore           Git ignore file
```

---

## ⚡ Keyboard Shortcuts

- **Enter** in login: Submit login
- **Tab**: Navigate between fields
- **Click** on book/member: Select item
- **Buttons**: All actions are button-based

---

## ❓ Common Issues & Solutions

| Problem | Solution |
|---------|----------|
| "No module named tkinter" | Install tkinter: `pip install tk` |
| Window appears blank | Wait for animation to load, it's loading data |
| Cannot login | Check credentials (case-sensitive) or create new student |
| Can't add books | Log in as Librarian (admin/123) first |

---

## 📞 Need Help?

1. Check [README.md](README.md) for full documentation
2. Run `python test.py` to diagnose issues
3. Use `python run.py` for detailed error messages

---

**Enjoy your Library Management System!** 📚✨
