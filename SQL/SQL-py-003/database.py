import sqlite3
from student import Student


class Database:

    def __init__(self, db_name="student_management.db"):
        self.db_name = db_name
        self.conn = None
        self.cursor = None

    def connect(self):
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()

    def create_table(self):
        query = """
        CREATE TABLE IF NOT EXISTS students (
            student_id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            age INTEGER NOT NULL CHECK(age > 0),
            course TEXT NOT NULL,
            marks REAL NOT NULL CHECK(marks >= 0 AND marks <= 100)
        )
        """

        self.cursor.execute(query)
        self.conn.commit()

    def add_student(self, student):
        student.validate()

        try:
            query = """
            INSERT INTO students
            (student_id, name, age, course, marks)
            VALUES (?, ?, ?, ?, ?)
            """

            self.cursor.execute(
                query,
                (
                    student.student_id,
                    student.name,
                    student.age,
                    student.course,
                    student.marks
                )
            )

            self.conn.commit()
            return True

        except sqlite3.Error:
            self.conn.rollback()
            raise

    def get_all_students(self):
        query = """
        SELECT student_id, name, age, course, marks
        FROM students
        ORDER BY student_id
        """

        self.cursor.execute(query)
        return self.cursor.fetchall()

    def get_student_by_id(self, student_id):
        query = """
        SELECT student_id, name, age, course, marks
        FROM students
        WHERE student_id = ?
        """

        self.cursor.execute(query, (student_id,))
        return self.cursor.fetchone()

    def update_student(self, student):
        student.validate()

        try:
            query = """
            UPDATE students
            SET name = ?, age = ?, course = ?, marks = ?
            WHERE student_id = ?
            """

            self.cursor.execute(
                query,
                (
                    student.name,
                    student.age,
                    student.course,
                    student.marks,
                    student.student_id
                )
            )

            self.conn.commit()
            return self.cursor.rowcount

        except sqlite3.Error:
            self.conn.rollback()
            raise

    def delete_student(self, student_id):
        try:
            query = """
            DELETE FROM students
            WHERE student_id = ?
            """

            self.cursor.execute(query, (student_id,))
            self.conn.commit()

            return self.cursor.rowcount

        except sqlite3.Error:
            self.conn.rollback()
            raise

    def close(self):
        if self.conn:
            self.conn.close()