import tkinter as tk
from tkinter import messagebox, ttk
import json
import os
import random
import time
import config  # Import config for DEFAULT_CREDENTIALS

# --- MODELS (OOP Concepts) ---

class Book:
    """Encapsulates book data."""
    def __init__(self, isbn, title, author, available=True):
        self.isbn = isbn
        self.title = title
        self.author = author
        self.available = available

    def to_dict(self):
        return self.__dict__

class User:
    """Base class for all users (Abstraction & Inheritance)."""
    def __init__(self, username, password, role, member_id=None):
        self.username = username
        self.password = password
        self.role = role
        self.member_id = member_id

    def to_dict(self):
        return {
            "username": self.username,
            "password": self.password,
            "role": self.role,
            "member_id": self.member_id
        }

class Student(User):
    """Inherits from User, specifically for students."""
    def __init__(self, username, password, member_id, borrowed_books=None):
        super().__init__(username, password, "Student", member_id)
        self.borrowed_books = borrowed_books if borrowed_books else []

    def to_dict(self):
        data = super().to_dict()
        data["borrowed_books"] = self.borrowed_books
        return data

class Librarian(User):
    """Inherits from User, specifically for staff."""
    def __init__(self, username, password, member_id="STAFF-ADMIN"):
        super().__init__(username, password, "Librarian", member_id)

# --- DATABASE LOGIC ---

class LibraryDatabase:
    """Manages data persistence using JSON."""
    def __init__(self, filename="bci_library_data.json"):
        self.filename = filename
        self.data = self._load_data()

    def _load_data(self):
        if os.path.exists(self.filename):
            try:
                with open(self.filename, 'r') as f:
                    return json.load(f)
            except:
                pass
        
        # Default starting data
        return {
            "books": config.DEFAULT_BOOKS,
            "users": [
                config.DEFAULT_ADMIN_USER,
                config.DEFAULT_TEST_USER
            ],
            "config": {"next_id": 2}
        }

    def save(self):
        with open(self.filename, 'w') as f:
            json.dump(self.data, f, indent=4)

# --- GUI INTERFACE ---

