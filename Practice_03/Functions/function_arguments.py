# Demonstrates different argument types

def describe_student(name, age=18):
    """Prints student description"""
    print(f"Name: {name}, Age: {age}")


describe_student("Ali") # Defoult value for age is 18 thats why it is not neseccerily to give argument 'age' some value 
describe_student("Aruzhan", 20)

