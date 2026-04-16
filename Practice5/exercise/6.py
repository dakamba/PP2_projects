# 6. Write a Python program to replace all occurrences of space, comma, or dot with a colon.

import re

text = "Hello, world. This is an example."

result = re.sub(r'[ ,.]', ':', text)
print(result)
