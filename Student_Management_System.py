"""
Student Management System
Beginner-friendly Python + SQLite CLI project.

Default demo admin:
    Username: admin
    Password: Admin@123

Run with: python main.py
"""

import sqlite3
import hashlib
import os
from getpass import getpass

DB_NAME = "student_management.db"


# -------------------- DATABASE --------------------

def connect_db():
    """Connect to SQLite and enable foreign key checks."""
    conn = sqlite3.connect(DB_NAME)
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def hash_password(password):
    """Hash passwords so plain-text passwords are not stored."""
    return hashlib.sha256(password.encode("utf-8")).hexdigest()


def setup_database():
    """Create all tables and insert starter courses/admin if needed."""
    with connect_db() as conn:
        cur = conn.cursor()

        cur.execute("""
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL UNIQUE,
                password_hash TEXT NOT NULL,
                role TEXT NOT NULL CHECK(role IN ('admin', 'staff'))
            )
        """)

        cur.execute("""
            CREATE TABLE IF NOT EXISTS courses (
                course_id INTEGER PRIMARY KEY AUTOINCREMENT,
                course_name TEXT NOT NULL UNIQUE
            )
        """)

        cur.execute("""
            CREATE TABLE IF NOT EXISTS students (
                student_id INTEGER PRIMARY KEY AUTOINCREMENT,
                full_name TEXT NOT NULL,
                age INTEGER NOT NULL CHECK(age BETWEEN 3 AND 100),
                email TEXT NOT NULL UNIQUE,
                phone TEXT NOT NULL,
                course_id INTEGER NOT NULL,
                FOREIGN KEY (course_id) REFERENCES courses(course_id)
                    ON UPDATE CASCADE ON DELETE RESTRICT
            )
        """)

        # Starter courses are added only when they do not already exist.
        for course in ("Python Programming", "Data Analytics", "Web Development"):
            cur.execute(
                "INSERT OR IGNORE INTO courses (course_name) VALUES (?)",
                (course,)
            )

        # Demo admin is created only if there are no users yet.
        cur.execute("SELECT COUNT(*) FROM users")
        if cur.fetchone()[0] == 0:
            cur.execute(
                "INSERT INTO users (username, password_hash, role) VALUES (?, ?, ?)",
                ("admin", hash_password("Admin@123"), "admin")
            )

    print("\nDatabase is ready.")


# -------------------- INPUT VALIDATION --------------------

def ask_non_empty(prompt):
    while True:
        value = input(prompt).strip()
        if value:
            return value
        print("Input cannot be empty. Please try again.")


def ask_integer(prompt, minimum=None, maximum=None):
    while True:
        value = input(prompt).strip()
        try:
            number = int(value)
            if minimum is not None and number < minimum:
                print(f"Enter a number greater than or equal to {minimum}.")
                continue
            if maximum is not None and number > maximum:
                print(f"Enter a number less than or equal to {maximum}.")
                continue
            return number
        except ValueError:
            print("Please enter a valid whole number.")


def ask_email(prompt="Email: "):
    while True:
        email = ask_non_empty(prompt).lower()
        if "@" in email and "." in email.split("@")[-1] and " " not in email:
            return email
        print("Please enter a valid email address.")


def get_password(prompt="Password: "):
    """Use hidden input where supported; fall back to normal input."""
    try:
        password = getpass(prompt)
    except (EOFError, Exception):
        password = input(prompt)
    return password


# -------------------- AUTHENTICATION --------------------

def register_user():
    print("\n--- User Registration (Staff account) ---")
    username = ask_non_empty("Choose username: ")
    password = get_password("Choose password (minimum 6 characters): ")

    if len(password) < 6:
        print("Password must contain at least 6 characters.")
        return

    try:
        with connect_db() as conn:
            conn.execute(
                "INSERT INTO users (username, password_hash, role) VALUES (?, ?, 'staff')",
                (username, hash_password(password))
            )
        print("Registration successful. You can now log in.")
    except sqlite3.IntegrityError:
        print("That username already exists. Please choose another.")
    except sqlite3.Error as error:
        print("Database error:", error)


