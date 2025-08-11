import json
import logging
import textwrap
import glob
from datetime import datetime
logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

class Task:
    """
    Represents a task with a title, start date,due date, and status.

    Attributes:
        title (str): The title of the task.
        start_date(datetime):the start date of the task
        due_date (datetime): The due date of the task.
        status (str): The status of the task (default is "Pending").
    """

    def __init__(self, title: str, start_date:datetime,due_date:datetime, status="Pending") -> None:
        """
        Initializes a new Task instance.

        Args:
            title (str): The task title.
            start_date(datetime):the start sate for the task
            due_date (datetime): The due date for the task.
            status (str, optional): The task status. Defaults to "Pending".
        """
        self.title = title
        self.start_date=start_date
        self.due_date = due_date
        self.status = status

       
        delta=(due_date-start_date).days
        if delta < 0 :
            raise ValueError("Due date must be after start date")
        self.needed_time = delta

    def task_look(self) -> dict[str, str]:
        """
        Returns a dictionary representation of the task (for JSON saving).

        Returns:
            dict[str, str]: A dictionary containing task details.
        """
        return {
        "title": self.title,
        "start_date": self.start_date.strftime("%Y-%m-%d"),
        "due_date": self.due_date.strftime("%Y-%m-%d"),
        "needed_time": self.needed_time,
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
        start = datetime.strptime(data["start_date"], "%Y-%m-%d")
        due = datetime.strptime(data["due_date"], "%Y-%m-%d")
        return cls(
        data["title"],
        start,
        due,
        data.get("status", "Pending")
         )

class TaskManager:
    """
    Manages a list of tasks and provides methods to add, delete, list, complete, save, and load tasks.
    """
    def __init__(self): 
        """
        Initializes the TaskManager with an empty task list.
        """
        self.tasks = []

    def date_formats(self,date:str) -> str:
        """
        Parses the input date string using allowed formats.
        Returns it in YYYY-MM-DD format or raises ValueError.
        """
        formats=["%d/%m/%Y","%d-%m-%Y"]
        for format in formats:
            try:
                parsed = datetime.strptime(date, format)
                return parsed.strftime("%Y-%m-%d")
            except ValueError:
                continue 
        raise ValueError("Invalid date format.")  
        
    def add_task(self, title: str, start_date: str, due_date: str) -> None:
        """
        Adds a new task after validating required fields.
        """
        if not title.strip():
            logging.error("Title is required and cannot be empty.")
            return

        try:
            start_str = self.date_formats(start_date)
            due_str   = self.date_formats(due_date)

            start_dt = datetime.strptime(start_str, "%Y-%m-%d")
            due_dt   = datetime.strptime(due_str,   "%Y-%m-%d")

            needed_days = (due_dt - start_dt).days
            if needed_days <= 0:
                raise ValueError("Needed time must be at least one day (due_date > start_date).")

            task = Task(title, start_dt, due_dt)
            self.tasks.append(task)
            logging.info(f"Task added: {title}")

        except ValueError as e:
            logging.error(f"Invalid input: {e}")

  
    def delete_task(self, task_number: int) -> None:
        """
        Deletes a task from the visible list (excluding deleted tasks).

        Args:
            task_number (int): The number of the task (as seen by the user) to delete.
        """
        visible_tasks = [task for task in self.tasks if task.status != "Deleted"]

        index = task_number - 1
        if 0 <= index < len(visible_tasks):
            task_to_delete = visible_tasks[index]
            if task_to_delete.status == "Deleted":
                logging.warning(f"Task {task_number} is already deleted.")
                return
            task_to_delete.status = "Deleted"
            logging.info(f"Marked task {task_number} as deleted: {task_to_delete.title}")
        else:
            logging.error("Invalid task number.")


    def list_task(self) -> None:
        """
        Lists all current tasks with their status and due dates.
        """
        visible_tasks = [task for task in self.tasks if task.status != "Deleted"]

        if not visible_tasks:
               logging.info("No tasks found.")
        else:
           for i, task in enumerate(visible_tasks, 1):
            logging.info(f"{i}. {task.title} | Start: {task.start_date.strftime('%Y-%m-%d')} | Due: {task.due_date.strftime('%Y-%m-%d')} | Needed Time: {task.needed_time} days | Status: {task.status}")

    def complete_task(self, task_number: int) -> None:
        """
        Marks a task as complete.        """
        visible_tasks=[ task for task in self.tasks if task.status!="Deleted"]
        index = task_number - 1
        if 0 <= index < len(visible_tasks):
            task_to_complete = visible_tasks[index]
            task_to_complete.status = "Done"
            logging.info(f"Marked task {task_number} as complete: {task_to_complete.title}")
        else:
            logging.error("Invalid task number.")
    

    def save_task(self, filename=None) -> None:
        """ 
        Saves the current tasks to a JSON file.
        If filename is not provided, prompts the user for one.
     """
        if not filename:
            json_files = glob.glob("*.json")
            if json_files:
                print("Available JSON files:")
                for f in json_files:
                    print(f" - {f}")
            filename = input("Enter filename to save to: ").strip() or "tasks.json"
        try:
         with open(filename, "w") as file:
             json.dump([task.task_look() for task in self.tasks], file)
         logging.info(f"Tasks saved successfully to {filename}.")
        except PermissionError:
            logging.warning(f"Permission denied when saving to {filename}. Tasks NOT saved.")
        except OSError as e:
            logging.error(f"OS error while saving to {filename}: {e}")
    

    def load_task(self, filename=None) -> None:
        """
    Loads tasks from a JSON file.
    """
        if not filename:
            json_files = glob.glob("*.json")
            if json_files:
                print("Available JSON files:")
                for f in json_files:
                    print(f" - {f}")
            filename = input("Enter filename to load from (press Enter for tasks.json): ").strip() or "tasks.json"

        try:
            with open(filename, "r") as file:
                raw=json.load(file)
                
            loaded=[]
            for idx,item in enumerate(raw):
                try:
                    loaded.append(Task.from_json(item))
                except(KeyError,ValueError)as e:
                    logging.warning(f"Skipping invalid task at index {idx}: {e}")
            self.tasks = loaded
            logging.info(f"Tasks loaded successfully from {filename}.")
        except FileNotFoundError:
            self.tasks = []
            logging.warning(f"No task file found: {filename}. Starting with empty list.")
        except json.JSONDecodeError:
            self.tasks = []
            logging.error(f"Corrupted JSON in {filename}. Starting with empty list.")
        except PermissionError:
            logging.warning(f"Permission denied when reading {filename}. Keeping current tasks.")
        except OSError as e:
            logging.error(f"OS error while loading {filename}: {e}")


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
            raw  =input("Choose an option: ")
            cleaned=raw.strip().replace('"','').replace("'","") # Remove spaces and quotes from input
            choice = int(cleaned)#convared to int 
        except ValueError:
            logging.warning("Invalid input. Please enter a number.")
            continue

        if choice == 1:
           title = input("Enter task title: ")
           start_date = input("Enter start date (dd/mm/yyyy or dd-mm-yyyy): ")
           due_date = input("Enter due date (dd/mm/yyyy or dd-mm-yyyy): ")
           user.add_task(title, start_date, due_date)


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

    