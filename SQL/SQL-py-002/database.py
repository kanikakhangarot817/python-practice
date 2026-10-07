import sqlite3
from pathlib import Path

class Database:

    def __init__(self, db_name="student_management.db"):
         self.db_name = Path(__file__).resolve().parent / db_name
         self.connection = None

    def connect(self):
        try:
            self.connection = sqlite3.connect(self.db_name)
            print("Database connected successfully")
        except sqlite3.Error as e:
            print(f"Database connection error: {e}")

    def create_table(self):
        try:
            query = """
            CREATE TABLE IF NOT EXISTS students (
                student_id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                age INTEGER NOT NULL CHECK(age > 0),
                course TEXT NOT NULL,
                marks REAL NOT NULL CHECK(marks >= 0 AND marks <= 100)
            )
            """

            self.connection.execute(query)
            self.connection.commit()

            print("Students table created successfully")

        except sqlite3.Error as e:
            print(f"Table creation error: {e}")

    def add_student(self, student):
        try:
            # Python-level validation
            student.validate()

            query = """
            INSERT INTO students
            (student_id, name, age, course, marks)
            VALUES (?, ?, ?, ?, ?)
            """

            self.connection.execute(
                query,
                (
                    student.student_id,
                    student.name,
                    student.age,
                    student.course,
                    student.marks
                )
            )

            self.connection.commit()

            print("Student added successfully")

        except ValueError as e:
            print(f"Validation error: {e}")

        except sqlite3.IntegrityError:
            self.connection.rollback()
            print("Student ID already exists")

        except sqlite3.Error as e:
            self.connection.rollback()
            print(f"Database error: {e}")

    def get_all_students(self):
        try:
            query = "SELECT * FROM students"

            cursor = self.connection.execute(query)

            return cursor.fetchall()

        except sqlite3.Error as e:
            print(f"Database error: {e}")
            return []

    def get_student_by_id(self, student_id):
        try:
            query = """
            SELECT * FROM students
            WHERE student_id = ?
            """

            cursor = self.connection.execute(
                query,
                (student_id,)
            )

            return cursor.fetchone()

        except sqlite3.Error as e:
            print(f"Database error: {e}")
            return None

    def close(self):
        if self.connection:
            self.connection.close()
            print("Database connection closed")