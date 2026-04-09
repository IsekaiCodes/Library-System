# BCI Campus Library Management System

A professional, feature-rich library management system built with Python and Tkinter, designed for campus libraries. This system manages book inventory, student memberships, and borrowing/returning processes with an intuitive GUI and persistent data storage.

## 🎯 Features

### For Librarians
- **Inventory Management**
  - Add new books to the library catalog
  - Delete books from inventory
  - View complete book listing with ISBN, title, author, and availability status
  
- **Member Registration**
  - Register new student members
  - Auto-generate unique library card IDs (format: BCI-YYYY-NNNN)
  - Assign initial passwords for students
  - View all registered members and their details.

### For Students
- **Book Browsing**
  - Browse all available books in the library catalog
  - View book details (ISBN, title, author)
  - Real-time availability updates

- **Borrowing System**
  - Borrow available books with one click
  - View your borrowed books list
  - Return books when finished

### General Features
- **User Authentication**
  - Secure login system with username/password
  - Role-based access control (Librarian vs Student)
  - Session management

- **Data Persistence**
  - All data stored in JSON format
  - Automatic data backup on every transaction
  - Loads previous data on application startup

- **Animated UI**
  - Flying books animation on the header
  - Modern dark theme with color-coded interface
  - Responsive design with tabbed interface for librarians

- **Object-Oriented Design**
  - Clean separation of concerns (Models, Database, GUI)
  - Inheritance and polymorphism for user roles
  - Encapsulation of business logic

## 📋 System Architecture

### Classes

#### Models
- **Book**: Represents a book with ISBN, title, author, and availability status
- **User**: Base class for all users with authentication
- **Student**: Inherits from User, manages borrowed books
- **Librarian**: Inherits from User, has administrative privileges

#### Database
- **LibraryDatabase**: Manages JSON file persistence and data loading/saving

#### GUI
- **LibraryApp**: Main application controller with login, librarian, and student interfaces

## 🚀 Getting Started

### Prerequisites
- Python 3.7 or higher
- tkinter (usually included with Python)

### Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/Library-System.git
cd Library-System
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
python main.py
```

## 📖 Usage Guide

### 🚀 Enhanced First-Time Login Experience (New!)
The login screen now features:
- **Welcome message** with first-time guidance
- **Toggleable default credential hints** (click "👁️ Show Default Credentials")
- **Smart placeholders** in input fields
- **Visual improvements**: Icons, hover effects, focus highlights
- **Success feedback** on login

### First Login
Use the default credentials to test the system (also shown in-app):

| Role | Username | Password |
|------|----------|----------|
| Librarian | admin | 123 |
| Student | dinith | 2002 |

### Librarian Workflow

1. **Login** with admin credentials
2. **Inventory Management Tab**
   - View all books
   - Click "+ Add New Book" to add new books
   - Select a book and click "Delete Selected" to remove it
3. **Member Registration Tab**
   - Enter student name and password
   - Click "Generate Member Card" to create new student account
   - Students receive an auto-generated Library Card ID

### Student Workflow

1. **Login** with your student credentials
2. **Browse Books** in the Library Catalog (left panel)
3. **Borrow Books** by selecting a book and clicking "Borrow Selected Book"
4. **View Borrowed Books** in the "Your Borrowed Items" panel (right side)
5. **Return Books** by selecting from your borrowed list and clicking "Return Selected"

## 💾 Data Storage

The system uses a JSON file (`bci_library_data.json`) to store:
- All registered users with credentials and roles
- Complete book inventory
- Borrowed books per student
- System configuration (next member ID to assign)

**Note:** The JSON file is automatically created on first run with default data.

## 🎨 UI Theme

The application features a modern dark theme:
- **Background**: Dark navy (#1e1e2f)
- **Accent**: Deep gray (#3d3d5c)
- **Highlight**: Bright green (#2ed573)
- **Buttons**: Red (#ff4757)
- **Text**: White (#ffffff)

## 🔒 Security Features

- User authentication before accessing any features
- Role-based access control (RBAC)
- Password storage for login verification
- Session management to track current user

## 🛠️ Technical Stack

- **Language**: Python 3.7+
- **GUI Framework**: Tkinter
- **Database**: JSON (file-based)
- **Design Patterns**: MVC (Model-View-Controller), OOP

## 📁 Project Structure

```
Library-System/
├── main.py                      # Main application file
├── config.py                    # Configuration settings
├── requirements.txt             # Project dependencies
├── README.md                    # This file
├── LICENSE                      # MIT License
└── bci_library_data.json        # Database (auto-generated)
```

## 🔄 API/Methods Overview

### LibraryDatabase
- `_load_data()`: Load data from JSON file
- `save()`: Save current data to JSON file

### LibraryApp
- `show_login()`: Display login interface
- `handle_login()`: Process login credentials
- `show_librarian_dashboard()`: Display librarian interface
- `show_student_dashboard()`: Display student interface
- `refresh_books()`: Update book list display
- `refresh_members()`: Update member list display
- `borrow_book()`: Record book borrowing
- `return_book()`: Record book return

## 🐛 Troubleshooting

### Application won't start
- Ensure Python 3.7+ is installed
- Verify tkinter is installed: `python -m tkinter`
- Check that you're in the correct directory

### Data loss
- The system saves data automatically after each action
- Check for `bci_library_data.json` file in the project directory
- Never delete this file unless you want to reset the system

### Login fails
- Default credentials: admin/123 (Librarian) or dinith/2002 (Student)
- Create new student accounts using the librarian dashboard

## 🎓 Learning Outcomes

This project demonstrates:
- ✅ Object-Oriented Programming (OOP) concepts
- ✅ Inheritance and Polymorphism
- ✅ File I/O and JSON handling
- ✅ GUI development with Tkinter
- ✅ MVC architecture
- ✅ Data persistence
- ✅ User authentication
- ✅ Event-driven programming

## 📝 Future Enhancements

- [ ] Database migration to SQL (SQLite/MySQL)
- [ ] Email notifications for due dates
- [ ] Fine management system
- [ ] Book reservations
- [ ] User profile customization
- [ ] Search and filter functionality
- [ ] Book categories and classifications
- [ ] Barcode scanning support
- [ ] Multi-language support
- [ ] Dark/Light theme toggle

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👥 Authors

- **Dinith** - Initial development

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📞 Support

For issues, questions, or feature requests, please create an issue in the repository.

---

**Last Updated**: March 2026  
**Version**: 1.0.0  
**Status**: Production Ready ✅