def login():
    print("\n--- Login ---")
    username = ask_non_empty("Username: ")
    password = get_password("Password: ")

    try:
        with connect_db() as conn:
            user = conn.execute(
                "SELECT user_id, username, password_hash, role FROM users WHERE username = ?",
                (username,)
            ).fetchone()

        if user and user[2] == hash_password(password):
            print(f"\nWelcome, {user[1]}! Role: {user[3].upper()}")
            return {"user_id": user[0], "username": user[1], "role": user[3]}

        print("Invalid username or password.")
    except sqlite3.Error as error:
        print("Database error:", error)
    return None


# -------------------- COURSES --------------------

def list_courses():
    with connect_db() as conn:
        rows = conn.execute(
            "SELECT course_id, course_name FROM courses ORDER BY course_id"
        ).fetchall()

    print("\n--- Available Courses ---")
    if not rows:
        print("No courses available.")
        return []
    for course_id, name in rows:
        print(f"{course_id}. {name}")
    return rows


def choose_course():
    courses = list_courses()
    if not courses:
        return None
    valid_ids = {row[0] for row in courses}
    while True:
        course_id = ask_integer("Choose course ID: ", minimum=1)
        if course_id in valid_ids:
            return course_id
        print("Invalid course ID. Choose an ID from the list.")


def add_course(user):
    if user["role"] != "admin":
        print("Access denied. Only admin can add courses.")
        return
    name = ask_non_empty("New course name: ")
    try:
        with connect_db() as conn:
            conn.execute("INSERT INTO courses (course_name) VALUES (?)", (name,))
        print("Course added successfully.")
    except sqlite3.IntegrityError:
        print("This course already exists.")
    except sqlite3.Error as error:
        print("Database error:", error)


# -------------------- STUDENT CRUD --------------------

def add_student():
    print("\n--- Add Student ---")
    name = ask_non_empty("Full name: ")
    age = ask_integer("Age (3-100): ", minimum=3, maximum=100)
    email = ask_email()
    phone = ask_non_empty("Phone number: ")
    course_id = choose_course()
    if course_id is None:
        print("No course found. Ask admin to add a course.")
        return

    try:
        with connect_db() as conn:
            conn.execute("""
                INSERT INTO students (full_name, age, email, phone, course_id)
                VALUES (?, ?, ?, ?, ?)
            """, (name, age, email, phone, course_id))
        print("Student added successfully.")
    except sqlite3.IntegrityError as error:
        if "students.email" in str(error):
            print("That email is already registered.")
        else:
            print("Could not add student. Check the entered details.")
    except sqlite3.Error as error:
        print("Database error:", error)


def view_students():
    print("\n--- Student List ---")
    try:
        with connect_db() as conn:
            rows = conn.execute("""
                SELECT s.student_id, s.full_name, s.age, s.email, s.phone, c.course_name
                FROM students AS s
                JOIN courses AS c ON s.course_id = c.course_id
                ORDER BY s.student_id
            """).fetchall()

        if not rows:
            print("No student records found.")
            return

        print("-" * 95)
        print(f"{'ID':<5}{'Name':<22}{'Age':<6}{'Email':<28}{'Phone':<16}Course")
        print("-" * 95)
        for student in rows:
            sid, name, age, email, phone, course = student
            print(f"{sid:<5}{name[:20]:<22}{age:<6}{email[:26]:<28}{phone[:14]:<16}{course}")
    except sqlite3.Error as error:
        print("Database error:", error)


def find_student(student_id):
    with connect_db() as conn:
        return conn.execute("""
            SELECT student_id, full_name, age, email, phone, course_id
            FROM students WHERE student_id = ?
        """, (student_id,)).fetchone()


