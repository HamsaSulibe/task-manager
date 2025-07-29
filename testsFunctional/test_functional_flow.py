import unittest
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from taskmannger.Task import TaskManager

class TestFunctionalFlow(unittest.TestCase):
    """
    Functional tests for full task manager scenarios:
    - Add, complete, save, load
    - Add, delete
    """

    def test_add_complete_and_load_task(self):
        """
        Scenario: Add a task, complete it, save to file, load into new manager, verify.
        """
        filename = "test_func_tasks.json"

        manager = TaskManager()
        manager.add_task("task A", "5/5/2026")
        manager.complete_task(1)
        manager.save_task(filename)

        new_manager = TaskManager()
        new_manager.load_task(filename)

        self.assertEqual(len(new_manager.tasks), 1)
        self.assertEqual(new_manager.tasks[0].title, "task A")
        self.assertEqual(new_manager.tasks[0].status, "Done")

        os.remove(filename)

    def test_add_and_delete_task(self):
        """
        Scenario: Add a task then delete it.
        """
        manager = TaskManager()
        manager.add_task("task B", "5/5/2025")

        self.assertEqual(len(manager.tasks), 1)

        manager.delete_task(1)
        self.assertEqual(len(manager.tasks), 0)


if __name__ == "__main__":
    unittest.main()
