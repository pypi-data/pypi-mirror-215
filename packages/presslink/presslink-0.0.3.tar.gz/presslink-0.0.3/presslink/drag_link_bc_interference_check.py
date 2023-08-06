import math
class Interference:
	"""
    A class to check the interference of a pivot link from a circular object 
    placed at a distance apart from pivot point
    ...
    
    Attributes
    ----------
    r : float
        radius of circle. assume circle is placed at origin of coordinate 
        system
    c : float
        distance of link pivot center from origin
    th_deg : float
        minimum angle between x axis and link measured from -X axis
    w : float
        width of link perpendicular to bore axis and perpendicular to line 
        joining 2 bore of link
    

    Methods
    -------
    distance():
        Returns the minimum gap between link edge and circle
    """
	def __init__(self, r, c, th_deg, w):
		"""
        Parameters
        ----------
        r : float
            radius of circle. assume circle is placed at origin of coordinate 
            system
        c : float
            distance of link pivot center from origin
        th_deg : float
            minimum angle between x axis and link measured from -X axis
        w : float
            width of link perpendicular to bore axis and perpendicular to line 
            joining 2 bore of link
        """
		th = th_deg * math.pi / 180
		self.d = (c * math.sin(th) - w / 2) - r
	
	def distance(self):
		"""Gives the distance between circle and link edges

        If the return value in negative, link is interfering with circle

        Parameters
        ----------

        Returns
        -------
        float
            minimum gap between link and circle placed at origin
        """
		return self.d

# program check
# obj = Interference(15, 36.67, 35, 20)
# d = obj.distance()
# print(d)