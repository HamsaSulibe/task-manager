import os
import sys
import unittest


sys.path.insert(
    0,
    os.path.abspath(os.path.join(os.path.dirname(__file__), "..")),
)

from taskmannger.Task import PENDING_STATE, DELETED_STATE, TaskManager


class TestNegativeFlow(unittest.TestCase):
    """
    Negative test cases: test how the system handles invalid task numbers.
    """

    def test_delete_invalid_task_number(self):
        manager = TaskManager()
        manager.add_task("task A", "12/12/2026", "15/12/2026")
        self.assertEqual(len(manager.tasks), 1)
        # Expect no exception, just no change
        manager.delete_task(4)
        visible_tasks = [t for t in manager.tasks if t.status != DELETED_STATE]
        self.assertEqual(len(visible_tasks), 1)
        self.assertEqual(visible_tasks[0].title, "task A")

    def test_complete_invalid_task_number(self):
        manager = TaskManager()
        manager.add_task("task B", "01/01/2025", "10/10/2025")
        self.assertEqual(len(manager.tasks), 1)

        manager.complete_task(3)

        self.assertEqual(manager.tasks[0].status, PENDING_STATE)

    def test_two_digit_year(self):
        manager = TaskManager()
        manager.add_task("task C", "01/01/25", "12/12/25")
        self.assertEqual(len(manager.tasks), 0)

    def test_add_wrong_format(self):
        m = TaskManager()
        m.add_task("mixed", "10/08-2025", "12/08-2025")
        self.assertEqual(len(m.tasks), 0)

    def test_add_task_wrongfrmDate(self):
        manager = TaskManager()
        manager.add_task("task C", "10.10/2025", "12/12/2025")
        self.assertEqual(len(manager.tasks), 0)

    def test_add_task_due_before_start(self):
        manager = TaskManager()
        manager.add_task("Invalid task", "15/12/2025", "01/01/2025")
        self.assertEqual(len(manager.tasks), 0)

    def test_delete_twice(self):
        manager = TaskManager()
        manager.add_task("task E", "01/01/2025", "05/01/2025")
        manager.delete_task(1)
        manager.delete_task(1)

        deleted_count = len([t for t in manager.tasks if t.status == DELETED_STATE])
        self.assertEqual(deleted_count, 1)

    def test_valid_date_format(self):
        manager = TaskManager()
        manager.add_task("Good Task", "10/08/2025", "15/08/2025")  # valid dd/mm/yyyy
        self.assertEqual(len(manager.tasks), 1)
        self.assertEqual(manager.tasks[0].title, "Good Task")

    def test_invalid_date_format(self):
        manager = TaskManager()
        manager.add_task("Bad Date Format", "2025-08-10", "2025-08-11")  # wrong format
        self.assertEqual(len(manager.tasks), 0)

    def test_nondate_string_task(self):
        manager = TaskManager()
        manager.add_task("task a ", "12/12/2025", "tomowro")
        self.assertEqual(len(manager.tasks), 0)


if __name__ == "__main__":
    unittest.main()
