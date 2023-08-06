# user calculation program for maylink

import math
from presslink.ml_modular import ModularMayLink
from presslink.pretty_graph_datagen import PrettyGraph
from datetime import datetime
from presslink.ml_graph_plot import get_graphs
from presslink.ml_excel_writer import write_to_excel
from presslink import diff_list
from presslink.ml_sizer import MayLinkSizer
from presslink.remove_trailing_zeros import remove_trailing_0_fcn
from presslink.ml_ternary_link_force import TernaryLink


# GEAR ROTATION IS CCW AS DEFAULT AND CAN NOT BE CHANGED

scale_fact = 1
# link lengths multiplied by this factor to change link lengths
# if interference is detected, increase the scale factor and run again
# also try increasing pin length l_pin

# ML link lengths
a = 150 * scale_fact  # eccentricity 
b = 905 * scale_fact  # conrod horizontal
c = 325 * scale_fact  # upper rocker link
d = -767.5 * scale_fact  # upper rocker pivot x from CS rotation center
# d is -ve for down pulling, 
# d is +ve for up pulling drive
e = 525 * scale_fact  # upper rocker pivot y from CS rotation center

# press data
pf = 400  # press force ton
rd = 7  # rated dist in mm
rpm = 30  # press rpm
f = 400  # ternary link vertical length
g = 585  # main conrod (vertical)
h = 0  # slide offset x
thd_offset_ccw_dir_add = 360 - 82.3  # angle in deg bw link f and b of ternary link in ccw dir
# 360 - thbf for down pulling
# thbf for up pulling
# this angle is measured from link b to link f in CCW direction always

l_pin = 500  # length of main pin in mm. this will depend on slide LR size
fra_rev = 0.1  # reverse load percenrage of rated force. 0.1 means 10%


drv_mode = "down pulling or up pushing"  # not used in calculations, just for showing in excel file
# drv_mode = "up pulling or down pushing"

# print("driving mode:", drv_mode)

# write to excel if no interference
write_excel_file_flag = True  # excel write if True

# show graph setting
show_graph_flag = True


# DO NOT CHANGE BELOW SETTINGS
# write to excel if no interference
link_ok_flag = False  # chk if links are not interfering

# Pretty Graph Setting

# ml cal setting
ROOT_OPTION = 2
# Root 2 for down pulling, 
# Root 3 for up pulling

# datetime setting
now = datetime.now()
dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
timestamp = int(round(now.timestamp()))

# project setting
ps_project_name = "Maylink press calculations"
ps_designer = "Sanchit"
ps_date = dt_string
ps_note = "0 deg is + ve X axis. +ve angle is in CCW direction as default. \
Raw preffix in geaph means that the 0 deg gear angle is at +ve X axis"


# intermediate calculations
w = 2 * math.pi * rpm / 60  # ang vel
t = 1 / (6 * rpm)  # sec per degree at input crank angle


# make kj object
ml_obj = ModularMayLink(a, b, c, d, e, f, g, h, 
    thd_offset_ccw_dir_add, rpm, root_op=ROOT_OPTION)

# get distance of slider from eg center
d_lst = ml_obj.get_d_lst()
d_max = round(max(abs(min(d_lst)), abs(max(d_lst))), 3)
# print("BOS from rot center: ", round(d_max,3))

# calculate stroke
stk = round(abs(min(d_lst) - max(d_lst)), 3)
# print("Stroke: ", round(stk,3))

# get all angles
th2d_lst = ml_obj.get_th2d_lst()  # input gear angle/crank angle in deg
th3d_lst = ml_obj.get_th3d_lst()  # horizontal conrod angle in deg
th4d_lst = ml_obj.get_th4d_lst()  # rocker link angle in deg
th5d_lst = ml_obj.get_th5d_lst()  # rocker link angle in deg
th5_lst = ml_obj.get_th5_lst()  # rocker link angle rad
th6d_lst = ml_obj.get_th6d_lst()  # conrod angle in deg
thabd_lst = ml_obj.get_thabd_lst()  # angle bw link a and b in deg
thbcd_lst = ml_obj.get_thbcd_lst()  # angle bw link b and c in deg
thab_lst = ml_obj.get_thab_lst()  # angle bw link a and b in rad
thbc_lst = ml_obj.get_thbc_lst()  # angle bw link b and c in rad
thbc_min = min(thbc_lst)  # min thab in rad


# crank angle th5 angular speed w5
w5_lst = diff_list.get_diff_lst(th5_lst, t)  # crank angle ang vel w5 in rad/s
# remove peaks
# w5_lst = peak_remover(w5_raw_lst)
# convert w into rpm
n5_lst = [this_i * 60 / (2 * math.pi) for this_i in w5_lst]


# make preety graph obj
pg = PrettyGraph(pf, rd, rpm, d_lst)

# get list of independent var th2 in deg
# th2d_lst = pg.get_th2d_lst()

# get fbos list raw
fbos_lst = pg.get_fbos_lst()

# get raw vel list
v_lst = pg.get_v_lst()

# get raw acc list
acc_lst = pg.get_acc_lst()

# get raw crank speed list
# n5_lst = pg.get_n5_lst()

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
# print("th2d_at_rd: ", th2d_at_rd)

# to get th2d index at rated distance in TDC to TDC graph only
th2d_index_tt_at_rd = pg.get_th2d_index_tt_at_rd()

# to get slide vel at rd
v_at_rd = abs(pg.get_v_at_rd())

# get torque
trq = pg.get_torque()
# print("trq: ", trq)


