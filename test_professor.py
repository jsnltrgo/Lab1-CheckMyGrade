import unittest
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from professor import Professor
from course import Course
from database import get_connection, initialize_database

class TestProfessor(unittest.TestCase):

    def setUp(self):
        initialize_database()
        self.p = Professor("", "", "", "")
        self.c = Course("", "", "")
        self.c.add_new_course("TEST101", "Test Course", "For unit testing")

    def tearDown(self):
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM professors WHERE course_id = 'TEST101'")
            cursor.execute("DELETE FROM courses WHERE course_id = 'TEST101'")
            conn.commit()

    def test_add_professor(self):
        self.p.add_new_professor("prof.test@sjsu.edu", "Test Prof", "Lecturer", "TEST101")
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM professors WHERE professor_id = 'prof.test@sjsu.edu'")
            row = cursor.fetchone()
        self.assertIsNotNone(row)
        self.assertEqual(row[1], "Test Prof")

    def test_delete_professor(self):
        self.p.add_new_professor("delete.prof@sjsu.edu", "Delete Me", "Lecturer", "TEST101")
        self.p.delete_professor("delete.prof@sjsu.edu")
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM professors WHERE professor_id = 'delete.prof@sjsu.edu'")
            row = cursor.fetchone()
        self.assertIsNone(row)

    def test_modify_professor(self):
        self.p.add_new_professor("modify.prof@sjsu.edu", "Old Name", "Lecturer", "TEST101")
        self.p.modify_professor("modify.prof@sjsu.edu", professor_name="New Name")
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT professor_name FROM professors WHERE professor_id = 'modify.prof@sjsu.edu'")
            row = cursor.fetchone()
        self.assertEqual(row[0], "New Name")

if __name__ == "__main__":
    unittest.main()