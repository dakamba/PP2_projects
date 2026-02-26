#1. Convert degrees to radians
import math

deg = float(input("Input degree: "))
rad = deg * math.pi / 180
print(f"radian: {rad:.6f}")

# Input degree: 15
# Output radian: 0.261904


#2. Area of a trapezoid
h = float(input("Height: "))
b1 = float(input("Base, first value: "))
b2 = float(input("Base, second value: "))
area = 0.5 * (b1 + b2) * h
print(f"Expected Output: {area}")

# Height: 5
# Base, first value: 5
# Base, second value: 6
# Expected Output: 27.5


#3. Area of a regular polygon
n = int(input("Input number of sides: "))
s = float(input("Input the length of a side: "))
area_polygon = (n * s**2) / (4 * math.tan(math.pi / n))
print(f"The area of the polygon is: {area_polygon}")

# Input number of sides: 4
# Input the length of a side: 25
# The area of the polygon is: 625.0


#4. Area of a parallelogram
b = float(input("Length of base: "))
h_par = float(input("Height of parallelogram: "))
area_par = b * h_par
print(f"Expected Output: {area_par}")

# Length of base: 5
# Height of parallelogram: 6
# Expected Output: 30.0