# Using lambda with sorted()

students = [
    {"name": "Ali", "grade": 85},
    {"name": "Aruzhan", "grade": 92},
    {"name": "Daulet", "grade": 78}
]

sorted_students = sorted(students, key=lambda x: x["grade"])

print(sorted_students)

# [  {'name': 'Daulet', 'grade': 78}, 
#    {'name': 'Ali', 'grade': 85}, 
#    {'name': 'Aruzhan', 'grade': 92}
# ] 
