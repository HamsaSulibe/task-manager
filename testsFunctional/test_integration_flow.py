import unittest
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from taskmannger.Task import TaskManager


class TestIntegrationFlow(unittest.TestCase):
 """
    Integration test: ensure that saving and loading tasks works as expected
    between TaskManager and JSON.
    """
 def test_save_and_load_integration(self):
  filename="integration_test.json"

  manager=TaskManager()
  manager.add_task("task A","25/5/2025")
  manager.save_task(filename)

  new_manager=TaskManager()
  new_manager.load_task(filename)


  self.assertEqual(len(new_manager.tasks),1)
  self.assertEqual(new_manager.tasks[0].title,"task A")
  self.assertEqual(new_manager.tasks[0].due_date, "25/5/2025")
  self.assertEqual(new_manager.tasks[0].status, "Pending")

        
  os.remove(filename)

if __name__ == "__main__":
    unittest.main()

