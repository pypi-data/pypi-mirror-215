import math
# import matplotlib.pyplot as plt

class Link5Rj4Sj1:
	"""
	A class for calculation of 5 link kinematic chain with 4 Revolute Joints and 1 Slider (Prismatic) joint
	Contains only positional analysis.
	Closed loop vector direction: a*e^(j*th2) - b*e^(j*th3) - c*e^(j*th4) - e*e^(j*th5) - d*e^(j*th6) = 0
	Center of rotation point in above is in Q1
	d vector is always horizontal. It is the x coordinate of slide center 
	e vector is always vertical. It is the y coordinate of slide center
	If slider is in Q1, d is + and e is +
	If slider is in Q2, d is - and e is +
	If slider is in Q3, d is - and e is -
	If slider is in Q4, d is + and e is -
	Origin of coordinate system is the center of rotation of link a

	...

	Attributes
	----------

	Methods
	------- 
	get_th4_1_lst():
		Returns list of 1st root of angle th4 in rad
		th4 is angle of link c 
	get_th4d_1_lst():
		Returns list of 1st root of angle th4 in deg
		th4 is angle of link c 
	get_th4_2_lst():
		Returns list of 2nd root of angle th4 in rad
		th4 is angle of link c 
	get_th4d_2_lst():
		Returns list of 2nd root of angle th4 in deg
		th4 is angle of link c 
	get_e_1_lst():
		Returns the root 1 of the y coordinate of slide center
	get_e_2_lst():
		Returns the root 3 of the y coordinate of slide center
	"""
	def __init__(self, a, b, c, d, th2_lst, th3_lst):
		"""
		Parameters
		----------
		a : float
			input 1 link length
		b : float
			input 2 link length
		c : float
			conrod link length
		d : float
			x location of slider center point (+ for Q1 and Q4, - for Q2 and Q3)
		th2_lst : list
			list of angle th2 covering full rotation in rad
		th3_lst : list
			list of angle th3 in rad corrosponding to index as th2 deg angle
		"""

		self.th4_1_lst = []
		self.th4d_1_lst = []

		self.th4_2_lst = []
		self.th4d_2_lst = []


		self.e_1_lst = []
		self.e_2_lst = []
		self.v_thd_lst = []

		for i in range(360):
			th2 = th2_lst[i]
			th3 = th3_lst[i]
			try:
				th4_1 = math.acos((a*math.cos(th2)-b*math.cos(th3)-d)/(c))
				if th4_1 < 0: th4_1 = th4_1 + 2 * math.pi
			except Exception as e:
				# print(e)
				th4_1 = 0
			
			th4d_1 = th4_1 * 180 / math.pi

			th4_2 = - th4_1
			if th4_2 < 0: th4_2 = th4_2 + 2 * math.pi
			th4d_2 = th4_2 * 180 / math.pi

			try:
				e_1 = a*math.sin(th2) - b*math.sin(th3)-c*math.sin(th4_1)
			except Exception as e:
				# print(e)
				e_1 = 0
			try:
				e_2 = a*math.sin(th2) - b*math.sin(th3)-c*math.sin(th4_2)
			except Exception as e:
				# print(e)
				e_2 = 0
			self.v_thd_lst.append(i)
			self.th4_1_lst.append(th4_1)
			self.th4d_1_lst.append(th4d_1)

			self.th4_2_lst.append(th4_2)
			self.th4d_2_lst.append(th4d_2)

			self.e_1_lst.append(e_1)
			self.e_2_lst.append(e_2)


	def get_th4_1_lst(self):
		"""
		Returns
		-------
		float
		Returns list of 1st root of angle th4 in rad
		th4 is angle of link c
		"""
		return self.th4_1_lst

	def get_th4d_1_lst(self):
		"""
		Returns
		-------
		float
		Returns list of 1st root of angle th4 in deg
		th4 is angle of link c
		"""
		return self.th4d_1_lst

	def get_th4_2_lst(self):
		"""
		Returns
		-------
		float
		Returns list of 2nd root of angle th4 in rad
		th4 is angle of link c
		"""
		return self.th4_2_lst

	def get_th4d_2_lst(self):
		"""
		Returns
		-------
		float
		Returns list of 2nd root of angle th4 in deg
		th4 is angle of link c
		"""
		return self.th4d_2_lst

	def get_e_1_lst(self):
		"""
		Returns
		-------
		float
		Returns the root 1 of the y coordinate of slide center
		"""
		return self.e_1_lst

	def get_e_2_lst(self):
		"""
		Returns
		-------
		float
		Returns the root 2 of the y coordinate of slide center
		"""
		return self.e_2_lst


# program test
# link_obj = Link4Rj4(25, 15, 25, 10, 10)
# plt.plot(link_obj.get_th2d_lst(), link_obj.get_th4_1_lst())
# plt.show()
