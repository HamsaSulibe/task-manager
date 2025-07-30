import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from taskmannger.Task import Task
import unittest

class TestTask(unittest.TestCase):
    """
    Unit tests for the Task class.
    Each test checks a specific feature of the Task object.
    """

    def test_creat(self):
        """
        Test creating a Task with default status.
        Checks that the title, due date, and default status are set correctly.
        """
        task = Task("buy game", "25/7/2025")
        self.assertEqual(task.title, "buy game")
        self.assertEqual(task.due_date, "25/7/2025")
        self.assertEqual(task.status, "Pending")

    def test_custom_status(self):
        """
        Test creating a Task with a custom status.
        Checks that the status is set to the provided value.
        """
        task = Task("buy game", "25/7/2025", "Done")
        self.assertEqual(task.status, "Done")

    def test_task_look(self):
        """
        Test the task_look method.
        Checks that it returns a dictionary with correct task data.
        """
        task = Task("take a nap", "25/7/2025", "Pending")
        expected_dict = {
            "title": "take a nap",
            "due_date": "25/7/2025",
            "status": "Pending"
        }
        self.assertEqual(task.task_look(), expected_dict)

    def test_from_json(self):
        """
        Test the from_json class method.
        Checks that a Task object is correctly created from dictionary data.
        """
        data = {
            "title": "Clean room",
            "due_date": "25/7/2025",
            "status": "Done"
        }
        task = Task.from_json(data)
        self.assertEqual(task.title, "Clean room")
        self.assertEqual(task.due_date, "25/7/2025")
        self.assertEqual(task.status, "Done")


if __name__ == "__main__":
    unittest.main()
