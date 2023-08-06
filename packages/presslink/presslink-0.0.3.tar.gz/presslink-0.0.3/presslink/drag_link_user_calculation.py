# user calculation program for drag link

import math
from presslink.drag_link_modular import ModularDragLink
from presslink.pretty_graph_datagen import PrettyGraph
from presslink.drag_link_rocker_force import get_rocker_dic
from presslink import drag_link_sizer
from datetime import datetime
from presslink.drag_link_graph_plot import get_graphs
from presslink.drag_link_excel_writer import write_to_excel
from presslink import diff_list
from presslink.diff_peak_remover import peak_remover
from mechpress import ed

# GEAR ROTATION IS CCW AS DEFAULT AND CAN NOT BE CHANGED

scale_fact = 1.1
# link lengths multiplied by this factor to change link lengths
# if interference is detected, increase the scale factor and run again

# A*** 800t progdie link lengths
# a = 564, b = 611, c = 352, d = -122, e = -70.5, pf = 800, rd = 12.7, rpm = 50,
# f = 200, thd_offset_ccw_dir_add = 170 
# drag gearbox
a = 564 * scale_fact  # gear link
b = 611 * scale_fact  # rocker
c = 352 * scale_fact  # crank connector
d = -122 * scale_fact  # crankshaft x
e = -70.5 * scale_fact  # crankshaft y

# press data
pf = 1250  # press force ton
rd = 1 * 14.35  # rated dist in mm
rpm = 30  # press rpm
f = 400 / 2  # ecc (half of press stroke)
g = 6 * f  # conrod
h = 0  # slide offset x
thd_offset_ccw_dir_add = 170  # offset angle in CCW dir
# in A*** design, this is 170 for progdie
# 190 for blanking (isgec aprox of a*** design)

# write to excel if no interference
write_excel_file_flag = True  # excel write if True

# show graph setting
show_graph_flag = False


# DO NOT CHANGE BELOW SETTINGS
# write to excel if no interference
link_ok_flag = False  # chk if links are not interfering

# Pretty Graph Setting

# Sizer setting
solid_shaft_flag = True  # Flase for splined hollow shaft

integral_crank_connector_flag = True
# Always True (integral) in hollow splined output shaft
# when solid output shaft, it is true in A*** design. False in MH design


# nr suspensions
nr_sus = 1  # 2 or 1 only


# drag link cal setting
ROOT_OPTION = 3  # 3 for A*** design. Do not change
# other root is 2 in case of old isgec design

# datetime setting
now = datetime.now()
dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
timestamp = int(round(now.timestamp()))

# project setting
ps_project_name = "Drag link press calculations"
ps_designer = "Sanchit"
ps_date = dt_string
ps_note = "0 deg is + ve X axis. +ve angle is in CCW direction as default. \
Raw preffix in geaph means that the 0 deg gear angle is at +ve X axis"


# intermediate calculations
w = 2 * math.pi * rpm / 60  # ang vel
t = 1 / (6 * rpm)  # sec per degree at input crank angle


# torque at CS
press_obj = ed.ED(f / 1000, g / 1000, rd / 1000, pf * 10000)  # to make ed press object
trq_cs = int(press_obj.get_torque()/1000)  # crank shaft torque in kNm for ED press


# make drag link object
drag_link_obj = ModularDragLink(a, b, c, d, e, f, g, h, 
    thd_offset_ccw_dir_add, rpm, root_op=ROOT_OPTION)

# get distance of slider from eg center
d_lst = drag_link_obj.get_d_lst()

