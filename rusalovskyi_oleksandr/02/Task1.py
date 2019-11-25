"""Check to see if a string has the same amount of 'x's and 'o's.
The string can contain any char.

Examples:

input: "ooxx"
output: True

input: "xooxx"
output: False

input: "ooxXm"
output: True

True when no 'x' and 'o' is present
input: "zpzpzpp"
output: True

author: Oleksandr Rusalovskyi
2019-11-25
"""


# Symbols that checked should be in lowercase and only 1 symbol per position should be used
SYMBOLS_CHECK = ('x', 'o')

# list for counts of symbols
counts = []

# make counts list length the same as length of SYMBOLS_CHECK. Add "0" cause if no symbols found,
# then anyway decision will be True
for l in SYMBOLS_CHECK:
    counts.append(0)

input_string = input('Please input the string to check: ')

# letter by letter comparison
for letter in input_string.lower():

    for idx,symbol in enumerate(SYMBOLS_CHECK):

        if symbol == letter:
            # counts length the same as SYMBOLS_CHECK
            counts[idx] += 1

result = True

# counts comparison
for i in range(1,len(counts)):
    result = result and counts[i-1] == counts[i]
    
print(result)
