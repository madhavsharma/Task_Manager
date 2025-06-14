# Task_Manager
This is a simple console based task manager.
How it works, in brief:

    Credentials are stored in users.json, with passwords hashed using bcrypt for safety.

    Each user’s tasks live in tasks_<username>.json.

    Menu loops handle registration, login, and task operations.

You can run this script directly. On first run, install bcrypt (pip install bcrypt).