def update_student():
    print("\n--- Update Student ---")
    student_id = ask_integer("Enter student ID: ", minimum=1)
    student = find_student(student_id)
    if not student:
        print("Student ID not found.")
        return

    print("Press Enter to keep the current value.")
    name = input(f"Full name [{student[1]}]: ").strip() or student[1]

    age_text = input(f"Age [{student[2]}]: ").strip()
    if age_text:
        try:
            age = int(age_text)
            if not 3 <= age <= 100:
                print("Age must be between 3 and 100.")
                return
        except ValueError:
            print("Age must be a whole number.")
            return
    else:
        age = student[2]

    email_input = input(f"Email [{student[3]}]: ").strip()
    email = student[3]
    if email_input:
        if "@" not in email_input or "." not in email_input.split("@")[-1] or " " in email_input:
            print("Invalid email address.")
            return
        email = email_input.lower()

    phone = input(f"Phone [{student[4]}]: ").strip() or student[4]
    change_course = input("Change course? (y/n): ").strip().lower()
    course_id = choose_course() if change_course == "y" else student[5]
    if course_id is None:
        return

    try:
        with connect_db() as conn:
            conn.execute("""
                UPDATE students
                SET full_name = ?, age = ?, email = ?, phone = ?, course_id = ?
                WHERE student_id = ?
            """, (name, age, email, phone, course_id, student_id))
        print("Student updated successfully.")
    except sqlite3.IntegrityError:
        print("That email is already used by another student.")
    except sqlite3.Error as error:
        print("Database error:", error)


def delete_student(user):
    if user["role"] != "admin":
        print("Access denied. Only admin can delete student records.")
        return

    print("\n--- Delete Student ---")
    student_id = ask_integer("Enter student ID to delete: ", minimum=1)
    student = find_student(student_id)
    if not student:
        print("Student ID not found.")
        return

    confirm = input(f"Delete '{student[1]}'? (y/n): ").strip().lower()
    if confirm != "y":
        print("Delete cancelled.")
        return

    try:
        with connect_db() as conn:
            conn.execute("DELETE FROM students WHERE student_id = ?", (student_id,))
        print("Student deleted successfully.")
    except sqlite3.Error as error:
        print("Database error:", error)


# -------------------- MENUS --------------------

def admin_menu(user):
    while True:
        print("""
========== ADMIN MENU ==========
1. Add student
2. View students
3. Update student
4. Delete student
5. View courses
6. Add course
7. Logout
""")
        choice = input("Choose option: ").strip()
        if choice == "1":
            add_student()
        elif choice == "2":
            view_students()
        elif choice == "3":
            update_student()
        elif choice == "4":
            delete_student(user)
        elif choice == "5":
            list_courses()
        elif choice == "6":
            add_course(user)
        elif choice == "7":
            print("Logged out successfully.")
            break
        else:
            print("Invalid menu selection. Choose 1-7.")


def staff_menu(user):
    while True:
        print("""
========== STAFF MENU ==========
1. Add student
2. View students
3. Update student
4. View courses
5. Logout
""")
        choice = input("Choose option: ").strip()
        if choice == "1":
            add_student()
        elif choice == "2":
            view_students()
        elif choice == "3":
            update_student()
        elif choice == "4":
            list_courses()
        elif choice == "5":
            print("Logged out successfully.")
            break
        else:
            print("Invalid menu selection. Choose 1-5.")


def main():
    try:
        setup_database()
        while True:
            print("""
====== STUDENT MANAGEMENT SYSTEM ======
1. Register staff account
2. Login
3. View courses
4. Exit
""")
            choice = input("Choose option: ").strip()

            if choice == "1":
                register_user()
            elif choice == "2":
                user = login()
                if user:
                    if user["role"] == "admin":
                        admin_menu(user)
                    else:
                        staff_menu(user)
            elif choice == "3":
                list_courses()
            elif choice == "4":
                print("Thank you for using the system. Goodbye!")
                break
            else:
                print("Invalid menu selection. Choose 1-4.")
    except KeyboardInterrupt:
        print("\nProgram stopped safely.")
    except sqlite3.Error as error:
        print("A database error occurred:", error)
    except Exception as error:
        print("An unexpected error occurred:", error)
        print("Please try again or contact your project guide.")


if __name__ == "__main__":
    main()
