from database import Database


def display_courses(courses):
    if not courses:
        print("\nNo courses found.")
        return

    print("\n" + "-" * 40)
    print(f"{'ID':<10}{'Course Name':<20}")
    print("-" * 40)

    for course_id, course_name in courses:
        print(f"{course_id:<10}{course_name:<20}")

    print("-" * 40)


def display_students(students):
    if not students:
        print("\nNo students found.")
        return

    print("\n" + "-" * 80)

    print(
        f"{'ID':<8}"
        f"{'Name':<18}"
        f"{'Age':<8}"
        f"{'Course':<15}"
        f"{'Marks':<10}"
    )

    print("-" * 80)

    for student in students:
        student_id, name, age, course, marks = student

        print(
            f"{student_id:<8}"
            f"{name:<18}"
            f"{age:<8}"
            f"{course:<15}"
            f"{marks:<10.2f}"
        )

    print("-" * 80)


def add_course(db):
    try:
        course_id = int(input("Enter course ID: "))
        course_name = input("Enter course name: ").strip()

        if not course_name:
            print("Course name cannot be empty.")
            return

        db.add_course(course_id, course_name)

    except ValueError:
        print("Please enter a valid course ID.")


def view_courses(db):
    courses = db.get_all_courses()
    display_courses(courses)


def add_student(db):
    try:
        student_id = int(input("Enter student ID: "))

        name = input("Enter student name: ").strip()

        age = int(input("Enter age: "))

        course_id = int(
            input("Enter course ID: ")
        )

        marks = float(
            input("Enter marks: ")
        )

        if not name:
            print("Student name cannot be empty.")
            return

        if age <= 0:
            print("Age must be greater than 0.")
            return

        if marks < 0 or marks > 100:
            print("Marks must be between 0 and 100.")
            return

        db.add_student(
            student_id,
            name,
            age,
            course_id,
            marks
        )

    except ValueError:
        print("Please enter valid values.")


def view_all_students(db):
    students = db.get_students_with_courses()

    display_students(students)


def search_student(db):
    try:
        student_id = int(
            input("Enter student ID: ")
        )

        student = db.get_student_by_id(student_id)

        if student is None:
            print("Student not found.")
            return

        print("\nStudent Found:")
        print("-" * 40)

        print(f"ID        : {student[0]}")
        print(f"Name      : {student[1]}")
        print(f"Age       : {student[2]}")
        print(f"Course ID : {student[3]}")
        print(f"Marks     : {student[4]}")

        print("-" * 40)

    except ValueError:
        print("Please enter a valid student ID.")


def search_students_by_course(db):
    course_name = input(
        "Enter course name: "
    ).strip()

    students = db.get_students_by_course(
        course_name
    )

    display_students(students)


def search_students_by_marks(db):
    try:
        minimum_marks = float(
            input("Enter minimum marks: ")
        )

        students = db.get_students_by_marks(
            minimum_marks
        )

        display_students(students)

    except ValueError:
        print("Please enter valid marks.")


def sort_students(db):
    students = db.sort_students()

    display_students(students)


def top_n_students(db):
    try:
        n = int(
            input("Enter number of students: ")
        )

        if n <= 0:
            print("Number must be greater than 0.")
            return

        students = db.get_top_students(n)

        display_students(students)

    except ValueError:
        print("Please enter a valid number.")


def update_student(db):
    try:
        student_id = int(
            input("Enter student ID: ")
        )

        existing = db.get_student_by_id(
            student_id
        )

        if existing is None:
            print("Student not found.")
            return

        name = input("Enter new name: ").strip()

        age = int(
            input("Enter new age: ")
        )

        course_id = int(
            input("Enter new course ID: ")
        )

        marks = float(
            input("Enter new marks: ")
        )

        if not name:
            print("Name cannot be empty.")
            return

        if age <= 0:
            print("Age must be greater than 0.")
            return

        if marks < 0 or marks > 100:
            print("Marks must be between 0 and 100.")
            return

        db.update_student(
            student_id,
            name,
            age,
            course_id,
            marks
        )

    except ValueError:
        print("Please enter valid values.")


