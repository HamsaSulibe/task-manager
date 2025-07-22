import json

class Task:
    def __init__(self, title:str, due_date:str, status="Pending") ->None:
        self.title = title
        self.due_date = due_date
        self.status = status
#save them as a dict to save it in json file
    def task_look(self) -> dict[str, str]:
        return {
            "title": self.title,
            "due_date": self.due_date,
            "status": self.status
        }
#this is method to show the task from json file 
    @classmethod # to creat obj from json 
    def from_json(cls, data: dict[str, str]) -> "Task":
        return cls(data["title"], data["due_date"], data["status"])

##class TaskManager to include the  tasks options:
class TaskManager:
    def __init__(self):
        self.tasks = [] #list
#add task:
    def add_ta(self, title:str, due_date:str)->None:
        task = Task(title, due_date)
        self.tasks.append(task)
        print(f"Task added: {title}")
#delete task:
    def del_ta(self, task_number:int)->None:
        index = task_number - 1
        if 0 <= index < len(self.tasks): #to make sure that index in list
            removed = self.tasks.pop(index)
            print(f"Deleted: {removed.title}")
        else:
            print("Invalid task number.")
#list (see all task)
    def list_ta(self) -> None:
        if not self.tasks:
            print("No tasks found.")
        else:
            for i, task in enumerate(self.tasks, 1):
                print(f"{i}. {task.title} | Due: {task.due_date} | Status: {task.status}")
                
#complete its mean to change it done task
    def comp_ta(self, task_number:int)->None:
        index = task_number - 1
        if 0 <= index < len(self.tasks): #if statment to make sure that the task valid
            self.tasks[index].status = "Done"
            print("Task marked as complete.")
        else:
            print("Invalid task number.")

#working with files : 
# save data in json file using dump 
    def save_ta(self, filename:str = "tasks.json") -> None:
        with open(filename, "w") as file:
            json.dump([task.task_look() for task in self.tasks], file)
        print("Tasks saved successfully.")

#read file using load 
    def load_ta(self, filename :str = "tasks.json") -> None:
        try:
            with open(filename, "r") as file:
                data = json.load(file)# here is how to read from json
                self.tasks = [Task.from_json(task) for task in data] #to ta7wel  dict data to obj task to put it in self.tasks (list)
        except FileNotFoundError:
            self.tasks = [] # if jsonfile 1empty
        except json.JSONDecodeError:# if json is wrong 
            print("Error: Couldn't load tasks.")

##main
def main()->None:
    user = TaskManager()
    user.load_ta()

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
            user.add_ta(title, due_date)

        elif choice == "2":
            user.list_ta()

        elif choice == "3":
            try:
                number = int(input("Enter task number to mark complete: "))
                user.comp_ta(number)
            except ValueError:
                print("Please enter a valid number.")

        elif choice == "4":
            try:
                number = int(input("Enter task number to delete: "))
                user.del_ta(number)
            except ValueError:
                print("Please enter a valid number.")

        elif choice == "5":
            user.save_ta()
            print("Goodbye!")
            break

        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
