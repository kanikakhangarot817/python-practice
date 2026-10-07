import sqlite3


class Database:

    def __init__(self, db_name="student_management.db"):
        self.db_name = db_name
        self.create_course_table()
        self.create_student_table()

    # ==================================================
    # DATABASE CONNECTION
    # ==================================================

    def connect(self):
        conn = sqlite3.connect(self.db_name)

        # SQLite foreign keys are disabled by default.
        # This enables foreign key checking.
        conn.execute("PRAGMA foreign_keys = ON")

        return conn

    # ==================================================
    # COURSE TABLE
    # ==================================================

    def create_course_table(self):
        conn = self.connect()
        cursor = conn.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS courses (
                course_id INTEGER PRIMARY KEY,
                course_name TEXT NOT NULL UNIQUE
            )
        """)

        conn.commit()
        conn.close()

    # ==================================================
    # STUDENT TABLE
    # ==================================================

    def create_student_table(self):
        conn = self.connect()
        cursor = conn.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS students (
                student_id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                age INTEGER NOT NULL CHECK(age > 0),
                course_id INTEGER NOT NULL,
                marks REAL NOT NULL CHECK(marks >= 0 AND marks <= 100),

                FOREIGN KEY (course_id)
                    REFERENCES courses(course_id)
            )
        """)

        conn.commit()
        conn.close()

    # ==================================================
    # COURSE METHODS
    # ==================================================

    def add_course(self, course_id, course_name):
        conn = self.connect()
        cursor = conn.cursor()

        try:
            cursor.execute("""
                INSERT INTO courses (course_id, course_name)
                VALUES (?, ?)
            """, (course_id, course_name))

            conn.commit()

            print("Course added successfully.")

        except sqlite3.IntegrityError as e:
            print(f"Error: {e}")

        finally:
            conn.close()

    def get_all_courses(self):
        conn = self.connect()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT course_id, course_name
            FROM courses
            ORDER BY course_id
        """)

        courses = cursor.fetchall()

        conn.close()

        return courses

    def get_course_by_id(self, course_id):
        conn = self.connect()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT course_id, course_name
            FROM courses
            WHERE course_id = ?
        """, (course_id,))

        course = cursor.fetchone()

        conn.close()

        return course

    def delete_course(self, course_id):
        conn = self.connect()
        cursor = conn.cursor()

        try:
            cursor.execute("""
                DELETE FROM courses
                WHERE course_id = ?
            """, (course_id,))

            if cursor.rowcount == 0:
                print("Course not found.")

            else:
                conn.commit()
                print("Course deleted successfully.")

        except sqlite3.IntegrityError:
            print(
                "Cannot delete this course because "
                "students are assigned to it."
            )

        finally:
            conn.close()

    # ==================================================
    # STUDENT METHODS
    # ==================================================

    def add_student(
        self,
        student_id,
        name,
        age,
        course_id,
        marks
    ):
        # First verify course exists
        course = self.get_course_by_id(course_id)

        if course is None:
            print("Invalid course ID.")
            return

        conn = self.connect()
        cursor = conn.cursor()

        try:
            cursor.execute("""
                INSERT INTO students (
                    student_id,
                    name,
                    age,
                    course_id,
                    marks
                )
                VALUES (?, ?, ?, ?, ?)
            """, (
                student_id,
                name,
                age,
                course_id,
                marks
            ))

            conn.commit()

            print("Student added successfully.")

        except sqlite3.IntegrityError as e:
            print(f"Error: {e}")

        finally:
            conn.close()

    def get_all_students(self):
        conn = self.connect()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT
                student_id,
                name,
                age,
                course_id,
                marks
            FROM students
            ORDER BY student_id
        """)

        students = cursor.fetchall()

        conn.close()

        return students

    def get_student_by_id(self, student_id):
        conn = self.connect()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT
                student_id,
                name,
                age,
                course_id,
                marks
            FROM students
            WHERE student_id = ?
        """, (student_id,))

        student = cursor.fetchone()

        conn.close()

        return student

    def update_student(
        self,
        student_id,
        name,
        age,
        course_id,
        marks
    ):
        # Verify course
        course = self.get_course_by_id(course_id)

        if course is None:
            print("Invalid course ID.")
            return

        conn = self.connect()
        cursor = conn.cursor()

        try:
            cursor.execute("""
                UPDATE students
                SET
                    name = ?,
                    age = ?,
                    course_id = ?,
                    marks = ?
                WHERE student_id = ?
            """, (
                name,
                age,
                course_id,
                marks,
                student_id
            ))

            if cursor.rowcount == 0:
                print("Student not found.")

            else:
                conn.commit()
                print("Student updated successfully.")

        except sqlite3.IntegrityError as e:
            print(f"Error: {e}")

        finally:
            conn.close()

    def delete_student(self, student_id):
        conn = self.connect()
        cursor = conn.cursor()

        cursor.execute("""
            DELETE FROM students
            WHERE student_id = ?
        """, (student_id,))

        if cursor.rowcount == 0:
            print("Student not found.")

        else:
            conn.commit()
            print("Student deleted successfully.")

        conn.close()

    # ==================================================
    # INNER JOIN
    # ==================================================

    def get_students_with_courses(self):
        conn = self.connect()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT
                s.student_id,
                s.name,
                s.age,
                c.course_name,
                s.marks
            FROM students AS s
            INNER JOIN courses AS c
                ON s.course_id = c.course_id
            ORDER BY s.student_id
        """)

        results = cursor.fetchall()

        conn.close()

        return results

    # ==================================================
    # SEARCH STUDENTS BY COURSE
    # ==================================================

    def get_students_by_course(self, course_name):
        conn = self.connect()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT
                s.student_id,
                s.name,
                s.age,
                c.course_name,
                s.marks
            FROM students AS s
            INNER JOIN courses AS c
                ON s.course_id = c.course_id
            WHERE c.course_name = ?
            ORDER BY s.marks DESC
        """, (course_name,))

        results = cursor.fetchall()

        conn.close()

        return results

    # ==================================================
    # SEARCH STUDENTS BY MARKS
    # ==================================================

    def get_students_by_marks(self, minimum_marks):
        conn = self.connect()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT
                s.student_id,
                s.name,
                s.age,
                c.course_name,
                s.marks
            FROM students AS s
            INNER JOIN courses AS c
                ON s.course_id = c.course_id
            WHERE s.marks >= ?
            ORDER BY s.marks DESC
        """, (minimum_marks,))

        results = cursor.fetchall()

        conn.close()

        return results

    # ==================================================
    # SORT STUDENTS
    # ==================================================

    def sort_students(self):
        conn = self.connect()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT
                s.student_id,
                s.name,
                s.age,
                c.course_name,
                s.marks
            FROM students AS s
            INNER JOIN courses AS c
                ON s.course_id = c.course_id
            ORDER BY s.marks DESC
        """)

        results = cursor.fetchall()

        conn.close()

        return results

    # ==================================================
    # TOP N STUDENTS
    # ==================================================

    def get_top_students(self, limit):
        conn = self.connect()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT
                s.student_id,
                s.name,
                s.age,
                c.course_name,
                s.marks
            FROM students AS s
            INNER JOIN courses AS c
                ON s.course_id = c.course_id
            ORDER BY s.marks DESC
            LIMIT ?
        """, (limit,))

        results = cursor.fetchall()

        conn.close()

        return results

    # ==================================================
    # STUDENT STATISTICS
    # ==================================================

    def get_student_statistics(self):
        conn = self.connect()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT
                COUNT(*) AS total_students,
                SUM(marks) AS total_marks,
                AVG(marks) AS average_marks,
                MAX(marks) AS highest_marks,
                MIN(marks) AS lowest_marks
            FROM students
        """)

        result = cursor.fetchone()

        conn.close()

        return result

    # ==================================================
    # COURSE STATISTICS
    # LEFT JOIN + GROUP BY
    # ==================================================

    def get_course_statistics(self):
        conn = self.connect()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT
                c.course_name,
                COUNT(s.student_id) AS total_students,
                AVG(s.marks) AS average_marks,
                MAX(s.marks) AS highest_marks,
                MIN(s.marks) AS lowest_marks
            FROM courses AS c
            LEFT JOIN students AS s
                ON c.course_id = s.course_id
            GROUP BY c.course_id, c.course_name
            ORDER BY c.course_id
        """)

        results = cursor.fetchall()

        conn.close()

        return results

    # ==================================================
    # COURSES WITHOUT STUDENTS
    # ==================================================

    def get_courses_without_students(self):
        conn = self.connect()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT
                c.course_name
            FROM courses AS c
            LEFT JOIN students AS s
                ON c.course_id = s.course_id
            WHERE s.student_id IS NULL
            ORDER BY c.course_id
        """)

        results = cursor.fetchall()

        conn.close()

        return results