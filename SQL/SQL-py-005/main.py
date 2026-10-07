from database import Database


def display_students(students):
    if not students:
        print("\nNo students found.")
        return

    print("\n" + "-" * 70)
    print(f"{'ID':<8}{'Name':<20}{'Course':<15}{'Marks':<10}")
    print("-" * 70)

    for student in students:
        student_id, name, course, marks = student

        print(
            f"{student_id:<8}"
            f"{name:<20}"
            f"{course:<15}"
            f"{marks:<10.2f}"
        )

    print("-" * 70)


def add_student(db):
    try:
        student_id = int(input("Enter student ID: "))
        name = input("Enter student name: ").strip()
        course = input("Enter course: ").strip()
        marks = float(input("Enter marks: "))

        if not name or not course:
            print("Name and course cannot be empty.")
            return

        if marks < 0 or marks > 100:
            print("Marks must be between 0 and 100.")
            return

        db.add_student(student_id, name, course, marks)

    except ValueError:
        print("Please enter valid values.")


def search_by_id(db):
    try:
        student_id = int(input("Enter student ID: "))

        student = db.get_student_by_id(student_id)

        if student:
            display_students([student])
        else:
            print("Student not found.")

    except ValueError:
        print("Please enter a valid student ID.")


def search_by_course(db):
    course = input("Enter course: ").strip()

    students = db.get_students_by_course(course)

    display_students(students)


def search_by_name(db):
    name = input("Enter student name: ").strip()

    students = db.get_students_by_name(name)

    display_students(students)


def filter_by_marks(db):
    try:
        minimum_marks = float(
            input("Enter minimum marks: ")
        )

        students = db.filter_students_by_marks(
            minimum_marks
        )

        display_students(students)

    except ValueError:
        print("Please enter valid marks.")


def sort_by_marks(db):
    students = db.sort_students_by_marks()

    display_students(students)


def top_n_students(db):
    try:
        n = int(input("Enter N: "))

        if n <= 0:
            print("N must be greater than 0.")
            return

        students = db.get_top_students(n)

        display_students(students)

    except ValueError:
        print("Please enter a valid number.")


def update_student(db):
    try:
        student_id = int(input("Enter student ID to update: "))

        existing = db.get_student_by_id(student_id)

        if not existing:
            print("Student not found.")
            return

        name = input("Enter new name: ").strip()
        course = input("Enter new course: ").strip()
        marks = float(input("Enter new marks: "))

        if not name or not course:
            print("Name and course cannot be empty.")
            return

        if marks < 0 or marks > 100:
            print("Marks must be between 0 and 100.")
            return

        db.update_student(
            student_id,
            name,
            course,
            marks
        )

    except ValueError:
        print("Please enter valid values.")


def delete_student(db):
    try:
        student_id = int(
            input("Enter student ID to delete: ")
        )

        db.delete_student(student_id)

    except ValueError:
        print("Please enter a valid student ID.")


def student_statistics(db):
    total_students = db.get_total_students()
    total_marks = db.get_total_marks()
    average_marks = db.get_average_marks()
    highest_marks = db.get_highest_marks()
    lowest_marks = db.get_lowest_marks()

    print("\n========== STUDENT STATISTICS ==========")

    print(f"Total Students : {total_students}")

    if total_marks is None:
        total_marks = 0

    if average_marks is None:
        average_marks = 0

    if highest_marks is None:
        highest_marks = 0

    if lowest_marks is None:
        lowest_marks = 0

    print(f"Total Marks    : {total_marks:.2f}")
    print(f"Average Marks  : {average_marks:.2f}")
    print(f"Highest Marks  : {highest_marks:.2f}")
    print(f"Lowest Marks   : {lowest_marks:.2f}")

    print("========================================")


def course_statistics(db):
    results = db.get_course_statistics()

    print("\n=============== COURSE-WISE STATISTICS ===============")

    if not results:
        print("No course data available.")
        print("=======================================================")
        return

    print(
        f"{'Course':<15}"
        f"{'Students':<12}"
        f"{'Average':<12}"
        f"{'Highest':<12}"
        f"{'Lowest':<12}"
    )

    print("-" * 63)

    for course, total_students, average, highest, lowest in results:

        print(
            f"{course:<15}"
            f"{total_students:<12}"
            f"{average:<12.2f}"
            f"{highest:<12.2f}"
            f"{lowest:<12.2f}"
        )

    print("=" * 63)


def courses_above_average(db):
    try:
        minimum_average = float(
            input("Enter minimum average: ")
        )

        results = db.get_courses_above_average(
            minimum_average
        )

        print(
            "\n========== COURSES ABOVE MINIMUM AVERAGE =========="
        )

        if not results:
            print("No courses found.")
            return

        print(
            f"{'Course':<20}"
            f"{'Average Marks':<20}"
        )

        print("-" * 40)

        for course, average in results:
            print(
                f"{course:<20}"
                f"{average:<20.2f}"
            )

        print("-" * 40)

    except ValueError:
        print("Please enter a valid average.")


def show_menu():
    print("\n")
    print("=" * 50)
    print("       STUDENT MANAGEMENT SYSTEM")
    print("             SQL-PY-005")
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
    print("11. Student Statistics")
    print("12. Course-wise Statistics")
    print("13. Courses Above Average")
    print("14. Exit")

    print("=" * 50)


def main():
    db = Database()

    while True:

        show_menu()

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            add_student(db)

        elif choice == "2":
            students = db.get_all_students()
            display_students(students)

        elif choice == "3":
            search_by_id(db)

        elif choice == "4":
            search_by_course(db)

        elif choice == "5":
            search_by_name(db)

        elif choice == "6":
            filter_by_marks(db)

        elif choice == "7":
            sort_by_marks(db)

        elif choice == "8":
            top_n_students(db)

        elif choice == "9":
            update_student(db)

        elif choice == "10":
            delete_student(db)

        elif choice == "11":
            student_statistics(db)

        elif choice == "12":
            course_statistics(db)

        elif choice == "13":
            courses_above_average(db)

        elif choice == "14":
            print("Thank you for using Student Management System.")
            break

        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()