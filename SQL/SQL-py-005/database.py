import sqlite3


class Database:
    def __init__(self, db_name="students.db"):
        self.db_name = db_name
        self.create_table()

    def connect(self):
        return sqlite3.connect(self.db_name)

    def create_table(self):
        conn = self.connect()
        cursor = conn.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS students (
                student_id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                course TEXT NOT NULL,
                marks REAL NOT NULL CHECK(marks >= 0 AND marks <= 100)
            )
        """)

        conn.commit()
        conn.close()

    # --------------------------------------------------
    # SQL-PY-003 / SQL-PY-004 METHODS
    # --------------------------------------------------

    def add_student(self, student_id, name, course, marks):
        conn = self.connect()
        cursor = conn.cursor()

        try:
            cursor.execute("""
                INSERT INTO students (student_id, name, course, marks)
                VALUES (?, ?, ?, ?)
            """, (student_id, name, course, marks))

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
            SELECT student_id, name, course, marks
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
            SELECT student_id, name, course, marks
            FROM students
            WHERE student_id = ?
        """, (student_id,))

        student = cursor.fetchone()

        conn.close()

        return student

    def get_students_by_course(self, course):
        conn = self.connect()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT student_id, name, course, marks
            FROM students
            WHERE course LIKE ?
        """, (f"%{course}%",))

        students = cursor.fetchall()

        conn.close()

        return students

    def get_students_by_name(self, name):
        conn = self.connect()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT student_id, name, course, marks
            FROM students
            WHERE name LIKE ?
        """, (f"%{name}%",))

        students = cursor.fetchall()

        conn.close()

        return students

    def filter_students_by_marks(self, minimum_marks):
        conn = self.connect()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT student_id, name, course, marks
            FROM students
            WHERE marks >= ?
            ORDER BY marks DESC
        """, (minimum_marks,))

        students = cursor.fetchall()

        conn.close()

        return students

    def sort_students_by_marks(self):
        conn = self.connect()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT student_id, name, course, marks
            FROM students
            ORDER BY marks DESC
        """)

        students = cursor.fetchall()

        conn.close()

        return students

    def get_top_students(self, limit):
        conn = self.connect()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT student_id, name, course, marks
            FROM students
            ORDER BY marks DESC
            LIMIT ?
        """, (limit,))

        students = cursor.fetchall()

        conn.close()

        return students

    def update_student(self, student_id, name, course, marks):
        conn = self.connect()
        cursor = conn.cursor()

        try:
            cursor.execute("""
                UPDATE students
                SET name = ?, course = ?, marks = ?
                WHERE student_id = ?
            """, (name, course, marks, student_id))

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

    # --------------------------------------------------
    # SQL-PY-005 ANALYTICS METHODS
    # --------------------------------------------------

    def get_total_students(self):
        """
        COUNT(*) counts the total number of students.
        """
        conn = self.connect()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT COUNT(*)
            FROM students
        """)

        result = cursor.fetchone()[0]

        conn.close()

        return result

    def get_average_marks(self):
        """
        AVG(marks) calculates the average marks.
        """
        conn = self.connect()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT AVG(marks)
            FROM students
        """)

        result = cursor.fetchone()[0]

        conn.close()

        return result

    def get_total_marks(self):
        """
        SUM(marks) calculates total marks.
        """
        conn = self.connect()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT SUM(marks)
            FROM students
        """)

        result = cursor.fetchone()[0]

        conn.close()

        return result

    def get_highest_marks(self):
        """
        MAX(marks) finds the highest marks.
        """
        conn = self.connect()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT MAX(marks)
            FROM students
        """)

        result = cursor.fetchone()[0]

        conn.close()

        return result

    def get_lowest_marks(self):
        """
        MIN(marks) finds the lowest marks.
        """
        conn = self.connect()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT MIN(marks)
            FROM students
        """)

        result = cursor.fetchone()[0]

        conn.close()

        return result

    def get_course_statistics(self):
        """
        Returns complete course-wise statistics.

        Uses:
        COUNT()
        AVG()
        MAX()
        MIN()
        GROUP BY
        """

        conn = self.connect()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT
                course,
                COUNT(*) AS total_students,
                AVG(marks) AS average_marks,
                MAX(marks) AS highest_marks,
                MIN(marks) AS lowest_marks
            FROM students
            GROUP BY course
            ORDER BY course
        """)

        results = cursor.fetchall()

        conn.close()

        return results

    def get_course_average_marks(self):
        """
        Returns average marks for each course.
        """

        conn = self.connect()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT
                course,
                AVG(marks) AS average_marks
            FROM students
            GROUP BY course
            ORDER BY course
        """)

        results = cursor.fetchall()

        conn.close()

        return results

    def get_course_highest_marks(self):
        """
        Returns highest marks for each course.
        """

        conn = self.connect()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT
                course,
                MAX(marks) AS highest_marks
            FROM students
            GROUP BY course
            ORDER BY course
        """)

        results = cursor.fetchall()

        conn.close()

        return results

    def get_course_lowest_marks(self):
        """
        Returns lowest marks for each course.
        """

        conn = self.connect()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT
                course,
                MIN(marks) AS lowest_marks
            FROM students
            GROUP BY course
            ORDER BY course
        """)

        results = cursor.fetchall()

        conn.close()

        return results

    def get_courses_above_average(self, min_average):
        """
        Returns courses whose average marks
        are greater than or equal to min_average.

        HAVING filters groups after GROUP BY.
        """

        conn = self.connect()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT
                course,
                AVG(marks) AS average_marks
            FROM students
            GROUP BY course
            HAVING AVG(marks) >= ?
            ORDER BY average_marks DESC
        """, (min_average,))

        results = cursor.fetchall()

        conn.close()

        return results