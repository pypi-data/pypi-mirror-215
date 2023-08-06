from presslink import diff_list
import math

class PrettyGraph:
	"""
	A class for generating plotable list of press characteristics  
	...

	Attributes
	----------
	f : float
		press froce in ton
	rd : float
		rated distance in mm
	spm : float
		stroke per minute of press
	d_lst : list
		list of slide position from rotating center in mm. index is input angle in deg.
		0 deg input angle corrosponding to pos x axis
	dir_ccw_bool : boolean
		True if rotation is CCW, False if rotation is CW
		It is not used as it is not validated and default dir should be CCW always


	Methods
	-------
	get_th2d_lst():
		Returns input angle th2 list in deg. 0 is the pos X axis
	get_fbos_lst():
		Returns fbos list in mm
	get_v_lst():
		Returns slide vel list in mm/s
	get_acc_lst():
		slide acc list in m/s2
	get_n5_lst():
		crank speed (in case of analysis of 2nd likage) list in rpm
	get_fbos2x_lst():
		Returns fbos list over 2 strokes
	get_v2x_lst():
		Returns slide vel list over 2 strokes
	get_th2d_tt720_lst():
		Returns input angle th2d (deg) list over 2 strokes
	get_th2d_tt360str_lst():
		Returns input angle list from Tdc to Tdc in deg as string
	get_th2d_tt360_lst():
		Returns input angle list from Tdc to Tdc in deg as float
	get_fbos_tt_lst():
		Returns fbos list from Tdc to Tdc in mm
	get_v_tt_lst():
		Returns slide vel list from Tdc to Tdc in mm/s
	get_acc_tt_lst():
		Returns slide acc list from Tdc to Tdc in mm/s2
	get_th2d_at_rd():
		Returns input angle th2d (deg) at rated distance
	get_rd_act():
		Returns actual rated distance at integer rated angle in mm
	get_th2d_index_tt_at_rd():
		Returns index of input angle th2d (deg) at rated distance in list of th2d
	get_v_at_rd():
		Returns slide vel at rated distance in mm/s
	get_torque():
		Returns required gear axis torque at rated distance in Nm
	get_mb_dic():
		Returns dictionary of th2d, fbos, vel and press force from Mid stroek to Bdc

    """
	
	def __init__(self, f, rd, spm, d_lst, dir_ccw_bool=True):
		"""
		Parameters
		----------
		f : float
			press froce in ton
		rd : float
			rated distance in mm
		spm : float
			stroke per minute of press
		d_lst : list
			list of slide position from rotating center in mm. index is input angle in deg.
			0 deg input angle corrosponding to pos x axis
		dir_ccw_bool : boolean
			True if rotation is CCW, False if rotation is CW
		"""
		self.f = f  # f in ton
		self.rd = rd  # in mm
		# self.th5_lst = th5_lst  # crank angle list in rad
		self.spm = spm
		self.w = 2 * math.pi * spm / 60  # rad/s
		self.dir_ccw_bool = dir_ccw_bool
		copy_d_lst = d_lst.copy()
		if dir_ccw_bool == False:
			copy_d_lst.reverse()
		self.d_lst = copy_d_lst  # in mm
		# self.thab_lst = thab_lst  # angle between link a and b in rad


		self.t = 1 / (6 * spm)  # sec per degree at input crank angle


		# Graph 1, x-axis (crank angle ca)
		self.th2d_lst = []  # also known as crank angle
		for i in range(360):
			self.th2d_lst.append(i)


		# Graph 1.1, y-axis (ca vs fbos)
		# make fbos_lst from d_lst. index is th2d
		self.fbos_lst = []
		d_abs_lst = []  # make all elements positive
		for x in self.d_lst:
			d_abs_lst.append(abs(x))
		max_d_abs_lst = max(d_abs_lst)
		for x in d_abs_lst:
			self.fbos_lst.append(max_d_abs_lst - x)

		# Graph 1.2, y-axis (ca vs vel)
		# get raw slide velocity wrt th2d. index is th2d
		self.v_lst = diff_list.get_diff_lst(self.fbos_lst, self.t)  # slide vel in mm/s

		# Graph 1.3, y-axis (ca vs acc)
		# get raw slide acc wrt th2d. index is th2d
		acc_mm_lst = diff_list.get_diff_lst(self.v_lst, self.t)  # slide acc in mm/s2
		self.acc_lst = [i * 0.001 for i in acc_mm_lst]

		# get crank angle th2d at TDC
		max_fbos = max(self.fbos_lst)
		self.th2d_tdc = self.fbos_lst.index(max_fbos)

		# get crank angle th2d at BDC
		min_fbos = min(self.fbos_lst)
		self.th2d_bdc = self.fbos_lst.index(min_fbos)

		# get stroke
		self.stk = max_fbos - min_fbos
		# print("self.stk", self.stk)

		# define th2d from TDC to TDC in 0 to 720 deg domain
		self.th2d_tt720_lst = []  # th2d is crank angle. 'tt' means Tdc to Tdc
		for i in range(self.th2d_tdc, self.th2d_tdc + 360):
			self.th2d_tt720_lst.append(i)

		# Graph 2, x-axis (crank angle Tdc to Tdc in 360 domain)
		# define th2d from TDC to TDC in 0 to 360 deg domain.
		self.th2d_tt360_lst = []  # th2d is crank angle. 'tt' means Tdc to Tdc. int
		self.th2d_tt360str_lst = []  # th2d is crank angle. 'tt' means Tdc to Tdc. str


		for i in self.th2d_tt720_lst:
			if i < 360:
				self.th2d_tt360_lst.append(i)
				self.th2d_tt360str_lst.append(str(i))

			else:
				self.th2d_tt360_lst.append(i - 360)
				self.th2d_tt360str_lst.append(str(i - 360))

		# v_lst
		self.v_lst = diff_list.get_diff_lst(self.fbos_lst, self.t)

		# 2x fbos raw list output
		self.fbos2x_lst = self.fbos_lst.copy()
		self.fbos2x_lst.extend(self.fbos2x_lst)

		# 2x v raw list output
		self.v2x_lst = diff_list.get_diff_lst(self.fbos_lst, self.t)  # 2x v_lst, from 0 to 720 deg
		self.v2x_lst.extend(self.v2x_lst)

		# Graph 2.1, y-axis (fbos Tdc to Tdc in 360 domain)
		# self.fbos2x_lst = self.fbos_lst.copy()  # 2x fbos_lst, from 0 to 720 deg
		# self.fbos2x_lst.extend(self.fbos2x_lst)
		self.fbos_tt_lst = []  # fbos list from tdc to tdc
		for i in self.th2d_tt720_lst:
			this_fbos = self.fbos2x_lst[i]
			self.fbos_tt_lst.append(round(this_fbos,3))

		# Graph 2.2, y-axis (vel Tdc to Tdc in 360 domain)
		# self.v2x_lst = diff_list.get_diff_lst(self.fbos_lst, self.t)  # 2x v_lst, from 0 to 720 deg
		# self.v2x_lst.extend(self.v2x_lst)
		self.v_tt_lst = []  # velocity list from tdc to tdc
		for i in self.th2d_tt720_lst:
			this_v = self.v2x_lst[i]
			self.v_tt_lst.append(round(this_v,1))

		# Graph 2.3, y-axis (acc Tdc to Tdc in 360 domain)
		# self.v_lst = diff_list.get_diff_lst(self.fbos_lst, self.t)  # 2x v_lst, from 0 to 720 deg
		self.acc2x_lst = diff_list.get_diff_lst(self.v_lst, self.t)  # 2x acc_lst, from 0 to 720 deg
		self.acc2x_lst.extend(self.acc2x_lst)
		self.acc_tt_lst = []  # velocity list from tdc to tdc
		for i in self.th2d_tt720_lst:
			this_acc = self.acc2x_lst[i]
			self.acc_tt_lst.append(this_acc)

		# th2d_at_rd and actual rd rd_act
		self.th2d_at_rd = 0
		self.rd_act = 0
		for i in range(len(self.fbos_tt_lst)):
			this_th2d = self.th2d_tt360_lst[i]
			this_fbos = self.fbos_tt_lst[i]
			self.rd_act = this_fbos
			if this_fbos <= self.rd:
				self.th2d_at_rd = this_th2d
				break


		# th2d_index_tt_at_rd
		self.th2d_index_tt_at_rd = 0
		for i in range(len(self.fbos_tt_lst)):
			this_th2d = self.th2d_tt360_lst[i]
			this_fbos = self.fbos_tt_lst[i]
			if this_fbos <= self.rd:
				self.th2d_index_tt_at_rd = i - 1  # index is kept 1 less to have conservative torque value
				break

		# v_at_rd
		self.v_at_rd = self.v_tt_lst[self.th2d_index_tt_at_rd]

		# torque
		self.trq = round(abs(self.f * 10 * self.v_at_rd / self.w), 0)  # Nm

		# mb_dic items - 'mb' meas mid to bottom of stroke
		th2d_mb_lst = []
		fbos_mb_lst = []
		v_mb_lst = []
		f_mb_lst = []

		for x in self.th2d_tt360_lst:
			this_fbos = self.fbos_lst[x]
			this_v = self.v_lst[x]  # mm/s
			if this_v < 0 and this_fbos < 0.5 * self.stk:
				# print("inside if block")
				th2d_mb_lst.append(str(x))
				# print("th2d:", x)
				fbos_mb_lst.append(this_fbos)
				v_mb_lst.append(abs(this_v))
				this_f = round(0.1 * self.trq * self.w / abs(this_v), 0)  # ton
				if this_f > self.f:
					this_f = self.f
				# print("press force :", this_f)

				f_mb_lst.append(abs(this_f))

		self.mb_dic = {
		'th2d_mb_lst':th2d_mb_lst,
		'fbos_mb_lst':fbos_mb_lst,
		'v_mb_lst':v_mb_lst,
		'f_mb_lst':f_mb_lst,
		}


	# simple raw output
	def get_th2d_lst(self):
		"""
        Returns
        -------
        list
        Returns input angle th2 list in deg. 0 is the pos X axis
        """
		return self.th2d_lst

	def get_fbos_lst(self):
		"""
        Returns
        -------
        list
        Returns fbos list in mm
        """
		return self.fbos_lst

	def get_v_lst(self):
		"""
        Returns
        -------
        list
        Returns slide vel list in mm/s
        """
		return self.v_lst  # raw v_lst

	def get_acc_lst(self):
		"""
        Returns
        -------
        list
        Returns slide acc list in mm/s2
        """
		return self.acc_lst

	def get_n5_lst(self):
		"""
        Returns
        -------
        list
        Returns crank speed list in rpm
        """
		return self.n5_lst  # raw n5 lst (crank speed in rpm)

	# 2x raw list output
	def get_fbos2x_lst(self):
		"""
        Returns
        -------
        list
        Returns fbos list over 2 strokes
        """
		return self.fbos2x_lst

	def get_v2x_lst(self):
		"""
        Returns
        -------
        list
        Returns slide vel list over 2 strokes
        """
		return self.v2x_lst

	# Tdc to Tdc output in 0 - 720 deg domain
	def get_th2d_tt720_lst(self):
		"""
        Returns
        -------
        list
        Returns input angle th2d (deg) list over 2 strokes
        """
		return self.th2d_tt720_lst  # crank angle th2d from Tdc to Tdc 

	# Tdc to Tdc output in 0 - 360 deg domain
	def get_th2d_tt360str_lst(self):
		"""
        Returns
        -------
        list
        Returns input angle list from Tdc to Tdc in deg as string
        """
		return self.th2d_tt360str_lst  # crank angle th2d from Tdc to Tdc 

	# Tdc to Tdc output in 0 - 360 deg domain
	def get_th2d_tt360_lst(self):
		"""
        Returns
        -------
        list
        Returns input angle list from Tdc to Tdc in deg as float
        """
		return self.th2d_tt360_lst  # crank angle th2d from Tdc to Tdc 

	# Graph 2.1, y-axis (fbos Tdc to Tdc in 360 domain)
	def get_fbos_tt_lst(self):
		"""
        Returns
        -------
        list
        Returns fbos list from Tdc to Tdc in mm
        """
		return self.fbos_tt_lst  # fbos list from tdc to tdc

	# Graph 2.2, y-axis (vel Tdc to Tdc in 360 domain)
	def get_v_tt_lst(self):
		"""
        Returns
        -------
        list
        Returns slide vel list from Tdc to Tdc in mm/s
        """
		return self.v_tt_lst  # velocity list from tdc to tdc

	# Graph 2.3, y-axis (acc Tdc to Tdc in 360 domain)
	def get_acc_tt_lst(self):
		"""
        Returns
        -------
        list
        Returns slide acc list from Tdc to Tdc in mm/s2
        """
		return self.acc_tt_lst  # velocity list from tdc to tdc

	def get_th2d_at_rd(self):
		"""
        Returns
        -------
        list
        Returns input angle th2d (deg) at rated distance
        """
		return self.th2d_at_rd

	def get_rd_act(self):
		"""
        Returns
        -------
        float
        Returns actual rated distance at integer rated angle
        """
		return self.rd_act

	def get_th2d_index_tt_at_rd(self):
		"""
        Returns
        -------
        list
        Returns index of input angle th2d (deg) at rated distance in list of th2d_tt
        """
		return self.th2d_index_tt_at_rd

	def get_v_at_rd(self):
		"""
        Returns
        -------
        list
        Returns slide vel at rated distance in mm/s
        """
		return self.v_at_rd

	def get_torque(self):
		"""
        Returns
        -------
        list
        Returns required gear axis torque at rated distance in Nm
        """
		return self.trq

	# # 'mb' means mid to bottom of stroke
	def get_mb_dic(self):
		"""
        Returns
        -------
        list
        Returns dictionary of th2d, fbos, vel and press force from Mid stroek to Bdc
        """
		return self.mb_dic


		# self.th2d_at_rd
		
	# def get_fb_max(self):
	# 	return self.fb_ton  # rocker force in ton

	# def get_th2d_at_fb_max(self):
	# 	return self.th2d_at_fb_max  # CA at max rocker force



