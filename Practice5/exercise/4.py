# 4. Write a Python program to find the sequences of one upper case letter followed by lower case letters.

import re

text = "Hello World This is a Test Example"

pattern = re.compile(r'\b[A-Z][a-z]+\b')

matches = pattern.findall(text)
print(matches)
