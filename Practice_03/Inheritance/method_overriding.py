# method_overriding.py
# Demonstrates method overriding

class Vehicle:
    """Parent class"""

    def move(self):
        print("Vehicle is moving")


class Car(Vehicle):
    """Child class overriding move()"""

    def move(self):
        print("Car is driving on the road")


class Airplane(Vehicle):
    """Another child class overriding move()"""

    def move(self):
        print("Airplane is flying in the sky")


# Testing polymorphism
vehicles = [Vehicle(), Car(), Airplane()]

for v in vehicles:
    v.move()
