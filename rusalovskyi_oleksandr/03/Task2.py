'''
Task 3.2 Custom map

Implement custom_map function, which will behave like the original Python map() function.

Add docstring.

author: Oleksandr Rusalovskyi
2019-11-29
'''


def custom_map(func, *args):
    """
    Function custom_map() makes the same result as function map()
    :param func: function to be implemented for all other arguments
    :param *args: itterable arguments. Number of arguments *args should match to number of arguments in func
	:type func: function
    :type *args: iterable
    :return: Result_list after execute of func() of each set iterables elements
    :rtype: list
    """

    result_set=[]

    for i in range(len(args[0])):

        func_args = []

        for k in range(len(args)):
            func_args.append(args[k][i])

        result_set.append(func(*func_args))

    return result_set


print(list  (map(lambda n, m: n * m, [1,2,3,4,5], [0,1,2,3,4])))
print(custom_map(lambda n, m: n * m, [1,2,3,4,5], [0,1,2,3,4]))
