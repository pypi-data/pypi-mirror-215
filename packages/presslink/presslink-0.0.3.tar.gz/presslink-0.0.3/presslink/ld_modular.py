import math
# import matplotlib.pyplot as plt
from presslink import link4_rj4, link5_rj4_sj1
from presslink import diff_list

class ModularDrawLink:
	"""
	A class for calculation of 6 bar standard draw link kinematic chain used in 
	presses
	Calculation is done in 2 parts
	In 1st part, upper kinematic chain is solved
	1st chain involves link a, b and c. d and e are position of rocker rotation 
	center
	Closed loop vector direction of 1st chain: a*e^(j*th2) + b*e^(j*th3) - 
	c*e^(j*th4) - e*e^(j*the) - d*e^(j*thd) = 0
	the is either 90 or 270 deg. thd is either 0 or 180 deg

	In 2 nd part, lower kinematic chain is solved
	2nd chain involves link a, f and g. h is the slider offset which can be + or -
	Closed loop vector direction of 2nd chain: a*e^(j*th2) - f*e^(j*th5) - 
	g*e^(j*th6) - h*e^(j*thh) - j*e^(j*thj) = 0
	thh is either 0 or 180 deg. thj is either 90 or 270 deg

	d vector is always horizontal. It is the x coordinate of center of rotation 
	of link c
	e vector is always vertical. It is the y coordinate of center of rotation of 
	link c
	If center of rotation of link c is in Q1, d is + and e is +
	If center of rotation of link c is in Q2, d is - and e is +
	If center of rotation of link c is in Q3, d is - and e is -
	If center of rotation of link c is in Q4, d is + and e is -
	Origin of coordinate system is the center of rotation of link a
	if slider is in Q1 or Q4, h is positive, otherwise negative
	As j vector is output. it is positive if it is in Q1 or Q2, otherwise negative
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
	thd_bf : float
		angle between ternary link sides b and f in deg
	rpm : float
		rpm of input link a
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
	get_thbc_lst():
		Returns list of angle thbc (bw link b and c) in rad
	get_thbcd_lst():
		Returns list of angle thbc (bw link b and c) in deg
	get_d_lst():
		Returns list of position of slide from EG gear rotating center in mm
		index of the list if crank angle in deg
		press slide moves in reverse direction as crank angle increments
	get_v_lst():
		Returns list of velocity of slide from EG gear rotating center in mm/s
		index of the list if crank angle in deg
		press slide moves in reverse direction as crank angle increments
	get_acc_lst():
		Returns list of acceleration of slide from EG gear rotating center in mm/s2
		index of the list if crank angle in deg
		press slide moves in reverse direction as crank angle increments
	get_fbos_from_d_lst(d_lst):
		Returns list of fbos of slide in mm
		It considers that BOS is away from rotation center.
		It is true in almost all of the cases except pull down press which is rare
		index of the list if crank angle in deg
		press slide moves in reverse direction as crank angle increments
	get_th2_at_rd_lst(fbos_lst, rd):
		Returns list of all crank angles when slide is in rated zone.
		It includes both downward and upward motion of slide
	get_torque_at_rd(f, w, v_lst, th2_at_rd_lst):
		Returns 2 torque values corrsponding of rated distance when press
		is moving downward and upward.
		Take minimum of the 2 values if pressing is slower than return
	"""


	def __init__(self, a, b, c, d, e, f, g, h, thd_bf, rpm, root_op):

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
		thd_bf : float
			angle between ternary link sides b and f in deg
		rpm : float
			rpm of input link a
		root_op : int
			each kinematic chain has 2 roots. 
			There are total 8 root options as there are 3 kinematic chains
			This is on the user to establist which root option works for 
			particular link arrangement
			This can be done by making link diagram in CAD and match fbos and angles
		"""

		ts_per_deg = 1 / (6 * rpm)  # sec per degree at input crank angle
		# th_bf = triangle.get_angle(b, f, i)['th_bf']  # ter link angle in rad
		# th_fi = triangle.get_angle(b, f, i)['th_fi']  # ter link angle in rad
		# th_ib = triangle.get_angle(b, f, i)['th_ib']  # ter link angle in rad
		th_bf = thd_bf * math.pi / 180

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
			this_th3 = self.th3_lst[x]
			if this_th3 < 0:  # to make all positive
				this_th3 = 2 * math.pi + this_th3
			# this_th5 = this_th3 + th_ib + th_fi   # old
			this_th5 = this_th3 - (math.pi - th_bf)

			this_th5d = this_th5 * 180 / math.pi

			self.th5_lst.append(this_th5)
			self.th5d_lst.append(this_th5d)


		obj2 = link5_rj4_sj1.Link5Rj4Sj1(a, f, g, h, th2_lst, self.th5_lst)  # bottom link cal

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

		
		self.thbc_lst = []
		self.thbcd_lst = []
		
		for x in range(360):
			this_th3 = self.th3_lst[x]
			this_th4 = self.th4_lst[x]
			this_thbc = abs(this_th3 - this_th4)
			this_thbcd = this_thbc * 180 / math.pi
			self.thbc_lst.append(this_thbc)
			self.thbcd_lst.append(this_thbcd)


		# Plot slide position
		# plt.plot(self.th2d_lst, self.dist_lst)
		# plt.show()

		# Plot conrod angle th6
		# plt.plot(self.th2d_lst, self.th6_lst)
		# plt.show()

		# Plot slide velocity
		self.v_lst = diff_list.get_diff_lst(self.dist_lst, ts_per_deg)  # slide vel in mm/s
		# plt.plot(self.th2d_lst, self.v_lst)
		# plt.show()

		# Plot slide acc
		self.acc_lst = diff_list.get_diff_lst(self.v_lst, ts_per_deg)  # slide acc in mm/s2
		# plt.plot(self.th2d_lst, self.acc_lst)
		# plt.show()

		# self.thab_lst = []
		# for i in range(360):
		# 	this_thab = self.th3_lst[i] - self.th2d_lst[i] - math.pi
		# 	self.thab_lst.append(this_thab)


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

	def get_v_lst(self):
		"""
		Returns
		-------
		list
		Returns list of velocity of slide from EG gear rotating center in mm/s
		index of the list if crank angle in deg
		press slide moves in reverse direction as crank angle increments
		"""
		return self.v_lst  # in mm/s

	def get_acc_lst(self):
		"""
		Returns
		-------
		list
		Returns list of acceleration of slide from EG gear rotating center in mm/s2
		index of the list if crank angle in deg
		press slide moves in reverse direction as crank angle increments
		"""
		return self.acc_lst  # in mm/s2

	def get_fbos_from_d_lst(self, d_lst):
		"""
		Parameters
        ----------
        d_lst : list
			slider distance from rotation center list wrt crank angle (full 360 deg)

		Returns
		-------
		list
		Returns list of fbos of slide in mm
		It considers that BOS is away from rotation center.
		It is true in almost all of the cases except pull down press which is rare
		index of the list if crank angle in deg
		press slide moves in reverse direction as crank angle increments
		"""
		pos_lst = []
		for x in d_lst:
			pos_lst.append(abs(x))
		max_lst = max(pos_lst)
		fbos_lst = []
		for x in pos_lst:
			fbos_lst.append(max_lst - x)
		return fbos_lst

	def get_th2_at_rd_lst(self, fbos_lst, rd):
		"""
		Parameters
        ----------
        fbos_lst : list
			fbos list wrt crank angle (full 360 deg)
		rd : float
			rated distance in mm
		
		Returns
		-------
		list
		Returns list of all crank angles when slide is in rated zone.
		It includes both downward and upward motion of slide
		"""
		# fbos list must be all + values
		sub_fbos_lst = []
		# max_fbos = max(fbos_lst)
		for x in fbos_lst:
			diff = x - rd
			if diff < 0:
				diff = 0
			sub_fbos_lst.append(diff)

		fbos_zone_index_lst = []
		for i in range(len(sub_fbos_lst)):
			if sub_fbos_lst[i] == 0:
				fbos_zone_index_lst.append(i)
		th2_at_rd_lst = [fbos_zone_index_lst[0], fbos_zone_index_lst[-1]]

		return th2_at_rd_lst

	def get_torque_at_rd(self, f, w, v_lst, th2_at_rd_lst):
		"""
		Parameters
        ----------
        f : float
			press force in N
		w : float
			angular velocity of Ecc gear in rad/s
		v_lst : lst
			list of slide velocity in mm/s from crang angle th2 = 0 to th2 = 359 degrees
		th2_at_rd_lst : lst
			list of all crank angles when slide is in rated zone

		Returns
		-------
		list
		Returns 2 torque values corrsponding of rated distance when press
		is moving downward and upward.
		Take minimum of the 2 values if pressing is slower than return
		"""
		v1 = v_lst[th2_at_rd_lst[0]]
		v2 = v_lst[th2_at_rd_lst[1]]
		trq1 = round(abs(f * v1 * 0.001 / w), 0)  # Nm
		trq2 = round(abs(f * v2 * 0.001 / w), 0)  # Nm
		trq_lst = [trq1, trq2]

		return trq_lst  # Nm


"""
# program test
a = 260  # ecc
b = 800  # ter (ecc-rocker)
c = 900  # rocker
d = 1175  # rocker x
e = -375  # rocker y
f = 1175  # ter (ecc-conrod)
g = 1175  # conrod
h = -25  # slide offset x
i = 1824  # ter (rocker-conrod)
rpm = 20  # angular vel in rad/s
w = 2 * math.pi * rpm / 60

