"""Calculates max inclination angle of rocker link

This script calculates max inclination angle of rocker link
"""
def get_th_rkr_max(thd_lst):
	"""This function calculates max inclination angle of rocker link

    Parameters
    ----------
    thd_lst : list
        list of float values of angle of rocker link

    Returns
    -------
    float
        max inclination angle in deg
    """
	thd_pos_lst = []  # list of all positive angles
	for x in thd_lst:
		this_x = x
		if x < 0:
			this_x = x + 360
		thd_pos_lst.append(this_x)
	
	thd_max = 90  # initialize inclination of rocker link with worst possible angle
	thd_from_270_lst = []
	for x in thd_pos_lst:
		if x > 270:
			this_thd = x - 270
		else:
			this_thd = 270 - x
		thd_from_270_lst.append(this_thd)
	
	thd_max = round(max(thd_from_270_lst),0)
	
	return thd_max