# get all angles
th2d_lst = drag_link_obj.get_th2d_lst()  # input gear angle in deg
th3d_lst = drag_link_obj.get_th3d_lst()  # rocker link angle in deg
th4d_lst = drag_link_obj.get_th4d_lst()  # crank connector angle in deg
th5d_lst = drag_link_obj.get_th5d_lst()  # crank angle in deg
th5_lst = drag_link_obj.get_th5_lst()  # crank angle in rad
th6d_lst = drag_link_obj.get_th6d_lst()  # conrod angle in deg
thabd_lst = drag_link_obj.get_thabd_lst()  # angle bw link a and b in deg
thbcd_lst = drag_link_obj.get_thbcd_lst()  # angle bw link a and b  in deg
thab_lst = drag_link_obj.get_thab_lst()  # angle bw link a and b in rad
thbc_lst = drag_link_obj.get_thbc_lst()  # angle bw link a and b  in rad
thbc_min = min(thbc_lst)  # min thab in rad


# crank angle th5 angular speed w5
w5_raw_lst = diff_list.get_diff_lst(th5_lst, t)  # crank angle ang vel w5 in rad/s
# remove peaks
w5_lst = peak_remover(w5_raw_lst)
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

# to get th2d index at rated distance in TDC to TDC graph only
th2d_index_tt_at_rd = pg.get_th2d_index_tt_at_rd()

# to get slide vel at rd
v_at_rd = abs(pg.get_v_at_rd())

# get torque
trq = pg.get_torque()

# actual rd
rd_act = pg.get_rd_act()
# print("actual rd: ", round(rd_act, 3))

mb_dic = pg.get_mb_dic()
th2d_mb_lst = mb_dic['th2d_mb_lst']
fbos_mb_lst = mb_dic['fbos_mb_lst']
v_mb_lst = mb_dic['v_mb_lst']
f_mb_lst = mb_dic['f_mb_lst']

rkr_data_dic = get_rocker_dic(a, trq, thab_lst, th2d_at_rd)
fb_max = abs(rkr_data_dic['fb_max_ton'])
th2d_at_fb_max = abs(rkr_data_dic['th2d_at_fb_max'])
fb_at_rd = abs(rkr_data_dic['fb_at_rd_ton'])


# check interference and get sizing data
sizer_obj = drag_link_sizer.DragLinkSizer(a, b, c, d, e, thbc_min, 
    fb_max, trq, w, nr_sus, solid_shaft_flag, integral_crank_connector_flag)
# respective booleans in above object are solid_out_shaft_flag, cc_integral_flag
# do not use False, False combination as it is never used
# True, True combination is most compact and is used by A***
# False, True combination is used in splined coupling that we used in many jobs

bore_in_bore = sizer_obj.bore_in_bore()
rkr_cc_hit = sizer_obj.rkr_cc_hit()
high_vel = sizer_obj.high_vel()
ds_trq_unit_out = round(sizer_obj.get_torque_unit_out_shaft_dia(), 0)
dp_rkr = round(sizer_obj.get_rocker_pin_dia(), 0)
w_bush_rkr = round(sizer_obj.get_rocker_bush_width(), 0)
d_cs = round(sizer_obj.get_crank_shaft_dia(), 0)
bush_v_gear = round(sizer_obj.get_bush_v(), 0)
w_rkr = round(sizer_obj.get_rocker_width(), 0)
thk_rkr = round(sizer_obj.get_rocker_thk(), 0)
gap_bc = round(sizer_obj.get_gap_bc(), 0)
gear_bore_dia = round(sizer_obj.get_gear_bore_dia(), 0)
d_in_clr_gear = round(sizer_obj.get_d_in_clr_gear(), 0)

cc_arm_thk = round(sizer_obj.get_cc_arm_thk(), 0)
w_bush_d_s = round(sizer_obj.get_w_bush_d_s(), 0)
w_bush_gear = round(sizer_obj.get_w_bush_gear(), 0)
w_gear_body = round(sizer_obj.get_w_gear_body(), 0)
w_trq_unit = round(sizer_obj.get_w_trq_unit(), 0)
len_d_s = round(sizer_obj.get_len_d_s(), 0)
wt_rkr = round(sizer_obj.get_wt_rkr(), 0)
wt_pin_rkr = round(sizer_obj.get_wt_pin_rkr(), 0)
wt_cc = round(sizer_obj.get_wt_cc(), 0)
wt_ecc_sup = round(sizer_obj.get_wt_ecc_sup(), 0)
wt_gear_body = round(sizer_obj.get_wt_gear_body(), 0)
wt_bush_rkr = round(sizer_obj.get_wt_bush_rkr(), 0)
wt_bush_d_s = round(sizer_obj.get_wt_bush_d_s(), 0)
wt_bush_gear = round(sizer_obj.get_wt_bush_gear(), 0)


