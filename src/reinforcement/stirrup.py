from typing import List

import NemAll_Python_Geometry as AllplanGeo



class Stirrups:

    class Shape:

        def __init__(self):
            self.points: List[AllplanGeo.Point2D] = []

        def add_point(self, point: AllplanGeo.Point2D):
            self.points.append(point)

    def __init__(self):
        pass