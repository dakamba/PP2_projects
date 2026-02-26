#1. Generator for squares up to N
N = int(input("Enter a number N: "))
def square_generator(N):
    for i in range(N + 1):
        yield i ** 2

print("Squares up to N:")
for sq in square_generator(N):
    print(sq, end=' ')
print()

# Example Input: 5
# Output: 0 1 4 9 16 25


#2. Even numbers between 0 and n
n = int(input("Enter a number n: "))
def even_generator(n):
    for i in range(n + 1):
        if i % 2 == 0:
            yield i

print("Even numbers up to n:")
print(','.join(str(num) for num in even_generator(n)))

# Example Input: 10
# Output: 0,2,4,6,8,10

#3. Numbers divisible by 3 and 4 between 0 and n
n = int(input("Enter a number n: "))
def divisible_by_3_and_4(n):
    for i in range(n + 1):
        if i % 3 == 0 and i % 4 == 0:
            yield i

print("Numbers divisible by 3 and 4:")
for num in divisible_by_3_and_4(n):
    print(num, end=' ')
print()

# Example Input: 50
# Output: 0 12 24 36 48

#4. Squares from a to b
a = int(input("Enter starting number a: "))
b = int(input("Enter ending number b: "))
def squares(a, b):
    for i in range(a, b + 1):
        yield i ** 2

print("Squares from a to b:")
for val in squares(a, b):
    print(val, end=' ')
print()

# Example Input: 3, 7
# Output: 9 16 25 36 49

#5. Countdown from n to 0
n = int(input("Enter number n: "))
def countdown(n):
    for i in range(n, -1, -1):
        yield i

print("Countdown from n to 0:")
for num in countdown(n):
    print(num, end=' ')
print()

# Example Input: 5
# Output: 5 4 3 2 1 0