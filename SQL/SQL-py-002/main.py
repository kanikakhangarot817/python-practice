from student import Student
from database import Database


def main():

    database = Database()

    database.connect()
    database.create_table()

    while True:

        print("\n--- Student Management System ---")
        print("1. Add Student")
        print("2. View All Students")
        print("3. Search Student")
        print("4. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":

            try:
                student_id = int(input("Enter Student ID: "))
                name = input("Enter Name: ")
                age = int(input("Enter Age: "))
                course = input("Enter Course: ")
                marks = float(input("Enter Marks: "))

                student = Student(
                    student_id,
                    name,
                    age,
                    course,
                    marks
                )

                database.add_student(student)

            except ValueError:
                print("Please enter valid numeric values.")

        elif choice == "2":

            students = database.get_all_students()

            if not students:
                print("No students found.")

            else:
                print("\n--- All Students ---")

                for student in students:
                    print(student)

        elif choice == "3":

            try:
                student_id = int(
                    input("Enter Student ID to search: ")
                )

                student = database.get_student_by_id(student_id)

                if student:
                    print("\nStudent found:")
                    print(student)

                else:
                    print("Student not found")

            except ValueError:
                print("Student ID must be a number.")

        elif choice == "4":

            database.close()

            print("Program closed.")

            break

        else:
            print("Invalid choice. Please select 1-4.")


if __name__ == "__main__":
    main()