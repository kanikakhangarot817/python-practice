from database import Database
from student import Student


# ==========================================
# DISPLAY STUDENTS
# ==========================================

def display_students(students):
    if not students:
        print("\nNo students found.")
        return

    print("\n" + "=" * 65)
    print(f"{'ID':<8}{'Name':<20}{'Course':<15}{'Marks':<10}")
    print("=" * 65)

    for student in students:
        print(
            f"{student[0]:<8}"
            f"{student[1]:<20}"
            f"{student[2]:<15}"
            f"{student[3]:<10}"
        )

    print("=" * 65)


# ==========================================
# GET VALID INTEGER
# ==========================================

def get_integer(prompt):
    while True:
        try:
            return int(input(prompt))
        except ValueError:
            print("Please enter a valid integer.")


# ==========================================
# GET VALID MARKS
# ==========================================

def get_valid_marks(prompt="Enter marks: "):
    while True:
        try:
            marks = float(input(prompt))

            if 0 <= marks <= 100:
                return marks

            print("Invalid marks. Marks must be between 0 and 100.")

        except ValueError:
            print("Please enter a valid number.")


# ==========================================
# GET VALID COURSE
# ==========================================

def get_valid_course():
    while True:
        course = input("Enter course: ").strip()

        if course:
            return course

        print("Course cannot be empty.")


# ==========================================
# ADD STUDENT
# ==========================================

def add_student(db):
    print("\n---------- ADD STUDENT ----------")

    student_id = get_integer("Enter student ID: ")

    name = input("Enter student name: ").strip()

    if not name:
        print("Name cannot be empty.")
        return

    course = get_valid_course()

    marks = get_valid_marks()

    student = Student(
        student_id,
        name,
        course,
        marks
    )

    success = db.add_student(student)

    if success:
        print("\nStudent added successfully.")
    else:
        print("\nStudent ID already exists.")


# ==========================================
# VIEW ALL STUDENTS
# ==========================================

def view_all_students(db):
    print("\n---------- ALL STUDENTS ----------")

    students = db.get_all_students()

    display_students(students)


# ==========================================
# SEARCH STUDENT BY ID
# ==========================================

def search_student_by_id(db):
    print("\n---------- SEARCH BY ID ----------")

    student_id = get_integer("Enter student ID: ")

    student = db.get_student_by_id(student_id)

    if student:
        display_students([student])
    else:
        print("\nStudent not found.")


# ==========================================
# SEARCH STUDENT BY COURSE
# ==========================================

def search_student_by_course(db):
    print("\n---------- SEARCH BY COURSE ----------")

    course = get_valid_course()

    students = db.get_students_by_course(course)

    display_students(students)


# ==========================================
# SEARCH STUDENT BY NAME
# ==========================================

def search_student_by_name(db):
    print("\n---------- SEARCH BY NAME ----------")

    keyword = input("Enter name keyword: ").strip()

    if not keyword:
        print("Search keyword cannot be empty.")
        return

    students = db.search_students_by_name(keyword)

    display_students(students)


# ==========================================
# FILTER STUDENTS BY MARKS
# ==========================================

def filter_students_by_marks(db):
    print("\n---------- FILTER BY MARKS ----------")

    min_marks = get_valid_marks(
        "Enter minimum marks: "
    )

    students = db.get_students_by_marks(min_marks)

    display_students(students)


# ==========================================
# SORT STUDENTS BY MARKS
# ==========================================

def sort_students_by_marks(db):
    print("\n---------- SORT BY MARKS ----------")

    print("1. Highest to Lowest")
    print("2. Lowest to Highest")

    choice = input("Enter your choice: ").strip()

    if choice == "1":
        students = db.get_students_sorted_by_marks(
            desc=True
        )

        display_students(students)

    elif choice == "2":
        students = db.get_students_sorted_by_marks(
            desc=False
        )

        display_students(students)

    else:
        print("Invalid choice.")


# ==========================================
# TOP N STUDENTS
# ==========================================

def top_n_students(db):
    print("\n---------- TOP N STUDENTS ----------")

    while True:
        limit = get_integer(
            "Enter number of top students: "
        )

        if limit > 0:
            break

        print(
            "Number of students must be greater than 0."
        )

    students = db.get_top_students(limit)

    display_students(students)


# ==========================================
# UPDATE STUDENT
# ==========================================

def update_student(db):
    print("\n---------- UPDATE STUDENT ----------")

    student_id = get_integer(
        "Enter student ID to update: "
    )

    existing_student = db.get_student_by_id(student_id)

    if not existing_student:
        print("\nStudent not found.")
        return

    print("\nCurrent student details:")
    display_students([existing_student])

    name = input("Enter new name: ").strip()

    if not name:
        print("Name cannot be empty.")
        return

    course = get_valid_course()

    marks = get_valid_marks(
        "Enter new marks: "
    )

    success = db.update_student(
        student_id,
        name,
        course,
        marks
    )

    if success:
        print("\nStudent updated successfully.")
    else:
        print("\nStudent update failed.")


# ==========================================
# DELETE STUDENT
# ==========================================

def delete_student(db):
    print("\n---------- DELETE STUDENT ----------")

    student_id = get_integer(
        "Enter student ID to delete: "
    )

    student = db.get_student_by_id(student_id)

    if not student:
        print("\nStudent not found.")
        return

    print("\nStudent to be deleted:")
    display_students([student])

    confirmation = input(
        "Are you sure you want to delete? (y/n): "
    ).strip().lower()

    if confirmation == "y":
        success = db.delete_student(student_id)

        if success:
            print("\nStudent deleted successfully.")
        else:
            print("\nStudent deletion failed.")

    else:
        print("\nDelete operation cancelled.")


# ==========================================
# MENU
# ==========================================

def show_menu():
    print("\n")
    print("=" * 50)
    print("       STUDENT MANAGEMENT SYSTEM")
    print("             SQL-PY-004")
    print("=" * 50)

    print("1. Add Student")
    print("2. View All Students")
    print("3. Search Student by ID")
    print("4. Search Student by Course")
    print("5. Search Student by Name")
    print("6. Filter Students by Marks")
    print("7. Sort Students by Marks")
    print("8. Top N Students")
    print("9. Update Student")
    print("10. Delete Student")
    print("11. Exit")

    print("=" * 50)


# ==========================================
# MAIN PROGRAM
# ==========================================

def main():

    db = Database()

    # Create table when program starts
    db.create_table()

    while True:

        show_menu()

        choice = input(
            "Enter your choice: "
        ).strip()

        if choice == "1":
            add_student(db)

        elif choice == "2":
            view_all_students(db)

        elif choice == "3":
            search_student_by_id(db)

        elif choice == "4":
            search_student_by_course(db)

        elif choice == "5":
            search_student_by_name(db)

        elif choice == "6":
            filter_students_by_marks(db)

        elif choice == "7":
            sort_students_by_marks(db)

        elif choice == "8":
            top_n_students(db)

        elif choice == "9":
            update_student(db)

        elif choice == "10":
            delete_student(db)

        elif choice == "11":
            db.close()
            print("\nThank you for using Student Management System.")
            break

        else:
            print("\nInvalid choice. Please select 1-11.")


# ==========================================
# PROGRAM START
# ==========================================

if __name__ == "__main__":
    main()