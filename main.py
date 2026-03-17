from login_user import LoginUser
from student import Student
from course import Course
from professor import Professor
from grades import Grades

def main():
    print("Welcome to CheckMyGrade System")
    email = input("Email: ")
    password = input("Password: ")
    user = LoginUser(email, password, "")
    if not user.login(email, password):
        print("Incorrect email or password.")
        return
    main_menu()

def main_menu():
    while True:
        print("\nMain Menu:")
        print("1. Manage Students")
        print("2. Manage Courses")
        print("3. Manage Professors")
        print("4. Manage Grades")
        print("5. Exit")
        choice = input("Select an option: ")
        if choice == '1':
            student_menu()
        elif choice == '2':
            course_menu()
        elif choice == '3':
            professor_menu()
        elif choice == '4':
            grades_menu()
        elif choice == '5':
            print("Goodbye!")
            break
        else:
            print("Invalid option. Try again.")

def student_menu():
    s = Student("", "", "", "", "", 0)
    while True:
        print("\nStudent Menu")
        print("1. Add Student")
        print("2. Delete Student")
        print("3. Update Student")
        print("4. Display All Students")
        print("5. Search Student")
        print("6. Sort Students")
        print("7. Check Grades")
        print("0. Back")
        
        choice = input("Enter your choice: ")
        
        if choice == "1":
            email = input("Email: ")
            first = input("First name: ")
            last = input("Last name: ")
            course = input("Course ID: ")
            grade = input("Grade: ")
            marks = float(input("Marks: "))
            s.add_new_student(email, first, last, course, grade, marks)
        elif choice == "2":
            email = input("Email: ")
            s.delete_student(email)
        elif choice == "3":
            email = input("Email: ")
            first = input("First name: ")
            last = input("Last name: ")
            marks = input("Marks: ")
            s.update_student_record(email, first or None, last or None, marks=float(marks) if marks else None)
        elif choice == "4": s.display_records()
        elif choice == "5":
            email = input("Email: ")
            s.search_student(email)
        elif choice == "6":
            by = input("Sort by (marks/email_address): ")
            order = input("Order (asc/desc): ")
            s.sort_students(by, order)
        elif choice == "7":
            email = input("Email: ")
            s.check_my_grades(email)
        elif choice == "0": break
        else: print("Invalid choice.")

def course_menu():
    c = Course("", "", "")
    while True:
        print ("\nCourse Menu")
        print("1. Add Course")
        print("2. Delete Course")
        print("3. Modify Course")
        print("4. Display All Courses")
        print("5. Display Grade Report by Course")
        print("6. Average Marks for Course")
        print("7. Median Marks for Course")
        print("0. Back")
        choice = input("Enter your choice: ")
        if choice == "1":
            course_id = input("Course ID: ")
            course_name = input("Course Name: ")
            credits = int(input("Credits: "))
            c.add_new_course(course_id, course_name, credits)
        elif choice == "2":
            course_id = input("Course ID: ")
            c.delete_course(course_id) 
        elif choice == "3":
            course_id = input("Course ID: ")
            course_name = input("New Course Name (leave blank to keep current): ")
            credits = input("New Credits (leave blank to keep current): ")
            c.modify_course(course_id, course_name or None, int(credits) if credits else None)
        elif choice == "4": 
            c.display_courses()
        elif choice == "5":
            course_id = input("Course ID: ")
            c.display_grade_report_by_course(course_id)
        elif choice == "6":
            course_id = input("Course ID: ")
            c.average_marks(course_id)
        elif choice == "7":
            course_id = input("Course ID: ")
            c.median_marks(course_id)
        elif choice == "0": break
        else: print("Invalid choice.") 

def professor_menu():
    p = Professor("", "", "", "")
    while True:
        print("\nProfessor Menu")
        print("1. Add Professor")
        print("2. Delete Professor")
        print("3. Modify Professor")
        print("4. Display All Professors")
        print("5. Show Course Details by Professor")
        print("6. Display Grade Report by Professor")
        print("0. Back")
        choice = input("Enter your choice: ")
        if choice == "1":
            professor_id = input("Professor Email: ")
            professor_name = input("Professor Name: ")
            rank = input("Rank: ")
            course_id = input("Course ID: ")
            p.add_new_professor(professor_id, professor_name, rank, course_id)
        elif choice == "2":
            professor_id = input("Professor Email: ")
            p.delete_professor(professor_id)
        elif choice == "3":
            professor_id = input("Professor Email: ")
            professor_name = input("New Name (blank to skip): ")
            rank = input("New Rank (blank to skip): ")
            course_id = input("New Course ID (blank to skip): ")
            p.modify_professor(professor_id, professor_name or None, rank or None, course_id or None)
        elif choice == "4": 
            p.display_professors()
        elif choice == "5":
            professor_id = input("Professor Email: ")
            p.show_course_details_by_professor(professor_id)
        elif choice == "6":
            professor_id = input("Professor Email: ")
            p.display_grade_report_by_professor(professor_id)
        elif choice == "0": break
        else: print("Invalid choice.")

def grades_menu():
    g = Grades("", "", 0, 0)
    while True:
        print("\nGrades Menu")
        print("1. Add Grade Scale")
        print("2. Delete Grade Scale")
        print("3. Modify Grade Scale")
        print("4. Display Grade Scale")
        print("5. Look Up Grade For Marks")
        print("0. Back")
        choice = input("Enter your choice: ")
        if choice == "1":
            grade_id = input("Grade ID (e.g. A): ")
            grade = input("Grade (e.g. A): ")
            marks_min = float(input("Min Marks: "))
            marks_max = float(input("Max Marks: "))
            g.add_grade(grade_id, grade, marks_min, marks_max)
        elif choice == "2":
            grade_id = input("Grade ID: ")
            g.delete_grade(grade_id)
        elif choice == "3":
            grade_id = input("Grade ID: ")
            grade = input("New Grade: ")
            marks_min = input("New Min Marks: ")
            marks_max = input("New Max Marks: ")
            g.modify_grade(grade_id, grade or None, float(marks_min) if marks_min else None, float(marks_max) if marks_max else None)
        elif choice == "4":
            g.display_grade_report()
        elif choice == "5":
            marks = float(input("Enter marks: "))
            g.get_grade_for_marks(marks)
        elif choice == "0": break
        else: print("Invalid choice.")

if __name__ == "__main__":
    main()