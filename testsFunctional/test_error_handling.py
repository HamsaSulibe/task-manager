import unittest
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from taskmannger.Task import TaskManager

class TestFunctionalFlow(unittest.TestCase):
    """
    Negative test cases: test how the system handles invalid task numbers.
    """

    def test_delete_invalid_task_number(self):
        manager = TaskManager()
        manager.add_task("task A", "12/12/2026")
        self.assertEqual(len(manager.tasks), 1)

        manager.delete_task(4)

        self.assertEqual(len(manager.tasks), 1)
        self.assertEqual(manager.tasks[0].title, "task A")

    def test_complete_invalid_task_number(self):
        manager = TaskManager()
        manager.add_task("task B", "10/10/2025")
        self.assertEqual(len(manager.tasks), 1)

        manager.complete_task(3)

        self.assertEqual(manager.tasks[0].status, "Pending")

    def test_add_task_wrongfrmDate(self):
       manager = TaskManager()
       manager.add_task("task C", "10.10/2025")
       self.assertEqual(len(manager.tasks), 0)

if __name__ == "__main__":
    unittest.main()
