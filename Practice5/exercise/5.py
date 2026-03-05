# 5. Write a Python program that matches a string that has an 'a' followed by anything, ending in 'b'.

import re

test_strings = ['ab', 'a123b', 'acb', 'a_b', 'b', 'ba']

pattern = re.compile(r'a.*b')  # 'a' followed by anything, ending with 'b'

for s in test_strings:
    if pattern.fullmatch(s):
        print(f"Match: {s}")
