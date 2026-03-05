#1. Write a Python program that matches a string that has an 'a' followed by zero or more 'b''s.

import re

# Test strings
test_strings = ['a', 'ab', 'abb', 'b', 'ba']

pattern = re.compile(r'ab*')  # 'a' followed by 0 or more 'b's

for s in test_strings:
    if pattern.fullmatch(s):
        print(f"Match: {s}")
