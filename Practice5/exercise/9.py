# 9. Write a Python program to insert spaces between words starting with capital letters.

import re

text = "HelloWorldThisIsPython"

result = re.sub(r'(?<!^)(?=[A-Z])', ' ', text)
print(result)
