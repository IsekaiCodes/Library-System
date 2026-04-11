import tkinter as tk
from tkinter import messagebox, ttk, simpledialog
import json
import os
import random
from datetime import datetime, timedelta

def get_remaining_days(date_str):
    """Automatically calculates remaining days based on the target date."""
    try:
        target_date = datetime.strptime(date_str, "%Y-%m-%d").date()
        today = datetime.now().date()
        return (target_date - today).days
    except:
        return 0

# Fallback configuration in case the config.py file is missing
try:
    import config 
except ImportError:
    class config:
        DEFAULT_BOOKS = [
            {"isbn": "101", "title": "Learn Python", "author": "John Doe", "available": True},
            {"isbn": "102", "title": "Tkinter GUI", "author": "Jane Smith", "available": True}
        ]
        DEFAULT_ADMIN_USER = {"username": "admin", "password": "123", "role": "Librarian", "member_id": "STAFF-ADMIN"}
        DEFAULT_TEST_USER = {"username": "student", "password": "123", "role": "Student", "member_id": "BCI-001", "borrowed_books": []}
        WINDOW_TITLE = "Library App"
        WINDOW_WIDTH = 1000
        WINDOW_HEIGHT = 600
        WINDOW_MIN_WIDTH = 800
        WINDOW_MIN_HEIGHT = 500
        COLOR_BG = "#1e1e2f"
        COLOR_ACCENT = "#2a2a40"
        COLOR_TEXT = "#ffffff"
        COLOR_BTN = "#ff4757"
        COLOR_HIGHLIGHT = "#2ed573"
        BOOK_COLORS = ["#ff4757", "#2ed573", "#1e90ff", "#ffa502"]
        NUM_FLYING_BOOKS = 5
        ANIMATION_FRAME_RATE = 50

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

# --- DATABASE LOGIC (Data persistence) ---

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
            except (json.JSONDecodeError, IOError):
                pass # If file is corrupt or unreadable, fall back to default
        
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

# --- GUI INTERFACE (User Interface) ---

