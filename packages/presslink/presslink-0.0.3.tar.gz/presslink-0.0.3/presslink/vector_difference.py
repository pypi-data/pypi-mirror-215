"""Subtraction of angles of 2 vectors

This script subtracts angles of 2 vectors
"""
def get_vec_diff(tha_deg, thb_deg):
	"""This function subtracts angles of 2 vectors

    Parameters
    ----------
    tha_deg : float
        angle of 1st vector in deg
    thb_deg : float
        angle of 2nd vector in deg

    Returns
    -------
    float
        difference of angles of 2 vectors
    """
	th_del_deg = tha_deg - thb_deg
	if abs(th_del_deg) > 180:
		if th_del_deg > 0:
			th_del_deg = 360 - th_del_deg
		if th_del_deg < 0:
			th_del_deg = 360 + th_del_deg
	else:
		if th_del_deg < 0:
			th_del_deg = abs(th_del_deg)

	return th_del_deg
