
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from taskmannger.Task import Task
import unittest

class TestTask(unittest.TestCase):

 def test_creat(self):
        task=Task("buy game","25/7/2025")
        self.assertEqual(task.title,"buy game")
        self.assertEqual(task.due_date,"25/7/2025")
        self.assertEqual(task.status,"Pending")

 def test_custom_status(self):
        task = Task("buy game", "25/7/2025", "Done")
        self.assertEqual(task.status, "Done")

 def test_task_look(self):
          task=Task("take a nap","25/7/2025","Pending")
          expected_dict={
                "title":"take a nap",
                "due_date":"25/7/2025",
                "status":"Pending"
          }
          self.assertEqual(task.task_look(), expected_dict)

 def test_from_json(self):
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
