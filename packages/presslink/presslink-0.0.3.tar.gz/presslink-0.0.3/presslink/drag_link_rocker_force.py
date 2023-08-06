"""To calculate rocker force in drag link mechanism

This script calculates force on rocker link in drag link mechanism.
2 forces are calculated. 1st is calculated when press is at rated distance.
2nd is calculated based on input torque. 2nd is generally higher than 1st and 
must be taken into conisderation while designing link.

"""

import math

def get_rocker_dic(a, trq, thab_lst, th2d_at_rd):
	"""
	Parameters
	----------
	a : float
	    gear link (input link) length of a drag link gearbox. In mm
	trq : float
	    troque on gear axis of a drag link gearbox. In Nm
	thab_lst : list
		list of angle between link a and link b in rad
	th2d_at_rd : int
		crank angle in deg at rated distance. CA is measured from + X axis

	Returns
	-------
	dictionary
	Returns dictionary object containing rocker link forces.

	dictionary item 1: fb_at_rd_ton
	It is rocker link force when press is at rated distance

	dictionary item 2: fb_max_ton
	It is max possible rocker link force due to input torque.

	dictionary item 3: th2d_at_fb_max
	It is the input gear angle where max possible rocker link force comes
	Angle is measured in CCW dir and 0 is st +ve X axis
	"""
	fat = trq / (0.001 * a)  # Tangential force on link a in N

	# calculate Fb at rated distance
	thab_at_rd = thab_lst[th2d_at_rd]
	fb_at_rd_ton = fat / (math.sin(thab_at_rd)*10000)  
	# rocker link force in ton at RD

	# calculate max possible Fb due to input torque. 
	#  This will be at min angle bw link a and b
	thab_min = min(thab_lst)
	fb_max_ton = fat / (math.sin(thab_min)*10000)  
	# max possible rocker link force in ton due to input gear torque

	# to get th2d where fb is max
	th2d_at_fb_max = thab_lst.index(thab_min)

	ans_dic = {
	'fb_at_rd_ton': round(fb_at_rd_ton, 0),
	'fb_max_ton': round(fb_max_ton, 0),
	'th2d_at_fb_max': th2d_at_fb_max,
	}

	return ans_dic
