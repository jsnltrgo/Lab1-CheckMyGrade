import unittest
import sys
import os
import time
import random
import csv
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from student import Student
from course import Course
from database import get_connection, initialize_database

class TestStudent(unittest.TestCase):

    def setUp(self):
        # seed a course first for foreign key
        initialize_database()
        self.s = Student("", "", "", "", "", 0)
        self.c = Course("", "", "")
        self.c.add_new_course("TEST101", "Test Course", "For unit testing")

    def tearDown(self):
        # clean up test records
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM students WHERE course_id = 'TEST101'")
            cursor.execute("DELETE FROM courses WHERE course_id = 'TEST101'")
            conn.commit()
        self.s.sync_to_csv()

    def test_add_student(self):
        self.s.add_new_student("test@sjsu.edu", "Test", "User", "TEST101", "A", 95)
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM students WHERE email_address = 'test@sjsu.edu'")
            row = cursor.fetchone()

        self.assertIsNotNone(row)
        self.assertEqual(row[1], "Test")
        self.assertEqual(row[5], 95)
    
    def test_delete_student(self):
        self.s.add_new_student("delete@sjsu.edu", "Delete", "Me", "TEST101", "B", 80)
        self.s.delete_student("delete@sjsu.edu")
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM students WHERE email_address = 'delete@sjsu.edu'")
            row = cursor.fetchone()
        self.assertIsNone(row)
    
    def test_update_student(self):
        self.s.add_new_student("update@sjsu.edu", "Update", "Me", "TEST101", "B", 80)
        self.s.update_student_record("update@sjsu.edu", marks=95)
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT marks FROM students WHERE email_address = 'update@sjsu.edu'")
            row = cursor.fetchone()
        self.assertEqual(row[0], 95.0)
    
    def test_1000_students(self):
        # add 1000 students
        for i in range(1000):
            email = f"student{i}@sjsu.edu"
            self.s.add_new_student(email, f"First{i}", f"Last{i}", "TEST101", "A", random.uniform(60, 100))

        # verify 1000 records exist
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM students WHERE course_id = 'TEST101'")
            count = cursor.fetchone()[0]
        self.assertEqual(count, 1000)

        # search timing
        start = time.time()
        self.s.search_student("student500@sjsu.edu")
        elapsed = time.time() - start
        print(f"\nSearch time (1000 records): {elapsed:.6f} seconds")

        # sort by marks timing defaults to ascending
        start = time.time()
        self.s.sort_students(by="marks", order="asc")
        elapsed = time.time() - start
        print(f"Sort by marks time (1000 records): {elapsed:.6f} seconds")

        # sort by email timing defaults to ascending
        start = time.time()
        self.s.sort_students(by="email_address", order="asc")
        elapsed = time.time() - start
        print(f"Sort by email time (1000 records): {elapsed:.6f} seconds")
    
    def test_sort_descending(self):
        for i in range(10):
            self.s.add_new_student(f"student{i}@sjsu.edu", f"First{i}", f"Last{i}", "TEST101", "A", float(i * 10))

        start = time.time()
        rows = self.s.sort_students(by="marks", order="desc")
        elapsed = time.time() - start
        print(f"\nSort by marks DESC time: {elapsed:.6f} seconds")
        self.assertEqual(rows[0][5], max(r[5] for r in rows)) 
        # verify descending order
        mark_values = [r[5] for r in rows]
        self.assertEqual(mark_values, sorted(mark_values, reverse=True))

        start = time.time()
        self.s.sort_students(by="email_address", order="desc")
        elapsed = time.time() - start
        print(f"Sort by email DESC time: {elapsed:.6f} seconds")

    def test_load_from_csv_and_search(self):
        self.s.add_new_student("csv_test@sjsu.edu", "CSV", "User", "TEST101", "B", 85)
        start = time.time()
        found = None
        with open('data/students.csv', newline='') as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row['email_address'] == 'csv_test@sjsu.edu':
                    found = row
                    break
        elapsed = time.time() - start
        print(f"\nCSV search time: {elapsed:.6f} seconds")
        self.assertIsNotNone(found)
        self.assertEqual(found['first_name'], 'CSV')