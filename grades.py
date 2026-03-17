import sqlite3
import csv
from database import get_connection

class Grades:
    def __init__(self, grade_id, grade, marks_min, marks_max):
        self.grade_id = grade_id
        self.grade = grade
        self.marks_min = marks_min
        self.marks_max = marks_max

    def add_grade(self, grade_id, grade, marks_min, marks_max):
        with get_connection() as conn:
            cursor = conn.cursor()
            try:
                cursor.execute(
                    "INSERT INTO grades (grade_id, grade, marks_min, marks_max) VALUES (?, ?, ?, ?)",
                    (grade_id, grade, marks_min, marks_max)
                )
                conn.commit()
                print(f"Grade {grade_id} added successfully.")
            except sqlite3.IntegrityError:
                print(f"Grade {grade_id} already exists.")
                return
        self.sync_to_csv()

    def delete_grade(self, grade_id):
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM grades WHERE grade_id = ?", (grade_id,))
            conn.commit()
        self.sync_to_csv()
        print(f"Grade {grade_id} deleted.")

    def modify_grade(self, grade_id, grade=None, marks_min=None, marks_max=None):
        with get_connection() as conn:
            cursor = conn.cursor()
            fields = []
            values = []
            if grade: 
                fields.append("grade = ?")
                values.append(grade)
            if marks_min is not None:
                fields.append("marks_min = ?")
                values.append(marks_min)
            if marks_max:
                fields.append("marks_max = ?")
                values.append(marks_max)
            if not fields:
                print("No fields to update.")
                return
            values.append(grade_id)
            cursor.execute(f"UPDATE grades SET {', '.join(fields)} WHERE grade_id = ?", values)
            conn.commit()
        self.sync_to_csv()
        print(f"Grade {grade_id} updated.")

    def display_grade_report(self):
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM grades")
            rows = cursor.fetchall()
        print(f"\n{'Grade ID':<12} {'Grade':<10} {'Min Marks':<12} {'Max Marks'}")
        print("-" * 45)
        for row in rows:
            print(f"{row[0]:<12} {row[1]:<10} {row[2]:<12} {row[3]}")

    def get_grade_for_marks(self, marks):
        """Look up what letter grade a mark score corresponds to."""
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT grade FROM grades WHERE ? BETWEEN marks_min AND marks_max",
                (marks,)
            )
            row = cursor.fetchone()
        if row:
            print(f"Marks {marks} corresponds to grade: {row[0]}")
            return row[0]
        else:
            print(f"No grade found for marks {marks}.")
            return None

    def sync_to_csv(self):
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM grades")
            rows = cursor.fetchall()
        with open('data/grades.csv', 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['grade_id', 'grade', 'marks_min', 'marks_max'])
            writer.writerows(rows)
        print("Grades CSV synced.")

if __name__ == "__main__":
    g = Grades("", "", 0, 0)
    g.add_grade("A", "A", 90, 100)
    g.add_grade("B", "B", 80, 89)
    g.add_grade("C", "C", 70, 79)
    g.add_grade("D", "D", 60, 69)
    g.add_grade("F", "F", 0, 59)
    g.display_grade_report()