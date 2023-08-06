"""Remove the peak of false differentiation

Remove the peak of false differentiation of list where angle of raw list before 
differentiation jumps from 359 to 0. This creates a false peak which can be removed by this script
"""


def peak_remover(lst):
	"""
    Parameters
    ----------
    lst : list
        list of float values, eg position of a particle

    Returns
    -------
    list
    Returns the list after removing the false peak when angle jumps from 359 to 0
    """
	
	max_lst = max(lst)  # get max value in list
	index_max_lst = lst.index(max_lst)  # get index of max value in list
	
	index_max_nxt_lst = index_max_lst + 1  # get index of next to max value in list
	max_nxt_lst = lst[index_max_nxt_lst]  # get value at above index in list
	
	index_max_prv_lst = index_max_lst - 1  # get index of previous to max value in list
	max_prv_lst = lst[index_max_prv_lst]  # get value at above index in list

	lst[index_max_lst] = (max_nxt_lst + max_prv_lst) / 2  # take avg of prev and nxt value

	# smoothn the min peak
	min_lst = min(lst)  # get max value in list
	index_min_lst = lst.index(min_lst)  # get index of max value in list

	index_min_nxt_lst = index_min_lst + 1  # get index of next to max value in list
	min_nxt_lst = lst[index_min_nxt_lst]  # get value at above index in list

	index_min_prv_lst = index_min_lst - 1  # get index of previous to max value in list
	min_prv_lst = lst[index_min_prv_lst]  # get value at above index in list

	lst[index_min_lst] = (min_nxt_lst + min_prv_lst) / 2  # take avg of prev and nxt value
	
	return lst
	