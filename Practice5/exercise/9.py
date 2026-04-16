# 9. Write a Python program to insert spaces between words starting with capital letters.

import re

text = "HelloWorldThisIsPython"

words = re.findall(r'[A-Z][a-z]*', text)

result = ' '.join(words)
print(result)
