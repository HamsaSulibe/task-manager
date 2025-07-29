import unittest
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from taskmannger.Task import Task, TaskManager

class TestTaskManager(unittest.TestCase):
    def setUp(self):
        self.manager = TaskManager()

    def test_add_task(self):
        self.manager.add_task("Test Task", "25/7/2025")
        self.assertEqual(len(self.manager.tasks), 1)
        self.assertEqual(self.manager.tasks[0].title, "Test Task")
    
    def test_delete_task(self):
        self.manager.add_task("Task A", "25/7/2025")
        self.manager.delete_task(1)
        self.assertEqual(len(self.manager.tasks), 0)

    def test_complete_task(self):
        self.manager.add_task("Task B", "25/7/2025")
        self.manager.complete_task(1)
        self.assertEqual(self.manager.tasks[0].status, "Done")

    def test_save_and_load_task(self):
        filename = "test_tasks.json"
        self.manager.add_task("Task C", "25/7/2025")
        self.manager.save_task(filename)

        new_manager = TaskManager()
        new_manager.load_task(filename)
        self.assertEqual(len(new_manager.tasks), 1)
        self.assertEqual(new_manager.tasks[0].title, "Task C")

        # os.remove(filename)

if __name__ == "__main__":
    unittest.main()
