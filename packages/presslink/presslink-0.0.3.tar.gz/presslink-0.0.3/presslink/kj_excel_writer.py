"""Writing to excel file

This script writes the incoming data into excel file

This script requires that `xlsxwriter` be installed within the Python
environment you are running this script in.

"""

from datetime import datetime
import xlsxwriter


def write_to_excel(ps_project_name, ps_designer, ps_date, ps_note,
    th2d_lst, th3d_lst, th4d_lst, th5d_lst, th6d_lst, thabd_lst, thbcd_lst, fbos_lst, v_lst, acc_lst, n5_lst,
    th2d_tt360str_lst, fbos_tt_lst, v_tt_lst, 
    fbos_mb_lst, v_mb_lst, f_mb_lst,
    a, b, c, d, e, f, g, h, thd_offset_ccw_dir_add, rpm, pf, rd, root_option, gear_rot_dir,
    trq, v_at_rd, fb_max, d_pin, w_frk, d_frk, w_cr_se, w_bush, th4d_max, link_ok_flag, intrf_c_fork_flag, intrf_g_fork_flag,
    stk, drv_mode, d_max, rd_act, th2d_at_rd, th3d_at_rd, th4d_at_rd, th6d_at_rd,
    sc_bush_all, sc_frk_all, st_frk_all, rat_cd_d_frk, fra_rev):
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
    excelFileName = "KnuckleJoint_" + \
    str(pf) + "t@" + \
    str(rd) + "rd_" + \
    str(a) + "ecc_" + \
    "r" + str(root_option) + "_"+ \
    gear_rot_dir + "_"+\
    str(thd_offset_ccw_dir_add) + "d_"+ \
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
    ws1_col_thabd = 5
    ws1_col_thbcd = 6
    ws1_col_fbos = 7
    ws1_col_vel = 8
    ws1_col_acc = 9
    ws1_col_n5 = 10



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
    ws4_row_thd_off = 9
    ws4_row_rpm = 10
    ws4_row_pf = 11
    ws4_row_rd = 12
    ws4_row_root = 13
    ws4_row_rot_dir = 14

    # ws5 data
    ws5_row_output_data = 0
    ws5_row_trq_gear = 1
    ws5_row_vrd = 2
    ws5_row_f_rkr = 3
    ws5_row_d_pin = 4
    ws5_row_w_frk = 5
    ws5_row_d_frk = 6
    ws5_row_w_cr_se = 7
    ws5_row_w_bush = 8
    ws5_row_th4d_max = 9
    ws5_row_link_ok_flag = 10
    ws5_row_intrf_c_fork_flag = 11
    ws5_row_intrf_g_fork_flag = 12
    ws5_row_stk = 13
    ws5_row_drv_mode = 14
    ws5_row_d_max = 15
    ws5_row_rd_act = 16
    ws5_row_th2d_at_rd = 17
    ws5_row_th3d_at_rd = 18
    ws5_row_th4d_at_rd = 19
    ws5_row_th6d_at_rd = 20

    # ws6 data
    ws6_row_setting = 0
    ws6_row_sc_bush_all = 1
    ws6_row_sc_frk_all = 2
    ws6_row_st_frk_all = 3
    ws6_row_rat_cd_d_frk = 4
    ws6_row_fra_rev = 5

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
    ws1.write(0, ws1_col_thabd, "thabd")
    ws1.write(0, ws1_col_thbcd, "thbcd")
    ws1.write(0, ws1_col_fbos, "fbos")
    ws1.write(0, ws1_col_vel, "slide_vel")
    ws1.write(0, ws1_col_acc, "slide_acc")
    ws1.write(0, ws1_col_n5, "crank_rpm")



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
    ws4.write(ws4_row_b, 0, "b (conrod horizontal)")
    ws4.write(ws4_row_c, 0, "c (upper rocker link)")
    ws4.write(ws4_row_d, 0, "d (cs_x)")
    ws4.write(ws4_row_e, 0, "e (cs_y)")
    ws4.write(ws4_row_f, 0, "f (=c, upper rocker link length)")
    ws4.write(ws4_row_g, 0, "g (main conrod)")
    ws4.write(ws4_row_h, 0, "h (slider_off_x)")
    ws4.write(ws4_row_thd_off, 0, "crank_offset_ccw")
    ws4.write(ws4_row_rpm, 0, "rpm")
    ws4.write(ws4_row_pf, 0, "press force (ton)")
    ws4.write(ws4_row_rd, 0, "rated dist (mm)")
    ws4.write(ws4_row_root, 0, "root option")
    ws4.write(ws4_row_rot_dir, 0, "rotation dir")

    # ws5 data
    ws5.write(ws5_row_output_data, 0, "OUTPUT DATA")
    ws5.write(ws5_row_trq_gear, 0, "gear torque (Nm)")
    ws5.write(ws5_row_vrd, 0, "slide vel at RD (mm/s)")
    ws5.write(ws5_row_f_rkr, 0, "conrod force (ton)")
    ws5.write(ws5_row_d_pin, 0, "dia of pin (mm)")
    ws5.write(ws5_row_w_frk, 0, "each fork width (mm)")
    ws5.write(ws5_row_d_frk, 0, "fork dia (OD) (mm)")
    ws5.write(ws5_row_w_cr_se, 0, "conrod small end width total (mm)")
    ws5.write(ws5_row_w_bush, 0, "main bush width (mm)")
    ws5.write(ws5_row_th4d_max, 0, "max rocker angle from Y axis (deg)")
    ws5.write(ws5_row_link_ok_flag, 0, "Link not interfering?")
    ws5.write(ws5_row_intrf_c_fork_flag, 0, "Link c interference with fork?")
    ws5.write(ws5_row_intrf_g_fork_flag, 0, "Link g interference with fork?")
    ws5.write(ws5_row_stk, 0, "Slide stroke (mm)")
    ws5.write(ws5_row_drv_mode, 0, "Drive mode")
    ws5.write(ws5_row_d_max, 0, "BOS point from top rocker link center")
    ws5.write(ws5_row_rd_act, 0, "Actual rated dist used in calculations (mm)")
    ws5.write(ws5_row_th2d_at_rd, 0, "Crank angle at RD (deg)")
    ws5.write(ws5_row_th3d_at_rd, 0, "th3 at RD (deg)")
    ws5.write(ws5_row_th4d_at_rd, 0, "th4 at RD (deg)")
    ws5.write(ws5_row_th6d_at_rd, 0, "th6 at RD (deg)")

    # ws6 data
    ws6.write(ws6_row_setting, 0, "SETTING")
    ws6.write(ws6_row_sc_bush_all, 0, "allowable contact stress in main bushes (N/mm2)")
    ws6.write(ws6_row_sc_frk_all, 0, "allowable contact stress in steel fork (N/mm2)")
    ws6.write(ws6_row_st_frk_all, 0, "allowable tensile stress in steel (N/mm2)")
    ws6.write(ws6_row_rat_cd_d_frk, 0, "min ratio of link center distance to fork dia (link od)")
    ws6.write(ws6_row_fra_rev, 0, "reverse load as a fraction of main rated force")

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
        ws1.write(i+1, ws1_col_thabd, thabd_lst[i])
        ws1.write(i+1, ws1_col_thbcd, thbcd_lst[i])
        ws1.write(i+1, ws1_col_fbos, fbos_lst[i])
        ws1.write(i+1, ws1_col_vel, v_lst[i])
        ws1.write(i+1, ws1_col_acc, acc_lst[i])
        ws1.write(i+1, ws1_col_n5, n5_lst[i])



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
    ws4.write(ws4_row_thd_off, 1, thd_offset_ccw_dir_add)
    ws4.write(ws4_row_rpm, 1, rpm)
    ws4.write(ws4_row_pf, 1, pf)
    ws4.write(ws4_row_rd, 1, rd)
    ws4.write(ws4_row_root, 1, root_option)
    ws4.write(ws4_row_rot_dir, 1, gear_rot_dir)

    # ws5 data
    ws5.write(ws5_row_trq_gear, 1, trq)
    ws5.write(ws5_row_vrd, 1, v_at_rd)
    ws5.write(ws5_row_f_rkr, 1, fb_max)
    ws5.write(ws5_row_d_pin, 1, d_pin)
    ws5.write(ws5_row_w_frk, 1, w_frk)
    ws5.write(ws5_row_d_frk, 1, d_frk)
    ws5.write(ws5_row_w_cr_se, 1, w_cr_se)
    ws5.write(ws5_row_w_bush, 1, w_bush)
    ws5.write(ws5_row_th4d_max, 1, th4d_max)
    ws5.write(ws5_row_link_ok_flag, 1, link_ok_flag)
    ws5.write(ws5_row_intrf_c_fork_flag, 1, intrf_c_fork_flag)
    ws5.write(ws5_row_intrf_g_fork_flag, 1, intrf_g_fork_flag)
    ws5.write(ws5_row_stk, 1, stk)
    ws5.write(ws5_row_drv_mode, 1, drv_mode)
    ws5.write(ws5_row_d_max, 1, d_max)
    ws5.write(ws5_row_rd_act, 1, rd_act)
    ws5.write(ws5_row_th2d_at_rd, 1, th2d_at_rd)
    ws5.write(ws5_row_th3d_at_rd, 1, th3d_at_rd)
    ws5.write(ws5_row_th4d_at_rd, 1, th4d_at_rd)
    ws5.write(ws5_row_th6d_at_rd, 1, th6d_at_rd)

    # ws6 data
    ws6.write(ws6_row_sc_bush_all, 1, sc_bush_all)
    ws6.write(ws6_row_sc_frk_all, 1, sc_frk_all)
    ws6.write(ws6_row_st_frk_all, 1, st_frk_all)
    ws6.write(ws6_row_rat_cd_d_frk, 1, rat_cd_d_frk)
    ws6.write(ws6_row_fra_rev, 1, fra_rev)

    workbook.close()
    print("Writing to excel file completed.")

