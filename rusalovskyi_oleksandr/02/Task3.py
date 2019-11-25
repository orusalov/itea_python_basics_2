"""Given an array, find the int that appears an odd number of times.
There will always be only one integer that appears an odd number of times.

Examples:

list: [1, 2, 3, 1, 3, 2, 1]
output: 1

author: Oleksandr Rusalovskyi
2019-11-25
"""


INT_LIST_TO_CHECK = (1, 2, 3, 1, 3, 2, 3)

# element by element comparison
for i in INT_LIST_TO_CHECK:

    count = 0
    for j in INT_LIST_TO_CHECK:

        if j == i:
            count += 1

    # There will always be only one integer that appears an odd number of times.
    # If we found it then break the searching cycle
    if count % 2:

        print(i)
        break
