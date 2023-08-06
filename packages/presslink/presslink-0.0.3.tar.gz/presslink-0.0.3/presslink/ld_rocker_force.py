import math

class RockerLink:
    """To calculate rocker link force in 6 link drive mechanism used in draw 
    presses

    This script calculates force on rocker in 6 link drive mechanism used in draw 
    presses. It generates list of forces at evergy angle from mid downstroke to BDC

    ...

    Attributes
    ----------
    b : float
        length of link b (horz conrod) in mm
    f : float
        length of link f (ter link vertical side) in mm
    th3d_lst : list
        list of angles in deg of ter link top side b
        index is th2d (gear angle) in deg
        0 deg th2d is +ve X axis
    th4d_lst : list
        list of angles in deg of rocker link c
    th5d_lst : list
        list of angles in deg of ter link vertical side f
    th6d_lst : list
        list of angles in deg of conrod g
    th2d_mb_lst : list
        list of gear angle from down mid stroke to BDC. Index is nothing
    f_mb_lst : list
        list of press force from down mid stroke to BDC. Index is nothing
        Respective th2d can be found in th2d_mb_lst

    Methods
    -------
    get_fc():
        Returns list of rocker force in ton
        force can be of 1 link or all links combined. depends on values of 
        force values contained in f_mb_lst
    """
    def __init__(self, b, f, th3d_lst, th4d_lst, th5d_lst, th6d_lst, th2d_mb_lst, f_mb_lst):
        """
        Parameters
        ----------
        b : float
            length of link b (horz conrod) in mm
        f : float
            length of link f (ter link vertical side) in mm
        th3d_lst : list
            list of angles in deg of ter link top side b
            index is th2d (gear angle) in deg
            0 deg th2d is +ve X axis
        th4d_lst : list
            list of angles in deg of rocker link c
        th5d_lst : list
            list of angles in deg of ter link vertical side f
        th6d_lst : list
            list of angles in deg of conrod g
        th2d_mb_lst : list
            list of gear angle from down mid stroke to BDC. Index is nothing
        f_mb_lst : list
            list of press force from down mid stroke to BDC. Index is nothing
            Respective th2d can be found in th2d_mb_lst
        """

        self.fc_lst = []

        for x in th2d_mb_lst:
            this_th2d = int(x)
            th3d = th3d_lst[this_th2d]
            th4d = th4d_lst[this_th2d]
            th5d = th5d_lst[this_th2d]
            th6d = th6d_lst[this_th2d]
            this_index = th2d_mb_lst.index(x)

            this_pf = f_mb_lst[this_index]

            # print("th3d at RD: ", round(th3d, 3))
            # print("th4d at RD: ", round(th4d, 3))
            # print("th5d at RD: ", round(th5d, 3))
            # print("th6d at RD: ", round(th6d, 3))

            th3 = th3d * math.pi / 180
            th4 = th4d * math.pi / 180
            th5 = th5d * math.pi / 180
            th6 = th6d * math.pi / 180

            fg = this_pf / math.cos(math.pi/2 - th6)
            th65 = (th6 - th5)
            th34 = (th3 - th4)
            fc = f * math.sin(th65) * fg / (b * math.sin(th34))
            self.fc_lst.append(round(fc, 0))

    def get_fc(self):
        """
        Returns
        -------
        list
        Returns list of rocker force in ton
        Force can be of 1 link or all links combined. depends on values of 
        force values contained in f_mb_lst
        """
        return self.fc_lst
