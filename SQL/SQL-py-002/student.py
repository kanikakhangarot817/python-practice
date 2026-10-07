class Student:

    def __init__(self, student_id, name, age, course, marks):
        self.student_id = student_id
        self.name = name
        self.age = age
        self.course = course
        self.marks = marks

    def validate(self):

        if not self.name.strip():
            raise ValueError("Student name cannot be empty")

        if self.age <= 0:
            raise ValueError("Age must be greater than 0")

        if not self.course.strip():
            raise ValueError("Course cannot be empty")

        if not isinstance(self.marks, (int, float)):
            raise ValueError("Marks must be a number")

        if self.marks < 0 or self.marks > 100:
            raise ValueError("Marks must be between 0 and 100")

        return True