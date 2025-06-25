import mysql.connector
from getpass import getpass

# MySQL Connection setup
db = {
    "host": "localhost",
    "user": "root",
    "password": "",
    "database": "auth",
}
dbc = mysql.connector.connect(**db)


def setup():
    c = dbc.cursor()
    c.execute(
        """CREATE TABLE IF NOT EXISTS users (
            id INT AUTO_INCREMENT PRIMARY KEY,
            username VARCHAR(255) NOT NULL UNIQUE,
            password VARCHAR(255) NOT NULL
        )"""
    )
    print("Database setup complete.")
    c.close()


def reg():
    username = input("Enter username: ")
    password = getpass("Enter password: ")
    c = dbc.cursor()
    try:
        c.execute(
            "INSERT INTO users (username, password) VALUES (%s, %s)",
            (username, password),
        )
        dbc.commit()
        print("User registered successfully.")
    except mysql.connector.IntegrityError:
        print("Username already exists. Please choose a different username.")
    finally:
        c.close()


def todolist():
    c = dbc.cursor()
    c.execute(
        "CREATE TABLE IF NOT EXISTS todo (id INT AUTO_INCREMENT PRIMARY KEY, task VARCHAR(255) NOT NULL, status BOOL NOT NULL DEFAULT FALSE)"
    )

    c.execute("SELECT * FROM todo")
    r = c.fetchall()
    if r:
        print("Todo list:")
        for row in r:
            print(
                f"ID: {row[0]}, Task: {row[1]}, Status: {'Done' if row[2] else 'Pending'}"
            )
    else:
        print("No tasks found in the todo list.")

    # ✅ Fix input checking
    action = input("Do you want to add a new task? (yes/no): ").strip().lower()
    if action in ["yes", "y"]:
        task = input("Enter the task: ")
        c.execute("INSERT INTO todo (task) VALUES (%s)", (task,))
        dbc.commit()
        print("Task added successfully.")

    a = input("Do you want to mark a task as done? (yes/no): ").strip().lower()
    if a in ["yes", "y"]:
        tasks = input("Enter the task to mark as done: ")
        c.execute("UPDATE todo SET status = true WHERE task = %s", (tasks,))
        dbc.commit()
        print("Task marked as done.")

    b = input("Do you want to delete a task? (yes/no): ").strip().lower()
    if b in ["yes", "y"]:
        task_to_delete = input("Enter the task to delete: ")
        c.execute("DELETE FROM todo WHERE task = %s", (task_to_delete,))
        dbc.commit()
        print("Task deleted successfully.")

    c.close()


def login():
    username = input("Enter username: ")
    password = getpass("Enter password: ")
    c = dbc.cursor()
    c.execute(
        "SELECT * FROM users WHERE username=%s AND password=%s",
        (username, password),
    )
    user = c.fetchone()
    if user:
        print("Login successful.")
        todolist()
    else:
        print("Invalid username or password.")
    c.close()


def display_tasks():
    c = dbc.cursor()
    c.execute("SELECT * FROM todo")
    tasks = c.fetchall()
    if tasks:
        print("\nTodo List:")
        for task in tasks:
            print(
                f"ID: {task[0]}, Task: {task[1]}, Status: {'Done' if task[2] else 'Pending'}"
            )
    else:
        print("\nNo tasks found.")
    c.close()


def main_menu():
    setup()
    while True:
        print("\nMain Menu:")
        print("1. Register")
        print("2. Login")
        print("3. Exit")
        print("4. View All Tasks")
        choice = input("Enter your choice: ")

        if choice == "1":
            reg()
        elif choice == "2":
            login()
        elif choice == "3":
            print("Exiting...")
            dbc.close()  # Close DB connection on exit
            break
        elif choice == "4":
            display_tasks()
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main_menu()
