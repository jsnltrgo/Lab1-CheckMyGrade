import unittest
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from course import Course
from database import get_connection, initialize_database

class TestCourse(unittest.TestCase):

    def setUp(self):
        initialize_database()
        self.c = Course("", "", "")

    def tearDown(self):
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM courses WHERE course_id LIKE 'TEST%'")
            conn.commit()
        self.c.sync_to_csv()

    def test_add_course(self):
        self.c.add_new_course("TEST101", "Test Course", 3)
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM courses WHERE course_id = 'TEST101'")
            row = cursor.fetchone()
        self.assertIsNotNone(row)
        self.assertEqual(row[1], "Test Course")

    def test_delete_course(self):
        self.c.add_new_course("TEST102", "Delete Me", 1)
        self.c.delete_course("TEST102")
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM courses WHERE course_id = 'TEST102'")
            row = cursor.fetchone()
        self.assertIsNone(row)

    def test_modify_course(self):
        self.c.add_new_course("TEST103", "Old Name", 3)
        self.c.modify_course("TEST103", course_name="New Name")
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT course_name FROM courses WHERE course_id = 'TEST103'")
            row = cursor.fetchone()
        self.assertEqual(row[0], "New Name")

if __name__ == "__main__":
    unittest.main()