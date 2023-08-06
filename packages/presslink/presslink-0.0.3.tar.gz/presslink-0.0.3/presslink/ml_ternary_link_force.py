import math

class TernaryLink:
    """To calculate link forces and angles at RD in may link presses

    This script calculates force on ter link, rocker link, conrod. It also
    calculates angles between ter-conrod and ter-rocker link

    ...

    Attributes
    ----------
    a : float
        eccentricity in mm
    b : float
        ternary link big end to rocker center distance in mm
    c : float
        rocker link in mm
    d : float
        x location in mm of rocker center of rotation 
        (+ for Q1 and Q4, - for Q2 and Q3)
    e : float
        y location in mm of rocker center of rotation 
        (+ for Q1 and Q2, - for Q3 and Q4)
    f : float
        ternary link vertical side in mm
    g : float
        conrod in mm
    pf : float
        press firce in ton
    rd : float
        rated dist in mm
    th2d_lst : list
        list of input angle th2 in deg
    th2d_at_rd : int
        th2 at RD in deg
    th3d_lst : list
        list of angle of ter horz link b in deg
    th4d_lst : list
        list of angle of rocker link c in deg
    th6d_lst : list
        list of angle of conrod g in deg
    fbos_lst : list
        list of fbos in mm. Index is th2d. 0 deg is +ve X axis
    thd_bf : float
        angle in deg between ternary vertical link f with upper horizontal 
        link b

    Methods
    -------
    get_fc():
        rocker force at RD in ton
    get_fg():
        conrod force at RD in ton
    get_fa():
        crankshaft force at RD in ton
    get_j():
        bottom horz link j length of ter link in mm
    get_thd_j():
        angle of link j at RD in deg
    get_thd_cb():
        angle between link b and c at RD in deg
    get_thd_bj():
        fixed angle between link b and j in deg
    get_thd_jg():
        angle between link j and g at RD in deg
    get_thd_a():
        angle of link a at RD in deg
    """
    def __init__(self, a, b, c, d, e, f, g, pf, rd, th2d_lst, th2d_at_rd, 
        th3d_lst, th4d_lst, th6d_lst, fbos_lst, thd_bf):
        """
        Parameters
        ----------
        a : float
            eccentricity in mm
        b : float
            ternary link big end to rocker center distance in mm
        c : float
            rocker link in mm
        d : float
            x location in mm of rocker center of rotation 
            (+ for Q1 and Q4, - for Q2 and Q3)
        e : float
            y location in mm of rocker center of rotation 
            (+ for Q1 and Q2, - for Q3 and Q4)
        f : float
            ternary link vertical side in mm
        g : float
            conrod in mm
        pf : float
            press firce in ton
        rd : float
            rated dist in mm
        th2d_lst : list
            list of input angle th2 in deg
        th2d_at_rd : int
            gear angle th2 at RD in deg. 0 is +ve x axis
        th3d_lst : list
            list of angle of ter horz link b in deg
        th4d_lst : list
            list of angle of rocker link c in deg
        th6d_lst : list
            list of angle of conrod g in deg
        fbos_lst : list
            list of fbos in mm. Index is th2d. 0 deg is +ve X axis
        thd_bf : float
            angle in deg between ternary vertical link f with upper horizontal 
            link b
        """
        th3d = th3d_lst[th2d_at_rd]
        th4d = th4d_lst[th2d_at_rd]
        th6d = th6d_lst[th2d_at_rd]
        # print("th3d at RD: ", round(th3d,3))
        # print("th4d at RD: ", round(th4d,3))
        # print("th6d at RD: ", round(th6d,3))

        th_bf = thd_bf * math.pi / 180
        th3 = th3d * math.pi / 180
        th4 = th4d * math.pi / 180
        th6 = th6d * math.pi / 180

        self.j = math.sqrt(f**2+b**2-2*b*f*math.cos(th_bf))  # ter link 3rd side
        # print("ter link 3rd side j: ", self.j)

        self.thd_cb = abs(th4d - th3d)  # angle bw c and b link
        th_cb = self.thd_cb * math.pi / 180

        th_bj = abs(math.asin((f/self.j)*math.sin(th_bf)))
        self.thd_bj = th_bj * 180 / math.pi
        # print("thbj deg", self.thd_bj)
        # if condition is used to detect relative positioning of vector j
        if d > 0:
            th7 = th3 - th_bj  # angle of side j of ter link
        else:
            th7 = th3 + th_bj  # angle of side j of ter link
        
        self.th7d = th7 * 180 / math.pi
        # print("th7 angle of link j: ", self.th7d)

        th_jg = th7 - th6  # angle bw j and g link
        self.thd_jg = th_jg * 180 / math.pi

        self.fg = abs(pf / math.cos(math.pi/2 - th6))  # force on link g
        # print("th6 at RD", th6d)
        # print("self.fg", self.fg)

        self.fc = abs(self.fg * math.sin(th_jg) * self.j / (math.sin(th_cb) * b))  # force on link c
        self.fa = math.sqrt(self.fc**2+self.fg**2+2*self.fc*self.fg*math.cos(th4-th6))

        # self.tha = math.asin((-self.fc * math.sin(th4) - self.fg * math.sin(th6)) / self.fa)
        # self.thad = self.tha * 180 / math.pi
        # print("thad: ", self.thad)

        tha = math.acos((-self.fc * math.cos(th4) - self.fg * math.cos(th6)) / self.fa)
        self.thd_a = tha * 180 / math.pi  # angle of conrod force from pos x axis
        # print("thd_a: ", self.thd_a)  



    def get_fc(self):
        """
        Returns
        -------
        float
        rocker force at RD in ton
        """
        return round(self.fc, 0)

    def get_fg(self):
        """
        Returns
        -------
        float
        conrod force at RD in ton
        """
        return round(self.fg, 0)

    def get_fa(self):
        """
        Returns
        -------
        float
        crankshaft force at RD in ton
        """
        return round(self.fa, 0)

    def get_j(self):
        """
        Returns
        -------
        float
        bottom horz link j length of ter link in mm
        """
        return round(self.j, 3)

    def get_thd_j(self):
        """
        Returns
        -------
        float
        angle of link j at RD in deg
        """
        return round(self.th7d, 1)

    def get_thd_cb(self):
        """
        Returns
        -------
        float
        angle between link b and c at RD in deg
        """
        return round(self.thd_cb, 1)

    def get_thd_bj(self):
        """
        Returns
        -------
        float
        fixed angle between link b and j in deg
        """
        return round(self.thd_bj, 1)

    def get_thd_jg(self):
        """
        Returns
        -------
        float
        angle between link j and g at RD in deg
        """
        return round(self.thd_jg, 1)

    def get_thd_a(self):
        """
        Returns
        -------
        float
        angle of link a at RD in deg
        """
        return round(self.thd_a, 1)
