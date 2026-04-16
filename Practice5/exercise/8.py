# 8. Write a Python program to split a string at uppercase letters.

import re

text = "HelloWorldThisIsPython"

result = re.findall(r'[A-Z][^A-Z]*', text)
print(result)
