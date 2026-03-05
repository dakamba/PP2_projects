# 10. Write a Python program to convert a given camel case string to snake case.

import re

def camel_to_snake(text):
    words = re.findall(r'[A-Z]?[a-z]+|[A-Z]+(?![a-z])', text)
    return '_'.join(word.lower() for word in words)

text1 = "camelCaseExampleTest"
text2 = "HTMLParserTest"

print(camel_to_snake(text1))  # camel_case_example_test
print(camel_to_snake(text2))  # html_parser_test
