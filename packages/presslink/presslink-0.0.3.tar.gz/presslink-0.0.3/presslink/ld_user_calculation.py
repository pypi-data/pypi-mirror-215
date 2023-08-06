# user calculation program for link drive press

import math
from presslink.ld_modular import ModularDrawLink
from presslink.pretty_graph_datagen import PrettyGraph
from datetime import datetime
from presslink.ld_graph_plot import get_graphs
from presslink.ld_excel_writer import write_to_excel
from presslink.ld_sizer import LinkDriveSizer
from presslink.remove_trailing_zeros import remove_trailing_0_fcn
from presslink.ld_rocker_force import RockerLink


# GEAR ROTATION IS CCW AS DEFAULT AND CAN NOT BE CHANGED

scale_fact = 1
# link lengths multiplied by this factor to change link lengths
# if interference is detected, increase the scale factor and run again

# Isgec std link for 2500t Transfer press
# a = 260, b = 800, c = 900, d = -1175, e = -375, f = 1175, g = 1175, h = 0, thd_bf = 134, nr_sus = 4


# LD link lengths
a = 260 * scale_fact  # eccentricity 
b = 800 * scale_fact  # conrod horizontal
c = 900 * scale_fact  # upper rocker link
d = -1175 * scale_fact  # upper rocker pivot x from CS rotation center
# d is -ve for down pulling,
# d is +ve for up pulling drive
e = -375 * scale_fact  # upper rocker pivot y from CS rotation center

# press data
pf = 2500  # press force ton
rd = 13  # rated dist in mm
rpm = 25  # press rpm
f = 1175  # ternary link vertical length
g = 1175  # main conrod (vertical)
h = 0  # slide offset x
thd_bf = 134  # angle in deg bw link f and b of ternary link 

nr_sus = 4  # number of suspensions

# write to excel if no interference
write_excel_file_flag = True  # excel write if True

# show graph setting
show_graph_flag = True


# DO NOT CHANGE BELOW SETTINGS
# write to excel if no interference
link_ok_flag = False  # chk if links are not interfering

# Pretty Graph Setting

# ml cal setting
ROOT_OPTION = 3
# Root 3 always in Link Drive

# datetime setting
now = datetime.now()
dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
timestamp = int(round(now.timestamp()))

# project setting
ps_project_name = "Link Drive press calculations"
ps_designer = "Sanchit"
ps_date = dt_string
ps_note = "0 deg is + ve X axis. +ve angle is in CCW direction as default. \
Raw preffix in geaph means that the 0 deg gear angle is at +ve X axis"


# intermediate calculations
w = 2 * math.pi * rpm / 60  # ang vel
t = 1 / (6 * rpm)  # sec per degree at input crank angle


# make kj object
ld_obj = ModularDrawLink(a, b, c, d, e, f, g, h, 
    thd_bf, rpm, root_op=ROOT_OPTION)

# get distance of slider from eg center
d_lst = ld_obj.get_d_lst()
d_max = round(max(abs(min(d_lst)), abs(max(d_lst))), 3)
# print("BOS from rot center: ", round(d_max,3))

# calculate stroke
stk = round(abs(min(d_lst) - max(d_lst)), 3)
# print("Stroke: ", round(stk, 3))

# get all angles
th2d_lst = ld_obj.get_th2d_lst()  # input gear angle/crank angle in deg
th3d_lst = ld_obj.get_th3d_lst()  # horizontal conrod angle in deg
th4d_lst = ld_obj.get_th4d_lst()  # rocker link angle in deg
th5d_lst = ld_obj.get_th5d_lst()  # rocker link angle in deg
th5_lst = ld_obj.get_th5_lst()  # rocker link angle rad
th6d_lst = ld_obj.get_th6d_lst()  # conrod angle in deg
# thabd_lst = ld_obj.get_thabd_lst()  # angle bw link a and b in deg
thbcd_lst = ld_obj.get_thbcd_lst()  # angle bw link b and c in deg
# thab_lst = ld_obj.get_thab_lst()  # angle bw link a and b in rad
thbc_lst = ld_obj.get_thbc_lst()  # angle bw link b and c in rad
thbc_min = min(thbc_lst)  # min thab in rad

# print("thbc_min", thbc_min * 180 / math.pi)
# crank angle th5 angular speed w5
# w5_lst = diff_list.get_diff_lst(th5_lst, t)  # crank angle ang vel w5 in rad/s
# remove peaks
# w5_lst = peak_remover(w5_raw_lst)
# convert w into rpm
# n5_lst = [this_i * 60 / (2 * math.pi) for this_i in w5_lst]


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
# print("actual rd: ", round(rd_act, 3))

mb_dic = pg.get_mb_dic()
th2d_mb_lst = mb_dic['th2d_mb_lst']
fbos_mb_lst = mb_dic['fbos_mb_lst']
v_mb_lst = mb_dic['v_mb_lst']
f_mb_lst = mb_dic['f_mb_lst']


# thabd_at_rd = thabd_lst[th2d_at_rd]  # thabd at rd (in deg)
# print("thabd_at_rd", round(thabd_at_rd,3))

