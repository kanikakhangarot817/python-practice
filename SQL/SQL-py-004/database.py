import sqlite3


class Database:
    def __init__(self, db_name="students.db"):
        self.db_name = db_name

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
                marks REAL NOT NULL
            )
        """)

        conn.commit()
        conn.close()

    # -----------------------------------
    # ADD STUDENT
    # -----------------------------------

    def add_student(self, student):
        conn = self.connect()
        cursor = conn.cursor()

        try:
            cursor.execute("""
                INSERT INTO students
                (student_id, name, course, marks)
                VALUES (?, ?, ?, ?)
            """, (
                student.student_id,
                student.name,
                student.course,
                student.marks
            ))

            conn.commit()
            return True

        except sqlite3.IntegrityError:
            return False

        finally:
            conn.close()

    # -----------------------------------
    # GET ALL STUDENTS
    # -----------------------------------

    def get_all_students(self):
        conn = self.connect()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT * FROM students
        """)

        students = cursor.fetchall()

        conn.close()
        return students

    # -----------------------------------
    # GET STUDENT BY ID
    # -----------------------------------

    def get_student_by_id(self, student_id):
        conn = self.connect()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT * FROM students
            WHERE student_id = ?
        """, (student_id,))

        student = cursor.fetchone()

        conn.close()
        return student

    # -----------------------------------
    # UPDATE STUDENT
    # -----------------------------------

    def update_student(self, student_id, name, course, marks):
        conn = self.connect()
        cursor = conn.cursor()

        cursor.execute("""
            UPDATE students
            SET name = ?, course = ?, marks = ?
            WHERE student_id = ?
        """, (
            name,
            course,
            marks,
            student_id
        ))

        conn.commit()

        updated_rows = cursor.rowcount

        conn.close()

        return updated_rows > 0

    # -----------------------------------
    # DELETE STUDENT
    # -----------------------------------

    def delete_student(self, student_id):
        conn = self.connect()
        cursor = conn.cursor()

        cursor.execute("""
            DELETE FROM students
            WHERE student_id = ?
        """, (student_id,))

        conn.commit()

        deleted_rows = cursor.rowcount

        conn.close()

        return deleted_rows > 0

    # ===================================
    # SQL-PY-004 NEW METHODS
    # ===================================

    # -----------------------------------
    # SEARCH STUDENTS BY COURSE
    # -----------------------------------

    def get_students_by_course(self, course):
        conn = self.connect()
        cursor = conn.cursor()

        query = """
            SELECT * FROM students
            WHERE course = ?
        """

        cursor.execute(query, (course,))

        students = cursor.fetchall()

        conn.close()

        return students

    # -----------------------------------
    # STUDENTS ABOVE MINIMUM MARKS
    # -----------------------------------

    def get_students_by_marks(self, min_marks):
        conn = self.connect()
        cursor = conn.cursor()

        query = """
            SELECT * FROM students
            WHERE marks >= ?
        """

        cursor.execute(query, (min_marks,))

        students = cursor.fetchall()

        conn.close()

        return students

    # -----------------------------------
    # SEARCH STUDENTS BY NAME
    # -----------------------------------

    def search_students_by_name(self, keyword):
        conn = self.connect()
        cursor = conn.cursor()

        keyword = f"%{keyword}%"

        query = """
            SELECT * FROM students
            WHERE name LIKE ?
        """

        cursor.execute(query, (keyword,))

        students = cursor.fetchall()

        conn.close()

        return students

    # -----------------------------------
    # SORT STUDENTS BY MARKS
    # -----------------------------------

    def get_students_sorted_by_marks(self, desc=True):
        conn = self.connect()
        cursor = conn.cursor()

        if desc:
            query = """
                SELECT * FROM students
                ORDER BY marks DESC
            """
        else:
            query = """
                SELECT * FROM students
                ORDER BY marks ASC
            """

        cursor.execute(query)

        students = cursor.fetchall()

        conn.close()

        return students

    # -----------------------------------
    # TOP N STUDENTS
    # -----------------------------------

    def get_top_students(self, limit):
        conn = self.connect()
        cursor = conn.cursor()

        query = """
            SELECT * FROM students
            ORDER BY marks DESC
            LIMIT ?
        """

        cursor.execute(query, (limit,))

        students = cursor.fetchall()

        conn.close()

        return students

    # -----------------------------------
    # CLOSE
    # -----------------------------------

    def close(self):
        pass