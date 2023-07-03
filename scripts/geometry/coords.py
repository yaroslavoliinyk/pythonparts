from typing import Optional

import NemAll_Python_Geometry as AllplanGeo    # type: ignore


class Coords:

    def __init__(self, start_point: Optional[AllplanGeo.Point3D]=None, end_point: Optional[AllplanGeo.Point3D]=None):
        if start_point is not None:
            self.__start_point = start_point
        if end_point is not None:
            self.__end_point   = end_point

    @property
    def start_point(self):
        return self.__start_point
    
    @start_point.setter
    def start_point(self, p: AllplanGeo.Point3D):
        self.__start_point = AllplanGeo.Point3D(p)
    
    @property
    def end_point(self):
        return self.__end_point
    
    @end_point.setter
    def end_point(self, p: AllplanGeo.Point3D):
        self.__end_point = AllplanGeo.Point3D(p)
    
    def __repr__(self):
        return f"Coords(start_point={self.start_point!r}, end_point={self.end_point!r})"

    def __str__(self):
        return repr(self)