# make object
draw_link_obj = ModularDrawLink(a,b,c,d,e,f,g,h,i,rpm)

# get list of independent var th2 in deg
th2d_lst = draw_link_obj.get_th2d_lst()

# get list of th3 (ternary link angle eg-rocker connector link)
# th3d_lst = draw_link_obj.get_th3d_lst()
# plt.plot(th2d_lst, th3d_lst)
# plt.show()

# get list of th4 (rocker link angle)
# th4d_lst = draw_link_obj.get_th4d_lst()
# plt.plot(th2d_lst, th4d_lst)
# plt.show()

# get list of th5 (ternary link angle eg-conrod connector link)
# th5d_lst = draw_link_obj.get_th5d_lst()
# plt.plot(th2d_lst, th5d_lst)
# plt.show()

# get list of th4 (conrod link angle)
# th6d_lst = draw_link_obj.get_th6d_lst()
# plt.plot(th2d_lst, th6d_lst)
# plt.show()

# get distance of slider from eg center
d_lst = draw_link_obj.get_d_lst()

# get FBOS
fbos_lst = draw_link_obj.get_fbos_from_d_lst(d_lst)  # get list of fbos from 
# list of raw d. d is the distance of slider from input link rotation center
# plot FBOS Vs crank angle
plt.plot(th2d_lst, d_lst)
plt.show()


# get Slide velocity
v_lst = draw_link_obj.get_v_lst()
plt.plot(th2d_lst, v_lst)
plt.show()

# get slide acceleration
acc_lst = draw_link_obj.get_acc_lst()
# plt.plot(th2d_lst, acc_lst)
# plt.show()

th2_at_rd_lst = draw_link_obj.get_th2_at_rd_lst(fbos_lst, 13) # th2 deg crank angle 
# list where fbos is less than rd
# print(th2_at_rd_lst)
f = 25000000  # press foce in N
trq_lst = draw_link_obj.get_torque_at_rd(f, w, v_lst, th2_at_rd_lst)  # EG torque in Nm
# in above list, there will be 2 values of torque, onr corrosponding to down motion and 
# other corrosponding to up motion
# we are always interested in downward motion when pressing is done
# other value is given only to avoid unforseen mistakes in torque calculations
print(trq_lst)
"""