import sqlite3
import csv
from database import get_connection

class Professor:
    def __init__(self, professor_id, professor_name, rank, course_id):
        self.professor_id = professor_id
        self.professor_name = professor_name
        self.rank = rank
        self.course_id = course_id

    def add_new_professor(self, professor_id, professor_name, rank, course_id):
        with get_connection() as conn:
            cursor = conn.cursor()
            try:
                cursor.execute(
                    "INSERT INTO professors (professor_id, professor_name, rank, course_id) VALUES (?, ?, ?, ?)",
                    (professor_id, professor_name, rank, course_id)
                )
                conn.commit()
                print(f"Professor {professor_id} added successfully.")
            except sqlite3.IntegrityError:
                print(f"Professor {professor_id} already exists.")
                return
        self.sync_to_csv()

    def delete_professor(self, professor_id):
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM professors WHERE professor_id = ?", (professor_id,))
            conn.commit()
        self.sync_to_csv()
        print(f"Professor {professor_id} deleted.")

    def modify_professor(self, professor_id, professor_name=None, rank=None, course_id=None):
        with get_connection() as conn:
            cursor = conn.cursor()
            fields = []
            values = []
            if professor_name: 
                fields.append("professor_name = ?")
                values.append(professor_name)
            if rank:
                fields.append("rank = ?")
                values.append(rank)
            if course_id:
                fields.append("course_id = ?")
                values.append(course_id)
            if not fields:
                print("No fields to update.")
                return
            values.append(professor_id)
            cursor.execute(f"UPDATE professors SET {', '.join(fields)} WHERE professor_id = ?", values)
            conn.commit()
        self.sync_to_csv()
        print(f"Professor {professor_id} updated.")

    def display_professors(self):
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM professors")
            rows = cursor.fetchall()
        print(f"\n{'Professor ID':<30} {'Name':<20} {'Rank':<20} {'Course ID'}")
        print("-" * 80)
        for row in rows:
            print(f"{row[0]:<30} {row[1]:<20} {row[2]:<20} {row[3]}")

    def show_course_details_by_professor(self, professor_id):
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                SELECT p.professor_name, c.course_id, c.course_name, c.credits
                FROM professors p
                JOIN courses c ON p.course_id = c.course_id
                WHERE p.professor_id = ?
                """,
                (professor_id,)
            )
            rows = cursor.fetchall()
        print(f"\nCourses for Professor {professor_id}:")
        print(f"{'Professor':<20} {'Course ID':<12} {'Course Name':<25} {'Description'}")
        print("-" * 75)
        for row in rows:
            print(f"{row[0]:<20} {row[1]:<12} {row[2]:<25} {row[3]}")

    def display_grade_report_by_professor(self, professor_id):
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                SELECT s.email_address, s.first_name, s.last_name, s.course_id, s.grade, s.marks
                FROM students s
                JOIN professors p ON s.course_id = p.course_id
                WHERE p.professor_id = ?
                """,
                (professor_id,)
            )
            rows = cursor.fetchall()
        print(f"\nGrade Report for Professor {professor_id}:")
        print(f"{'Email':<30} {'First':<15} {'Last':<15} {'Course':<10} {'Grade':<8} {'Marks'}")
        print("-" * 85)
        for row in rows:
            print(f"{row[0]:<30} {row[1]:<15} {row[2]:<15} {row[3]:<10} {row[4]:<8} {row[5]}")

    def sync_to_csv(self):
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM professors")
            rows = cursor.fetchall()
        with open('data/professors.csv', 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['professor_id', 'professor_name', 'rank', 'course_id'])
            writer.writerows(rows)
        print("Professors CSV synced.")

if __name__ == "__main__":
    p = Professor("", "", "", "")
    p.add_new_professor("paramdeep.saini@sjsu.edu", "Paramdeep Saini", "Professor", "DATA200")
    p.display_professors()