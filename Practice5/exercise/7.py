# 7. Write a python program to convert snake case string to camel case string.

def snake_to_camel(snake_str):
    components = snake_str.split('_')
    return components[0] + ''.join(x.title() for x in components[1:])

text = "this_is_a_test"
print(snake_to_camel(text))
