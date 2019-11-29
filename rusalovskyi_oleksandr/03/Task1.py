'''
Task 3.1 Array difference

Implement a difference function, which subtracts one list from another and returns the result.

It should remove all values (all of its occurrences) from list a, which are present in list b.

Add docstring.

Examples:

call: array_diff([1, 2], [1])
return: [2]

call: array_diff([1, 2, 2, 2, 3], [2])
return: [1,3]

author: Oleksandr Rusalovskyi
2019-11-29
'''


def custom_substract(initial_set,substructed_set):
    """
    Function custom_substract substracts elements of second list from first list
    :param initial_set: List to be subtracted
    :param substructed_set: List of subtracting elements
    :type initial_set: list
    :type substructed_set: list
    :return: substructed list
    :rtype: list
    """
    result_set = []
        
    for ini in initial_set:

        insert_into_result = True

        for sub in substructed_set:
            insert_into_result = insert_into_result and ini != sub

        if insert_into_result:
            result_set.append(ini)

    return result_set


print(custom_substract([1, 2, 2, 2, 3], [2]))
