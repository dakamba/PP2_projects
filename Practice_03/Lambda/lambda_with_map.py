# Using lambda with map()

numbers = [1, 2, 3, 4]

squared = list(map(lambda x: x * x, numbers))

print(squared) # [1, 4, 9, 16]