# th3, 4, 5 and 6 at RD
th3d_at_rd = round(th3d_lst[th2d_at_rd], 1)
th4d_at_rd = round(th4d_lst[th2d_at_rd], 1)
th5d_at_rd = round(th5d_lst[th2d_at_rd], 1)
th6d_at_rd = round(th6d_lst[th2d_at_rd], 1)

if th5d_at_rd > 359:
    th5d_at_rd = th5d_at_rd - 360

# actual rd
rd_act = pg.get_rd_act()
# print("actual rd: ", round(rd_act,3))

mb_dic = pg.get_mb_dic()
th2d_mb_lst = mb_dic['th2d_mb_lst']
fbos_mb_lst = mb_dic['fbos_mb_lst']
v_mb_lst = mb_dic['v_mb_lst']
f_mb_lst = mb_dic['f_mb_lst']


thabd_at_rd = thabd_lst[th2d_at_rd]  # thabd at rd (in deg)
# print("thabd_at_rd", round(thabd_at_rd,3))

tl_obj = TernaryLink(a, b, c, d, e, f, g, pf, rd, th2d_lst, th2d_at_rd, 
    th3d_lst, th4d_lst, th6d_lst, fbos_lst, thd_offset_ccw_dir_add)

fg = tl_obj.get_fg()
fc = tl_obj.get_fc()
fa = tl_obj.get_fa()
j = tl_obj.get_j()
thd_j = tl_obj.get_thd_j()
thd_cb = tl_obj.get_thd_cb()
thd_bj = tl_obj.get_thd_bj()
thd_jg = tl_obj.get_thd_jg()
fb_max = tl_obj.get_fa()
thd_a = tl_obj.get_thd_a()



# print("fg", fg)
# print("fc", fc)
# print("fa", fa)
# print("j", j)
# print("thd_j", thd_j)
# print("thd_cb", thd_cb)
# print("thd_bj", thd_bj)
# print("thd_jg", thd_jg)
# print("conrod force fb_max", fb_max)
# print("conrod link b force angle", thd_a)


sizer_obj = MayLinkSizer(c, pf, f, g, l_pin, fra_rev, th4d_lst)
d_pin = round(sizer_obj.get_d_pin(), 0)
th4d_max = round(sizer_obj.get_th4d_max(), 0)
w_frk = round(sizer_obj.get_w_frk(), 0)
d_frk = round(sizer_obj.get_d_frk(), 0)
# w_cr_se = round(sizer_obj.get_w_cr_se(), 0)
w_bush = round(sizer_obj.get_w_bush(), 0)

link_ok_flag = sizer_obj.get_link_ok_flag()

intrf_c_fork_flag = sizer_obj.get_intrf_c_fork_flag()
intrf_f_bore_flag = sizer_obj.get_intrf_f_bore_flag()
intrf_g_fork_flag = sizer_obj.get_intrf_g_fork_flag()

# getting sizer setting data
sizer_setting_dic = sizer_obj.get_setting_dic()
sc_bush_all = sizer_setting_dic['sc_bush_all']
sc_frk_all = sizer_setting_dic['sc_frk_all']
st_frk_all = sizer_setting_dic['st_frk_all']
rat_cd_d_frk = sizer_setting_dic['rat_cd_d_frk']
rat_cd_f = sizer_setting_dic['rat_cd_f']
fra_rev = sizer_setting_dic['fra_rev']


# Graph plot
if show_graph_flag:
    graph_plot = get_graphs(th2d_lst, fbos_lst, v_lst, acc_lst, 
        th2d_tt360str_lst, fbos_tt_lst, v_tt_lst, fbos_mb_lst, v_mb_lst, f_mb_lst)


# gear rotation direction
GEAR_ROT_DIR = "CCW"  # gear rotation is always ccw

# print message if interference is detected
if not link_ok_flag:
    print("Interference detected in links. Check output worksheet of generated excel file and try following:")
    print("1. Increasing pin length l_pin.")
    print("2. Increasing link c if interfering with fork.")
    print("3. Increasing link g if interfering with fork.")
    print("4. Increasing link f if bores are coming too close.")
    print("5. Increasing fork width and reduce fork OD. This can be done by reducing the allowable contact stress of fork in Sizer Class.")
    print("6. Increasing scale factor scale_fact.")

# excel write
if write_excel_file_flag:
    write_to_excel(ps_project_name, ps_designer, ps_date, ps_note,  # ws0
        th2d_lst, th3d_lst, th4d_lst, th5d_lst, th6d_lst, thabd_lst, thbcd_lst, fbos_lst, v_lst, acc_lst, n5_lst,  # ws1
        th2d_tt360str_lst, fbos_tt_lst, v_tt_lst,  # ws2
        fbos_mb_lst, v_mb_lst, f_mb_lst,  # ws3
        a, b, c, d, e, f, g, h, thd_offset_ccw_dir_add, rpm, pf, rd, ROOT_OPTION,  # ws4 line 1
        GEAR_ROT_DIR,  # ws4 line 2
        trq, v_at_rd, fb_max, d_pin, l_pin, w_frk, d_frk, w_bush, th4d_max, link_ok_flag, intrf_c_fork_flag, intrf_f_bore_flag, intrf_g_fork_flag, fg, fc, fa, j,   # ws5 line 1
        th2d_at_rd, th3d_at_rd, th4d_at_rd, th5d_at_rd, th6d_at_rd, thd_j, thd_cb, thd_bj, thd_jg, thd_a, # ws5 line 2
        stk, drv_mode, d_max, rd_act,  # ws5 line 3
        sc_bush_all, sc_frk_all, st_frk_all, rat_cd_d_frk, rat_cd_f, fra_rev)  # ws6
