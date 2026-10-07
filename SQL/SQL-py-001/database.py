import sqlite3


class Database:
    def __init__(self, db_name="student_management.db"):
        self.db_name = db_name
        self.connection = None

    def connect(self):
        try:
            self.connection = sqlite3.connect(self.db_name)
            print("Database connected successfully.")
        except sqlite3.Error as e:
            print("Database connection error:", e)

    def create_table(self):
        try:
            cursor = self.connection.cursor()

            query = """
            CREATE TABLE IF NOT EXISTS students (
                student_id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                age INTEGER NOT NULL,
                course TEXT NOT NULL,
                marks REAL NOT NULL
            )
            """

            cursor.execute(query)
            self.connection.commit()

            print("Students table created successfully.")

        except sqlite3.Error as e:
            print("Table creation error:", e)

    def insert_student(self, student):
        try:
            student.validate()

            query = """
            INSERT INTO students
            (student_id, name, age, course, marks)
            VALUES (?, ?, ?, ?, ?)
            """

            cursor = self.connection.cursor()

            cursor.execute(
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

            print("Student stored successfully.")

        except ValueError as e:
            print("Validation error:", e)

        except sqlite3.Error as e:
            print("Database insertion error:", e)

    def get_all_students(self):
        try:
            cursor = self.connection.cursor()

            query = "SELECT * FROM students"

            cursor.execute(query)

            students = cursor.fetchall()

            return students

        except sqlite3.Error as e:
            print("Database retrieval error:", e)
            return []

    def get_student_by_id(self, student_id):
        try:
            cursor = self.connection.cursor()

            query = """
            SELECT * FROM students
            WHERE student_id = ?
            """

            cursor.execute(query, (student_id,))

            student = cursor.fetchone()

            return student

        except sqlite3.Error as e:
            print("Search error:", e)
            return None

    def close(self):
        if self.connection:
            self.connection.close()
            print("Database connection closed.")