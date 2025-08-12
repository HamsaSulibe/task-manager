import unittest
import os
import sys


sys.path.insert(
    0,
    os.path.abspath(os.path.join(os.path.dirname(__file__), "..")),
)

from taskmannger.Task import DELETED_STATE, DONE_STATE, Task, TaskManager


class TestTaskManager(unittest.TestCase):
    """
    Unit tests for the TaskManager class.

    This test class checks the main features:
    - Adding tasks
    - Deleting tasks
    - Completing tasks
    - Saving and loading tasks from a JSON file
    - Loading from nonexistent file
    """

    def setUp(self):
        """
        Runs before each test.
        Creates a fresh TaskManager instance for testing.
        """
        self.manager = TaskManager()
        self.test_filename = "test_task.json"

    def tearDown(self):
        """
        Runs after each test to clean up files.
        """
        if os.path.exists(self.test_filename):
            os.remove(self.test_filename)

    def test_add_task(self):
        """
        Test that a task is added correctly to the task list.
        """
        self.manager.add_task("Test Task", "24/7/2025", "25/7/2025")
        self.assertEqual(len(self.manager.tasks), 1)
        self.assertEqual(self.manager.tasks[0].title, "Test Task")

    def test_add_task_no_title(self):
        manager = TaskManager()
        with self.assertRaises(AssertionError):
            manager.add_task("", "01/01/2025", "12/12/2025")

    def test_delete_task(self):
        """
        Test that a task is deleted properly using its number.
        """
        self.manager.add_task("Task A", "24/7/2025", "25/7/2025")
        self.manager.delete_task(1)
        self.assertEqual(self.manager.tasks[0].status, DELETED_STATE)

    def test_complete_task(self):
        """
        Test that a task is marked as completed (status becomes 'Done').
        """
        self.manager.add_task("Task B", "24/7/2025", "26/7/2025")
        self.manager.complete_task(1)
        self.assertEqual(self.manager.tasks[0].status, DONE_STATE)

    def test_save_and_load_task(self):
        """
        Test saving tasks to a file and loading them back with a new TaskManager instance.
        """
        self.manager.add_task("Task C", "24/7/2025", "27/7/2025")
        self.manager.add_task("Task D", "01/8/2025", "03/8/2025")

        self.manager.save_task(self.test_filename)

        new_manager = TaskManager()
        new_manager.load_task(self.test_filename)
        self.assertEqual(len(new_manager.tasks), 2)
        self.assertEqual(new_manager.tasks[0].title, "Task C")
        self.assertEqual(new_manager.tasks[1].title, "Task D")

    def test_load_from_nonexistent_file(self):
        manager = TaskManager()
        manager.load_task("nonexistent.json")
        self.assertEqual(manager.tasks, [])


if __name__ == "__main__":
    unittest.main()
