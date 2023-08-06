"""To plot various graphs

This script plots various graphs from incoming lists

This script requires that `numpy` be installed within the Python
environment you are running this script in.

This script requires that `matplotlib` be installed within the Python
environment you are running this script in.

"""

import numpy as np
import matplotlib.pyplot as plt

def get_graphs(th2d_lst, fbos_lst, v_lst, acc_lst, n5_lst, th2d_tt360str_lst, 
	fbos_tt_lst, v_tt_lst, fbos_mb_lst, v_mb_lst, f_mb_lst):
	"""Plots various graphs
	Parameters
	----------
	th2d_lst: list
	    List of gear angle theta2 in deg
	fbos_lst: list
	    List of FBOS in mm
	v_lst: list
	    List of slide velocity in mm/s
	acc_lst: list
	    List of slide acceleration in mm/s2
	n5_lst: list
	    List of crankshaft rpm
	th2d_tt360str_lst: list
	    List of gear angle theta2 in deg starting from TDC and ending at TDC.
	    The values are string type
	fbos_tt_lst: list
	    List of FBOS in mm starting from TDC and ending at TDC.
	v_tt_lst: list
	    List of slide velocity in mm/s starting from TDC and ending at TDC.
	fbos_mb_lst: list
	    List of FBOS in mm starting from downstroke mid and ending at BDC.
	v_mb_lst: list
	    List of slide velocity in mm/s starting from downstroke mid and ending
	    at BDC.
	f_mb_lst: list
	    List of press force in ton starting from downstroke mid and ending
	    at BDC.


	Returns
	-------
	none
	    Plot graphs
	"""

	fig, axs = plt.subplots(2, 4, figsize=(24, 10))
	fig.suptitle('press characteristic curves')
	plt.subplots_adjust(left=None, bottom=None, right=None, top=None,
		wspace=0.4, hspace=0.4)

	graph_00, = axs[0, 0].plot(th2d_lst, fbos_lst, 'tab:red')
	# axs[0, 0].legend(['fbos'], loc="upper right")
	axs[0, 0].grid(visible=None, which='major', axis='both')
	axs[0, 0].title.set_text('raw fbos vs. gear angle')
	axs[0, 0].set_xlabel('gear angle (deg)')
	axs[0, 0].set_ylabel('fbos (mm)')
	axs[0, 0].set_ylim(ymin=0)
	axs[0, 0].text(0.5, 0.5, 'Isgec, India ', transform=axs[0, 0].transAxes,
	    fontsize=30, color='gray', alpha=0.2,
	    ha='center', va='center')

	graph_10, = axs[1, 0].plot(th2d_lst, v_lst, 'tab:red')
	# axs[1, 0].legend(['velocity'], loc="upper right")
	axs[1, 0].grid(visible=None, which='major', axis='both')
	axs[1, 0].title.set_text('raw vel vs. gear angle')
	axs[1, 0].set_xlabel('gear angle (deg)')
	axs[1, 0].set_ylabel('vel (mm/s)')
	# axs[1, 0].set_ylim(ymin=0)
	axs[1, 0].text(0.5, 0.5, 'Isgec, India ', transform=axs[1, 0].transAxes,
	    fontsize=30, color='gray', alpha=0.2,
	    ha='center', va='center')

	graph_01, = axs[0, 1].plot(th2d_tt360str_lst, fbos_tt_lst, 'tab:red')
	# axs[0, 1].legend(['fbos'], loc="upper right")
	# axs[0, 1].grid(visible=None, which='major', axis='both')
	axs[0, 1].grid(visible=None, which='major', axis='both')
	axs[0, 1].title.set_text('fbos vs. gear angle')
	axs[0, 1].set_xlabel('gear angle (deg)')
	axs[0, 1].set_ylabel('fbos (mm)')
	axs[0, 1].set_xticks(np.arange(0, 360, 59.9))
	axs[0, 1].set_ylim(ymin=0)
	axs[0, 1].text(0.5, 0.5, 'Isgec, India ', transform=axs[0, 1].transAxes,
	    fontsize=30, color='gray', alpha=0.2,
	    ha='center', va='center')

	graph_11, = axs[1, 1].plot(th2d_tt360str_lst, v_tt_lst, 'tab:red')
	# axs[1, 1].legend(['vel'], loc="upper right")
	axs[1, 1].grid(visible=None, which='major', axis='both')
	axs[1, 1].title.set_text('vel vs. gear angle')
	axs[1, 1].set_xlabel('gear angle (deg)')
	axs[1, 1].set_ylabel('vel (mm/s)')
	axs[1, 1].set_xticks(np.arange(0, 360, 59.9))
	# axs[1, 1].set_ylim(ymin=0)
	axs[1, 1].text(0.5, 0.5, 'Isgec, India ', transform=axs[1, 1].transAxes,
	    fontsize=30, color='gray', alpha=0.2,
	    ha='center', va='center')

	graph_02, = axs[0, 2].plot(fbos_mb_lst, v_mb_lst, 'tab:red')
	# axs[0, 2].legend(['vel'], loc="upper right")
	axs[0, 2].grid(visible=None, which='major', axis='both')
	axs[0, 2].title.set_text('vel vs. fbos in forming zone')
	axs[0, 2].set_xlabel('fbos (mm)')
	axs[0, 2].set_ylabel('vel (mm/s)')
	axs[0, 2].set_ylim(ymin=0)
	axs[0, 2].text(0.5, 0.5, 'Isgec, India ', transform=axs[0, 2].transAxes,
	    fontsize=30, color='gray', alpha=0.2,
	    ha='center', va='center')

	graph_12, = axs[1, 2].plot(fbos_mb_lst, f_mb_lst, 'tab:red')
	# axs[1, 2].legend(['force'], loc="upper right")
	axs[1, 2].grid(visible=None, which='major', axis='both')
	axs[1, 2].title.set_text('force vs. fbos in forming zone')
	axs[1, 2].set_xlabel('fbos (mm)')
	axs[1, 2].set_ylabel('force (ton)')
	axs[1, 2].set_ylim(ymin=0)
	axs[1, 2].text(0.5, 0.5, 'Isgec, India ', transform=axs[1, 2].transAxes,
	    fontsize=30, color='gray', alpha=0.2,
	    ha='center', va='center')

	graph_03, = axs[0, 3].plot(th2d_lst, acc_lst, 'tab:red')
	# axs[0, 2].legend(['vel'], loc="upper right")
	axs[0, 3].grid(visible=None, which='major', axis='both')
	axs[0, 3].title.set_text('raw acc vs. gear angle')
	axs[0, 3].set_xlabel('gear angle (deg)')
	axs[0, 3].set_ylabel('acc (m/s2)')
	# axs[0, 3].set_ylim(ymin=0)
	axs[0, 3].text(0.5, 0.5, 'Isgec, India ', transform=axs[0, 3].transAxes,
	    fontsize=30, color='gray', alpha=0.2,
	    ha='center', va='center')

	graph_13, = axs[1, 3].plot(th2d_lst, n5_lst, 'tab:red')
	# axs[1, 2].legend(['force'], loc="upper right")
	axs[1, 3].grid(visible=None, which='major', axis='both')
	axs[1, 3].title.set_text('raw crank rpm vs. gear angle')
	axs[1, 3].set_xlabel('gear angle (deg)')
	axs[1, 3].set_ylabel('crank rpm')
	# axs[1, 3].set_ylim(ymin=0)
	axs[1, 3].text(0.5, 0.5, 'Isgec, India ', transform=axs[1, 3].transAxes,
	    fontsize=30, color='gray', alpha=0.2,
	    ha='center', va='center')

	plt.show()
