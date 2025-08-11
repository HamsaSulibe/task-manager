import sys
import os
from datetime import datetime
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from taskmannger.Task import PENDING_STATE, DONE_STATE, Task
import unittest

class TestTask(unittest.TestCase):
    """
    Unit tests for the Task class.
    Each test checks a specific feature of the Task object.
    """
    def test_create_task(self):
        """
        Test creating a Task with default status and correct needed_time calculation.
        """
        start = datetime.strptime("2025-07-24", "%Y-%m-%d")
        due = datetime.strptime("2025-07-27", "%Y-%m-%d")
        task = Task("Buy game", start, due)
        self.assertEqual(task.title, "Buy game")
        self.assertEqual(task.start_date, start)
        self.assertEqual(task.due_date, due)
        self.assertEqual(task.status, PENDING_STATE)
        self.assertEqual(task.needed_time, 3)

    def test_custom_status(self):
        """
        Test creating a Task with a custom status.
        """
        start = datetime.strptime("2025-07-25", "%Y-%m-%d")
        due = datetime.strptime("2025-07-26", "%Y-%m-%d")
        task = Task("Do something", start, due, DONE_STATE)
        self.assertEqual(task.status, DONE_STATE)

    def test_invalid_dates(self):
        """
        Test that Task raises ValueError if due_date is before start_date.
        """
        start = datetime.strptime("2025-07-27", "%Y-%m-%d")
        due = datetime.strptime("2025-07-24", "%Y-%m-%d")
        with self.assertRaises(ValueError):
            Task("Invalid", start, due)

    def test_task_look(self):
        """
        Test that task_look returns correct dictionary format.
        """
        start = datetime.strptime("2025-07-24", "%Y-%m-%d")
        due = datetime.strptime("2025-07-26", "%Y-%m-%d")
        task = Task("Take a nap", start, due, PENDING_STATE)
        expected = {
            "title": "Take a nap",
            "start_date": "2025-07-24",
            "due_date": "2025-07-26",
            "needed_time": 2,
            "status": PENDING_STATE
        }
        self.assertEqual(task.task_look(), expected)

    def test_from_json(self):
        """
        Test creating a Task from a JSON-like dictionary.
        """
        data = {
            "title": "Clean room",
            "start_date": "2025-07-24",
            "due_date": "2025-07-26",
            "status": DONE_STATE
        }
        task = Task.from_json(data)
        self.assertEqual(task.title, "Clean room")
        self.assertEqual(task.start_date.strftime("%Y-%m-%d"), "2025-07-24")
        self.assertEqual(task.due_date.strftime("%Y-%m-%d"), "2025-07-26")
        self.assertEqual(task.status, DONE_STATE)
        self.assertEqual(task.needed_time, 2)

if __name__ == "__main__":
    unittest.main()
