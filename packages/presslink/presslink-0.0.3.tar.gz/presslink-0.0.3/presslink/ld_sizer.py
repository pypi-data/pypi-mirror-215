from presslink import shaft
import math


class LinkDriveSizer:
	"""
	A class for sizing of link drive mechanism items
	...

	Attributes
	----------
	a : float
		eccentricity in mm
	b : float
		ter link upper side in mm
	f : float
		ter link vertical side (from bigend to conrod) in mm
	thbc_min : float
		min angle between b and c in rad
	f_sus : float
		suspension force in ton 
		0 is +ve x axis
	f_rkr : float
		force on rocker link in ton


	Methods
	-------
	get_d_pin_eg():
		eg pin dia in mm
	get_d_be():
		big end dia in mm
	get_od_be_ring():
		ter link big end casting od in mm
	get_d_pin_rkr():
		rocker pin dia in mm
	get_l_bush_rkr():
		rocker bush length in axial dir in mm
	get_w_rkr():
		rocker width in mm
	get_thk_rkr():
		rocker thk in axial dir in mm
	get_od_ring_rkr():
		rocker link od in mm (in pin area)
	get_d_pin_cr():
		conrod pin dia in mm
	get_l_bush_cr():
		conrod bush length in mm in axial dir
	get_d_ring_cr():
		conrod od in mm (in pin area)
	get_rkr_ring_ter_intrf_flag():
		flag to check interference between rocker ring and ternary link casted big end od
	get_rkr_link_ter_intrf_flag():
		flag to check interference between rocker link side and ternary link casted big end od
	get_cr_ter_intrf_flag():
		flag to check interference between conrod casted ring and ternary link casted big end od
	get_link_ok_flag():
		flag to check if links are ok and do not interfere anywhere
	get_setting_dic():
		contains all setting data like allowable stresses etc
    """

	def __init__(self, a, b, f, thbc_min, f_sus, f_rkr):
		"""
		Parameters
		----------
		a : float
			eccentricity in mm
		b : float
			ter link upper side in mm
		f : float
			ter link vertical side (from bigend to conrod) in mm
		thbc_min : float
			min angle between b and c in rad
		f_sus : float
			suspension force in ton 
			0 is +ve x axis
		f_rkr : float
			force on rocker link in ton
		"""

		# ldr = 1.4  # l/d ratio of rocker bush
		sc_bush_rkr = 40  # rocker bush nominal allowable contact stress in N/mm2.
		# sc_bush_be = 20  # big end bush nominal allowable contact stress in N/mm2.
		# sc_bush_eg_pin = 30  # eg pin nominal allowable contact stress in N/mm2.
		ss_all_eg_pin = 40  # allowable shear stress in eg pin. considering double shear
		rat_oi_rkr = 2  # OD to ID ratio of rocker link pin ring
		rat_wp_rkr = 1.4  # ratio of rocker width to rocker pin dia
		rat_ld_bush_rkr = 1.3  # ratio of rocker bush length to rocker pin dia

		rat_oi_be_ring = 1.125  # ratio of big end bore to big end ring OD
		thk_lip_gear = 35  # lip thk of gear bw pin and lobe on  up side
		thk_wall_bush_pin_eg = 10  # eg bush wall thk
		mrg_hit = 10  # rocker and ternary link hitting margin

		# conrod data
		rat_oi_cr = 1.6  # OD to ID ratio of conrod pin ring
		sc_bush_cr = 50  # big end bush nominal allowable contact stress in N/mm2.
		rat_ld_bush_cr = 0.6  # ratio of cr bush length to cr pin dia


		self.d_pin_eg = round(math.sqrt(2 * f_sus * 10000 / (math.pi * ss_all_eg_pin)), 0)  # eg pin dia
		# self.d_pin_eg = 470  # eg pin dia

		self.d_be = round(2 * (a + 0.5 * self.d_pin_eg + thk_wall_bush_pin_eg + thk_lip_gear), 0)  # ecc gear big end dia
		self.od_be_ring = round(rat_oi_be_ring * self.d_be, 0)  # outer dia of big end ring

		self.d_pin_rkr = round(math.sqrt(f_rkr * 10000 / (sc_bush_rkr * rat_ld_bush_rkr)), 0)
		self.l_bush_rkr = round(self.d_pin_rkr * rat_ld_bush_rkr, 0)
		self.w_rkr = round(rat_wp_rkr * self.d_pin_rkr, 0)
		self.thk_rkr = self.l_bush_rkr
		self.od_ring_rkr = round(self.d_pin_rkr * rat_oi_rkr, 0)


		# conrod upper pin chk
		self.d_pin_cr = round(math.sqrt(f_sus * 10000 / (sc_bush_cr * rat_ld_bush_cr)), 0)  # conrod upper pin dia
		self.l_bush_cr = round(self.d_pin_cr * rat_ld_bush_cr, 0)
		self.d_ring_cr = round(self.d_pin_cr * rat_oi_cr, 0)

		# print("self.d_pin_eg", self.d_pin_eg)
		# print("self.d_be", self.d_be)
		# print("self.od_be_ring", self.od_be_ring)
		# print("self.d_pin_rkr", self.d_pin_rkr)
		# print("self.l_bush_rkr", self.l_bush_rkr)
		# print("self.w_rkr", self.w_rkr)
		# print("self.thk_rkr", self.thk_rkr)
		# print("self.od_ring_rkr", self.od_ring_rkr)
		# print("self.d_pin_cr", self.d_pin_cr)
		# print("self.l_bush_cr", self.l_bush_cr)
		# print("self.d_ring_cr", self.d_ring_cr)

		# chk rocker od ring intrf with ter link od ring
		self.rkr_ring_ter_intrf_flag = True
		gap_bc_ring = b - (self.od_ring_rkr / 2 + self.od_be_ring / 2 + mrg_hit)
		# print("gap_bc_ring", gap_bc_ring)
		if gap_bc_ring >= 0:
			self.rkr_ring_ter_intrf_flag = False
		# print("self.rkr_ring_ter_intrf_flag", self.rkr_ring_ter_intrf_flag)


		# chk rocker link slide intrf with ter link od ring
		self.rkr_link_ter_intrf_flag = True
		gap_bc_side = (b * math.sin(thbc_min) - self.w_rkr / 2) - self.od_be_ring / 2 - mrg_hit
		# print("gap_bc_side", gap_bc_side)
		if gap_bc_side >= 0:
			self.rkr_link_ter_intrf_flag = False
		# print("self.rkr_link_ter_intrf_flag", self.rkr_link_ter_intrf_flag)


		# chk conrod intrf with ter link od ring
		self.cr_ter_intrf_flag = True
		gap_bf_ring = f - (self.d_ring_cr / 2 + self.od_be_ring / 2 + mrg_hit)
		# print("gap_bf_ring", gap_bf_ring)
		if gap_bf_ring >= 0:
			self.cr_ter_intrf_flag = False
		# print("self.cr_ter_intrf_flag", self.cr_ter_intrf_flag)


		# check overall link ok condition
		self.link_ok_flag = False
		if not self.rkr_ring_ter_intrf_flag and not self.rkr_link_ter_intrf_flag and not self.cr_ter_intrf_flag:
			self.link_ok_flag = True

		# setting dic
		self.setting_dic = {
		'sc_bush_rkr': sc_bush_rkr,
		'ss_all_eg_pin': ss_all_eg_pin,
		'rat_oi_rkr': rat_oi_rkr,
		'rat_wp_rkr': rat_wp_rkr,
		'rat_ld_bush_rkr': rat_ld_bush_rkr,
		'rat_oi_be_ring': rat_oi_be_ring,
		'thk_lip_gear': thk_lip_gear,
		'thk_wall_bush_pin_eg': thk_wall_bush_pin_eg,
		'mrg_hit': mrg_hit,
		'rat_oi_cr': rat_oi_cr,
		'sc_bush_cr': sc_bush_cr,
		'rat_ld_bush_cr': rat_ld_bush_cr,
		}

	def get_d_pin_eg(self):
		"""
        Returns
        -------
        float
        eg pin dia in mm
        """
		return self.d_pin_eg

	def get_d_be(self):
		"""
        Returns
        -------
        float
        big end dia in mm
        """
		return self.d_be

	def get_od_be_ring(self):
		"""
        Returns
        -------
        float
        ter link big end casting od in mm
        """
		return self.od_be_ring

	def get_d_pin_rkr(self):
		"""
        Returns
        -------
        float
        rocker pin dia in mm
        """
		return self.d_pin_rkr

	def get_l_bush_rkr(self):
		"""
        Returns
        -------
        float
        rocker bush length in axial dir in mm
        """
		return self.l_bush_rkr

	def get_w_rkr(self):
		"""
        Returns
        -------
        float
        rocker width in mm
        """
		return self.w_rkr

	def get_thk_rkr(self):
		"""
        Returns
        -------
        float
        rocker thk in axial dir in mm
        """
		return self.thk_rkr

	def get_od_ring_rkr(self):
		"""
        Returns
        -------
        float
        rocker link od in mm (in pin area)
        """
		return self.od_ring_rkr

	def get_d_pin_cr(self):
		"""
        Returns
        -------
        float
        conrod pin dia in mm
        """
		return self.d_pin_cr

	def get_l_bush_cr(self):
		"""
        Returns
        -------
        float
        conrod bush length in mm in axial dir
        """
		return self.l_bush_cr

	def get_d_ring_cr(self):
		"""
        Returns
        -------
        float
        conrod od in mm (in pin area)
        """
		return self.d_ring_cr

	def get_rkr_ring_ter_intrf_flag(self):
		"""
        Returns
        -------
        boolean
        flag to check interference between rocker ring and ternary link casted big end od
        """
		return self.rkr_ring_ter_intrf_flag

	def get_rkr_link_ter_intrf_flag(self):
		"""
        Returns
        -------
        boolean
        flag to check interference between rocker link side and ternary link casted big end od
        """
		return self.rkr_link_ter_intrf_flag

	def get_cr_ter_intrf_flag(self):
		"""
        Returns
        -------
        boolean
        flag to check interference between conrod casted ring and ternary link casted big end od
        """
		return self.cr_ter_intrf_flag

	def get_link_ok_flag(self):
		"""
        Returns
        -------
        boolean
        flag to check if links are ok and do not interfere anywhere
        """
		return self.link_ok_flag

	def get_setting_dic(self):
		"""
        Returns
        -------
        dictionary
        contains all setting data like allowable stresses etc
        """
		return self.setting_dic