tl_obj = RockerLink(b, f, th3d_lst, th4d_lst, th5d_lst, th6d_lst, th2d_mb_lst, f_mb_lst)

fc_mb_lst = tl_obj.get_fc()
max_f_rkr_per_sus = max(abs(max(fc_mb_lst)), abs(min(fc_mb_lst))) / nr_sus
# print("Rocker force list (ton): ", fc_mb_lst)
# print("Max rocker force (ton): ", max_f_rkr_per_sus)


sizer_obj = LinkDriveSizer(a, b, f, thbc_min, pf/nr_sus, max_f_rkr_per_sus)

d_pin_eg = sizer_obj.get_d_pin_eg()
d_be = sizer_obj.get_d_be()
od_be_ring = sizer_obj.get_od_be_ring()
d_pin_rkr = sizer_obj.get_d_pin_rkr()
l_bush_rkr = sizer_obj.get_l_bush_rkr()
w_rkr = sizer_obj.get_w_rkr()
thk_rkr = sizer_obj.get_thk_rkr()
od_ring_rkr = sizer_obj.get_od_ring_rkr()
d_pin_cr = sizer_obj.get_d_pin_cr()
l_bush_cr = sizer_obj.get_l_bush_cr()
d_ring_cr = sizer_obj.get_d_ring_cr()
rkr_ring_ter_intrf_flag = sizer_obj.get_rkr_ring_ter_intrf_flag()
rkr_link_ter_intrf_flag = sizer_obj.get_rkr_link_ter_intrf_flag()
cr_ter_intrf_flag = sizer_obj.get_cr_ter_intrf_flag()
link_ok_flag = sizer_obj.get_link_ok_flag()

setting_dic = sizer_obj.get_setting_dic()

sc_bush_rkr = setting_dic['sc_bush_rkr']
ss_all_eg_pin = setting_dic['ss_all_eg_pin']
rat_oi_rkr = setting_dic['rat_oi_rkr']
rat_wp_rkr = setting_dic['rat_wp_rkr']
rat_ld_bush_rkr = setting_dic['rat_ld_bush_rkr']
rat_oi_be_ring = setting_dic['rat_oi_be_ring']
thk_lip_gear = setting_dic['thk_lip_gear']
thk_wall_bush_pin_eg = setting_dic['thk_wall_bush_pin_eg']
mrg_hit = setting_dic['mrg_hit']
rat_oi_cr = setting_dic['rat_oi_cr']
sc_bush_cr = setting_dic['sc_bush_cr']
rat_ld_bush_cr = setting_dic['rat_ld_bush_cr']


# Graph plot
if show_graph_flag:
    graph_plot = get_graphs(th2d_lst, fbos_lst, v_lst, acc_lst, 
        th2d_tt360str_lst, fbos_tt_lst, v_tt_lst, fbos_mb_lst, v_mb_lst, f_mb_lst, fc_mb_lst)


# gear rotation direction
GEAR_ROT_DIR = "CCW"  # gear rotation is always ccw

# print message if interference is detected
if not link_ok_flag:
    print("Interference detected in links. Check output worksheet of generated excel file and try following:")
    print("1. Increasing link b if interference is detected there.")
    print("2. Increasing link f if interference is detected there.")    
    print("3. Increasing scale factor scale_fact.")

# excel write
if write_excel_file_flag:
    write_to_excel(ps_project_name, ps_designer, ps_date, ps_note,  # ws0
        th2d_lst, th3d_lst, th4d_lst, th5d_lst, th6d_lst, thbcd_lst, fbos_lst, v_lst, acc_lst, # ws1
        th2d_tt360str_lst, fbos_tt_lst, v_tt_lst,  # ws2
        fbos_mb_lst, v_mb_lst, f_mb_lst,  # ws3
        a, b, c, d, e, f, g, h, thd_bf, rpm, pf, rd, nr_sus, ROOT_OPTION,  GEAR_ROT_DIR,  # ws4 line 1
        trq, v_at_rd, max_f_rkr_per_sus, stk, d_max, rd_act, d_pin_eg, d_be,  # ws5 line 1 
        od_be_ring, d_pin_rkr, l_bush_rkr, w_rkr, thk_rkr, od_ring_rkr,  # ws5 line 2
        d_pin_cr, l_bush_cr, d_ring_cr, rkr_ring_ter_intrf_flag,  # ws5 line 3
        rkr_link_ter_intrf_flag, cr_ter_intrf_flag, link_ok_flag,  # ws5 line 4
        th2d_at_rd, th3d_at_rd, th4d_at_rd, th5d_at_rd, th6d_at_rd,  # ws5 line 5
        sc_bush_rkr, ss_all_eg_pin, rat_oi_rkr, rat_wp_rkr, rat_ld_bush_rkr,  # ws6 line 1
        rat_oi_be_ring, thk_lip_gear, thk_wall_bush_pin_eg, mrg_hit, rat_oi_cr,  # ws6 line 2
        sc_bush_cr, rat_ld_bush_cr)  # ws6 line 3
