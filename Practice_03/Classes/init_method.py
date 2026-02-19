# Demonstrates __init__ method

class Student:
    def __init__(self, name, gpa):
        self.name = name
        self.gpa = gpa


student = Student("Daulet", 4.0)
print(student.name, student.gpa)
