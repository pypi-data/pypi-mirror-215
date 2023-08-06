import math
import matplotlib.pyplot as plt

class Link4Rj4:
	"""
	A class for calculation of 4 link kinematic chain with 4 Revolute Joints
	There is no Prismatic (or Slider) joint
	Contains only positional analysis.
	Closed loop vector direction: a*e^(j*th2) + b*e^(j*th3) - c*e^(j*th4) - e*e^(j*th5) - d*e^(j*th6) = 0
	Center of rotation point in above is in Q1
	d vector is always horizontal. It is the x coordinate of center of rotation of link c
	e vector is always vertical. It is the y coordinate of center of rotation of link c
	If center of rotation of link c is in Q1, d is + and e is +
	If center of rotation of link c is in Q2, d is - and e is +
	If center of rotation of link c is in Q3, d is - and e is -
	If center of rotation of link c is in Q4, d is + and e is -
	Origin of coordinate system is the center of rotation of link a

	...

	Attributes
	----------

	Methods
	-------
	get_th2d_lst():
		Returns list of input angle th2 in deg.
		th2 is angle of link a
	get_th2_lst():
		Returns list of input angle th2 in rad
		th2 is angle of link a 
	get_th3_1_lst():
		Returns list of 1st root of angle th3 in rad
		th3 is angle of link b 
	get_th3d_1_lst():
		Returns list of 1st root of angle th3 in deg
		th3 is angle of link b 
	get_th3_2_lst():
		Returns list of 2nd root of angle th3 in rad
		th3 is angle of link b 
	get_th3d_2_lst():
		Returns list of 2nd root of angle th3 in deg
		th3 is angle of link b 
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
	"""
	def __init__(self, a, b, c, d, e):
		"""
		Parameters
		----------
		a : float
			input link length
		b : float
			coupler link length
		c : float
			output link length
		d : float
			x location of link c rotation center point (+ for Q1 and Q4, - for Q2 and Q3)
		e : float
			y location of link c rotation center point (+ for Q1 and Q2, - for Q3 and Q4)
		"""
		try:
			k1 = d / c
			k2 = e / a
			k3 = e / c
			k4 = d / a
			k5 = (a**2 + c**2 + d**2 + e**2 - b**2) / (2 * a * c)

			k6 = d / a
			k7 = d / b
			k8 = e / a
			k9 = e / b
			k10 = (a**2 + b**2 + d**2 + e**2 - c**2) / (2 * a * b)
		except Exception as e:
			print(e)

		self.th2d_lst = []
		self.th2_lst = []


		self.th3d_1_lst = []
		self.th3_1_lst = []

		self.th3d_2_lst = []
		self.th3_2_lst = []

		self.th4d_1_lst = []
		self.th4_1_lst = []

		self.th4d_2_lst = []
		self.th4_2_lst = []

		for th2d in range(360):
			th2 = th2d * math.pi / 180
			A = k5 - k1 * math.cos(th2) - k3 * math.sin(th2) + math.cos(th2) - k4
			B = 2 * k2 - 2 * math.sin(th2)
			C = k5 - k1 * math.cos(th2) - k3 * math.sin(th2) - math.cos(th2) + k4
			
			# finding root 1 of th4
			try:
				th4_1 = 2 * math.atan((-B + math.sqrt(B**2 - 4 * A * C)) / (2 * A))
				if th4_1 < 0: th4_1 = th4_1 + 2 * math.pi
			except Exception as e:
				# print(e)
				th4_1 = 0
			th4d_1 = th4_1 * 180 / math.pi

			
			# finding root 2 of th4
			try:
				th4_2 = 2 * math.atan((-B - math.sqrt(B**2 - 4 * A * C)) / (2 * A))
				if th4_2 < 0: th4_2 = th4_2 + 2 * math.pi
			except Exception as e:
				# print(e)
				th4_2 = 0
			th4d_2 = th4_2 * 180 / math.pi

			
			D = - k9 * math.sin(th2) - k7 * math.cos(th2) + k10 + k6 - math.cos(th2)
			E = - 2 * k8 + 2 * math.sin(th2)
			F = - k9 * math.sin(th2) - k7 * math.cos(th2) + k10 - k6 + math.cos(th2)
			
			# finding root 1 of th3
			try:
				th3_1 = 2 * math.atan((-E + math.sqrt(E**2 - 4 * D * F)) / (2 * D))
				if th3_1 < 0: th3_1 = th3_1 + 2 * math.pi
			except Exception as e:
				# print(e)
				th3_1 = 0
			th3d_1 = th3_1 * 180 / math.pi
			
			# finding root 2 of th3
			try:
				th3_2 = 2 * math.atan((-E - math.sqrt(E**2 - 4 * D * F)) / (2 * D))
				if th3_2 < 0: th3_2 = th3_2 + 2 * math.pi
			except Exception as e:
				# print(e)
				th3_2 = 0
			th3d_2 = th3_2 * 180 / math.pi


			self.th2d_lst.append(th2d)
			self.th2_lst.append(th2)

			self.th3_1_lst.append(th3_1)
			self.th3d_1_lst.append(th3d_1)

			self.th3_2_lst.append(th3_2)
			self.th3d_2_lst.append(th3d_2)
			# print("th3d: ", th3d_2)


			self.th4_1_lst.append(th4_1)
			self.th4d_1_lst.append(th4d_1)

			self.th4_2_lst.append(th4_2)
			self.th4d_2_lst.append(th4d_2)

	
	def get_th2d_lst(self):
		"""
		Returns
		-------
		list
		Returns list of input angle th2 in deg.
		th2 is angle of link a
		"""
		return self.th2d_lst

	def get_th2_lst(self):
		"""
		Returns
		-------
		list
		Returns list of input angle th2 in rad
		th2 is angle of link a
		"""
		return self.th2_lst

	def get_th3_1_lst(self):
		"""
		Returns
		-------
		list
		Returns list of 1st root of angle th3 in rad
		th3 is angle of link b
		"""
		return self.th3_1_lst

	def get_th3d_1_lst(self):
		"""
		Returns
		-------
		list
		Returns list of 1st root of angle th3 in deg
		th3 is angle of link b
		"""
		return self.th3d_1_lst

	def get_th3_2_lst(self):
		"""
		Returns
		-------
		list
		Returns list of 2nd root of angle th3 in rad
		th3 is angle of link b
		"""
		return self.th3_2_lst

	def get_th3d_2_lst(self):
		"""
		Returns
		-------
		list
		Returns list of 2nd root of angle th3 in deg
		th3 is angle of link b
		"""
		return self.th3d_2_lst

	def get_th4_1_lst(self):
		"""
		Returns
		-------
		list
		Returns list of 1st root of angle th4 in rad
		th4 is angle of link c
		"""
		return self.th4_1_lst

	def get_th4d_1_lst(self):
		"""
		Returns
		-------
		list
		Returns list of 1st root of angle th4 in deg
		th4 is angle of link c
		"""
		return self.th4d_1_lst

	def get_th4_2_lst(self):
		"""
		Returns
		-------
		list
		Returns list of 2nd root of angle th4 in rad
		th4 is angle of link c
		"""
		return self.th4_2_lst

	def get_th4d_2_lst(self):
		"""
		Returns
		-------
		list
		Returns list of 2nd root of angle th4 in deg
		th4 is angle of link c
		"""
		return self.th4d_2_lst


# program test

# a = 564 * scale_fact  # gear link
# b = 611 * scale_fact  # rocker
# c = 352 * scale_fact  # crank connector
# d = -122 * scale_fact  # crankshaft x
# e = -70.5 * scale_fact  # crankshaft y


# link_obj = Link4Rj4(564, 611, 352, -122, -70.5)
# plt.plot(link_obj.get_th2d_lst(), link_obj.get_th4d_1_lst())
# plt.plot(link_obj.get_th2d_lst(), link_obj.get_th3d_2_lst())

# plt.show()





