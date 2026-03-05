# 10. Write a Python program to convert a given camel case string to snake case.

import re

def camel_to_snake(name):
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()

text = "camelCaseExampleTest"
print(camel_to_snake(text))