"""
#  draw link program test
a = 260  # ecc
b = 800  # ter (ecc-rocker)
c = 900  # rocker
d = 1175  # rocker x
e = -375  # rocker y
f = 1175  # ter (ecc-conrod)
g = 1175  # conrod
h = 0  # slide offset x
i = 1824  # ter (rocker-conrod)
rpm = 20  # rpm
# w = 2 * math.pi * rpm / 60

# make draw link object
draw_link_obj = draw_link_modular.ModularDrawLink(a, b, c, d, e, f, g, h, i, rpm)
# get distance of slider from eg center
d_lst = draw_link_obj.get_d_lst()


# make pg obj
pg = PrettyGraph(2500, 13, rpm, d_lst, False)

# get list of independent var th2 in deg
th2d_lst = pg.get_th2d_lst()

# get fbos list raw
fbos_lst = pg.get_fbos_lst()

# get raw vel list
v_lst = pg.get_v_lst()

# tdc to tdc crank angle th2d in 720 deg domain
# th2d_tt720_lst = pg.get_th2d_tt720_lst()

# tdc to tdc crank angle th2d in 360 deg domain
th2d_tt360str_lst = pg.get_th2d_tt360str_lst()
# print(th2d_tt360str_lst)

# tdc to tdc fbos
fbos_tt_lst = pg.get_fbos_tt_lst()

# tdc to tdc velocity
v_tt_lst = pg.get_v_tt_lst()

# to get th2d at rated distance
th2d_at_rd = pg.get_th2d_at_rd()
print("th2d at RD: ", th2d_at_rd)

# to get th2d index at rated distance
th2d_index_tt_at_rd = pg.get_th2d_index_tt_at_rd()
print("th2d index at RD: ", th2d_index_tt_at_rd)

# to get slide vel at rd
v_at_rd = pg.get_v_at_rd()
print("vel at RD", v_at_rd)

# get torque
trq = pg.get_torque()
print("torque", trq)

mb_dic = pg.get_mb_dic()
th2d_mb_lst = mb_dic['th2d_mb_lst']
fbos_mb_lst = mb_dic['fbos_mb_lst']
v_mb_lst = mb_dic['v_mb_lst']
f_mb_lst = mb_dic['f_mb_lst']



# multiple plots
fig, axs = plt.subplots(2, 3, figsize=(18, 10))
fig.suptitle('Mechanical press energy graphs')
plt.subplots_adjust(left=None, bottom=None, right=None, top=None,
	wspace=0.4, hspace=0.4)

graph_00, = axs[0, 0].plot(th2d_lst, fbos_lst, 'tab:red')
# axs[0, 0].legend(['fbos'], loc="upper right")
axs[0, 0].grid(visible=None, which='major', axis='both')
axs[0, 0].title.set_text('raw fbos vs. ca')
axs[0, 0].set_xlabel('ca')
axs[0, 0].set_ylabel('fbos (mm)')
axs[0, 0].set_ylim(ymin=0)
axs[0, 0].text(0.5, 0.5, 'Isgec, India ', transform=axs[0, 0].transAxes,
    fontsize=30, color='gray', alpha=0.2,
    ha='center', va='center')

graph_10, = axs[1, 0].plot(th2d_lst, v_lst, 'tab:red')
# axs[1, 0].legend(['velocity'], loc="upper right")
axs[1, 0].grid(visible=None, which='major', axis='both')
axs[1, 0].title.set_text('raw vel vs. ca')
axs[1, 0].set_xlabel('ca')
axs[1, 0].set_ylabel('vel (mm/s)')
# axs[1, 0].set_ylim(ymin=0)
axs[1, 0].text(0.5, 0.5, 'Isgec, India ', transform=axs[1, 0].transAxes,
    fontsize=30, color='gray', alpha=0.2,
    ha='center', va='center')

graph_01, = axs[0, 1].plot(th2d_tt360str_lst, fbos_tt_lst, 'tab:red')
# axs[0, 1].legend(['fbos'], loc="upper right")
axs[0, 1].grid(visible=None, which='major', axis='both')
axs[0, 1].title.set_text('fbos vs. ca')
axs[0, 1].set_xlabel('ca')
axs[0, 1].set_ylabel('fbos (mm)')
# axs[0, 1].set_ylim(ymin=0)
axs[0, 1].text(0.5, 0.5, 'Isgec, India ', transform=axs[0, 1].transAxes,
    fontsize=30, color='gray', alpha=0.2,
    ha='center', va='center')

graph_11, = axs[1, 1].plot(th2d_tt360str_lst, v_tt_lst, 'tab:red')
# axs[1, 1].legend(['vel'], loc="upper right")
axs[1, 1].grid(visible=None, which='major', axis='both')
axs[1, 1].title.set_text('vel vs. ca')
axs[1, 1].set_xlabel('ca')
axs[1, 1].set_ylabel('vel (mm/s)')
# axs[1, 1].set_ylim(ymin=0)
axs[1, 1].text(0.5, 0.5, 'Isgec, India ', transform=axs[1, 1].transAxes,
    fontsize=30, color='gray', alpha=0.2,
    ha='center', va='center')

graph_02, = axs[0, 2].plot(th2d_mb_lst, v_mb_lst, 'tab:red')
# axs[0, 2].legend(['vel'], loc="upper right")
axs[0, 2].grid(visible=None, which='major', axis='both')
axs[0, 2].title.set_text('vel vs. ca in forming zone')
axs[0, 2].set_xlabel('ca')
axs[0, 2].set_ylabel('vel (mm/s)')
# axs[0, 2].set_ylim(ymin=0)
axs[0, 2].text(0.5, 0.5, 'Isgec, India ', transform=axs[0, 2].transAxes,
    fontsize=30, color='gray', alpha=0.2,
    ha='center', va='center')

graph_12, = axs[1, 2].plot(th2d_mb_lst, f_mb_lst, 'tab:red')
# axs[1, 2].legend(['force'], loc="upper right")
axs[1, 2].grid(visible=None, which='major', axis='both')
axs[1, 2].title.set_text('force vs. ca in forming zone')
axs[1, 2].set_xlabel('ca')
axs[1, 2].set_ylabel('force (ton)')
# axs[1, 2].set_ylim(ymin=0)
axs[1, 2].text(0.5, 0.5, 'Isgec, India ', transform=axs[1, 2].transAxes,
    fontsize=30, color='gray', alpha=0.2,
    ha='center', va='center')

plt.show()
"""
