from presslink import shaft
import math
from presslink.kj_rkr_th_finder import get_th_rkr_max


class KnuckleJointSizer:
	"""
	A class for sizing of knuckle joint mechanism items
	...

	Attributes
	----------
	c : float
		length of rocker link in mm
	pf : float
		press force in ton
	l_pin : float
		main pin length. Depends on slide LR size. in mm
	fra_rev : float
		fraction of reverse load on press. eg 0.1, 0.15 etc
	th4d_lst : list
		list of rocker link angle in deg. index is th2d (crank angle). 
		0 is +ve x axis
	fb_max : float
		max force on link b in ton


	Methods
	-------
	get_d_pin():
		pin dia of 3 link joint, rocker and small end in mm
	get_th4d_max():
		maximum rocker link angle in deg
	get_w_frk():
		fork width of each fork in mm
	get_d_frk():
		fork outer dia in mm
	get_w_cr_se():
		conrod small end width total in mm
	get_w_bush():
		main press load bearing bush width in mm
	get_link_ok_flag():
		flag which is true if links do not interfere and are OK

    """

	def __init__(self, c, g, pf, l_pin, fra_rev, th4d_lst, fb_max):
		"""
		Parameters
		----------
		c : float
			length of rocker link in mm
		g : float
			length of conrod in mm
		pf : float
			press force in ton
		l_pin : float
			main pin length. Depends on slide LR size. in mm
		fra_rev : float
			fraction of reverse load on press. eg 0.1, 0.15 etc
		th4d_lst : list
			list of rocker link angle in deg. index is th2d (crank angle). 
			0 is +ve x axis
		fb_max : float
			max force on link b in ton
		"""
		sc_bush_all = 80  # MPa, allowable contact stress in bronze bush for main load
		sc_frk_all = 80  # MPa, allowable contact stress in link fork area (Class 4 forging including SCF)
		st_frk_all = 120  # MPa, allowable tensile stress in link fork area (Class 4 forging including SCF)

		rat_cd_d_frk = 1.3  # ratio of link center distance to fork dia (link od)
		pf_rev = fra_rev * pf  # reverse load in ton
		self.th4d_max = get_th_rkr_max(th4d_lst)
		th4_max = self.th4d_max * math.pi / 180
		self.d_pin = (pf + 2 * pf_rev + fb_max) * 10000 / (sc_bush_all * l_pin * math.cos(th4_max))
		self.w_frk = 0.5 * pf_rev * 10000 / (sc_frk_all * self.d_pin)  # fork width of each fork in mm
		self.d_frk = (0.5 * pf_rev * 10000 + self.w_frk * self.d_pin * st_frk_all) / (self.w_frk * st_frk_all)  # fork OD
		self.w_cr_se = fb_max * 10000 / (sc_bush_all * self.d_pin)  # conrod small end width total in mm
		self.w_bush = pf * 10000 / (sc_bush_all * self.d_pin)  # main bush width in mm


		# dia is calculated considering:
		# fwd force, rev force on upper link + rev force on lower link + conrod force
		# only bush allowable stress is considered while calculating dia of pin
		self.link_ok_flag = False

		self.intrf_c_fork_flag = False
		self.intrf_g_fork_flag = False

		if c / self.d_frk < rat_cd_d_frk:
			self.intrf_c_fork_flag = True

		if g / self.d_frk <= rat_cd_d_frk:
			self.intrf_g_fork_flag = True

		if not self.intrf_c_fork_flag and not self.intrf_g_fork_flag:
			self.link_ok_flag = True

		# setting dic
		self.setting_dic = {
		'sc_bush_all': sc_bush_all,
		'sc_frk_all': sc_frk_all,
		'st_frk_all': st_frk_all,
		'rat_cd_d_frk': rat_cd_d_frk,
		'fra_rev': fra_rev,
		}
		
	def get_d_pin(self):
		"""
        Returns
        -------
        float
        pin dia of 3 link joint, rocker and small end in mm
        """
		return self.d_pin

	def get_th4d_max(self):
		"""
        Returns
        -------
        float
        maximum rocker link angle in deg
        """

		return self.th4d_max

	def get_w_frk(self):
		"""
        Returns
        -------
        float
        fork width of each fork in mm
        """
		return self.w_frk  # fork width of each fork in mm

	def get_d_frk(self):
		"""
        Returns
        -------
        float
        fork outer dia in mm
        """
		return self.d_frk  # fork outer dia in mm

	def get_w_cr_se(self):
		"""
        Returns
        -------
        float
        conrod small end width total in mm
        """
		return self.w_cr_se  # conrod small end width total in mm

	def get_w_bush(self):
		"""
        Returns
        -------
        float
        main press load bearing bush width in mm
        """
		return self.w_bush  # main bush width in mm

	def get_link_ok_flag(self):
		"""
        Returns
        -------
        boolean
        flag which is true if links do not interfere and are OK
        """
		return self.link_ok_flag  # True if links do not interfere and are OK

	def get_intrf_c_fork_flag(self):
		"""
        Returns
        -------
        boolean
        flag to check interf of fork grooves of rocker link c
        """
		return self.intrf_c_fork_flag  # True if interference

	def get_intrf_g_fork_flag(self):
		"""
        Returns
        -------
        boolean
        flag to check interf of fork grooves of conrod link g
        """
		return self.intrf_g_fork_flag  # True if interference

	def get_setting_dic(self):
		"""
        Returns
        -------
        dictionary
        contains all setting data like allowable stresses etc
        """
		return self.setting_dic  