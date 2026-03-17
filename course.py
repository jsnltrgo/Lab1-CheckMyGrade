import sqlite3
import csv
from database import get_connection

class Course:
    def __init__(self, course_id, course_name, credits):
        self.course_id = course_id
        self.course_name = course_name
        self.credits = credits

    def add_new_course(self, course_id, course_name, credits):
        with get_connection() as conn:
            cursor = conn.cursor()
            try:
                cursor.execute(
                    "INSERT INTO courses (course_id, course_name, credits) VALUES (?, ?, ?)",
                    (course_id, course_name, credits)
                )
                conn.commit()
                print(f"Course {course_id} added successfully.")
            except sqlite3.IntegrityError:
                print(f"Course {course_id} already exists.")
                return
        self.sync_to_csv()

    def delete_course(self, course_id):
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM courses WHERE course_id = ?", (course_id,))
            conn.commit()
        self.sync_to_csv()
        print(f"Course {course_id} deleted.")

    def modify_course(self, course_id, course_name=None, credits=None):
        with get_connection() as conn:
            cursor = conn.cursor()
            fields = []
            values = []
            if course_name:
                fields.append("course_name = ?")
                values.append(course_name)
            if credits is not None:
                fields.append("credits = ?")
                values.append(credits)
            if not fields:
                print("No fields to update.")
                return
            values.append(course_id)
            cursor.execute(f"UPDATE courses SET {', '.join(fields)} WHERE course_id = ?", values)
            conn.commit()
        self.sync_to_csv()
        print(f"Course {course_id} updated.")

    def display_courses(self):
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM courses")
            rows = cursor.fetchall()
        # display with column spacers
        print(f"\n{'Course ID':<12} {'Course Name':<25} {'Credits'}")
        print("-" * 60)
        for row in rows:
            print(f"{row[0]:<12} {row[1]:<25} {row[2]}")

    def display_grade_report_by_course(self, course_id):
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT email_address, first_name, last_name, grade, marks FROM students WHERE course_id = ?",
                (course_id,)
            )
            rows = cursor.fetchall()
            print(f"\nGrade Report for {course_id}:")
            print(f"{'Email':<30} {'First':<15} {'Last':<15} {'Grade':<8} {'Marks'}")
            print("-" * 75)
            for row in rows:
                print(f"{row[0]:<30} {row[1]:<15} {row[2]:<15} {row[3]:<8} {row[4]}")
    
    def average_marks(self, course_id):
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT AVG(marks) FROM students WHERE course_id = ?", (course_id,))
            avg = cursor.fetchone()[0]
        print(f"Average marks for {course_id}: {avg:.2f}")
        return avg

    def median_marks(self, course_id):
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT marks FROM students WHERE course_id = ? ORDER BY marks", (course_id,))
            marks = [row[0] for row in cursor.fetchall()]
        n = len(marks)
        if n == 0:
            print("No records found.")
            return None
        median = marks[n // 2] if n % 2 != 0 else (marks[n // 2 - 1] + marks[n // 2]) / 2
        print(f"Median marks for {course_id}: {median}")
        return median

    def sync_to_csv(self):
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM courses")
            rows = cursor.fetchall()
        with open('data/courses.csv', 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['course_id', 'course_name', 'credits'])
            writer.writerows(rows)
        print("Courses CSV synced.")

if __name__ == "__main__":
    c = Course("", "", "")
    c.add_new_course("DATA200", "Programming for Data Intelligence", 3)
    c.display_courses()
