import sqlite3
import csv
import time
from database import get_connection

class Student:
    def __init__(self, email_address, first_name, last_name, course_id, grade, marks):
        self.email_address = email_address
        self.first_name = first_name
        self.last_name = last_name
        self.course_id = course_id
        self.grade = grade
        self.marks = marks

    def add_new_student(self, email_address, first_name, last_name, course_id, grade, marks):
        #open DB

        with get_connection() as conn:
            cursor = conn.cursor()
        #Insert new student record
            try:
                cursor.execute(
                    "INSERT INTO students (email_address, first_name, last_name, course_id, grade, marks) VALUES (?, ?, ?, ?, ?, ?)",
                    (email_address, first_name, last_name, course_id, grade, marks)
                )
                conn.commit()
                print(f"Student {email_address} added successfully.")
            except sqlite3.IntegrityError as e:
                print(f"Student {email_address} already exists. Error: {e}")
                return

        # write
        self.sync_to_csv()

    def delete_student(self, email_address):
        with get_connection() as conn:
            cursor = conn.cursor()
            #deletes if email matches existing record
            cursor.execute("DELETE FROM students WHERE email_address = ?", (email_address,))
            conn.commit()
        # syncs csv
        self.sync_to_csv()
        #print result
        print(f"Student {email_address} deleted.")

    def update_student_record(self, email_address, first_name=None, last_name=None, course_id=None, grade=None, marks=None):
        #dynmically build update query based on provided fields
        with get_connection() as conn:
            cursor = conn.cursor()
            fields = []
            values = []
            if first_name:
                fields.append("first_name = ?")
                values.append(first_name)
            if last_name:
                fields.append("last_name = ?")
                values.append(last_name)
            if course_id:
                fields.append("course_id = ?")
                values.append(course_id)
            if grade:
                fields.append("grade = ?")
                values.append(grade)
            if marks is not None:
                fields.append("marks = ?")
                values.append(marks)
            if not fields:
                print("No fields to update.")
                return
            values.append(email_address)
            cursor.execute(f"UPDATE students SET {', '.join(fields)} WHERE email_address = ?", values)
            conn.commit()
        self.sync_to_csv()
        print(f"Student {email_address} updated.")

    def display_records(self):
        #prints formatted table of all student records
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM students")
            rows = cursor.fetchall()
            print(f"\n{'Email':<30} {'First':<15} {'Last':<15} {'Course':<10} {'Grade':<8} {'Marks'}")
            print("-" * 85)
            for row in rows:
                print(f"{row[0]:<30} {row[1]:<15} {row[2]:<15} {row[3]:<10} {row[4]:<8} {row[5]}")

    def check_my_grades(self, email_address):
        #prints all courses, grades, and marks for a given student email
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT course_id, grade, marks FROM students WHERE email_address = ?", (email_address,))
            rows = cursor.fetchall()
        print(f"\nGrades for {email_address}:")
        for row in rows:
            print(f"  Course: {row[0]}  Grade: {row[1]}  Marks: {row[2]}")

    def search_student(self, email_address):
        #searches for student by email and prints result with search time
        with get_connection() as conn:
            cursor = conn.cursor()
            start = time.time()
            cursor.execute("SELECT * FROM students WHERE email_address = ?", (email_address,))
            row = cursor.fetchone()
            elapsed = time.time() - start
        if row:
            print(f"Found: {row}")
        else:
            print(f"Student {email_address} not found.")
        print(f"Search time: {elapsed:.6f} seconds")
        return row

    def sort_students(self, by="marks", order="asc"):
        with get_connection() as conn:
            cursor = conn.cursor()
            direction = "ASC" if order == "asc" else "DESC"
            start = time.time()
            cursor.execute(f"SELECT * FROM students ORDER BY {by} {direction}")
            rows = cursor.fetchall()
            elapsed = time.time() - start
            print(f"\nStudents sorted by {by} ({order}):")
            for row in rows:
                print(row)
            print(f"Sort time: {elapsed:.6f} seconds")
            return rows

    def sync_to_csv(self):
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM students")
            rows = cursor.fetchall()
        with open('data/students.csv', 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['email_address', 'first_name', 'last_name', 'course_id', 'grade', 'marks'])
            writer.writerows(rows)
        print("Students CSV synced.")


if __name__ == "__main__":
    s = Student("", "", "", "", "", 0)
    s.add_new_student("jason.letargo@sjsu.edu", "Jason", "Letargo", "DATA200", "A", 96)
    s.display_records()    
