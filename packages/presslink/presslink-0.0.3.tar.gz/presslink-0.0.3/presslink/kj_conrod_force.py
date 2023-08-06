"""To calculate horizontal connecting rod force in knuckle joint (KJ) mechanism

This script calculates force on horizontal conrod link in KJ mechanism.
"""
import math

def get_conrod_force(a, trq, thabd_at_rd):
	"""
    Parameters
    ----------
    a : float
        gear link (input link) length of a drag link gearbox. In mm
    trq : float
        troque on gear axis of a drag link gearbox. In Nm
    thabd_at_rd : float
    	angle between link a and b at rd in deg
        link b is the horizontal conrod

    Returns
    -------
    float
    Returns force on conrod in ton
    """

	thab_at_rd = thabd_at_rd * math.pi / 180
	bp = a * math.sin(thab_at_rd) / 1000  # perpend dist of b from origin in m
	fb_ton = round((trq / bp) / 10000, 0)  # rocker link force in ton 
	return fb_ton
