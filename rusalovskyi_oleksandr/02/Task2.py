"""

Task 2.2 - Reverse String

Reverse a string

Examples:

input: "Hello"
output: "olleH"

author: Oleksandr Rusalovskyi
2019-11-25
"""


output = ''

input_string = input('Please input the string to reverse: ')

# index will be used for reverse access
for i in range(1, len(input_string) + 1):
    output += input_string[-i]

"""alternative version:
for letter in input_string:
    output = letter + output
"""

print(output)
