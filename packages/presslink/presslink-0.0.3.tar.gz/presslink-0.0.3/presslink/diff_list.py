"""Differentiation of list

This script differentiates a list wrt time.
"""


def get_diff_lst(lst, t):
	"""This function differentiates a list wrt time.

    Parameters
    ----------
    lst : list
        list of float values, eg position of a particle
    t : float
        time interval between 2 values in list, eg time required to 
        change in position from 1 value in list to another

    Returns
    -------
    list
        list containing differentiation of items
    """
	diff_lst = []
	copy_lst = lst[:]
	e = copy_lst.pop(0)
	copy_lst.append(e)
	for x in range(len(lst)):
		diff_lst.append((copy_lst[x] - lst[x]) / t)
	return diff_lst
