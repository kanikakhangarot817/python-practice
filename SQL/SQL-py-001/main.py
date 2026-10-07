from student import Student
from database import Database


def main():

    database = Database()

    try:
        database.connect()
        database.create_table()

        # Sample students
        students = [
            Student(1, "Rahul", 20, "BCA", 82),
            Student(2, "Priya", 21, "BCA", 88),
            Student(3, "Amit", 20, "BBA", 76),
            Student(4, "Neha", 22, "BCA", 91),
            Student(5, "Rohit", 21, "BBA", 69)
        ]

        # Insert students
        for student in students:
            database.insert_student(student)

        # Display all students
        print("\n--- All Students ---")

        all_students = database.get_all_students()

        for student in all_students:
            print(student)

        # Search student
        print("\n--- Search Student ---")

        student_id = int(input("Enter Student ID: "))

        student = database.get_student_by_id(student_id)

        if student:
            print("Student found:")
            print(student)
        else:
            print("Student not found.")

    except ValueError:
        print("Please enter a valid integer.")

    except Exception as e:
        print("Unexpected error:", e)

    finally:
        database.close()


if __name__ == "__main__":
    main()