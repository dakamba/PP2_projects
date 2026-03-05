# 2. Write a Python program that matches a string that has an 'a' followed by two to three 'b'.

import re

test_strings = ['ab', 'abb', 'abbb', 'abbbb', 'a']

pattern = re.compile(r'ab{2,3}')  # 'a' followed by 2-3 'b's

for s in test_strings:
    if pattern.fullmatch(s):
        print(f"Match: {s}")