def delete_student(db):
    try:
        student_id = int(
            input("Enter student ID: ")
        )

        db.delete_student(student_id)

    except ValueError:
        print("Please enter a valid student ID.")


def student_statistics(db):
    result = db.get_student_statistics()

    total_students = result[0]
    total_marks = result[1]
    average_marks = result[2]
    highest_marks = result[3]
    lowest_marks = result[4]

    print("\n========== STUDENT STATISTICS ==========")

    print(
        f"Total Students : {total_students}"
    )

    if total_marks is None:
        total_marks = 0

    if average_marks is None:
        average_marks = 0

    if highest_marks is None:
        highest_marks = 0

    if lowest_marks is None:
        lowest_marks = 0

    print(
        f"Total Marks    : {total_marks:.2f}"
    )

    print(
        f"Average Marks  : {average_marks:.2f}"
    )

    print(
        f"Highest Marks  : {highest_marks:.2f}"
    )

    print(
        f"Lowest Marks   : {lowest_marks:.2f}"
    )

    print("========================================")


def course_statistics(db):
    results = db.get_course_statistics()

    print("\n=============== COURSE STATISTICS ===============")

    if not results:
        print("No courses found.")
        return

    print(
        f"{'Course':<15}"
        f"{'Students':<12}"
        f"{'Average':<12}"
        f"{'Highest':<12}"
        f"{'Lowest':<12}"
    )

    print("-" * 63)

    for (
        course,
        total_students,
        average,
        highest,
        lowest
    ) in results:

        average_display = (
            f"{average:.2f}"
            if average is not None
            else "N/A"
        )

        highest_display = (
            f"{highest:.2f}"
            if highest is not None
            else "N/A"
        )

        lowest_display = (
            f"{lowest:.2f}"
            if lowest is not None
            else "N/A"
        )

        print(
            f"{course:<15}"
            f"{total_students:<12}"
            f"{average_display:<12}"
            f"{highest_display:<12}"
            f"{lowest_display:<12}"
        )

    print("=" * 63)


def courses_without_students(db):
    results = db.get_courses_without_students()

    print("\n========== COURSES WITHOUT STUDENTS ==========")

    if not results:
        print("All courses have students.")
        return

    for course in results:
        print(f"- {course[0]}")

    print("==============================================")


def show_menu():
    print("\n")
    print("=" * 55)
    print("       STUDENT MANAGEMENT SYSTEM")
    print("              SQL-PY-006")
    print("=" * 55)

    print("1. Add Course")
    print("2. View Courses")
    print("3. Add Student")
    print("4. View All Students")
    print("5. Search Student")
    print("6. Search Students by Course")
    print("7. Search Students by Marks")
    print("8. Sort Students")
    print("9. Top N Students")
    print("10. Update Student")
    print("11. Delete Student")
    print("12. Student Statistics")
    print("13. Course-wise Statistics")
    print("14. Courses Without Students")
    print("15. Exit")

    print("=" * 55)


def main():
    db = Database()

    while True:

        show_menu()

        choice = input(
            "Enter your choice: "
        ).strip()

        if choice == "1":
            add_course(db)

        elif choice == "2":
            view_courses(db)

        elif choice == "3":
            add_student(db)

        elif choice == "4":
            view_all_students(db)

        elif choice == "5":
            search_student(db)

        elif choice == "6":
            search_students_by_course(db)

        elif choice == "7":
            search_students_by_marks(db)

        elif choice == "8":
            sort_students(db)

        elif choice == "9":
            top_n_students(db)

        elif choice == "10":
            update_student(db)

        elif choice == "11":
            delete_student(db)

        elif choice == "12":
            student_statistics(db)

        elif choice == "13":
            course_statistics(db)

        elif choice == "14":
            courses_without_students(db)

        elif choice == "15":
            print(
                "Thank you for using "
                "Student Management System."
            )
            break

        else:
            print(
                "Invalid choice. Please select "
                "a number from 1 to 15."
            )


if __name__ == "__main__":
    main()