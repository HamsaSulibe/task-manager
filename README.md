# Task Manager CLI Application

This is a Python-based Command-Line Interface (CLI) application that allows users to manage tasks (like a to-do list) directly from the terminal.

Tasks are stored in a JSON file so they can be saved and reloaded between sessions.

---

## Features

- Add a new task with a title and due date
- List all tasks with their current status
- Mark a task as complete
- Delete a task
- Save and load tasks from a JSON file



## How to Run

1. Save the script in a file, for example: `Task.py`
2. Open your terminal and run:

```bash
python Task.py
````



## Example Usage

```
1. Add Task
2. List Tasks
3. Complete Task
4. Delete Task
5. Save & Exit
Choose an option: 1
Enter task title: Finish Python assignment
Enter due date: 2025-07-30
INFO: Task added: Finish Python assignment

Choose an option: 2
INFO: 1. Finish Python assignment | Due: 2025-07-30 | Status: Pending

Choose an option: 3
Enter task number to mark complete: 1
INFO: Task 1 marked as complete.
```



## Code Structure

### Class: `Task`

Represents a single task with the following attributes and methods:

#### Attributes:

* `title` (str): The task title
* `due_date` (str): Due date for the task
* `status` (str): Current task status, default is `"Pending"`

#### Methods:

* `task_look()`
  Returns the task data as a dictionary for saving to JSON.

* `from_json(data: dict)`
  Class method that creates a `Task` object from a dictionary (used when loading tasks from file).

---

### Class: `TaskManager`

Responsible for handling all task-related operations:

#### Attributes:

* `tasks` (list): A list of `Task` objects

#### Methods:

* `add_task(title, due_date)`
  Adds a new task to the list.

* `delete_task(task_number)`
  Deletes the task by its number (1-based index).

* `list_task()`
  Lists all tasks with their number, title, due date, and status.

* `complete_task(task_number)`
  Marks the selected task as complete by setting status to `"Done"`.

* `save_task(filename="tasks.json")`
  Saves all current tasks to a JSON file (default: `tasks.json`).

* `load_task(filename="tasks.json")`
  Loads tasks from a JSON file, if it exists.

---

### Function: `main()`

This is the entry point of the application. It:

* Loads tasks on start
* Shows a user menu with options
* Handles user input and calls the appropriate methods
* Saves the task list and exits when the user chooses



## File Structure

```
task_manager.py     # Main application code
tasks.json          # Auto-generated file to store tasks persistently
README.md           # Documentation file 
```



## Logging and Output

The program uses the built-in `logging` module to print info, warnings, and error messages .

This makes the feedback more consistent and easier to follow.


