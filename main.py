import sqlite3

# Connect to SQLite database (it will create one if it doesn't exist)
try:
    conn = sqlite3.connect('employee_directory.db')
    cursor = conn.cursor()
except sqlite3.Error as e:
    print(f"Error connecting to database: {e}")

# Create the employees table
try:
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
except sqlite3.Error as e:
    print(f"Error creating table: {e}")


# Function to add a new employee
def add_employee(name, department, position, salary):
    try:
        cursor.execute('''
            INSERT INTO employees (name, department, position, salary)
            VALUES (?, ?, ?, ?)
        ''', (name, department, position, salary))
        conn.commit()
        print(f"Employee '{name}' added successfully.")
    except sqlite3.Error as e:
        print(f"Error adding employee: {e}")


# Function to update an employee's details
def update_employee(employee_id, name=None, department=None, position=None, salary=None):
    try:
        employee = cursor.execute('SELECT * FROM employees WHERE id = ?', (employee_id,)).fetchone()
        if employee:
            cursor.execute('''
                UPDATE employees
                SET name = COALESCE(?, name),
                    department = COALESCE(?, department),
                    position = COALESCE(?, position),
                    salary = COALESCE(?, salary)
                WHERE id = ?
            ''', (name, department, position, salary, employee_id))
            conn.commit()
            print(f"Employee with ID {employee_id} updated successfully.")
        else:
            print(f"Employee with ID {employee_id} not found.")
    except sqlite3.Error as e:
        print(f"Error updating employee: {e}")


# Function to delete an employee by ID
def delete_employee(employee_id):
    try:
        cursor.execute('DELETE FROM employees WHERE id = ?', (employee_id,))
        conn.commit()
        print(f"Employee with ID {employee_id} deleted successfully.")
    except sqlite3.Error as e:
        print(f"Error deleting employee: {e}")


# Function to search employees by name, department, or position
def search_employees(keyword):
    try:
        cursor.execute('''
            SELECT * FROM employees
            WHERE name LIKE ? OR department LIKE ? OR position LIKE ?
        ''', (f'%{keyword}%', f'%{keyword}%', f'%{keyword}%'))
        results = cursor.fetchall()
        if results:
            print("Search Results:")
            for emp in results:
                print(f"ID: {emp[0]}, Name: {emp[1]}, Department: {emp[2]}, Position: {emp[3]}, Salary: {emp[4]}")
        else:
            print("No employees found with that search keyword.")
    except sqlite3.Error as e:
        print(f"Error searching employees: {e}")


# Function to display all employees
def display_employees():
    try:
        cursor.execute('SELECT * FROM employees')
        employees = cursor.fetchall()
        if employees:
            print("Employee Directory:")
            for emp in employees:
                print(f"ID: {emp[0]}, Name: {emp[1]}, Department: {emp[2]}, Position: {emp[3]}, Salary: {emp[4]}")
        else:
            print("No employees in the directory.")
    except sqlite3.Error as e:
        print(f"Error displaying employees: {e}")


# Main menu for user interaction
def main_menu():
    while True:
        print("\nEmployee Directory Menu")
        print("1. Add Employee")
        print("2. Update Employee")
        print("3. Delete Employee")
        print("4. Search Employees")
        print("5. Display All Employees")
        print("6. Exit")

        choice = input("Enter your choice (1-6): ")

        if choice == '1':
            try:
                name = input("Enter employee name: ")
                department = input("Enter department: ")
                position = input("Enter position: ")
                salary = float(input("Enter salary: "))
                add_employee(name, department, position, salary)
            except ValueError:
                print("Invalid input for salary. Please enter a number.")

        elif choice == '2':
            try:
                employee_id = int(input("Enter employee ID to update: "))
                name = input("Enter new name (or leave blank to skip): ")
                department = input("Enter new department (or leave blank to skip): ")
                position = input("Enter new position (or leave blank to skip): ")
                salary_input = input("Enter new salary (or leave blank to skip): ")
                salary = float(salary_input) if salary_input else None
                update_employee(employee_id, name or None, department or None, position or None, salary)
            except ValueError:
                print("Invalid input. Please enter valid data for ID and salary.")

        elif choice == '3':
            try:
                employee_id = int(input("Enter employee ID to delete: "))
                delete_employee(employee_id)
            except ValueError:
                print("Invalid input for employee ID. Please enter a valid number.")

        elif choice == '4':
            keyword = input("Enter search keyword (name, department, or position): ")
            search_employees(keyword)

        elif choice == '5':
            display_employees()

        elif choice == '6':
            print("Exiting the program.")
            break

        else:
            print("Invalid choice. Please try again.")


# Run the main menu
try:
    main_menu()
except Exception as e:
    print(f"An unexpected error occurred: {e}")
finally:
    conn.close()
