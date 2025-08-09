import unittest
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from taskmannger.Task import TaskManager

class TestFunctionalFlow(unittest.TestCase):
    """
    Functional tests for full task manager scenarios:
    These tests simulate user actions in memory (no file I/O):
    - Add and complete
    - Add and delete
    - Add, list, complete
    """

    def test_add_and_complete_task(self):
        """
        Scenario: Add a task, complete it, verify it's done.
        """
        manager = TaskManager()
        manager.add_task("task A", "1/5/2025","5/5/2026")
        manager.complete_task(1)

        self.assertEqual(len(manager.tasks), 1)
        self.assertEqual(manager.tasks[0].title, "task A")
        self.assertEqual(manager.tasks[0].status, "Done")

    def test_add_and_delete_task(self):
        """
        Scenario: Add a task then delete it.
        """
        manager = TaskManager()
        manager.add_task("task B", "5/5/2025", "10/5/2025")
        self.assertEqual(len(manager.tasks), 1)

        manager.delete_task(1)
        self.assertEqual(manager.tasks[0].status, "Deleted")

        visible = [t for t in manager.tasks if t.status != "Deleted"]
        self.assertEqual(len(visible), 0)

    def test_add_list_and_complete_task(self):
        """
        Scenario: Add a task, list it (simulate viewing), then complete it.
        """
        manager = TaskManager()
        manager.add_task("task E","12/1/2025","12/12/2025")
        
        # Just simulate viewing tasks
        manager.list_task()

        manager.complete_task(1)

        self.assertEqual(len(manager.tasks), 1)
        self.assertEqual(manager.tasks[0].title, "task E")
        self.assertEqual(manager.tasks[0].status, "Done")


if __name__ == "__main__":
    unittest.main()
