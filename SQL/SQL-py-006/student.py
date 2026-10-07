class Student:
    def __init__(self, student_id, name, age, course_id, marks):
        self.student_id = student_id
        self.name = name
        self.age = age
        self.course_id = course_id
        self.marks = marks

    def validate(self):
        if not isinstance(self.student_id, int):
            raise ValueError("Student ID must be an integer.")

        if not self.name.strip():
            raise ValueError("Student name cannot be empty.")

        if not isinstance(self.age, int) or self.age <= 0:
            raise ValueError("Age must be greater than 0.")

        if not isinstance(self.course_id, int):
            raise ValueError("Course ID must be an integer.")

        if self.marks < 0 or self.marks > 100:
            raise ValueError("Marks must be between 0 and 100.")

        return True

    def __str__(self):
        return (
            f"ID: {self.student_id}, "
            f"Name: {self.name}, "
            f"Age: {self.age}, "
            f"Course ID: {self.course_id}, "
            f"Marks: {self.marks}"
        )