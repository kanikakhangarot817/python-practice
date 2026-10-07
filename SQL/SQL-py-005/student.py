class Student:
    def __init__(self, student_id, name, course, marks):
        self.student_id = student_id
        self.name = name
        self.course = course
        self.marks = marks

    def __str__(self):
        return (
            f"ID: {self.student_id}, "
            f"Name: {self.name}, "
            f"Course: {self.course}, "
            f"Marks: {self.marks}"
        )