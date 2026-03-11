from functools import reduce

numbers = [1, 2, 3, 4, 5]

# Using map
squared = list(map(lambda x: x**2, numbers))

# Using filter
even = list(filter(lambda x: x % 2 == 0, numbers))

# Using reduce
summed = reduce(lambda a, b: a + b, numbers)

print("Squared numbers:", squared)
print("Even numbers:", even)
print("Sum of numbers:", summed)