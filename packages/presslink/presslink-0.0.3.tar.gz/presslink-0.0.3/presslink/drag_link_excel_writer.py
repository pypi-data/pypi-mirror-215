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
    a, b, c, d, e, f, g, h, thd_offset_ccw_dir_add, rpm, pf, rd, root_option, gear_rot_dir, solid_shaft_flag, integral_crank_connector_flag, nr_sus,
    trq, v_at_rd, fb_max, th2d_at_fb_max, fb_at_rd, ds_trq_unit_out, dp_rkr, w_bush_rkr, d_cs, w_rkr, thk_rkr, gear_bore_dia, bush_v_gear, d_in_clr_gear, 
    cc_arm_thk, w_bush_d_s, w_bush_gear, w_gear_body, w_trq_unit, len_d_s, wt_rkr, wt_pin_rkr, wt_cc, wt_ecc_sup, wt_gear_body, 
    wt_bush_rkr, wt_bush_d_s, wt_bush_gear, bore_in_bore, rkr_cc_hit, high_vel, rd_act, trq_cs,
    sc, se, sy, kf, kfs, fos, v_max_all_bush_gear, cc_mid_cut_fact):
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
    excelFileName = "DragLink_" + \
    str(pf) + "t@" + \
    str(round(rd, 1)) + "rd_" + \
    str(int(f)) + "ecc_" + \
    "r" + str(root_option) + "_"+ \
    str(nr_sus) + "sus_" + \
    "TU" + str(trq_cs) + "_" + \
    gear_rot_dir + "_" + \
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
    ws4_row_solid_out_shaft = 15
    ws4_row_integral_cc = 16
    ws4_row_nr_sus = 17


    # ws5 data
    ws5_row_output_data = 0
    ws5_row_trq_gear = 1
    ws5_row_vrd = 2
    ws5_row_f_rkr = 3
    ws5_row_th2d_at_fb_max = 4
    ws5_row_f_rkr_rd = 5
    ws5_row_d_s_out = 6
    ws5_row_d_p_rkr = 7
    ws5_row_w_bush_rkr = 8
    ws5_row_d_cs = 9
    ws5_row_w_rkr = 10
    ws5_row_thk_rkr = 11
    ws5_row_bore_gear = 12
    ws5_row_v_bush_gear = 13
    ws5_row_d_clr_gear = 14

    ws5_row_cc_arm_thk = 15
    ws5_row_w_bush_d_s = 16
    ws5_row_w_bush_gear = 17
    ws5_row_w_gear_body = 18
    ws5_row_w_trq_unit = 19
    ws5_row_len_d_s = 20
    ws5_row_wt_rkr = 21
    ws5_row_wt_pin_rkr = 22
    ws5_row_wt_cc = 23
    ws5_row_wt_ecc_sup = 24
    ws5_row_wt_gear_body = 25
    ws5_row_wt_bush_rkr = 26
    ws5_row_wt_bush_d_s = 27
    ws5_row_wt_bush_gear = 28

    ws5_row_bore_in_bore_flag = 29
    ws5_row_rkr_cc_hit_flag = 30
    ws5_row_high_vel_flag = 31
    ws5_row_rd_act = 32
    ws5_row_trq_cs = 33

    

    # ws6 data
    ws6_row_setting = 0
    ws6_row_sc = 1
    ws6_row_se = 2
    ws6_row_sy = 3
    ws6_row_kf = 4
    ws6_row_kfs = 5
    ws6_row_fos = 6
    ws6_row_v_max = 7
    ws6_row_mid_cut_fact = 8

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
    ws4.write(ws4_row_a, 0, "a (gear link)")
    ws4.write(ws4_row_b, 0, "b (rocker)")
    ws4.write(ws4_row_c, 0, "c (crank_connector)")
    ws4.write(ws4_row_d, 0, "d (cs_x)")
    ws4.write(ws4_row_e, 0, "e (cs_y)")
    ws4.write(ws4_row_f, 0, "f (ecc)")
    ws4.write(ws4_row_g, 0, "g (conrod)")
    ws4.write(ws4_row_h, 0, "h (slider_off_x)")
    ws4.write(ws4_row_thd_off, 0, "crank_offset_ccw")
    ws4.write(ws4_row_rpm, 0, "rpm")
    ws4.write(ws4_row_pf, 0, "press force (ton)")
    ws4.write(ws4_row_rd, 0, "rated dist (mm)")
    ws4.write(ws4_row_root, 0, "root option")
    ws4.write(ws4_row_rot_dir, 0, "rotation dir")
    ws4.write(ws4_row_solid_out_shaft, 0, "solid output shaft")
    ws4.write(ws4_row_integral_cc, 0, "integral crank connector")
    ws4.write(ws4_row_nr_sus, 0, "no of suspension")


    # ws5 data
    ws5.write(ws5_row_output_data, 0, "OUTPUT DATA")
    ws5.write(ws5_row_trq_gear, 0, "gear torque (Nm)")
    ws5.write(ws5_row_vrd, 0, "slide vel at RD (mm/s)")
    ws5.write(ws5_row_f_rkr, 0, "max rocker force in cycle (ton) [considered in calculations]")
    ws5.write(ws5_row_th2d_at_fb_max, 0, "raw CA at max rocker force in cycle (deg)")
    ws5.write(ws5_row_f_rkr_rd, 0, "rocker force at rd (ton) [not considered in calculations]")
    ws5.write(ws5_row_d_s_out, 0, "dia of torque unit out shaft (mm)")
    ws5.write(ws5_row_d_p_rkr, 0, "dia of rocker pin (mm)")
    ws5.write(ws5_row_w_bush_rkr, 0, "width of rocker bush (mm)")
    ws5.write(ws5_row_d_cs, 0, "dia of crank shaft (mm)")
    ws5.write(ws5_row_w_rkr, 0, "width of rocker (mm)")
    ws5.write(ws5_row_thk_rkr, 0, "thickness of rocker (mm)")
    ws5.write(ws5_row_bore_gear, 0, "bore dia of gear (mm)")
    ws5.write(ws5_row_v_bush_gear, 0, "rubbing vel of gear bush  (mm/s)")
    ws5.write(ws5_row_d_clr_gear, 0, "inside clear dia of gear (mm)")
    ws5.write(ws5_row_cc_arm_thk , 0, "crank connector arm thk (mm)")
    ws5.write(ws5_row_w_bush_d_s , 0, "torque unit out shaft bush width (mm)")
    ws5.write(ws5_row_w_bush_gear , 0, "main gear bush width (mm)")
    ws5.write(ws5_row_w_gear_body , 0, "main gear body width (mm)")
    ws5.write(ws5_row_w_trq_unit , 0, "torque unit housing fab width (mm)")
    ws5.write(ws5_row_len_d_s , 0, "out shaft total LR length (mm)")
    ws5.write(ws5_row_wt_rkr , 0, "rocker link weight (kg)")
    ws5.write(ws5_row_wt_pin_rkr , 0, "rocker pin weight (kg)")
    ws5.write(ws5_row_wt_cc , 0, "crank connector weight (kg)")
    ws5.write(ws5_row_wt_ecc_sup , 0, "eccentric support weight (kg)")
    ws5.write(ws5_row_wt_gear_body , 0, "gear body weight (excluding rim) (kg)")
    ws5.write(ws5_row_wt_bush_rkr , 0, "rocker bush weight (kg)")
    ws5.write(ws5_row_wt_bush_d_s , 0, "outshaft bush weight  (kg)")
    ws5.write(ws5_row_wt_bush_gear , 0, "gear bush weight (kg)")
    ws5.write(ws5_row_bore_in_bore_flag, 0, "bore mearging?")
    ws5.write(ws5_row_rkr_cc_hit_flag, 0, "rocker hitting crank connector?")
    ws5.write(ws5_row_high_vel_flag, 0, "gear bush vel too high?")
    ws5.write(ws5_row_rd_act, 0, "Actual rated dist used in calculations (mm)")
    ws5.write(ws5_row_trq_cs, 0, "Total crankshaft torque (kNm)")



    # ws6 data
    ws6.write(ws6_row_setting, 0, "SETTING")
    ws6.write(ws6_row_sc, 0, "allowable contact stress in rocker bush (N/mm2)")
    ws6.write(ws6_row_se, 0, "shaft endurance (N/mm2)")
    ws6.write(ws6_row_sy, 0, "shaft yield (N/mm2)")
    ws6.write(ws6_row_kf, 0, "scf bending")
    ws6.write(ws6_row_kfs, 0, "scf torsion")
    ws6.write(ws6_row_fos, 0, "shaft fos")
    ws6.write(ws6_row_v_max, 0, "allowable bush rubbing speed (mm/s)")
    ws6.write(ws6_row_mid_cut_fact, 0, "percentage dia cut in crank connector center")

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
    ws4.write(ws4_row_solid_out_shaft, 1, solid_shaft_flag)
    ws4.write(ws4_row_integral_cc, 1, integral_crank_connector_flag)
    ws4.write(ws4_row_nr_sus, 1, nr_sus)

    # ws5 data
    ws5.write(ws5_row_trq_gear, 1, trq)
    ws5.write(ws5_row_vrd, 1, v_at_rd)
    ws5.write(ws5_row_f_rkr, 1, fb_max)
    ws5.write(ws5_row_th2d_at_fb_max, 1, th2d_at_fb_max)
    ws5.write(ws5_row_f_rkr_rd, 1, fb_at_rd)
    ws5.write(ws5_row_d_s_out, 1, ds_trq_unit_out)
    ws5.write(ws5_row_d_p_rkr, 1, dp_rkr)
    ws5.write(ws5_row_w_bush_rkr, 1, w_bush_rkr)
    ws5.write(ws5_row_d_cs, 1, d_cs)
    ws5.write(ws5_row_w_rkr, 1, w_rkr)
    ws5.write(ws5_row_thk_rkr, 1, thk_rkr)
    ws5.write(ws5_row_bore_gear, 1, gear_bore_dia)
    ws5.write(ws5_row_v_bush_gear, 1, bush_v_gear)
    ws5.write(ws5_row_d_clr_gear, 1, d_in_clr_gear)
    ws5.write(ws5_row_cc_arm_thk, 1, cc_arm_thk)
    ws5.write(ws5_row_w_bush_d_s, 1, w_bush_d_s)
    ws5.write(ws5_row_w_bush_gear, 1, w_bush_gear)
    ws5.write(ws5_row_w_gear_body, 1, w_gear_body)
    ws5.write(ws5_row_w_trq_unit, 1, w_trq_unit)
    ws5.write(ws5_row_len_d_s, 1, len_d_s)
    ws5.write(ws5_row_wt_rkr, 1, wt_rkr)
    ws5.write(ws5_row_wt_pin_rkr, 1, wt_pin_rkr)
    ws5.write(ws5_row_wt_cc, 1, wt_cc)
    ws5.write(ws5_row_wt_ecc_sup, 1, wt_ecc_sup)
    ws5.write(ws5_row_wt_gear_body, 1, wt_gear_body)
    ws5.write(ws5_row_wt_bush_rkr, 1, wt_bush_rkr)
    ws5.write(ws5_row_wt_bush_d_s, 1, wt_bush_d_s)
    ws5.write(ws5_row_wt_bush_gear, 1, wt_bush_gear)
    ws5.write(ws5_row_bore_in_bore_flag, 1, bore_in_bore)
    ws5.write(ws5_row_rkr_cc_hit_flag, 1, rkr_cc_hit)
    ws5.write(ws5_row_high_vel_flag, 1, high_vel)
    ws5.write(ws5_row_rd_act, 1, rd_act)
    ws5.write(ws5_row_trq_cs, 1, trq_cs)

    
    
    # ws6 data
    ws6.write(ws6_row_sc, 1, sc)
    ws6.write(ws6_row_se, 1, se)
    ws6.write(ws6_row_sy, 1, sy)
    ws6.write(ws6_row_kf, 1, kf)
    ws6.write(ws6_row_kfs, 1, kfs)
    ws6.write(ws6_row_fos, 1, fos)
    ws6.write(ws6_row_v_max, 1, v_max_all_bush_gear)
    ws6.write(ws6_row_mid_cut_fact, 1, cc_mid_cut_fact)

    workbook.close()
    print("Writing to excel file completed.")