class LibraryApp:
    def __init__(self, root):
        self.root = root
        self.root.title(config.WINDOW_TITLE)
        self.root.geometry(f"{config.WINDOW_WIDTH}x{config.WINDOW_HEIGHT}")
        self.root.minsize(config.WINDOW_MIN_WIDTH, config.WINDOW_MIN_HEIGHT)
        
        self.db = LibraryDatabase()
        self.current_user = None
        
        # UI Colors from Config
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
        glow_colors = ["#ff4757", "#2ed573", "#1e90ff", "#ffa502"]  # Use solid colors; Tkinter doesn't support alpha in hex
        for _ in range(config.NUM_FLYING_BOOKS):
            # Stagger starting positions to create gaps between books
            x = -60 - random.randint(0, 800)
            y = random.randint(10, 120)
            # Moderate the speed for a calmer animation
            base_speed = random.uniform(1.0, 2.5)
            
            idx = random.randint(0, 3)
            color = colors[idx]
            glow_color = glow_colors[idx]
            
            # Modern book: glow shadow + body + spine + shine
            glow_shadow = self.canvas.create_rectangle(x-5, y-5, x+50, y+65, fill=glow_color, outline="", width=0)
            book_body = self.canvas.create_rectangle(x, y, x+45, y+60, fill=color, outline="#ffffff", width=3)
            book_spine = self.canvas.create_line(x+2, y+2, x+2, y+58, fill="#ffffff", width=3)
            shine = self.canvas.create_oval(x+35, y+10, x+42, y+20, fill="#eeeeee", outline="")
            
            self.flying_books.append({
                "glow": glow_shadow,
                "body": book_body,
                "line": book_spine,
                "shine": shine,
                "speed": base_speed,
                "accel": 0,  # For easing
                "trail": [],  # Particle trail
                "y_speed": random.uniform(-0.5, 0.5) # Vertical speed for bouncing
            })

    def animate_loop(self):
        window_width = self.root.winfo_width()
        reset_x = window_width + 50  # Dynamic full span
        
        for book in self.flying_books:
            # Speed easing (accelerate then decelerate)
            book["accel"] += random.uniform(-0.02, 0.02)
            book["accel"] = max(-0.1, min(0.1, book["accel"]))
            curr_speed = book["speed"] * (1 + book["accel"])

            pos = self.canvas.coords(book["body"])
            if not pos: continue # Skip if book was somehow deleted

            # Vertical bouncing effect to make movement more dynamic
            if not (10 < pos[1] < 90): # Keep within vertical bounds
                book["y_speed"] *= -1
            dy = book["y_speed"]

            # Move all book parts
            self.canvas.move(book["glow"], curr_speed, dy)
            self.canvas.move(book["body"], curr_speed, dy)
            self.canvas.move(book["line"], curr_speed, dy)
            self.canvas.move(book["shine"], curr_speed, dy)
            trail_pos = pos[0] - 30, pos[1] + 20
            alpha = random.uniform(0.3, 0.8)
            trail_dot = self.canvas.create_oval(trail_pos[0]-3, trail_pos[1]-3, trail_pos[0]+3, trail_pos[1]+3, 
                                               fill="#aaaaaa", outline="")
            book["trail"].append((trail_dot, alpha))
            
            if len(book["trail"]) > 10:
                old_dot, _ = book["trail"].pop(0)
                self.canvas.delete(old_dot)
            
            # Fade old trails
            for i in range(len(book["trail"])-1, -1, -1):
                dot, a = book["trail"][i]
                a *= 0.97
                if a < 0.05:
                    self.canvas.delete(dot)
                    del book["trail"][i]
                else:
                    book["trail"][i] = (dot, a)
            
            # Reset when off right end
            if pos[0] > reset_x:
                y_pos = pos[1]
                self.canvas.coords(book["glow"], -65, y_pos-5, 5, y_pos+65)
                self.canvas.coords(book["body"], -60, y_pos, 5, y_pos+60)
                self.canvas.coords(book["line"], -58, y_pos+2, -58, y_pos+58)
                self.canvas.coords(book["shine"], -25, y_pos+10, -18, y_pos+20)

                # --- FIX: Delete old trail particles from canvas before clearing list ---
                for dot, _ in book["trail"]:
                    self.canvas.delete(dot)
                book["trail"] = [] # Now clear the list

                book["accel"] = 0
                book["y_speed"] = random.uniform(-0.5, 0.5) # Reset vertical speed
        
        self.root.after(config.ANIMATION_FRAME_RATE, self.animate_loop)

    def clear_screen(self):
        for widget in self.main_container.winfo_children():
            widget.destroy()

    def setup_entry_placeholder(self, entry, placeholder):
        """Set placeholder text for an entry."""
        if placeholder:
            entry.insert(0, placeholder)
            entry.bind('<FocusIn>', lambda e: e.widget.delete(0, tk.END) if e.widget.get() == placeholder else None)
            entry.bind('<FocusOut>', lambda e: e.widget.insert(0, placeholder) if not e.widget.get() else None)

    # --- LOGIN INTERFACE ---
    def show_login(self):
        self.clear_screen()
        
        # Professional centered card style frame
        self.login_frame = tk.Frame(self.main_container, bg=self.color_accent, padx=50, pady=40, relief="flat", bd=0, highlightbackground=self.color_highlight, highlightthickness=1)
        self.login_frame.place(relx=0.5, rely=0.45, anchor="center")

        # Welcome Message
        welcome_title = tk.Label(self.login_frame, text="🌟 Welcome to BCI Campus Library", 
                                 font=("Helvetica", 18, "bold"), fg=self.color_highlight, bg=self.color_accent)
        welcome_title.pack(pady=(0, 5))
        
        welcome_sub = tk.Label(self.login_frame, text="Your smart way to manage library services", 
                               font=("Arial", 11), fg=self.color_text, bg=self.color_accent)
        welcome_sub.pack(pady=(0, 25))

        # Form Container
        form_frame = tk.Frame(self.login_frame, bg=self.color_accent)
        form_frame.pack()

        # Role Selection
        tk.Label(form_frame, text="👥 Select Role", fg=self.color_text, bg=self.color_accent, 
                 font=("Arial", 10, "bold")).pack(anchor="center", pady=(5, 2))
        self.role_var = tk.StringVar(value="Student")
        self.role_combo = ttk.Combobox(form_frame, textvariable=self.role_var, values=["Student", "Librarian"], 
                                       state="readonly", font=("Arial", 12), width=28, justify="center")
        self.role_combo.pack(pady=(0, 15), ipady=4)

        # Username
        tk.Label(form_frame, text="👤 Username", fg=self.color_text, bg=self.color_accent, 
                 font=("Arial", 10, "bold")).pack(anchor="center", pady=(5, 2))
        self.ent_user = tk.Entry(form_frame, font=("Arial", 12), width=30, bg="#2c2c44", fg="white", 
                                 insertbackground="white", borderwidth=0, justify="center")
        self.ent_user.pack(pady=(0, 15), ipady=7)
        self.setup_entry_placeholder(self.ent_user, "Enter username...")

        # Password
        tk.Label(form_frame, text="🔒 Password", fg=self.color_text, bg=self.color_accent, 
                 font=("Arial", 10, "bold")).pack(anchor="center", pady=(5, 2))
        self.ent_pass = tk.Entry(form_frame, font=("Arial", 12), width=30, show="*", bg="#2c2c44", fg="white", 
                                 insertbackground="white", borderwidth=0, justify="center")
        self.ent_pass.pack(pady=(0, 25), ipady=7)
        self.setup_entry_placeholder(self.ent_pass, "Enter password...")

        # Login Button
        self.login_btn = tk.Button(form_frame, text="🚀 Login", font=("Arial", 12, "bold"), bg=self.color_btn, fg="white", 
                                   activebackground="#ff6b81", cursor="hand2", command=self.handle_login, 
                                   width=28, relief="flat", bd=0)
        self.login_btn.pack(ipady=5)

        self.ent_user.focus()

        # Hover effects
        def on_enter(e): e.widget.config(bg="#ff6b81")
        def on_leave(e): e.widget.config(bg=self.color_btn)
        def on_focus(e): e.widget.config(bg="#3a3a5c") 
        def on_unfocus(e): e.widget.config(bg="#2c2c44")
        
        self.login_btn.bind("<Enter>", on_enter)
        self.login_btn.bind("<Leave>", on_leave)
        
        self.ent_user.bind("<FocusIn>", on_focus, add="+")
        self.ent_user.bind("<FocusOut>", on_unfocus, add="+")
        self.ent_pass.bind("<FocusIn>", on_focus, add="+")
        self.ent_pass.bind("<FocusOut>", on_unfocus, add="+")

    def handle_login(self):
        u = self.ent_user.get().strip()
        p = self.ent_pass.get().strip()
        r = self.role_var.get() 
        
        # Ignore placeholders
        if u == "Enter username...": u = ""
        if p == "Enter password...": p = ""
        
        found = next((user for user in self.db.data["users"] if user["username"] == u and user["password"] == p and user["role"] == r), None)
        
        if found:
            messagebox.showinfo("Login Successful!", f"Welcome back, {found['username']}!\n\nYou have logged in as a {found['role']}.")
            self.current_user = found
            if found["role"] == "Librarian":
                self.check_reminders() # Show reminders upon login
                self.show_librarian_dashboard()
            else:
                self.show_student_dashboard()
        else:
            messagebox.showerror("Login Failed!", "❌ Invalid username or password. Please try again.")

    def check_reminders(self):
        """Librarian reminder popup for overdue and due soon books."""
        overdue_count = 0
        due_soon_count = 0
        for u in self.db.data["users"]:
            if u["role"] == "Student" and "borrowed_books" in u:
                for b in u["borrowed_books"]:
                    if isinstance(b, dict):
                        days_left = get_remaining_days(b["return_date"])
                        if days_left < 0:
                            overdue_count += 1
                        elif 0 <= days_left <= 2:
                            due_soon_count += 1
        
        msg = ""
        if overdue_count > 0:
            msg += f"🚨 {overdue_count} book(s) are overdue!\n"
        if due_soon_count > 0:
            msg += f"⚠️ {due_soon_count} book(s) are due soon (1-2 days left).\n"
            
        if msg:
            messagebox.showwarning("Librarian Reminder", msg)

    # --- LIBRARIAN DASHBOARD ---
    def show_librarian_dashboard(self):
        self.clear_screen()
        
        header = tk.Frame(self.main_container, bg=self.color_accent, pady=10)
        header.pack(fill="x")
        tk.Label(header, text=f"Librarian Portal | {self.current_user['username'].upper()}", fg=self.color_highlight, bg=self.color_accent, font=("Arial", 12, "bold")).pack(side="left", padx=20)
        tk.Button(header, text="Logout", command=self.show_login, bg="#e74c3c", fg="white", borderwidth=0).pack(side="right", padx=20)

        style = ttk.Style()
        style.theme_use('clam')
        style.configure("TNotebook", background=self.color_bg, borderwidth=0)
        style.configure("TNotebook.Tab", background=self.color_accent, foreground="white", padding=[20, 10])
        style.map("TNotebook.Tab", background=[("selected", self.color_highlight)], foreground=[("selected", "black")])

        nb = ttk.Notebook(self.main_container)
        nb.pack(fill="both", expand=True, padx=20, pady=20)

        # Tab 1: Inventory
        book_tab = tk.Frame(nb, bg=self.color_bg)
        nb.add(book_tab, text="Inventory")
        self.setup_book_tab(book_tab)

        # Tab 2: Registration
        member_tab = tk.Frame(nb, bg=self.color_bg)
        nb.add(member_tab, text="Registration")
        self.setup_member_tab(member_tab)

        # Tab 3: Active Loans
        loans_tab = tk.Frame(nb, bg=self.color_bg)
        nb.add(loans_tab, text="Active Loans")
        self.setup_loans_tab(loans_tab)

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
        form_frame = tk.Frame(parent, bg=self.color_accent, padx=20, pady=20)
        form_frame.pack(side="left", fill="y", padx=10, pady=10)

        tk.Label(form_frame, text="New Student Registration", font=("Arial", 12, "bold"), fg=self.color_highlight, bg=self.color_accent).pack(pady=10)
        
        tk.Label(form_frame, text="Full Name", bg=self.color_accent, fg="white").pack(anchor="w")
        self.reg_name = tk.Entry(form_frame, font=("Arial", 11)); self.reg_name.pack(fill="x", pady=5)
        
        tk.Label(form_frame, text="Initial Password", bg=self.color_accent, fg="white").pack(anchor="w")
        self.reg_pass = tk.Entry(form_frame, font=("Arial", 11)); self.reg_pass.pack(fill="x", pady=5)

        tk.Button(form_frame, text="Create Member Card", bg=self.color_highlight, font=("Arial", 10, "bold"), 
                  command=self.register_member, pady=10).pack(fill="x", pady=20)

        table_frame = tk.Frame(parent, bg=self.color_bg)
        table_frame.pack(side="right", fill="both", expand=True, padx=10, pady=10)
        
        cols = ("Card ID", "Username", "Role")
        self.mem_tree = ttk.Treeview(table_frame, columns=cols, show="headings")
        for col in cols: self.mem_tree.heading(col, text=col)
        self.mem_tree.pack(fill="both", expand=True)
        
        self.refresh_members()

    def setup_loans_tab(self, parent):
        """Displays books borrowed by all students with return dates."""
        cols = ("Student", "Book Title", "Status", "Return Date")
        self.loans_tree = ttk.Treeview(parent, columns=cols, show="headings")
        for col in cols: self.loans_tree.heading(col, text=col)
        self.loans_tree.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Configure Color tags
        self.loans_tree.tag_configure('overdue', foreground='white', background='#ff4757') # Red
        self.loans_tree.tag_configure('due_soon', foreground='black', background='#ffa502') # Orange
        self.loans_tree.tag_configure('normal', foreground='black', background='#2ed573') # Green
        
        self.refresh_loans()

    def refresh_loans(self):
        """Fetches all active borrowed books from all students."""
        for i in self.loans_tree.get_children(): self.loans_tree.delete(i)
        for u in self.db.data["users"]:
            if u["role"] == "Student" and "borrowed_books" in u:
                for b in u["borrowed_books"]:
                    if isinstance(b, dict):
                        # Auto-updating remaining days
                        days_left = get_remaining_days(b["return_date"])
                        
                        if days_left < 0:
                            tag = 'overdue'
                            status = f"Overdue ({-days_left} days)"
                        elif days_left <= 2:
                            tag = 'due_soon'
                            status = f"{days_left} days left"
                        else:
                            tag = 'normal'
                            status = f"{days_left} days left"
                            
                        self.loans_tree.insert("", "end", values=(u["username"], b["title"], status, b["return_date"]), tags=(tag,))
                    else:
                        self.loans_tree.insert("", "end", values=(u["username"], b, "N/A", "N/A"))

    def register_member(self):
        name = self.reg_name.get().strip()
        pw = self.reg_pass.get().strip()
        
        if not name or not pw:
            messagebox.showwarning("Incomplete Info", "Please fill in all fields.")
            return
            
        count = self.db.data["config"]["next_id"]
        card_id = f"BCI-2026-{count:04d}"
        
        new_student = Student(name, pw, card_id)
        self.db.data["users"].append(new_student.to_dict())
        self.db.data["config"]["next_id"] += 1
        self.db.save()
        
        messagebox.showinfo("Success", f"Member registered successfully!\n\nLibrary Card ID: {card_id}")
        self.reg_name.delete(0, tk.END); self.reg_pass.delete(0, tk.END)
        self.refresh_members()

    def refresh_books(self):
        for i in self.book_tree.get_children(): self.book_tree.delete(i)
        for b in self.db.data["books"]:
            status = "Available" if b["available"] else "(Borrowed/Missing)"
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
        if not selected:
            messagebox.showwarning("No Selection", "Please select a book to delete.")
            return

        item = self.book_tree.item(selected[0])
        isbn, title, _, status = item['values']

        if status != "Available":
            messagebox.showerror("Deletion Failed", "Cannot delete a book that is currently borrowed.")
            return

        if not messagebox.askyesno("Confirm Deletion", f"Are you sure you want to delete '{title}'?"):
            return

        self.db.data["books"] = [b for b in self.db.data["books"] if str(b["isbn"]) != str(isbn)]
        self.db.save()
        self.refresh_books()
        messagebox.showinfo("Success", f"'{title}' was deleted successfully.")

    # --- STUDENT DASHBOARD ---
    def show_student_dashboard(self):
        self.clear_screen()
        
        header = tk.Frame(self.main_container, bg=self.color_accent, pady=10)
        header.pack(fill="x")
        tk.Label(header, text=f"Student Portal | ID: {self.current_user['member_id']}", fg=self.color_highlight, bg=self.color_accent, font=("Arial", 11, "bold")).pack(side="left", padx=20)
        tk.Button(header, text="Logout", command=self.show_login, bg="#e74c3c", fg="white", borderwidth=0).pack(side="right", padx=20)

        content = tk.Frame(self.main_container, bg=self.color_bg, padx=20, pady=20)
        content.pack(fill="both", expand=True)

        tk.Label(content, text=f"Welcome, {self.current_user['username']}!", font=("Arial", 18, "bold"), fg="white", bg=self.color_bg).pack(pady=10)
        
        split_frame = tk.Frame(content, bg=self.color_bg)
        split_frame.pack(fill="both", expand=True)

        # Left: Catalog
        left_p = tk.Frame(split_frame, bg=self.color_bg)
        left_p.pack(side="left", fill="both", expand=True, padx=10)
        tk.Label(left_p, text="Library Catalog", fg=self.color_highlight, bg=self.color_bg).pack(anchor="w")
        
        cols = ("ISBN", "Title", "Author")
        self.stu_tree = ttk.Treeview(left_p, columns=cols, show="headings", height=10)
        for col in cols: self.stu_tree.heading(col, text=col)
        self.stu_tree.pack(fill="both", expand=True)
        self.refresh_stu_catalog()

        tk.Button(left_p, text="Borrow Book", bg=self.color_highlight, font=("Arial", 10, "bold"), 
                  command=self.borrow_book).pack(pady=10)

        # Right: My Books
        right_p = tk.Frame(split_frame, bg=self.color_accent, padx=20, pady=10)
        right_p.pack(side="right", fill="y", padx=10)
        tk.Label(right_p, text="Your Borrowed Books", fg="white", bg=self.color_accent, font=("Arial", 10, "bold")).pack()
        
        self.my_books_list = tk.Listbox(right_p, bg="#2c2c44", fg="white", borderwidth=0, font=("Arial", 10), width=45)
        self.my_books_list.pack(fill="both", expand=True, pady=10)
        
        tk.Button(right_p, text="Return Book", bg=self.color_btn, fg="white", command=self.return_book).pack(fill="x")
        
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
            if isinstance(b, dict):
                # Auto update remaining days
                days_left = get_remaining_days(b["return_date"])
                if days_left < 0:
                    time_status = f"Overdue ({-days_left} days late!)"
                else:
                    time_status = f"{days_left} days left"
                    
                display_text = f"📖 {b['title']} (Due: {b['return_date']} | {time_status})"
                self.my_books_list.insert(tk.END, display_text)
            else:
                # Old string structure fallback
                self.my_books_list.insert(tk.END, f"📖 {b}")

    def borrow_book(self):
        selected = self.stu_tree.selection()
        if not selected: return
        val = self.stu_tree.item(selected[0])['values']
        isbn, title = str(val[0]), val[1]

        # Duration Input Request
        duration = simpledialog.askinteger("Borrow Duration", 
                                           f"How many days do you want to borrow '{title}'?", 
                                           initialvalue=14, minvalue=1, maxvalue=365)
        if duration is None:
            return  # Cancelled by user
        
        # Calculate Return Date
        return_date = (datetime.now() + timedelta(days=duration)).strftime("%Y-%m-%d")

        for b in self.db.data["books"]:
            if str(b["isbn"]) == isbn: b["available"] = False
        
        # Save as a dictionary with dates
        borrow_record = {
            "isbn": isbn,
            "title": title,
            "duration": duration,
            "return_date": return_date
        }
        self.current_user["borrowed_books"].append(borrow_record)
        
        for u in self.db.data["users"]:
            if u["username"] == self.current_user["username"]:
                u["borrowed_books"] = self.current_user["borrowed_books"]
                break
        
        self.db.save()
        self.refresh_stu_catalog()
        self.update_my_borrowed_ui()
        messagebox.showinfo("Success", f"Successfully borrowed: {title}\nReturn Date: {return_date}")

    def return_book(self):
        selection = self.my_books_list.curselection()
        if not selection:
            messagebox.showwarning("No Selection", "Please select a book from your list to return.")
            return
        
        index = selection[0]
        borrowed_item = self.current_user["borrowed_books"][index]

        # Extract identifier (ISBN if available, else title for legacy)
        identifier = None
        is_isbn = False
        if isinstance(borrowed_item, dict) and "isbn" in borrowed_item:
            identifier = borrowed_item["isbn"]
            title = borrowed_item["title"]
            is_isbn = True
        else: # Fallback for old data structure (string or dict without isbn)
            identifier = borrowed_item["title"] if isinstance(borrowed_item, dict) else borrowed_item
            title = identifier

        # Find book in DB and mark as available
        book_found = False
        for b in self.db.data["books"]:
            key_to_check = str(b["isbn"]) if is_isbn else b["title"]
            if str(key_to_check) == str(identifier):
                b["available"] = True
                book_found = True
                break
        
        # Remove from user's borrowed list by index
        self.current_user["borrowed_books"].pop(index)
        
        for u in self.db.data["users"]:
            if u["username"] == self.current_user["username"]:
                u["borrowed_books"] = self.current_user["borrowed_books"]
                break
        
        self.db.save()
        self.refresh_stu_catalog()
        self.update_my_borrowed_ui()
        messagebox.showinfo("Success", f"Successfully returned: {title}")

# --- ENTRY POINT ---
if __name__ == "__main__":
    root = tk.Tk()
    app = LibraryApp(root)
    root.mainloop()