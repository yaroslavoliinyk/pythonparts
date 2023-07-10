from typing import Optional

import NemAll_Python_Geometry as AllplanGeo    # type: ignore

from ..exceptions import AttributePermissionError


class Coords:

    def __init__(self, start_point: Optional[AllplanGeo.Point3D]=None, end_point: Optional[AllplanGeo.Point3D]=None):
        self.__start_point = start_point
        self.__end_point   = end_point

    @classmethod
    def from_empty(cls):
        return Coords(None, None)

    @property
    def start_point(self):
        return self.__start_point
    
    @start_point.setter
    def start_point(self, p: AllplanGeo.Point3D):
        if not isinstance(p, AllplanGeo.Point3D):
            raise TypeError("start_point should be of type AllplanGeo.Point3D")
        self.__start_point = p
    
    @property
    def end_point(self):
        return self.__end_point

    @end_point.setter
    def end_point(self, p: AllplanGeo.Point3D):
        if not isinstance(p, AllplanGeo.Point3D):
            raise TypeError("end_point should be of type AllplanGeo.Point3D")
        self.__end_point = p

    def move_start_point(self, vec: AllplanGeo.Vector3D):
        if not isinstance(vec, AllplanGeo.Vector3D):
            raise TypeError(f"Wrong type: {vec}.\n You can move point only with AllplanGeo.Vector3D")
        self.start_point = self.start_point + vec

    def move_end_point(self, vec: AllplanGeo.Vector3D):
        if not isinstance(vec, AllplanGeo.Vector3D):
            raise TypeError(f"Wrong type: {vec}.\n You can move point only with AllplanGeo.Vector3D")
        self.end_point = self.end_point + vec

    def move(self, vec: AllplanGeo.Vector3D):
        self.move_start_point(vec)
        self.move_end_point(vec)

    def __eq__(self, other_coords) -> bool:
        return self.start_point == other_coords.start_point and self.end_point == other_coords.end_point

    def __repr__(self):
        return f"Coords(start_point={self.start_point!r}, end_point={self.end_point!r})"

    def __str__(self):
        return repr(self)
