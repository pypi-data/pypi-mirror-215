import math
from presslink import link4_rj4
from presslink import link5_rj4_sj1
from presslink.vector_difference import get_vec_diff


class ModularDragLink:
	"""
	A class for calculation standard drag link kinematic chain used in 
	presses
	Calculation is done in 2 parts
	In 1st part, drag link kinematic chain is solved
	1st chain involves link a, b and c. d and e are position of output link 
	rotation center
	Closed loop vector direction of 1st chain: a*e^(j*th2) + b*e^(j*th3) - 
	c*e^(j*th4) - e*e^(j*the) - d*e^(j*thd) = 0
	the is either 90 or 270 deg. thd is either 0 or 180 deg

	In 2 nd part, slider-crank kinematic chain is solved
	2nd chain involves link a, f and g. h is the slider offset which can be + or -
	Closed loop vector direction of 2nd chain: f*e^(j*th5) - 
	g*e^(j*th6) - h*e^(j*thh) - i*e^(j*thi) = 0
	thh is either 0 or 180 deg. thj is either 90 or 270 deg

	Details of first kinematc chain
	d vector is always horizontal. It is the x coordinate of center of rotation of 
	link c
	e vector is always vertical. It is the y coordinate of center of rotation of 
	link c
	If center of rotation of link c is in Q1, d is + and e is +
	If center of rotation of link c is in Q2, d is - and e is +
	If center of rotation of link c is in Q3, d is - and e is -
	If center of rotation of link c is in Q4, d is + and e is -
	Origin of coordinate system is the center of rotation of link a
	
	Details of 2nd kinematic chain
	if slider is in Q1 or Q4, h is positive, otherwise negative
	As i vector is output. it is positive if it is in Q1 or Q2, otherwise negative
	In almost all cases, j will be negative as slide moves downward (Q3 or Q4)

	Generally, there is a offset angle between output link "c" of kinematic 
	chain 1 and input link of kinematic chain2.	This angle is thcf. 
	thcf is measure in ccw direction of link c. changing this angle changes the 
	behaviour of slide slowdown. angle of inpuit link of slider crank kinematic 
	chain is found by adding this thcf angle to the angle of link c.

	Program works only in CCW direction. If your link works in CW direction, 
	just look it it from other side and it will work in CCW direction.

	...

	Attributes
	----------
	a : float
		eccentricity
	b : float
		ternary link big end to rocker center distance
	c : float
		rocker link
	d : float
		x location of rocker center of rotation (+ for Q1 and Q4, - for Q2 and Q3)
	e : float
		y location of rocker center of rotation (+ for Q1 and Q2, - for Q3 and Q4)
	f : float
		ternary link big end to conrod center distance
	g : float
		rocker link
	h : float
		slider offset from y axis (+ for Q1 and Q4, - for Q2 and Q3)
	thd_offset_ccw_dir_add : float
		offset angle between output of drag link and input of crank. It is measured 
		in ccw direction. It is positive always and is added to the output of drag 
		link angle to get the crank angle which is input of slider crank kinematic chain.
	rpm : float
		rpm of the input link
	root_op : int
		each kinematic chain has 2 roots. 
		There are total 8 root options as there are 3 kinematic chains
		This is on the user to establist which root option works for 
		particular link arrangement
		This can be done by making link diagram in CAD and match fbos and angles

	Methods
	-------
	get_th2d_lst():
		Returns list of input angle th2 in deg.
		th2 is angle of link a
	get_th3_lst():
		Returns list of angle th3 in rad
		th3 is angle of link b 
	get_th3d_lst():
		Returns list of angle th3 in deg
		th3 is angle of link b 
	get_th4_lst():
		Returns list of angle th4 in rad
		th4 is angle of link c 
	get_th4d_lst():
		Returns list of angle th4 in deg
		th4 is angle of link c 
	get_th5_lst():
		Returns list of angle th5 in rad
		th5 is angle of link f 
	get_th5d_lst():
		Returns list of angle th5 in deg
		th5 is angle of link f 
	get_th6_lst():
		Returns list of angle th6 in rad
		th6 is angle of link g
	get_th6d_lst():
		Returns list of angle th6 in deg
		th6 is angle of link g
	get_thab_lst():
		Returns list of angle thab in rad.
		thab is angle between link a and b
	get_thabd_lst():
		Returns list of angle thab in deg.
		thab is angle between link a and b
	get_thbc_lst():
		Returns list of angle thbc in rad.
		thbc is angle between link b and c
	get_thbcd_lst():
		Returns list of angle thbc in deg.
		thbc is angle between link b and c
	get_d_lst():
		Returns list of position of slide from EG gear rotating center in mm
		index of the list if crank angle in deg
		press slide moves in reverse direction as crank angle increments
	"""

	def __init__(self, a, b, c, d, e, f, g, h, thd_offset_ccw_dir_add, rpm, root_op):

		"""
		Parameters
		----------
		a : float
			eccentricity
		b : float
			ternary link big end to rocker center distance
		c : float
			rocker link
		d : float
			x location of rocker center of rotation (+ for Q1 and Q4, - for Q2 and Q3)
		e : float
			y location of rocker center of rotation (+ for Q1 and Q2, - for Q3 and Q4)
		f : float
			ternary link big end to conrod center distance
		g : float
			rocker link
		h : float
			slider offset from y axis (+ for Q1 and Q4, - for Q2 and Q3)
		thd_offset_ccw_dir_add : float
			offset angle between output of drag link and input of crank. It is measured 
			in ccw direction. It is positive always and is added to the output of drag 
			link angle to get the crank angle which is input of slider crank kinematic chain.
		rpm : float
			rpm of the input link
		root_op : int
			each kinematic chain has 2 roots. Our std drag link works well with root option 3.
			There are total 8 root options as there are 3 kinematic chains
		"""

		ts_per_deg = 1 / (6 * rpm)  # sec per degree at input crank angle

		obj1 = link4_rj4.Link4Rj4(a, b, c, d, e)  # 4 link calculations
		self.th2d_lst = obj1.get_th2d_lst()  # ecc angle list in deg
		th2_lst = obj1.get_th2_lst()  # ecc angle list in rad

		# root options
		# root op1: r1 of th3, r1 of th4, r1 of th6
		# root op2: r1 of th3, r2 of th4, r1 of th6
		# root op3: r2 of th3, r1 of th4, r1 of th6
		# root op4: r2 of th3, r2 of th4, r1 of th6
		
		# root op5: r1 of th3, r1 of th4, r2 of th6
		# root op6: r1 of th3, r2 of th4, r2 of th6
		# root op7: r2 of th3, r1 of th4, r2 of th6
		# root op8: r2 of th3, r2 of th4, r2 of th6

		#  link1
		# root op1: r1 of th3, r1 of th4, r1 of th6
		if root_op == 1 or root_op == 5:
			self.th3_lst = obj1.get_th3_1_lst()
			self.th3d_lst = obj1.get_th3d_1_lst()

			self.th4_lst = obj1.get_th4_1_lst()
			self.th4d_lst = obj1.get_th4d_1_lst()


		#  link1
		# root op2: r1 of th3, r2 of th4, r1 of th6
		if root_op == 2 or root_op == 6:
			self.th3_lst = obj1.get_th3_1_lst()  # angle of b link
			self.th3d_lst = obj1.get_th3d_1_lst()  # angle of b link

			self.th4_lst = obj1.get_th4_2_lst()  # angle of c link
			self.th4d_lst = obj1.get_th4d_2_lst()  # angle of c link

		#  link1
		# root op3: r2 of th3, r1 of th4, r1 of th6
		if root_op == 3 or root_op == 7:
			self.th3_lst = obj1.get_th3_2_lst()  # angle of b link
			self.th3d_lst = obj1.get_th3d_2_lst()  # angle of b link

			self.th4_lst = obj1.get_th4_1_lst()  # angle of c link
			self.th4d_lst = obj1.get_th4d_1_lst()  # angle of c link

		#  link1
		# root op4: r2 of th3, r2 of th4, r1 of th6
		if root_op == 4 or root_op == 8:
			self.th3_lst = obj1.get_th3_2_lst()  # angle of b link
			self.th3d_lst = obj1.get_th3d_2_lst()  # angle of b link

			self.th4_lst = obj1.get_th4_2_lst()  # angle of c link
			self.th4d_lst = obj1.get_th4d_2_lst()  # angle of c link

		self.th5_lst = []  # angle list of f link
		self.th5d_lst = []  # angle list of f link

		for x in range(360):
			this_th4 = self.th4_lst[x]
			this_th5 = this_th4 + thd_offset_ccw_dir_add * math.pi / 180
			this_th5d = this_th5 * 180 / math.pi

			self.th5_lst.append(this_th5)
			self.th5d_lst.append(this_th5d)

		obj2 = link5_rj4_sj1.Link5Rj4Sj1(f, 0, g, h, self.th5_lst, self.th5_lst)  # bottom link cal

		#  link2
		if root_op == 1 or root_op == 2 or root_op == 3 or root_op == 4:
			self.th6_lst = obj2.get_th4_1_lst()  # root 1 of th6
			self.th6d_lst = obj2.get_th4d_1_lst()  # root 1 of th6
			self.dist_lst = obj2.get_e_1_lst()  # slide dist from eg pin center

		#  link2
		if root_op == 5 or root_op == 6 or root_op == 7 or root_op == 8:
			self.th6_lst = obj2.get_th4_2_lst()  # root 2 of th6
			self.th6d_lst = obj2.get_th4d_2_lst()  # root 2 of th6
			self.dist_lst = obj2.get_e_2_lst()

		# Plot slide position
		# plt.plot(self.th2d_lst, self.dist_lst)
		# plt.show()

		# Plot conrod angle th6
		# plt.plot(self.th2d_lst, self.th6_lst)
		# plt.show()

		# Plot slide velocity
		# self.v_lst = diff_list.get_diff_lst(self.dist_lst, ts_per_deg)  # slide vel in mm/s
		# plt.plot(self.th2d_lst, self.v_lst)
		# plt.show()

		# Plot slide acc
		# self.acc_lst = diff_list.get_diff_lst(self.v_lst, ts_per_deg)  # slide acc in mm/s2
		# plt.plot(self.th2d_lst, self.acc_lst)
		# plt.show()

		self.thab_lst = []
		self.thbc_lst = []

		self.thabd_lst = []
		self.thbcd_lst = []

		for i in range(360):
			
			this_th3 = self.th3_lst[i]
			if this_th3 < 0:
				this_th3 = 2 * math.pi + this_th3  # to make angle positive (bw 0-359 deg)
			this_th3d = this_th3 * 180 / math.pi
			
			this_th2d = self.th2d_lst[i]
			this_th2 = this_th2d * math.pi/180

			this_th4 = self.th4_lst[i]
			if this_th4 < 0:
				this_th4 = 2 * math.pi + this_th4  # to make angle positive (bw 0-359 deg)
			this_th4d = this_th4 * 180 / math.pi

			this_thabd = 180 - get_vec_diff(this_th2d, this_th3d)
			this_thab = this_thabd * math.pi / 180
			# print("th_ab: ",this_thabd)

			this_thbcd = get_vec_diff(this_th3d, this_th4d)
			this_thbc = this_thbcd * math.pi / 180
			# print("th_bc: ", this_thbcd)
			# print("\n")


			self.thab_lst.append(this_thab)
			self.thabd_lst.append(this_thabd)


			self.thbc_lst.append(this_thbc)
			self.thbcd_lst.append(this_thbcd)


			# print("th2", round(this_th2 * 180 / math.pi, 1))
			# print("th3", round(this_th3 * 180 / math.pi, 1))
			# print("th4", round(self.th4_lst[i] * 180 / math.pi, 1))
			# print("thab", round(this_thab * 180 / math.pi, 1))
			# print("\n")


			# print("th2", round(this_th2 * 180 / math.pi, 1))
			# print("th3", round(this_th3 * 180 / math.pi, 1))
			# print("th4", round(this_th4 * 180 / math.pi, 1))
			# print("thbc", round(this_thbc * 180 / math.pi, 1))
			# print("\n")


	def get_th2d_lst(self):
		"""
		Returns
		-------
		list
		Returns list of input angle th2 in deg.
		th2 is angle of link a
		"""
		return self.th2d_lst

	def get_th3_lst(self):
		"""
		Returns
		-------
		list
		Returns list of angle th3 in rad.
		th3 is angle of link b
		"""
		return self.th3_lst

	def get_th3d_lst(self):
		"""
		Returns
		-------
		list
		Returns list of angle th3 in deg.
		th3 is angle of link b
		"""
		return self.th3d_lst

	def get_th4_lst(self):
		"""
		Returns
		-------
		list
		Returns list of angle th4 in rad.
		th4 is angle of link c
		"""
		return self.th4_lst

	def get_th4d_lst(self):
		"""
		Returns
		-------
		list
		Returns list of angle th4 in deg.
		th4 is angle of link c
		"""
		return self.th4d_lst

	def get_th5_lst(self):
		"""
		Returns
		-------
		list
		Returns list of angle th5 in rad.
		th5 is angle of link f
		"""
		return self.th5_lst

	def get_th5d_lst(self):
		"""
		Returns
		-------
		list
		Returns list of angle th5 in deg.
		th5 is angle of link f
		"""
		return self.th5d_lst

	def get_th6_lst(self):
		"""
		Returns
		-------
		list
		Returns list of angle th6 in rad.
		th6 is angle of link g
		"""
		return self.th6_lst

	def get_th6d_lst(self):
		"""
		Returns
		-------
		list
		Returns list of angle th6 in deg.
		th6 is angle of link g
		"""
		return self.th6d_lst

	def get_thab_lst(self):
		"""
		Returns
		-------
		list
		Returns list of angle thab in rad.
		thab is angle between link a and b
		"""
		return self.thab_lst

	def get_thabd_lst(self):
		"""
		Returns
		-------
		list
		Returns list of angle thab in deg.
		thab is angle between link a and b
		"""
		return self.thabd_lst

	def get_thbc_lst(self):
		"""
		Returns
		-------
		list
		Returns list of angle thbc in rad.
		thbc is angle between link b and c
		"""
		return self.thbc_lst

	def get_thbcd_lst(self):
		"""
		Returns
		-------
		list
		Returns list of angle thbc in deg.
		thbc is angle between link b and c
		"""
		return self.thbcd_lst

	def get_d_lst(self):
		"""
		Returns
		-------
		list
		Returns list of position of slide from EG gear rotating center in mm
		index of the list if crank angle in deg
		press slide moves in reverse direction as crank angle increments
		"""
		return self.dist_lst  # in mm
