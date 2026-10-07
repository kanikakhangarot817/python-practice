class Student:
    def __init__(self, student_id, name, age, course, marks):
        self.student_id = student_id
        self.name = name
        self.age = age
        self.course = course
        self.marks = marks

    def validate(self):
        if not isinstance(self.student_id, int):
            raise ValueError("Student ID must be an integer.")

        if not self.name.strip():
            raise ValueError("Name cannot be empty.")

        if not isinstance(self.age, int) or self.age <= 0:
            raise ValueError("Age must be greater than 0.")

        if not self.course.strip():
            raise ValueError("Course cannot be empty.")

        if not isinstance(self.marks, (int, float)) or not 0 <= self.marks <= 100:
            raise ValueError("Marks must be between 0 and 100.")

        return True

    def display(self):
        return (
            f"ID: {self.student_id}, "
            f"Name: {self.name}, "
            f"Age: {self.age}, "
            f"Course: {self.course}, "
            f"Marks: {self.marks}"
        )