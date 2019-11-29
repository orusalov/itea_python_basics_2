'''ask 3.3 Custom filter

Implement custom_filter function,
which will behave like the original Python filter() function.

Add docstring.

author: Oleksandr Rusalovskyi
2019-11-29
'''


def custom_filter(func, args):
    """
    Function custom_filter() makes the same as basic filter() function.
    :param func: check function to be run for each elements of args
    :param args: List for processing
    :type func: function
    :type iterables: list
    :return: list with elements which return True on func()
    :rtype: list
    """

    result_set=[]
    for arg in args:
        if func(arg):
            result_set.append(arg)

    return result_set


def alternative_lambda(n):
    return n[0]>n[1]


# Checking the results
print(list(  filter(lambda n: n[0]>n[1],[(1,9),(2,8),(3,7),(4,6),(5,5),(6,4),(7,3),(8,2),(9,1)])))
print(custom_filter(lambda n: n[0]>n[1],[(1,9),(2,8),(3,7),(4,6),(5,5),(6,4),(7,3),(8,2),(9,1)]))

print(custom_filter(alternative_lambda, [(1,9),(2,8),(3,7),(4,6),(5,5),(6,4),(7,3),(8,2),(9,1)]))
