# Demonstrates *args and **kwargs

def print_numbers(*args):
    """Prints all positional arguments"""
    for number in args:
        print(number)


def print_info(**kwargs):
    """Prints keyword arguments"""
    for key, value in kwargs.items():
        print(f"{key}: {value}")

def together(*args, **kwargs):
    '''kwargs positions have to be after *args becouse kwargs more importnt than args (args < kwargs by positions)'''


print_numbers(1, 2, 3)
print_info(name="Daulet", age=17)