# getting sizer setting data
sizer_setting_dic = sizer_obj.get_setting_dic()
sc = sizer_setting_dic['sc']
se = sizer_setting_dic['se']
sy = sizer_setting_dic['sy']
fos = sizer_setting_dic['fos']
kf = sizer_setting_dic['kf']
kfs = sizer_setting_dic['kfs']
v_max_all_bush_gear = sizer_setting_dic['v_max_all_bush_gear']
cc_mid_cut_fact = sizer_setting_dic['cc_mid_cut_fact']




# print interference data
# print("Gear bore interfering with rocker pin bore?", bore_in_bore)
# print("rkr hitting crank connector?", rkr_cc_hit)
# print("Is bush vel too high?", high_vel)

# link combination is ok if no interference
if not bore_in_bore and not rkr_cc_hit and not high_vel:
    link_ok_flag = True


# Graph plot
if show_graph_flag:
    graph_plot = get_graphs(th2d_lst, fbos_lst, v_lst, acc_lst, n5_lst, 
        th2d_tt360str_lst, fbos_tt_lst, v_tt_lst, fbos_mb_lst, v_mb_lst, f_mb_lst)


# gear rotation direction
GEAR_ROT_DIR = "CCW"  # gear rotation is always ccw


# print message if interference is detected
if not link_ok_flag:
    print("Interference detected in links. Check output worksheet of generated excel file and try following:")
    print("1. use solid and integral crank connector shaft.")
    print("2. Increasing allowable stress level in Sizer class.")
    print("3. Increasing the link where interference is detected.")
    print("4. Increasing scale factor scale_fact to increase all link lengths in proportion.")


# excel write
if write_excel_file_flag and link_ok_flag:
    write_to_excel(ps_project_name, ps_designer, ps_date, ps_note,  # ws0
        th2d_lst, th3d_lst, th4d_lst, th5d_lst, th6d_lst, thabd_lst, thbcd_lst, fbos_lst, v_lst, acc_lst, n5_lst,  # ws1
        th2d_tt360str_lst, fbos_tt_lst, v_tt_lst,  # ws2
        fbos_mb_lst, v_mb_lst, f_mb_lst,  # ws3
        a, b, c, d, e, f, g, h, thd_offset_ccw_dir_add, rpm, pf, rd, ROOT_OPTION,  # ws4 line 1
        GEAR_ROT_DIR, solid_shaft_flag, integral_crank_connector_flag, nr_sus,  # ws4 line 2
        trq, v_at_rd, fb_max, th2d_at_fb_max, fb_at_rd, ds_trq_unit_out, dp_rkr, w_bush_rkr, d_cs, w_rkr, thk_rkr,  # ws5 line 1 
        gear_bore_dia, bush_v_gear, d_in_clr_gear, cc_arm_thk, w_bush_d_s, w_bush_gear,   # ws5 line 2
        w_gear_body, w_trq_unit, len_d_s, wt_rkr, wt_pin_rkr, wt_cc, wt_ecc_sup, wt_gear_body,   # ws5 line 3
        wt_bush_rkr, wt_bush_d_s, wt_bush_gear, bore_in_bore, rkr_cc_hit, high_vel, rd_act, trq_cs,  # ws5 line 4
        sc, se, sy, kf, kfs, fos, v_max_all_bush_gear, cc_mid_cut_fact)  # ws6
