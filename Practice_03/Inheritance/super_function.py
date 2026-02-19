# super_function.py
# Demonstrates usage of super() to call parent constructor

class Person:
    """Parent class"""

    def __init__(self, name, age):
        self.name = name
        self.age = age
        print("Person initialized")

    def introduce(self):
        print(f"My name is {self.name} and I am {self.age} years old.")


class Student(Person):
    """Child class using super()"""

    def __init__(self, name, age, university):
        # Call parent constructor
        super().__init__(name, age)
        self.university = university
        print("Student initialized")

    def study(self):
        print(f"{self.name} studies at {self.university}")


# Testing
student = Student("Daulet", 17, "KazNU")

student.introduce()  # From parent
student.study()      # From child
