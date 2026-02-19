# multiple_inheritance.py
# Demonstrates multiple inheritance

class Engine:
    def start_engine(self):
        print("Engine started")


class ElectricSystem:
    def charge_battery(self):
        print("Battery charging")


class ElectricCar(Engine, ElectricSystem):
    """Inherits from two parent classes"""
    
    def drive(self):
        print("Electric car is driving silently")


# Testing
tesla = ElectricCar()

tesla.start_engine()
tesla.charge_battery()
tesla.drive()
