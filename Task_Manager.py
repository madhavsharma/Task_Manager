import os
import json
import bcrypt

USERS_FILE = "users.json"

def load_users():
    if not os.path.exists(USERS_FILE):
        return {}
    with open(USERS_FILE, "r") as f:
        return json.load(f)

def save_users(users):
    with open(USERS_FILE, "w") as f:
        json.dump(users, f)

def register():
    users = load_users()
    print("\n== Registration ==")
    while True:
        username = input("Choose a username: ").strip()
        if username in users:
            print("Username taken, try again.")
        elif username == "":
            print("Username cannot be blank.")
        else:
            break

    while True:
        pwd = input("Choose a password: ")
        pwd2 = input("Confirm password: ")
        if pwd != pwd2:
            print("Passwords do not match.")
        elif pwd == "":
            print("Password cannot be blank.")
        else:
            break

    hashed = bcrypt.hashpw(pwd.encode(), bcrypt.gensalt()).decode()
    users[username] = hashed
    save_users(users)
    print(f"User '{username}' registered successfully.\n")

def login():
    users = load_users()
    print("\n== Login ==")
    username = input("Username: ").strip()
    pwd = input("Password: ")

    if username not in users:
        print("No such user.\n")
        return None

    hashed = users[username].encode()
    if bcrypt.checkpw(pwd.encode(), hashed):
        print(f"Welcome back, {username}!\n")
        return username
    else:
        print("Invalid password.\n")
        return None

def tasks_file(username):
    return f"tasks_{username}.json"

def load_tasks(username):
    path = tasks_file(username)
    if not os.path.exists(path):
        return []
    with open(path, "r") as f:
        return json.load(f)

def save_tasks(username, tasks):
    with open(tasks_file(username), "w") as f:
        json.dump(tasks, f, indent=2)

def add_task(username):
    tasks = load_tasks(username)
    desc = input("Task description: ").strip()
    if not desc:
        print("Cannot add empty task.\n")
        return
    task_id = max([t["id"] for t in tasks], default=0) + 1
    tasks.append({"id": task_id, "desc": desc, "status": "Pending"})
    save_tasks(username, tasks)
    print(f"Task {task_id} added.\n")

def view_tasks(username):
    tasks = load_tasks(username)
    if not tasks:
        print("No tasks yet.\n")
        return
    print("\nYour Tasks:")
    print("-"*30)
    for t in tasks:
        print(f"[{t['id']}] {t['desc']} ({t['status']})")
    print()

def mark_completed(username):
    tasks = load_tasks(username)
    if not tasks:
        print("No tasks to update.\n")
        return
    try:
        tid = int(input("Enter task ID to mark completed: "))
    except ValueError:
        print("Invalid ID.\n")
        return

    for t in tasks:
        if t["id"] == tid:
            if t["status"] == "Completed":
                print("Already completed.\n")
            else:
                t["status"] = "Completed"
                save_tasks(username, tasks)
                print(f"Task {tid} marked completed.\n")
            return
    print("Task ID not found.\n")

def delete_task(username):
    tasks = load_tasks(username)
    if not tasks:
        print("No tasks to delete.\n")
        return
    try:
        tid = int(input("Enter task ID to delete: "))
    except ValueError:
        print("Invalid ID.\n")
        return

    new_tasks = [t for t in tasks if t["id"] != tid]
    if len(new_tasks) == len(tasks):
        print("Task ID not found.\n")
    else:
        save_tasks(username, new_tasks)
        print(f"Task {tid} deleted.\n")

def main_menu(username):
    while True:
        print("== Task Manager ==")
        print("1) Add Task")
        print("2) View Tasks")
        print("3) Mark Completed")
        print("4) Delete Task")
        print("5) Logout")
        choice = input("Choose an option: ").strip()

        if choice == "1":
            add_task(username)
        elif choice == "2":
            view_tasks(username)
        elif choice == "3":
            mark_completed(username)
        elif choice == "4":
            delete_task(username)
        elif choice == "5":
            print(f"Goodbye, {username}!\n")
            break
        else:
            print("Invalid option.\n")

def main():
    try:
        import bcrypt
    except ImportError:
        print("This program requires the 'bcrypt' library.")
        print("Install via: pip install bcrypt")
        return

    print("Welcome to the CLI Task Manager")
    while True:
        print("1) Register")
        print("2) Login")
        print("3) Exit")
        cmd = input("Select: ").strip()

        if cmd == "1":
            register()
        elif cmd == "2":
            user = login()
            if user:
                main_menu(user)
        elif cmd == "3":
            print("Exiting. Have a nice day!")
            break
        else:
            print("Invalid choice.\n")

if __name__ == "__main__":
    main()