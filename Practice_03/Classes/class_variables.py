# Demonstrates class variables

class Student:
    school_name = "Physics and Math School"

    def __init__(self, name):
        self.name = name


print(Student.school_name)
