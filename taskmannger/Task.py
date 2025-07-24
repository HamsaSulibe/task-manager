import json
import logging
import textwrap

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")


class Task:
    """
    Represents a task with a title, due date, and status.

    Attributes:
        title (str): The title of the task.
        due_date (str): The due date of the task.
        status (str): The status of the task (default is "Pending").
    """

    def __init__(self, title: str, due_date: str, status="Pending") -> None:
        """
        Initializes a new Task instance.

        Args:
            title (str): The task title.
            due_date (str): The due date for the task.
            status (str, optional): The task status. Defaults to "Pending".
        """
        self.title = title
        self.due_date = due_date
        self.status = status

    def task_look(self) -> dict[str, str]:
        """
        Returns a dictionary representation of the task (for JSON saving).

        Returns:
            dict[str, str]: A dictionary containing task details.
        """
        return {
            "title": self.title,
            "due_date": self.due_date,
            "status": self.status
        }

    @classmethod
    def from_json(cls, data: dict[str, str]) -> "Task":
        """
        Creates a Task object from a dictionary (used for loading from JSON).

        Args:
            data (dict[str, str]): The dictionary with task data.

        Returns:
            Task: A Task instance.
        """
        return cls(data["title"], data["due_date"], data["status"])


class TaskManager:
    """
    Manages a list of tasks and provides methods to add, delete, list, complete, save, and load tasks.
    """

    def __init__(self):
        """
        Initializes the TaskManager with an empty task list.
        """
        self.tasks = []

    def add_task(self, title: str, due_date: str) -> None:
        """
        Adds a new task to the list.

        Args:
            title (str): The task title.
            due_date (str): The due date for the task.
        """
        task = Task(title, due_date)
        self.tasks.append(task)
        logging.info(f"Task added: {title}")

    def delete_task(self, task_number: int) -> None:
        """
        Deletes a task from the list by its number.

        Args:
            task_number (int): The number of the task to delete.
        """
        index = task_number - 1
        if 0 <= index < len(self.tasks):
            removed = self.tasks.pop(index)
            logging.info(f"Deleted task {task_number}: {removed.title}")
        else:
            logging.error("Invalid task number.")

    def list_task(self) -> None:
        """
        Lists all current tasks with their status and due dates.
        """
        if not self.tasks:
            logging.info("No tasks found.")
        else:
            for i, task in enumerate(self.tasks, 1):
                logging.info(f"{i}. {task.title} | Due: {task.due_date} | Status: {task.status}")

    def complete_task(self, task_number: int) -> None:
        """
        Marks a task as complete.

        Args:
            task_number (int): The number of the task to mark as done.
        """
        index = task_number - 1
        if 0 <= index < len(self.tasks):
            self.tasks[index].status = "Done"
            logging.info(f"Task {task_number} marked as complete.")
        else:
            logging.error("Invalid task number.")

    def save_task(self, filename: str = "tasks.json") -> None:
        """
        Saves all tasks to a JSON file.

        Args:
            filename (str, optional): The name of the file to save. Defaults to "tasks.json".
        """
        with open(filename, "w") as file:
            json.dump([task.task_look() for task in self.tasks], file)
        logging.info("Tasks saved successfully.")

    def load_task(self, filename: str = "tasks.json") -> None:
        """
        Loads tasks from a JSON file if it exists.

        Args:
            filename (str, optional): The name of the file to load. Defaults to "tasks.json".
        """
        try:
            with open(filename, "r") as file:
                data = json.load(file)
                self.tasks = [Task.from_json(task) for task in data]
        except FileNotFoundError:
            self.tasks = []
            logging.warning("No existing task file found. Starting with empty list.")
        except json.JSONDecodeError:
            logging.error("Error: Couldn't load tasks.")


def main() -> None:
    """
    Main function to run the CLI task manager application.
    Displays menu options and handles user input in a loop.
    """
    user = TaskManager()
    user.load_task()

    while True:
        menu = textwrap.dedent("""\
        1. Add Task
        2. List Tasks
        3. Complete Task
        4. Delete Task
        5. Save & Exit
        """)
        print(menu)
        try:
            choice = int(input("Choose an option: "))
        except ValueError:
            logging.warning("Invalid input. Please enter a number.")
            continue

        if choice == 1:
            title = input("Enter task title: ")
            due_date = input("Enter due date: ")
            user.add_task(title, due_date)

        elif choice == 2:
            user.list_task()

        elif choice == 3:
            try:
                number = int(input("Enter task number to mark complete: "))
                user.complete_task(number)
            except ValueError:
                logging.error("Please enter a valid number.")

        elif choice == 4:
            try:
                number = int(input("Enter task number to delete: "))
                user.delete_task(number)
            except ValueError:
                logging.error("Please enter a valid number.")

        elif choice == 5:
            user.save_task()
            logging.info("Goodbye!")
            break

        else:
            logging.warning("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()
