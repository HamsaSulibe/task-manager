import json
import logging
logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
class Task:
    def __init__(self, title: str, due_date: str, status="Pending") -> None:
        self.title = title
        self.due_date = due_date
        self.status = status

    # Return task details as a dictionary (used for saving to JSON)
    def task_look(self) -> dict[str, str]:
        return {
            "title": self.title,
            "due_date": self.due_date,
            "status": self.status
        }

    # Create a Task object from a dictionary (loaded from JSON)
    @classmethod
    def from_json(cls, data: dict[str, str]) -> "Task":
        return cls(data["title"], data["due_date"], data["status"])

class TaskManager:
    def __init__(self):
        self.tasks = []

    def add_task(self, title: str, due_date: str) -> None:
        task = Task(title, due_date)
        self.tasks.append(task)
        logging.info(f"Task added: {title}")

    def delete_task(self, task_number: int) -> None:
        index = task_number - 1
        if 0 <= index < len(self.tasks):
            removed = self.tasks.pop(index)
            logging.info(f"Deleted task {task_number}: {removed.title}")
        else:
            logging.error("Invalid task number.")

    def list_task(self) -> None:
        if not self.tasks:
            logging.info("No tasks found.")
        else:
            for i, task in enumerate(self.tasks, 1):
                logging.info(f"{i}. {task.title} | Due: {task.due_date} | Status: {task.status}")

    def complete_task(self, task_number: int) -> None:
        index = task_number - 1
        if 0 <= index < len(self.tasks):
            self.tasks[index].status = "Done"
            logging.info(f"Task {task_number} marked as complete.")
        else:
            logging.error("Invalid task number.")

    # Save tasks to a JSON file
    def save_task(self, filename: str = "tasks.json") -> None:
        with open(filename, "w") as file:
            json.dump([task.task_look() for task in self.tasks], file)
        logging.info("Tasks saved successfully.")

    # Load tasks from a JSON file
    def load_task(self, filename: str = "tasks.json") -> None:
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
    user = TaskManager()
    user.load_task()

    while True:
        print("\n1. Add Task")
        print("2. List Tasks")
        print("3. Complete Task")
        print("4. Delete Task")
        print("5. Save & Exit")

        choice = input("Choose an option: ")

        if choice == "1":
            title = input("Enter task title: ")
            due_date = input("Enter due date: ")
            user.add_task(title, due_date)

        elif choice == "2":
            user.list_task()

        elif choice == "3":
            try:
                number = int(input("Enter task number to mark complete: "))
                user.complete_task(number)
            except ValueError:
                logging.error("Please enter a valid number.")

        elif choice == "4":
            try:
                number = int(input("Enter task number to delete: "))
                user.delete_task(number)
            except ValueError:
                logging.error("Please enter a valid number.")

        elif choice == "5":
            user.save_task()
            logging.info("Goodbye!")
            break

        else:
            logging.warning("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
