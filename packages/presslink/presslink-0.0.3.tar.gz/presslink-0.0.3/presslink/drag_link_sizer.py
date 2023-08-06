from presslink import shaft
import math


class DragLinkSizer:
	"""
	A class for sizing of drag link gearbox items
	...

	Attributes
	----------
	a : float
		length of gear link a in mm
	b : float
		length of rocker link b in mm
	c : float
		length of crank connector link c in mm
	d : float
		x coordinate of crank connector axis in mm
	e : float
		y coordinate of crank connector axis in mm
	thbc_min : float
		min angle bw link b and c in rad
	fb : float
		rocker link force in ton
	trq : float
		gear axis torque in Nm
	w : float
		angular velocity of gear in rad/s
	solid_out_shaft_flag : boolean
		True if solid shaft, False for hollow splined shaft
	cc_integral_flag : boolean
		True if crank connector is integral to shaft


	Methods
	-------
	bore_in_bore():
		Returns boolean (T or F)
		True if interference, false if no interference
	rkr_cc_hit():
		Returns boolean (T or F)
		True if interference, false if no interference
	high_vel():
		Returns boolean (T or F)
		True if velocity higher than acceptable, false if within limit
	get_torque_unit_out_shaft_dia():
		Returns torque unit output shaft dia in mm
	get_crank_shaft_dia():
		Returns crank shaft dia in mm
	get_rocker_pin_dia():
		Returns rocker pin dia in mm
	get_rocker_bush_width():
		Returns rocker pin bush width in mm
	get_gear_bore_dia():
		Returns gear bore dia in mm
	get_gap_bc():
		Returns min gap between crank connector and rocker link in mm
	get_rocker_width():
		Returns width (perpendicular direction to pin axis) of rocker link in mm
	get_rocker_thk():
		Returns thickness (in pin axis direction) of rocker link in mm
	get_bush_v():
		Returns rubbing velocity of gear bush in mm/s
	get_d_in_clr_gear():
		Returns clear inner dia of gear. rim ID must be larger than this dia
	get_cc_arm_thk():
		Returns crank connector arm thk (parallel to axis) in mm
	get_w_bush_d_s():
		Returns torque unit out shaft bush width in mm
	get_w_bush_gear():
		Returns main gear bush width in mm
	get_w_gear_body():
		Returns main gear body width in mm
	get_w_trq_unit():
		Returns torque unit housing fab width in mm
	get_len_d_s():
		Returns out shaft total LR length in mm
	get_wt_rkr():
		Returns rocker link weight in kg
	get_wt_pin_rkr():
		Returns rocker pin weight in kg
	get_wt_cc():
		Returns crank connector weight in kg
	get_wt_ecc_sup():
		Returns eccentric support weight in kg
	get_wt_gear_body():
		Returns gear body weight (excluding rim) in kg
	get_wt_bush_rkr():
		Returns rocker bush weight in kg
	get_wt_bush_d_s():
		Returns outshaft bush weight in kg
	get_wt_bush_gear():
		Returns gear bush weight in kg
	get_setting_dic():
		Returns dictionary of setting data of sizer
    """
	def __init__(self, a, b, c, d, e, thbc_min, fb, trq, w, nr_sus,
		solid_out_shaft_flag, cc_integral_flag):
		"""
		Parameters
		----------
		a : float
			length of gear link a in mm
		b : float
			length of rocker link b in mm
		c : float
			length of crank connector link c in mm
		d : float
			x coordinate of crank connector axis in mm
		e : float
			y coordinate of crank connector axis in mm
		thbc_min : float
			min angle bw link b and c in rad
		fb : float
			rocker link force in ton
		trq : float
			gear axis torque in Nm
		w : float
			angular velocity of gear in rad/s
		solid_out_shaft_flag : boolean
			True if solid shaft, False for hollow splined shaft
		cc_integral_flag : boolean
			True if crank connector is integral to shaft
		"""

		#  cc_integral_flag is a boolean. It is valid only for solid output shafts. 
		#  It has no effect on hollow shaft with internal splines
		#  cc_integral_flag True means: crank connector is integral with torque unit output shaft
		#  cc_integral_flag False menas: crank connector is separate with torque unit output shaft 
		#  and fitted with either key or shrink fitting or keyless coupling

		# user defined flags
		self.solid_out_shaft_flag = solid_out_shaft_flag
		self.cc_integral_flag = cc_integral_flag



		# define various rejection flags
		self.bore_in_bore_flag = False  # to check if bore of link 'a' pivot is coming in main bore of gear
		self.rkr_cc_hit_flag = False  # to check if rocker link is interfering with crank connector
		self.high_vel_flag = False  # to check if gear bush velocity is higher than allowed limit

		self.hs_oir = 1.4  # OD to ID ratio of Hollow shaft

		# we will define 2 multiplication factors for 2 options of flag
		out_d_mul_fac = 1
		mid_d_mul_fac = 1
		
		if self.solid_out_shaft_flag:
			out_d_mul_fac = 1
		else:  # hollow shaft output
			out_d_mul_fac = self.hs_oir


		if self.cc_integral_flag:
			mid_d_mul_fac = 1
		else:
			mid_d_mul_fac = 1.5



		ldr = 1  # l/d ratio of rocker bush
		sc = 80  # rocker bush nominal allowable contact stress in N/mm2. This is as per Aida design
		sc_bush_gear = 20  # gear main bush nominal allowable contact stress in N/mm2. This is as per Aida design
		se = 200  # torque unit out shaft endurance in N/mm2
		sy = 380  # torque unit out shaft yield in N/mm2
		fos = 2  # torque unit out shaft fos on torque
		kf = 2  # scf for bending
		kfs = 1.5  # scf for torsion
		oir = 2  # OD to ID ratio of link with pin bore. eg use in crank connector
		mrg_cc_assy = 10  # assy marging of inserting crank connector in gear main bore
		mrg_bc_hit = 10  # minimum marging of rocker link hitting with crank connector
		thk_lig_ecc_disc = 25  # in ecc disc, it is ligament thk between OD and cs bush bore.
		#  One is main bore other is torque unit out shaft bore
		cc_mid_cut_fact = 0.5  # mid cc dia ids multiplied by this factor to
		# avoid hitting with rocker link. Such cut is usually provided always

		thk_lig_rkr_bore_gear = 10  # ligament thk between rocker pin bore in gear and gear main bore
		v_max_all_bush_gear = 2200  # gear main bore bush allowable rubbing velocity in mm/s (avg)

		if nr_sus == 2:
		# for 2 sus press, output dia is smaller as torque is divided into 2 shafts
			shaft_obj = shaft.Shaft(trq/4, trq/4, trq/8, trq/8, kf, kfs, se*1e6, sy*1e6, fos)  # shaft object to calculate torque unit out shaft dia
		if nr_sus == 1:
		# for 1 sus press, output dia is larger as torque is transmitted by only 1 shaft
			shaft_obj = shaft.Shaft(trq/2, trq/2, trq/4, trq/4, kf, kfs, se*1e6, sy*1e6, fos)  # shaft object to calculate torque unit out shaft dia

		
		self.d_s = out_d_mul_fac * shaft_obj.get_shaft_dia() * 1000  # out shaft dia in mm

		self.cc_d_mid = mid_d_mul_fac * self.d_s  # crank connector shaft dia in mid (mm)

		self.d_p = math.sqrt(fb*10000/(ldr*sc))  # rocker pin dia in mm
		self.w_bush_rkr = round(ldr * self.d_p, 0)  # rocker bush widt in mm 
		self.w_rkr = 1.25 * self.d_p  # rocker link width in mm
		self.thk_rkr = ldr * self.d_p  # rocker thk in mm. to be used in weight cal probably
		lmx_c = c + 0.5 * self.d_s + 0.5 * (oir * self.d_p)  # max end to end length of crank connector link 'c'
		cd_gear_cs_axis = math.sqrt(d**2 + e**2)  # offset radial distance of crank shaft axis from gear axis
		
		# min bore in gear due to limitation 1: due to cs axis offset and out shaft dia
		gb_min1 = 2 * (cd_gear_cs_axis + 0.5 * self.d_s) + thk_lig_ecc_disc

		# min bore in gear due to imitation 2: assy of crank connector inside gear bore
		gb_min2 = lmx_c + mrg_cc_assy
		
		# worst case of gear bore limitation out of limitation 1 and limitation 2
		self.gb_min = round(max(gb_min1, gb_min2),0)
		# print("gb_min",self.gb_min)

		
		if self.gb_min > 2 * (a - 0.5 * self.d_p - thk_lig_rkr_bore_gear):
			self.bore_in_bore_flag = True  # rocker pin bore merge in gear main bore
		# print("gear bore compare value", 2 * (a - 0.5 * self.d_p - thk_lig_rkr_bore_gear))


		
		self.gap_bc = (c * math.sin(thbc_min) - self.w_rkr/2) - self.d_s*cc_mid_cut_fact/2  # gap between link b and c at min thab angle
		if self.gap_bc < mrg_bc_hit:
			self.rkr_cc_hit_flag = True  # rkr_cc_hit_bool
		# print("gap_bc",self.gap_bc)
		# print("thbc deg",thbc_min*180/math.pi)
		# print("w_rkr",self.w_rkr)


		# gear bush rubbing speed mm/s
		self.v_gear_bush = 0.5 * self.gb_min * w
		if self.v_gear_bush > v_max_all_bush_gear:
			self.high_vel_flag = True  # high_vel_bool
		# print("self.v_gear_bush",self.v_gear_bush)

		# clear gear dia
		self.d_in_clr_gear = 2 * (a + 0.5 * (oir * self.d_p)) + 25

		# setting dic
		self.setting_dic = {
		'sc':sc,
		'se':se,
		'sy':sy,
		'fos':fos,
		'kf':kf,
		'kfs':kfs,
		'v_max_all_bush_gear':v_max_all_bush_gear,
		'cc_mid_cut_fact':cc_mid_cut_fact,
		}

		# crank connector arm thk (parll to axis)
		self.cc_arm_thk = 0.6 * self.d_p

		# crank connector arm width (perp to axis)
		self.cc_arm_width = oir * self.d_s  # ds kept on purpose in formula

		# torque unit out shaft bush width
		self.w_bush_d_s = 0.5 * self.d_s

		# main gear bush width
		self.w_bush_gear = 0.5 * fb * 10000 / (sc_bush_gear * self.gb_min)

		# main gear body width
		self.w_gear_body = (self.d_p + 10) + (2 * self.cc_arm_thk + 10) + (2 * self.w_bush_gear + 10)

		# torque unit width
		self.w_trq_unit = (self.d_p + 10) + (2 * self.cc_arm_thk + 10) + (2 * self.w_bush_d_s + 25)

		# outshaft length in mm
		self.len_d_s = 2 * 1.5 * self.d_s + self.w_trq_unit

		# rocker pin length in mm
		self.len_pin_rkr = self.w_trq_unit

		# rocker link raw material length (end to end) in mm
		self.len_rkr = b + 2 * (0.5 * self.d_p * oir)

		# rocker link weight in kg
		self.wt_rkr = 7850 * 1e-9 * self.len_rkr * self.thk_rkr * self.w_rkr

		# rocker pin weight in kg
		self.wt_pin_rkr = 7850 * 1e-9 * 0.7854 * self.d_p**2 * self.len_pin_rkr

		# crank connector raw material length (end to end) in mm
		self.len_cc = c + 2 * (0.5 * self.d_p * oir)

		# crank connector link weight in kg (solid full block)
		self.wt_cc = 7850 * 1e-9 * (self.len_cc * 4 * self.cc_arm_thk * self.cc_arm_width)

		# ecc support weight in kg
		self.wt_ecc_sup = 7850 * 1e-9 * 0.7854 * self.gb_min**2 * (self.w_bush_d_s + 25)

		# gear body weight in kg (excluding rim)
		self.wt_gear_body = 7850 * 1e-9 * 0.7854 * self.d_in_clr_gear**2 * self.w_bush_gear + \
		7850 * 1e-9 * 3.14 * self.d_in_clr_gear * (self.w_bush_gear * 0.5) * self.w_gear_body + \
		4 * self.wt_pin_rkr

		# rocker bush weight in kg
		self.wt_bush_rkr = 8900 * 1e-9 * 3.14 * self.d_p * 10 * self.w_bush_rkr

		# outshaft bush weight in kg
		self.wt_bush_d_s = 8900 * 1e-9 * 3.14 * self.d_s * 10 * self.w_bush_d_s

		# gear bush weight in kg
		self.wt_bush_gear = 8900 * 1e-9 * 3.14 * self.gb_min * 15 * self.w_bush_gear
		


	def bore_in_bore(self):
		"""
        Returns
        -------
        boolean
        Returns True if interference, false if no interference
        """
		return self.bore_in_bore_flag

	def rkr_cc_hit(self):
		"""
        Returns
        -------
        boolean
        Returns True if interference, false if no interference
        """
		return self.rkr_cc_hit_flag

	def high_vel(self):
		"""
        Returns
        -------
        boolean
        Returns True if velocity higher than acceptable, false if within limit
        """
		return self.high_vel_flag

	def get_torque_unit_out_shaft_dia(self):
		"""
        Returns
        -------
        float
        Returns torque unit output shaft dia in mm
        """
		return self.d_s  # mm

	def get_crank_shaft_dia(self):
		"""
        Returns
        -------
        float
        Returns crank shaft dia in mm
        """
		if self.solid_out_shaft_flag:
			return self.d_s  # mm
		else:
			return self.d_s / self.hs_oir  # mm

	def get_rocker_pin_dia(self):
		"""
        Returns
        -------
        float
        Returns rocker pin dia in mm
        """
		return self.d_p  # mm

	def get_rocker_bush_width(self):
		"""
        Returns
        -------
        float
        Returns rocker pin bush width in mm
        """
		return self.w_bush_rkr  # mm

	def get_gear_bore_dia(self):
		"""
        Returns
        -------
        float
        Returns gear bore dia in mm
        """
		return self.gb_min  # min gear bore dia in mm

	def get_gap_bc(self):
		"""
        Returns
        -------
        float
        Returns min gap between crank connector and rocker link in mm
        """
		return self.gap_bc  # gap bw link b and c in mm

	def get_rocker_width(self):
		"""
        Returns
        -------
        float
        Returns width (perpendicular direction to pin axis) of rocker link in mm
        """
		return self.w_rkr  # rocker width in mm

	def get_rocker_thk(self):
		"""
        Returns
        -------
        float
        Returns thickness (in pin axis direction) of rocker link in mm
        """
		return self.thk_rkr  # rocker thk in axial dir in mm
		
	def get_bush_v(self):
		"""
        Returns
        -------
        float
        Returns rubbing velocity of gear bush in mm/s
        """
		return self.v_gear_bush  # bush rubbing vel in mm/s

	def get_d_in_clr_gear(self):
		"""
        Returns
        -------
        float
        Returns clear inner dia of gear. rim ID must be larger than this dia
        """
		return self.d_in_clr_gear  # clear id in gear in mm

	def get_cc_arm_thk(self):
		"""
        Returns
        -------
        float
        Returns crank connector arm thk (parallel to axis) in mm
        """
		return self.cc_arm_thk  # crank connector arm thk (parll to axis) in mm

	def get_w_bush_d_s(self):
		"""
        Returns
        -------
        float
        Returns torque unit out shaft bush width in mm
        """
		return self.w_bush_d_s  # torque unit out shaft bush width in mm

	def get_w_bush_gear(self):
		"""
        Returns
        -------
        float
        Returns main gear bush width in mm
        """
		return self.w_bush_gear  # main gear bush width in mm

	def get_w_gear_body(self):
		"""
        Returns
        -------
        float
        Returns main gear body width in mm
        """
		return self.w_gear_body  # main gear body width in mm

	def get_w_trq_unit(self):
		"""
        Returns
        -------
        float
        Returns torque unit housing fab width in mm
        """
		return self.w_trq_unit  # torque unit housing fab width in mm

	def get_len_d_s(self):
		"""
        Returns
        -------
        float
        Returns out shaft total LR length in mm
        """
		return self.len_d_s # out shaft total LR length in mm

	def get_wt_rkr(self):
		"""
        Returns
        -------
        float
        Returns rocker link weight in kg
        """
		return self.wt_rkr # rocker link weight in kg

	def get_wt_pin_rkr(self):
		"""
        Returns
        -------
        float
        Returns rocker pin weight in kg
        """
		return self.wt_pin_rkr # rocker pin weight in kg

	def get_wt_cc(self):
		"""
        Returns
        -------
        float
        Returns crank connector weight in kg
        """
		return self.wt_cc # crank connector weight in kg

	def get_wt_ecc_sup(self):
		"""
        Returns
        -------
        float
        Returns eccentric support weight in kg
        """
		return self.wt_ecc_sup # eccentric support weight in kg

	def get_wt_gear_body(self):
		"""
        Returns
        -------
        float
        Returns gear body weight (excluding rim) in kg
        """
		return self.wt_gear_body # gear body weight (excluding rim) in kg

	def get_wt_bush_rkr(self):
		"""
        Returns
        -------
        float
        Returns rocker bush weight in kg
        """
		return self.wt_bush_rkr # rocker bush weight in kg

	def get_wt_bush_d_s(self):
		"""
        Returns
        -------
        float
        Returns outshaft bush weight in kg
        """
		return self.wt_bush_d_s # outshaft bush weight in kg

	def get_wt_bush_gear(self):
		"""
        Returns
        -------
        float
        Returns gear bush weight in kg
        """
		return self.wt_bush_gear # gear bush weight in kg

	def get_setting_dic(self):
		"""
        Returns
        -------
        dictionary
        Returns dictionary of setting data of sizer
        """
		return self.setting_dic

