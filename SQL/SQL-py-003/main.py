from database import Database
from student import Student


# =====================================================
# DISPLAY MENU
# =====================================================

def show_menu():
    print("\n")
    print("=" * 45)
    print("       STUDENT MANAGEMENT SYSTEM")
    print("=" * 45)
    print("1. Add Student")
    print("2. View All Students")
    print("3. Search Student")
    print("4. Update Student")
    print("5. Delete Student")
    print("6. Exit")
    print("=" * 45)


# =====================================================
# ADD STUDENT
# =====================================================

def add_student(db):
    print("\n--- ADD STUDENT ---")

    try:
        student_id = int(input("Enter Student ID: "))

        name = input("Enter Name: ").strip()

        age = int(input("Enter Age: "))

        course = input("Enter Course: ").strip()

        marks = float(input("Enter Marks: "))

        # Create Student object
        student = Student(
            student_id,
            name,
            age,
            course,
            marks
        )

        # Add student to database
        db.add_student(student)

        print("\nStudent added successfully.")

    except ValueError as e:
        print(f"\nValidation Error: {e}")

    except Exception as e:
        print(f"\nError: {e}")


# =====================================================
# VIEW ALL STUDENTS
# =====================================================

def view_students(db):
    print("\n--- ALL STUDENTS ---")

    try:
        students = db.get_all_students()

        if not students:
            print("No students found.")
            return

        print("-" * 75)
        print(
            f"{'ID':<8}"
            f"{'Name':<20}"
            f"{'Age':<8}"
            f"{'Course':<15}"
            f"{'Marks':<10}"
        )
        print("-" * 75)

        for student in students:
            print(
                f"{student[0]:<8}"
                f"{student[1]:<20}"
                f"{student[2]:<8}"
                f"{student[3]:<15}"
                f"{student[4]:<10}"
            )

        print("-" * 75)

    except Exception as e:
        print(f"Error: {e}")


# =====================================================
# SEARCH STUDENT
# =====================================================

def search_student(db):
    print("\n--- SEARCH STUDENT ---")

    try:
        student_id = int(
            input("Enter Student ID to search: ")
        )

        student = db.get_student_by_id(student_id)

        if student:
            print("\nStudent Found!")
            print("-" * 35)
            print(f"Student ID : {student[0]}")
            print(f"Name       : {student[1]}")
            print(f"Age        : {student[2]}")
            print(f"Course     : {student[3]}")
            print(f"Marks      : {student[4]}")
            print("-" * 35)

        else:
            print("\nStudent not found.")

    except ValueError:
        print("\nStudent ID must be an integer.")

    except Exception as e:
        print(f"\nError: {e}")


# =====================================================
# UPDATE STUDENT
# =====================================================

def update_student(db):
    print("\n--- UPDATE STUDENT ---")

    try:
        student_id = int(
            input("Enter Student ID to update: ")
        )

        # First search for existing student
        existing_student = db.get_student_by_id(student_id)

        if not existing_student:
            print("\nStudent not found.")
            return

        # Display current information
        print("\nCurrent Student Information")
        print("-" * 35)
        print(f"Student ID : {existing_student[0]}")
        print(f"Name       : {existing_student[1]}")
        print(f"Age        : {existing_student[2]}")
        print(f"Course     : {existing_student[3]}")
        print(f"Marks      : {existing_student[4]}")
        print("-" * 35)

        print("\nEnter New Information")

        name = input("Enter New Name: ").strip()

        age = int(
            input("Enter New Age: ")
        )

        course = input("Enter New Course: ").strip()

        marks = float(
            input("Enter New Marks: ")
        )

        # Create updated Student object
        # Student ID remains unchanged
        student = Student(
            student_id,
            name,
            age,
            course,
            marks
        )

        # Update database
        affected_rows = db.update_student(student)

        if affected_rows == 1:
            print("\nStudent updated successfully.")

        else:
            print("\nStudent not found.")

    except ValueError as e:
        print(f"\nValidation Error: {e}")

    except Exception as e:
        print(f"\nError: {e}")


# =====================================================
# DELETE STUDENT
# =====================================================

def delete_student(db):
    print("\n--- DELETE STUDENT ---")

    try:
        student_id = int(
            input("Enter Student ID to delete: ")
        )

        # Find student first
        student = db.get_student_by_id(student_id)

        if not student:
            print("\nStudent not found.")
            return

        # Display student before deleting
        print("\nStudent to be deleted:")
        print("-" * 35)
        print(f"Student ID : {student[0]}")
        print(f"Name       : {student[1]}")
        print(f"Age        : {student[2]}")
        print(f"Course     : {student[3]}")
        print(f"Marks      : {student[4]}")
        print("-" * 35)

        # Confirmation
        confirmation = input(
            "Are you sure you want to delete this student? (yes/no): "
        ).strip().lower()

        if confirmation != "yes":
            print("\nDeletion cancelled.")
            return

        # Delete student
        affected_rows = db.delete_student(student_id)

        if affected_rows == 1:
            print("\nStudent deleted successfully.")

        else:
            print("\nStudent not found.")

    except ValueError:
        print("\nStudent ID must be an integer.")

    except Exception as e:
        print(f"\nError: {e}")


# =====================================================
# MAIN FUNCTION
# =====================================================

def main():

    # Create database object
    db = Database()

    try:
        # Connect to database
        db.connect()

        # Create table if it doesn't exist
        db.create_table()

        # Main application loop
        while True:

            show_menu()

            choice = input(
                "Enter your choice (1-6): "
            ).strip()

            # CREATE
            if choice == "1":
                add_student(db)

            # READ - ALL
            elif choice == "2":
                view_students(db)

            # READ - SEARCH
            elif choice == "3":
                search_student(db)

            # UPDATE
            elif choice == "4":
                update_student(db)

            # DELETE
            elif choice == "5":
                delete_student(db)

            # EXIT
            elif choice == "6":
                print("\nExiting Student Management System...")
                break

            # INVALID CHOICE
            else:
                print("\nInvalid choice.")
                print("Please enter a number between 1 and 6.")

    except Exception as e:
        print(f"\nApplication Error: {e}")

    finally:
        # Always close database
        db.close()
        print("Database connection closed.")


# =====================================================
# PROGRAM START
# =====================================================

if __name__ == "__main__":
    main()