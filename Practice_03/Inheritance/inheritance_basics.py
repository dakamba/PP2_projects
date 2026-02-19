# inheritance_basics.py
# Demonstrates basic parent → child relationship

class Animal:
    """Parent class"""

    def __init__(self, name):
        self.name = name

    def speak(self):
        print(f"{self.name} makes a sound")


class Dog(Animal):
    """Child class inheriting from Animal"""

    def fetch(self):
        print(f"{self.name} is fetching the ball")


# Testing
dog = Dog("Rex")

dog.speak()   # Inherited method
dog.fetch()   # Child method