class LibraryApp:
    def __init__(self, root):
        self.root = root
        self.root.title(config.WINDOW_TITLE)
        self.root.geometry(f"{config.WINDOW_WIDTH}x{config.WINDOW_HEIGHT}")
        self.root.minsize(config.WINDOW_MIN_WIDTH, config.WINDOW_MIN_HEIGHT)
        
        self.db = LibraryDatabase()
        self.current_user = None
        
        # UI Colors from config
        self.color_bg = config.COLOR_BG
        self.color_accent = config.COLOR_ACCENT
        self.color_text = config.COLOR_TEXT
        self.color_btn = config.COLOR_BTN
        self.color_highlight = config.COLOR_HIGHLIGHT

        self.root.configure(bg=self.color_bg)

        # --- ANIMATION SETUP ---
        self.canvas = tk.Canvas(self.root, height=150, bg=self.color_bg, highlightthickness=0)
        self.canvas.pack(fill="x")
        self.flying_books = []
        self.init_flying_books()

        # --- MAIN CONTAINER ---
        self.main_container = tk.Frame(self.root, bg=self.color_bg)
        self.main_container.pack(fill="both", expand=True)
        
        self.show_login()
        self.animate_loop()

    # --- ANIMATION ENGINE ---
    def init_flying_books(self):
        colors = config.BOOK_COLORS
        for _ in range(config.NUM_FLYING_BOOKS):
            x = random.randint(0, 900)
            y = random.randint(20, 100)
            speed = random.uniform(1.5, 4.0)
            
            # Draw a "book" shape (rectangle + lines for pages)
            book_body = self.canvas.create_rectangle(x, y, x+40, y+55, fill=random.choice(colors), outline="white", width=2)
            book_line = self.canvas.create_line(x+5, y+5, x+5, y+50, fill="white")
            
            self.flying_books.append({
                "body": book_body,
                "line": book_line,
                "speed": speed,
                "tilt": 0
            })

    def animate_loop(self):
        for book in self.flying_books:
            self.canvas.move(book["body"], book["speed"], 0)
            self.canvas.move(book["line"], book["speed"], 0)
            
            pos = self.canvas.coords(book["body"])
            
            # If book goes off screen, reset to left
            if pos[0] > 950:
                self.canvas.coords(book["body"], -60, pos[1], -20, pos[3])
                self.canvas.coords(book["line"], -55, pos[1]+5, -55, pos[3]-5)
        
        self.root.after(config.ANIMATION_FRAME_RATE, self.animate_loop)

    def clear_screen(self):
        for widget in self.main_container.winfo_children():
            widget.destroy()

    # --- NEW HELPER METHODS FOR USER-FRIENDLY LOGIN ---
    def setup_entry_placeholder(self, entry, placeholder):
        """Set placeholder text for entry."""
        entry.insert(0, placeholder)
        entry.bind('<FocusIn>', lambda e: e.widget.delete(0, tk.END) if e.widget.get() == placeholder else None)
        entry.bind('<FocusOut>', lambda e: e.widget.insert(0, placeholder) if not e.widget.get() else None)

    def toggle_credential_hint(self):
        """Toggle visibility of credential hint frame."""
        if hasattr(self, 'hint_frame') and self.hint_frame.winfo_ismapped():
            self.hint_frame.pack_forget()
            self.hint_btn.config(text="👁️ Show Default Credentials")
        else:
            self.show_credential_hint()
            self.hint_btn.config(text="🙈 Hide Credentials")

    def show_credential_hint(self):
        """Display default credentials hint."""
        self.hint_frame = tk.LabelFrame(self.login_frame, text="First Time? Use These Defaults", 
                                        font=("Arial", 10, "bold"), fg=self.color_highlight, 
                                        bg=self.color_accent, relief="ridge", padx=15, pady=10)
        self.hint_frame.pack(pady=10, fill="x")
        
        hint_text = tk.Text(self.hint_frame, height=4, bg="#2c2c44", fg=self.color_text, font=("Courier", 10), 
                            wrap="word", state="normal", borderwidth=0)
        hint_text.pack(fill="x", pady=5)
        
        creds_info = "Librarian: admin / 123\nStudent:  dinith / 2002\n\n💡 Dismiss after use."
        hint_text.insert("1.0", creds_info)
        hint_text.config(state="disabled")

    # --- LOGIN INTERFACE (ENHANCED) ---
    def show_login(self):
        self.clear_screen()
        
        self.login_frame = tk.Frame(self.main_container, bg=self.color_accent, padx=50, pady=50, relief="raised", bd=2)
        self.login_frame.place(relx=0.5, rely=0.45, anchor="center")

        # Welcome Messages
        welcome_title = tk.Label(self.login_frame, text="🌟 Welcome to BCI Campus Library!", 
                                 font=("Helvetica", 22, "bold"), fg=self.color_highlight, bg=self.color_accent)
        welcome_title.pack(pady=(0, 5))
        
        welcome_sub = tk.Label(self.login_frame, text="First time logging in? Check default credentials below or register as Librarian to add students.", 
                               font=("Arial", 11), fg=self.color_text, bg=self.color_accent, wraplength=500)
        welcome_sub.pack(pady=(0, 25))

        # Username
        tk.Label(self.login_frame, text="👤 Username", fg=self.color_text, bg=self.color_accent, 
                 font=("Arial", 11, "bold")).pack(anchor="w")
        self.ent_user = tk.Entry(self.login_frame, font=("Arial", 12), width=32, bg="#2c2c44", fg="white", 
                                 insertbackground="white", borderwidth=0, relief="solid", bd=1)
        self.ent_user.pack(pady=5, fill="x")
        self.setup_entry_placeholder(self.ent_user, "Enter username...")

        # Password
        tk.Label(self.login_frame, text="🔒 Password", fg=self.color_text, bg=self.color_accent, 
                 font=("Arial", 11, "bold")).pack(anchor="w", pady=(15, 0))
        self.ent_pass = tk.Entry(self.login_frame, font=("Arial", 12), width=32, show="*", bg="#2c2c44", fg="white", 
                                 insertbackground="white", borderwidth=0, relief="solid", bd=1)
        self.ent_pass.pack(pady=5, fill="x")
        self.setup_entry_placeholder(self.ent_pass, "Enter password...")

        # Buttons Frame
        btn_frame = tk.Frame(self.login_frame, bg=self.color_accent)
        btn_frame.pack(pady=25)

        self.login_btn = tk.Button(btn_frame, text="🚀 LOGIN", font=("Arial", 13, "bold"), bg=self.color_btn, fg="white", 
                                   activebackground="#ff6b81", cursor="hand2", command=self.handle_login, 
                                   width=22, height=2, relief="raised", bd=2)
        self.login_btn.pack(side="left", padx=(0, 10))

        self.hint_btn = tk.Button(btn_frame, text="👁️ Show Default Credentials", font=("Arial", 10), 
                                  bg=self.color_highlight, fg="black", command=self.toggle_credential_hint, 
                                  width=24, relief="raised", bd=2)
        self.hint_btn.pack(side="right")

        # Focus first entry
        self.ent_user.focus()

        # Style bindings for hover/focus
        def on_enter(e): e.widget.config(bg="#ff6b81")
        def on_leave(e): e.widget.config(bg=self.color_btn)
        def on_focus(e): e.widget.config(relief="sunken", bd=2)
        def on_unfocus(e): e.widget.config(relief="raised", bd=2)
        
        self.login_btn.bind("<Enter>", on_enter)
        self.login_btn.bind("<Leave>", on_leave)
        self.ent_user.bind("<FocusIn>", lambda e: setattr(self.ent_user, 'focused', True) or on_focus(e))
        self.ent_user.bind("<FocusOut>", lambda e: setattr(self.ent_user, 'focused', False) or on_unfocus(e))
        self.ent_pass.bind("<FocusIn>", lambda e: setattr(self.ent_pass, 'focused', True) or on_focus(e))
        self.ent_pass.bind("<FocusOut>", lambda e: setattr(self.ent_pass, 'focused', False) or on_unfocus(e))

    def handle_login(self):
        u = self.ent_user.get().strip()
        p = self.ent_pass.get().strip()
        
        # Clear placeholders if still there
        if u == "Enter username...": u = ""
        if p == "Enter password...": p = ""
        
        found = next((user for user in self.db.data["users"] if user["username"] == u and user["password"] == p), None)
        
        if found:
            role_msg = "Librarian" if found["role"] == "Librarian" else "Student"
            messagebox.showinfo("Login Successful!", f"Welcome back, {found['username']}!\n\nAccessing {role_msg} Dashboard...")
            self.current_user = found
            if found["role"] == "Librarian":
                self.show_librarian_dashboard()
            else:
                self.show_student_dashboard()
        else:
            messagebox.showerror("Login Failed", "❌ Invalid username or password.\n\n💡 Hint: Try admin/123 or dinith/2002")

    # --- LIBRARIAN DASHBOARD (unchanged) ---
    def show_librarian_dashboard(self):
        self.clear_screen()
        
        header = tk.Frame(self.main_container, bg=self.color_accent, pady=10)
        header.pack(fill="x")
        tk.Label(header, text=f"LIBRARIAN PORTAL | {self.current_user['username'].upper()}", fg=self.color_highlight, bg=self.color_accent, font=("Arial", 12, "bold")).pack(side="left", padx=20)
        tk.Button(header, text="Logout", command=self.show_login, bg="#e74c3c", fg="white", borderwidth=0).pack(side="right", padx=20)

        # Tabs for Books and Members
        style = ttk.Style()
        style.theme_use('clam')
        style.configure("TNotebook", background=self.color_bg, borderwidth=0)
        style.configure("TNotebook.Tab", background=self.color_accent, foreground="white", padding=[20, 10])
        style.map("TNotebook.Tab", background=[("selected", self.color_highlight)], foreground=[("selected", "black")])

        nb = ttk.Notebook(self.main_container)
        nb.pack(fill="both", expand=True, padx=20, pady=20)

        # Tab 1: Books
        book_tab = tk.Frame(nb, bg=self.color_bg)
        nb.add(book_tab, text="Inventory Management")
        self.setup_book_tab(book_tab)

        # Tab 2: Members
        member_tab = tk.Frame(nb, bg=self.color_bg)
        nb.add(member_tab, text="Member Registration")
        self.setup_member_tab(member_tab)

    def setup_book_tab(self, parent):
        cols = ("ISBN", "Title", "Author", "Status")
        self.book_tree = ttk.Treeview(parent, columns=cols, show="headings", height=12)
        for col in cols: self.book_tree.heading(col, text=col)
        self.book_tree.pack(fill="both", expand=True, pady=10)
        
        btn_frame = tk.Frame(parent, bg=self.color_bg)
        btn_frame.pack(fill="x")
        tk.Button(btn_frame, text="+ Add New Book", bg=self.color_highlight, command=self.add_book_ui).pack(side="left", padx=5)
        tk.Button(btn_frame, text="Delete Selected", bg="#ff4757", fg="white", command=self.delete_book).pack(side="left", padx=5)
        
        self.refresh_books()

    def setup_member_tab(self, parent):
        # Registration Form
        form_frame = tk.Frame(parent, bg=self.color_accent, padx=20, pady=20)
        form_frame.pack(side="left", fill="y", padx=10, pady=10)

        tk.Label(form_frame, text="REGISTER NEW STUDENT", font=("Arial", 12, "bold"), fg=self.color_highlight, bg=self.color_accent).pack(pady=10)
        
        tk.Label(form_frame, text="Full Name", bg=self.color_accent, fg="white").pack(anchor="w")
        self.reg_name = tk.Entry(form_frame, font=("Arial", 11)); self.reg_name.pack(fill="x", pady=5)
        
        tk.Label(form_frame, text="Initial Password", bg=self.color_accent, fg="white").pack(anchor="w")
        self.reg_pass = tk.Entry(form_frame, font=("Arial", 11)); self.reg_pass.pack(fill="x", pady=5)

        tk.Button(form_frame, text="Generate Member Card", bg=self.color_highlight, font=("Arial", 10, "bold"), 
                  command=self.register_member, pady=10).pack(fill="x", pady=20)

        # Member Table
        table_frame = tk.Frame(parent, bg=self.color_bg)
        table_frame.pack(side="right", fill="both", expand=True, padx=10, pady=10)
        
        cols = ("Card ID", "Username", "Role")
        self.mem_tree = ttk.Treeview(table_frame, columns=cols, show="headings")
        for col in cols: self.mem_tree.heading(col, text=col)
        self.mem_tree.pack(fill="both", expand=True)
        
        self.refresh_members()

    def register_member(self):
        name = self.reg_name.get().strip()
        pw = self.reg_pass.get().strip()
        
        if not name or not pw:
            messagebox.showwarning("Incomplete Data", "Please fill in all fields.")
            return
            
        # Automatic ID Generation
        count = self.db.data["config"]["next_id"]
        card_id = f"BCI-2026-{count:04d}"
        
        new_student = Student(name, pw, card_id)
        self.db.data["users"].append(new_student.to_dict())
        self.db.data["config"]["next_id"] += 1
        self.db.save()
        
        messagebox.showinfo("Success", f"Member Registered Successfully!\n\nLibrary Card ID: {card_id}")
        self.reg_name.delete(0, tk.END); self.reg_pass.delete(0, tk.END)
        self.refresh_members()

    def refresh_books(self):
        for i in self.book_tree.get_children(): self.book_tree.delete(i)
        for b in self.db.data["books"]:
            status = "Available" if b["available"] else "Borrowed"
            self.book_tree.insert("", "end", values=(b["isbn"], b["title"], b["author"], status))

    def refresh_members(self):
        for i in self.mem_tree.get_children(): self.mem_tree.delete(i)
        for u in self.db.data["users"]:
            self.mem_tree.insert("", "end", values=(u.get("member_id", "N/A"), u["username"], u["role"]))

    def add_book_ui(self):
        win = tk.Toplevel(self.root)
        win.title("Add New Book")
        win.geometry("300x350")
        win.configure(bg=self.color_accent)

        tk.Label(win, text="Book Title", bg=self.color_accent, fg="white").pack(pady=5)
        e_title = tk.Entry(win); e_title.pack()
        tk.Label(win, text="Author", bg=self.color_accent, fg="white").pack(pady=5)
        e_author = tk.Entry(win); e_author.pack()
        tk.Label(win, text="ISBN", bg=self.color_accent, fg="white").pack(pady=5)
        e_isbn = tk.Entry(win); e_isbn.pack()

        def save():
            t, a, i = e_title.get(), e_author.get(), e_isbn.get()
            if t and a and i:
                self.db.data["books"].append(Book(i, t, a).to_dict())
                self.db.save()
                self.refresh_books()
                win.destroy()
        
        tk.Button(win, text="Save Book", bg=self.color_highlight, command=save).pack(pady=20)

    def delete_book(self):
        selected = self.book_tree.selection()
        if not selected: return
        isbn = self.book_tree.item(selected[0])['values'][0]
        self.db.data["books"] = [b for b in self.db.data["books"] if str(b["isbn"]) != str(isbn)]
        self.db.save()
        self.refresh_books()

    # --- STUDENT DASHBOARD (unchanged) ---
    def show_student_dashboard(self):
        self.clear_screen()
        
        header = tk.Frame(self.main_container, bg=self.color_accent, pady=10)
        header.pack(fill="x")
        tk.Label(header, text=f"STUDENT PORTAL | ID: {self.current_user['member_id']}", fg=self.color_highlight, bg=self.color_accent, font=("Arial", 11, "bold")).pack(side="left", padx=20)
        tk.Button(header, text="Logout", command=self.show_login, bg="#e74c3c", fg="white", borderwidth=0).pack(side="right", padx=20)

        content = tk.Frame(self.main_container, bg=self.color_bg, padx=20, pady=20)
        content.pack(fill="both", expand=True)

        tk.Label(content, text=f"Welcome, {self.current_user['username']}!", font=("Arial", 18, "bold"), fg="white", bg=self.color_bg).pack(pady=10)
        
        # Borrowing Section
        split_frame = tk.Frame(content, bg=self.color_bg)
        split_frame.pack(fill="both", expand=True)

        # Left: Available Books
        left_p = tk.Frame(split_frame, bg=self.color_bg)
        left_p.pack(side="left", fill="both", expand=True, padx=10)
        tk.Label(left_p, text="Library Catalog", fg=self.color_highlight, bg=self.color_bg).pack(anchor="w")
        
        cols = ("ISBN", "Title", "Author")
        self.stu_tree = ttk.Treeview(left_p, columns=cols, show="headings", height=10)
        for col in cols: self.stu_tree.heading(col, text=col)
        self.stu_tree.pack(fill="both", expand=True)
        self.refresh_stu_catalog()

        tk.Button(left_p, text="Borrow Selected Book", bg=self.color_highlight, font=("Arial", 10, "bold"), 
                  command=self.borrow_book).pack(pady=10)

        # Right: My Borrowed List
        right_p = tk.Frame(split_frame, bg=self.color_accent, padx=20, pady=10)
        right_p.pack(side="right", fill="y", padx=10)
        tk.Label(right_p, text="Your Borrowed Items", fg="white", bg=self.color_accent, font=("Arial", 10, "bold")).pack()
        
        self.my_books_list = tk.Listbox(right_p, bg="#2c2c44", fg="white", borderwidth=0, font=("Arial", 10))
        self.my_books_list.pack(fill="both", expand=True, pady=10)
        
        tk.Button(right_p, text="Return Selected", bg=self.color_btn, fg="white", command=self.return_book).pack(fill="x")
        
        # Info note
        tk.Label(content, text="* Only Librarians can modify student profile details *", font=("Arial", 9, "italic"), fg="#7f8c8d", bg=self.color_bg).pack(pady=10)
        
        self.update_my_borrowed_ui()

    def refresh_stu_catalog(self):
        for i in self.stu_tree.get_children(): self.stu_tree.delete(i)
        for b in self.db.data["books"]:
            if b["available"]:
                self.stu_tree.insert("", "end", values=(b["isbn"], b["title"], b["author"]))

    def update_my_borrowed_ui(self):
        self.my_books_list.delete(0, tk.END)
        for b in self.current_user["borrowed_books"]:
            self.my_books_list.insert(tk.END, b)

    def borrow_book(self):
        selected = self.stu_tree.selection()
        if not selected: return
        val = self.stu_tree.item(selected[0])['values']
        isbn, title = str(val[0]), val[1]

        # Update DB
        for b in self.db.data["books"]:
            if str(b["isbn"]) == isbn: b["available"] = False
        
        # Update Session
        self.current_user["borrowed_books"].append(title)
        
        # Sync DB Users
        for u in self.db.data["users"]:
            if u["username"] == self.current_user["username"]:
                u["borrowed_books"] = self.current_user["borrowed_books"]
        
        self.db.save()
        self.refresh_stu_catalog()
        self.update_my_borrowed_ui()
        messagebox.showinfo("Success", f"Successfully borrowed: {title}")

    def return_book(self):
        selection = self.my_books_list.curselection()
        if not selection: return
        title = self.my_books_list.get(selection[0])

        for b in self.db.data["books"]:
            if b["title"] == title: b["available"] = True
        
        self.current_user["borrowed_books"].remove(title)
        for u in self.db.data["users"]:
            if u["username"] == self.current_user["username"]:
                u["borrowed_books"] = self.current_user["borrowed_books"]
        
        self.db.save()
        self.refresh_stu_catalog()
        self.update_my_borrowed_ui()

# --- ENTRY POINT ---
if __name__ == "__main__":
    root = tk.Tk()
    # Handle window close to save data
    app = LibraryApp(root)
    root.mainloop()

