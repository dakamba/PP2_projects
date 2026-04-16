# 3. Write a Python program to find sequences of lowercase letters joined with an underscore.

import re

text = "hello_world this_is_a_test Not_this One_more_example"

pattern = re.compile(r'\b[a-z]+(?:_[a-z]+)+\b')

matches = pattern.findall(text)
print(matches)
