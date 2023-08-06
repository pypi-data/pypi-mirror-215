"""Writing to excel file

This script writes the incoming data into excel file

This script requires that `xlsxwriter` be installed within the Python
environment you are running this script in.

"""
from datetime import datetime
import xlsxwriter


def write_to_excel(ps_project_name, ps_designer, ps_date, ps_note,  # ws0
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
    sc_bush_cr, rat_ld_bush_cr):
    """Gets and writes the data in excel file
    Parameters
    ----------
    floats
        data to write in excel file

    Returns
    -------
    none
        writes the data into an excel file
    """

    # datetime setting
    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    timestamp = int(round(now.timestamp()))

    # giving filename
    excelFileName = "LinkDrive_" + \
    str(pf) + "t@" + \
    str(rd) + "rd_" + \
    str(a) + "ecc_" + \
    "r" + str(ROOT_OPTION) + "_"+ \
    GEAR_ROT_DIR + "_"+\
    str(thd_bf) + "d_"+ \
    str(timestamp) + ".xlsx"

    workbook = xlsxwriter.Workbook(excelFileName)
    
    ws0 = workbook.add_worksheet('ws0_general')
    ws1 = workbook.add_worksheet('ws1_raw')
    ws2 = workbook.add_worksheet('ws2_tt')
    ws3 = workbook.add_worksheet('ws3_mb')
    ws4 = workbook.add_worksheet('ws4_input')
    ws5 = workbook.add_worksheet('ws5_output')
    ws6 = workbook.add_worksheet('ws6_setting')

    # ws0 data
    ws0_row_general = 0
    ws0_row_project_name = 1
    ws0_row_designer = 2
    ws0_row_date = 3
    ws0_row_note = 4

    # ws1 data
    ws1_col_th2d = 0
    ws1_col_th3d = 1
    ws1_col_th4d = 2
    ws1_col_th5d = 3
    ws1_col_th6d = 4
    ws1_col_thbcd = 5
    ws1_col_fbos = 6
    ws1_col_vel = 7
    ws1_col_acc = 8



    # ws2 data
    ws2_col_th2d_tt = 0
    ws2_col_fbos_tt = 1
    ws2_col_v_tt = 2

    # ws3 data
    ws3_col_fbos_mb = 0
    ws3_col_v_mb = 1
    ws3_col_f_mb = 2

    # ws4 data
    ws4_row_input_data = 0
    ws4_row_a = 1
    ws4_row_b = 2
    ws4_row_c = 3
    ws4_row_d = 4
    ws4_row_e = 5
    ws4_row_f = 6
    ws4_row_g = 7
    ws4_row_h = 8
    ws4_row_thd_bf = 9
    ws4_row_rpm = 10
    ws4_row_pf = 11
    ws4_row_rd = 12
    ws4_row_nr_sus = 13
    ws4_row_root = 14
    ws4_row_rot_dir = 15

    # ws5 data
    ws5_row_output_data = 0
    ws5_row_trq = 1
    ws5_row_v_at_rd = 2
    ws5_row_max_f_rkr_per_sus = 3
    ws5_row_stk = 4
    ws5_row_d_max = 5
    ws5_row_rd_act = 6
    ws5_row_d_pin_eg = 7
    ws5_row_d_be = 8
    ws5_row_od_be_ring = 9
    ws5_row_d_pin_rkr = 10
    ws5_row_l_bush_rkr = 11
    ws5_row_w_rkr = 12
    ws5_row_thk_rkr = 13
    ws5_row_od_ring_rkr = 14
    ws5_row_d_pin_cr = 15
    ws5_row_l_bush_cr = 16
    ws5_row_d_ring_cr = 17
    ws5_row_link_ok_flag = 18
    ws5_row_rkr_ring_ter_intrf_flag = 19
    ws5_row_rkr_link_ter_intrf_flag = 20
    ws5_row_cr_ter_intrf_flag = 21
    ws5_row_th2d_at_rd = 22
    ws5_row_th3d_at_rd = 23
    ws5_row_th4d_at_rd = 24
    ws5_row_th5d_at_rd = 25
    ws5_row_th6d_at_rd = 26

    # ws6 data
    ws6_row_setting = 0
    ws6_row_sc_bush_rkr = 1
    ws6_row_ss_all_eg_pin = 2
    ws6_row_rat_oi_rkr = 3
    ws6_row_rat_wp_rkr = 4
    ws6_row_rat_ld_bush_rkr = 5
    ws6_row_rat_oi_be_ring = 6
    ws6_row_thk_lip_gear = 7
    ws6_row_thk_wall_bush_pin_eg = 8
    ws6_row_mrg_hit = 9
    ws6_row_rat_oi_cr = 10
    ws6_row_sc_bush_cr = 11
    ws6_row_rat_ld_bush_cr = 12

    # w0 data
    ws0.write(ws0_row_general, 0, "GENERAL")
    ws0.write(ws0_row_project_name, 0, "Project")
    ws0.write(ws0_row_designer, 0, "Designer")
    ws0.write(ws0_row_date, 0, "Date")
    ws0.write(ws0_row_note, 0, "Note")

    # ws1 data
    ws1.write(0, ws1_col_th2d, "th2d")
    ws1.write(0, ws1_col_th3d, "th3d")
    ws1.write(0, ws1_col_th4d, "th4d")
    ws1.write(0, ws1_col_th5d, "th5d")
    ws1.write(0, ws1_col_th6d, "th6d")
    ws1.write(0, ws1_col_thbcd, "thdbc")
    ws1.write(0, ws1_col_fbos, "fbos")
    ws1.write(0, ws1_col_vel, "slide_vel")
    ws1.write(0, ws1_col_acc, "slide_acc")

    # ws2 data
    ws2.write(0, ws2_col_th2d_tt, "th2d_tt")
    ws2.write(0, ws2_col_fbos_tt, "fbos_tt")
    ws2.write(0, ws2_col_v_tt, "v_tt")

    # ws3 data
    ws3.write(0, ws3_col_fbos_mb, "fbos_mb")
    ws3.write(0, ws3_col_v_mb, "v_mb")
    ws3.write(0, ws3_col_f_mb, "f_mb")

    # ws4 data
    ws4.write(ws4_row_input_data, 0, "INPUT DATA")
    ws4.write(ws4_row_a, 0, "a (eccentricity)")
    ws4.write(ws4_row_b, 0, "b (ter link uper side)")
    ws4.write(ws4_row_c, 0, "c (rocker link)")
    ws4.write(ws4_row_d, 0, "d (rkr_x)")
    ws4.write(ws4_row_e, 0, "e (rkr_y)")
    ws4.write(ws4_row_f, 0, "f (ternary link vertical length)")
    ws4.write(ws4_row_g, 0, "g (conrod)")
    ws4.write(ws4_row_h, 0, "h (slider_off_x)")
    ws4.write(ws4_row_thd_bf, 0, "ter link angle between link b and f (deg)")
    ws4.write(ws4_row_rpm, 0, "rpm")
    ws4.write(ws4_row_pf, 0, "press force (ton)")
    ws4.write(ws4_row_rd, 0, "rated dist (mm)")
    ws4.write(ws4_row_nr_sus, 0, "Nr of suspensions")
    ws4.write(ws4_row_root, 0, "root option")
    ws4.write(ws4_row_rot_dir, 0, "rotation dir")

    # ws5 data
    ws5.write(ws5_row_output_data, 0, "OUTPUT DATA")
    ws5.write(ws5_row_trq, 0, "total gear axis torque (considering 1 gear for press) (Nm)")
    ws5.write(ws5_row_v_at_rd, 0, "slide vel at RD (mm/s)")
    ws5.write(ws5_row_max_f_rkr_per_sus, 0, "force on each rocker link (ton)")
    ws5.write(ws5_row_stk, 0, "Slide stroke (mm)")
    ws5.write(ws5_row_d_max, 0, "BOS from eg roatating center (mm)")
    ws5.write(ws5_row_rd_act, 0, "Actual RD used in calculation (mm)")
    ws5.write(ws5_row_d_pin_eg, 0, "EG pin dia (mm)")
    ws5.write(ws5_row_d_be, 0, "Big end lobe dia (mm)")
    ws5.write(ws5_row_od_be_ring, 0, "Ter link casted od at big end (mm)")
    ws5.write(ws5_row_d_pin_rkr, 0, "Rocker pin dia (mm)")
    ws5.write(ws5_row_l_bush_rkr, 0, "Rocker bush length in axial dir (mm)")
    ws5.write(ws5_row_w_rkr, 0, "Rocker link width (mm)")
    ws5.write(ws5_row_thk_rkr, 0, "Rocker link thk in axial dir (mm)")
    ws5.write(ws5_row_od_ring_rkr, 0, "Rocker link OD (mm)")
    ws5.write(ws5_row_d_pin_cr, 0, "Conrod pin dia (mm)")
    ws5.write(ws5_row_l_bush_cr, 0, "Conrod bush length in axial dir (mm)")
    ws5.write(ws5_row_d_ring_cr, 0, "Conrod OD (mm)")
    ws5.write(ws5_row_link_ok_flag, 0, "Link not interfering?")
    ws5.write(ws5_row_rkr_ring_ter_intrf_flag, 0, "Rocker OD interf with ter link OD?")
    ws5.write(ws5_row_rkr_link_ter_intrf_flag, 0, "Rocker lik side interf with ter link OD?")
    ws5.write(ws5_row_cr_ter_intrf_flag, 0, "Conrod OD interf with ter link OD?")
    ws5.write(ws5_row_th2d_at_rd, 0, "Crank angle at RD (deg)")
    ws5.write(ws5_row_th3d_at_rd, 0, "th3 at RD (deg)")
    ws5.write(ws5_row_th4d_at_rd, 0, "th4 at RD (deg)")
    ws5.write(ws5_row_th5d_at_rd, 0, "th5 at RD (deg)")
    ws5.write(ws5_row_th6d_at_rd, 0, "th6 at RD (deg)")

    # ws6 data
    ws6.write(ws6_row_setting, 0, "SETTING")
    ws6.write(ws6_row_sc_bush_rkr, 0, "Allowable contact stress in rocker bushes (N/mm2)")
    ws6.write(ws6_row_ss_all_eg_pin, 0, "Allowable contact stress in EG pin (N/mm2)")
    ws6.write(ws6_row_rat_oi_rkr, 0, "OD to ID ratio of rocker bore")
    ws6.write(ws6_row_rat_wp_rkr, 0, "Width to pin dia ratio of rocker pin")
    ws6.write(ws6_row_rat_ld_bush_rkr, 0, "Length to dia ratio of rocker bush")
    ws6.write(ws6_row_rat_oi_be_ring, 0, "OD to ID ratio of ter link big end")
    ws6.write(ws6_row_thk_lip_gear, 0, "Gear lip thk from eg pin bore to lobe on upper side")
    ws6.write(ws6_row_thk_wall_bush_pin_eg, 0, "EG pin bush wall thk (mm)")
    ws6.write(ws6_row_mrg_hit, 0, "Interference margin in link (mm)")
    ws6.write(ws6_row_rat_oi_cr, 0, "OD to ID ratio of conrod bore")
    ws6.write(ws6_row_sc_bush_cr, 0, "Allowable contact stress in conrod bushes (N/mm2)")
    ws6.write(ws6_row_rat_ld_bush_cr, 0, "Length to dia ratio of rocker bush")

    # ws0 data
    ws0.write(ws0_row_project_name, 1, ps_project_name)
    ws0.write(ws0_row_designer, 1, ps_designer)
    ws0.write(ws0_row_date, 1, ps_date)
    ws0.write(ws0_row_note, 1, ps_note)

    # ws1, ws2 data
    for i in range(360):
        # ws1 data
        ws1.write(i+1, ws1_col_th2d, th2d_lst[i])
        ws1.write(i+1, ws1_col_th3d, th3d_lst[i])
        ws1.write(i+1, ws1_col_th4d, th4d_lst[i])
        ws1.write(i+1, ws1_col_th5d, th5d_lst[i])
        ws1.write(i+1, ws1_col_th6d, th6d_lst[i])
        ws1.write(i+1, ws1_col_thbcd, thbcd_lst[i])
        ws1.write(i+1, ws1_col_fbos, fbos_lst[i])
        ws1.write(i+1, ws1_col_vel, v_lst[i])
        ws1.write(i+1, ws1_col_acc, acc_lst[i])

        # ws2 data
        ws2.write(i+1, ws2_col_th2d_tt, th2d_tt360str_lst[i])
        ws2.write(i+1, ws2_col_fbos_tt, fbos_tt_lst[i])
        ws2.write(i+1, ws2_col_v_tt, v_tt_lst[i])

    # ws3 data
    for i in range(len(fbos_mb_lst)):
        ws3.write(i+1, ws3_col_fbos_mb, fbos_mb_lst[i])
        ws3.write(i+1, ws3_col_v_mb, v_mb_lst[i])
        ws3.write(i+1, ws3_col_f_mb, f_mb_lst[i])

    # ws4 data
    ws4.write(ws4_row_a, 1, a)
    ws4.write(ws4_row_b, 1, b)
    ws4.write(ws4_row_c, 1, c)
    ws4.write(ws4_row_d, 1, d)
    ws4.write(ws4_row_e, 1, e)
    ws4.write(ws4_row_f, 1, f)
    ws4.write(ws4_row_g, 1, g)
    ws4.write(ws4_row_h, 1, h)
    ws4.write(ws4_row_thd_bf, 1, thd_bf)
    ws4.write(ws4_row_rpm, 1, rpm)
    ws4.write(ws4_row_pf, 1, pf)
    ws4.write(ws4_row_rd, 1, rd)
    ws4.write(ws4_row_nr_sus, 1, nr_sus)
    ws4.write(ws4_row_root, 1, ROOT_OPTION)
    ws4.write(ws4_row_rot_dir, 1, GEAR_ROT_DIR)


    # ws5 data
    ws5.write(ws5_row_trq, 1, trq)
    ws5.write(ws5_row_v_at_rd, 1, v_at_rd)
    ws5.write(ws5_row_max_f_rkr_per_sus, 1, max_f_rkr_per_sus)
    ws5.write(ws5_row_stk, 1, stk)
    ws5.write(ws5_row_d_max, 1, d_max)
    ws5.write(ws5_row_rd_act, 1, rd_act)
    ws5.write(ws5_row_d_pin_eg, 1, d_pin_eg)
    ws5.write(ws5_row_d_be, 1, d_be)
    ws5.write(ws5_row_od_be_ring, 1, od_be_ring)
    ws5.write(ws5_row_d_pin_rkr, 1, d_pin_rkr)
    ws5.write(ws5_row_l_bush_rkr, 1, l_bush_rkr)
    ws5.write(ws5_row_w_rkr, 1, w_rkr)
    ws5.write(ws5_row_thk_rkr, 1, thk_rkr)
    ws5.write(ws5_row_od_ring_rkr, 1, od_ring_rkr)
    ws5.write(ws5_row_d_pin_cr, 1, d_pin_cr)
    ws5.write(ws5_row_l_bush_cr, 1, l_bush_cr)
    ws5.write(ws5_row_d_ring_cr, 1, d_ring_cr)
    ws5.write(ws5_row_link_ok_flag, 1, link_ok_flag)
    ws5.write(ws5_row_rkr_ring_ter_intrf_flag, 1, rkr_ring_ter_intrf_flag)
    ws5.write(ws5_row_rkr_link_ter_intrf_flag, 1, rkr_link_ter_intrf_flag)
    ws5.write(ws5_row_cr_ter_intrf_flag, 1, cr_ter_intrf_flag)
    ws5.write(ws5_row_th2d_at_rd, 1, th2d_at_rd)
    ws5.write(ws5_row_th3d_at_rd, 1, th3d_at_rd)
    ws5.write(ws5_row_th4d_at_rd, 1, th4d_at_rd)
    ws5.write(ws5_row_th5d_at_rd, 1, th5d_at_rd)
    ws5.write(ws5_row_th6d_at_rd, 1, th6d_at_rd)



    # ws6 data
    ws6.write(ws6_row_sc_bush_rkr, 1, sc_bush_rkr)
    ws6.write(ws6_row_ss_all_eg_pin, 1, ss_all_eg_pin)
    ws6.write(ws6_row_rat_oi_rkr, 1, rat_oi_rkr)
    ws6.write(ws6_row_rat_wp_rkr, 1, rat_wp_rkr)
    ws6.write(ws6_row_rat_ld_bush_rkr, 1, rat_ld_bush_rkr)
    ws6.write(ws6_row_rat_oi_be_ring, 1, rat_oi_be_ring)
    ws6.write(ws6_row_thk_lip_gear, 1, thk_lip_gear)
    ws6.write(ws6_row_thk_wall_bush_pin_eg, 1, thk_wall_bush_pin_eg)
    ws6.write(ws6_row_mrg_hit, 1, mrg_hit)
    ws6.write(ws6_row_rat_oi_cr, 1, rat_oi_cr)
    ws6.write(ws6_row_sc_bush_cr, 1, sc_bush_cr)
    ws6.write(ws6_row_rat_ld_bush_cr, 1, rat_ld_bush_cr)

    workbook.close()
    print("Writing to excel file completed.")

