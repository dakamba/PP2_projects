
names = ["Alice", "Bob", "Charlie"]
ages = [25, 30, 35]

# Using enumerate
print("Example of enumerate:")
for i, name in enumerate(names):
    print(i, name)

# Using zip
print("\nExample of zip:")
for name, age in zip(names, ages):
    print(name, age)