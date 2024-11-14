import sqlite3
import tkinter as tk
from tkinter import messagebox, simpledialog, ttk

# Connect to SQLite database
conn = sqlite3.connect('employee_directory.db')
cursor = conn.cursor()

# Create the employees table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS employees (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        department TEXT NOT NULL,
        position TEXT NOT NULL,
        salary REAL NOT NULL
    )
''')
conn.commit()

# GUI setup
root = tk.Tk()
root.title("Employee Directory")
root.geometry("600x400")
root.configure(bg="#f0f4f8")  # Light background color

# Set style
style = ttk.Style()
style.configure("Treeview", font=("Arial", 10), background="#e0ebf0", foreground="#2d2d2d")
style.configure("Treeview.Heading", font=("Arial", 12, "bold"), background="#37474f", foreground="white")
style.map("Treeview", background=[("selected", "#b0bec5")])
style.configure("TButton", font=("Arial", 10, "bold"), background="#4caf50", foreground="white", padding=6)
style.map("TButton", background=[("active", "#66bb6a")])

# Function to add a new employee
def add_employee():
    name = simpledialog.askstring("Add Employee", "Enter employee name:")
    department = simpledialog.askstring("Add Employee", "Enter department:")
    position = simpledialog.askstring("Add Employee", "Enter position:")
    try:
        salary = float(simpledialog.askstring("Add Employee", "Enter salary:"))
        cursor.execute('''
            INSERT INTO employees (name, department, position, salary)
            VALUES (?, ?, ?, ?)
        ''', (name, department, position, salary))
        conn.commit()
        messagebox.showinfo("Success", f"Employee '{name}' added successfully.")
        display_employees()
    except ValueError:
        messagebox.showerror("Input Error", "Invalid input for salary.")

# Function to update an employee's details
def update_employee():
    try:
        employee_id = int(simpledialog.askstring("Update Employee", "Enter employee ID to update:"))
        name = simpledialog.askstring("Update Employee", "Enter new name (or leave blank to skip):")
        department = simpledialog.askstring("Update Employee", "Enter new department (or leave blank to skip):")
        position = simpledialog.askstring("Update Employee", "Enter new position (or leave blank to skip):")
        salary_input = simpledialog.askstring("Update Employee", "Enter new salary (or leave blank to skip):")
        salary = float(salary_input) if salary_input else None

        cursor.execute('''
            UPDATE employees
            SET name = COALESCE(?, name),
                department = COALESCE(?, department),
                position = COALESCE(?, position),
                salary = COALESCE(?, salary)
            WHERE id = ?
        ''', (name or None, department or None, position or None, salary, employee_id))
        conn.commit()
        messagebox.showinfo("Success", f"Employee with ID {employee_id} updated successfully.")
        display_employees()
    except ValueError:
        messagebox.showerror("Input Error", "Invalid input for ID or salary.")

# Function to delete an employee by ID
def delete_employee():
    try:
        employee_id = int(simpledialog.askstring("Delete Employee", "Enter employee ID to delete:"))
        cursor.execute('DELETE FROM employees WHERE id = ?', (employee_id,))
        conn.commit()
        messagebox.showinfo("Success", f"Employee with ID {employee_id} deleted successfully.")
        display_employees()
    except ValueError:
        messagebox.showerror("Input Error", "Invalid input for employee ID.")

# Function to search employees
def search_employees():
    keyword = simpledialog.askstring("Search Employees", "Enter search keyword (name, department, or position):")
    cursor.execute('''
        SELECT * FROM employees
        WHERE name LIKE ? OR department LIKE ? OR position LIKE ?
    ''', (f'%{keyword}%', f'%{keyword}%', f'%{keyword}%'))
    results = cursor.fetchall()
    display_employees(results)

# Function to display employees in the table
def display_employees(records=None):
    for row in tree.get_children():
        tree.delete(row)
    if records is None:
        cursor.execute('SELECT * FROM employees')
        records = cursor.fetchall()
    for emp in records:
        tree.insert('', 'end', values=(emp[0], emp[1], emp[2], emp[3], emp[4]))

# GUI Components
frame = tk.Frame(root, bg="#f0f4f8")
frame.pack(pady=10)

# Employee Treeview
columns = ("ID", "Name", "Department", "Position", "Salary")
tree = ttk.Treeview(frame, columns=columns, show="headings")
for col in columns:
    tree.heading(col, text=col)
tree.pack(fill="both", expand=True)

# Buttons for CRUD operations
button_frame = tk.Frame(root, bg="#f0f4f8")
button_frame.pack(pady=10)

tk.Button(button_frame, text="Add Employee", command=add_employee, bg="#4caf50", fg="white", font=("Arial", 10, "bold")).grid(row=0, column=0, padx=5)
tk.Button(button_frame, text="Update Employee", command=update_employee, bg="#ffa726", fg="white", font=("Arial", 10, "bold")).grid(row=0, column=1, padx=5)
tk.Button(button_frame, text="Delete Employee", command=delete_employee, bg="#ef5350", fg="white", font=("Arial", 10, "bold")).grid(row=0, column=2, padx=5)
tk.Button(button_frame, text="Search Employees", command=search_employees, bg="#29b6f6", fg="white", font=("Arial", 10, "bold")).grid(row=0, column=3, padx=5)
tk.Button(button_frame, text="Display All Employees", command=lambda: display_employees(), bg="#8e24aa", fg="white", font=("Arial", 10, "bold")).grid(row=0, column=4, padx=5)

# Load and display all employees when the program starts
display_employees()

# Run the main loop
root.mainloop()

# Close the database connection on program exit
conn.close()
