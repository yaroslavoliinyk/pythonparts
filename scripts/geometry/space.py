import math

from abc import ABC
from typing import Optional, List

from .coords import Coords, AllplanGeo
from ..utils import center_calc
from ..exceptions import AttributePermissionError


class Space:
    
    __created_with_classmethod = False


    def __init__(
        self, local: Coords, global_: Coords
    ):
        if not self.__created_with_classmethod:
            raise TypeError("You cannot instatiate this class directly. Use classmethod.")
        if (global_ != Coords.from_empty() and 
            (local.end_point - local.start_point) != 
            (global_.end_point - global_.start_point)):
            raise ValueError(f"Incorrect global or local coordinates!\nlocal={local}\nglobal={global_}")
        self._local  = local
        self._global = global_
        self._children: List[Space] = []
        self._visible               = True
        self._union_parent          = True
        self.__created_with_classmethod = False

    @classmethod
    def from_local_points(cls, start_point, end_point):
        local_coords  = Coords(start_point, end_point)
        global_coords = Coords.from_empty()
        cls.__created_with_classmethod = True
        return cls(local_coords, global_coords)

    @classmethod
    def from_points(cls, local_start_pnt, local_end_pnt, global_start_pnt):
        local_coords = Coords(local_start_pnt, local_end_pnt)
        global_coords = Coords(global_start_pnt, global_start_pnt + (local_end_pnt - local_start_pnt))
        cls.__created_with_classmethod = True
        return cls(local_coords, global_coords)
    
    @property
    def local(self):
        return self._local
    
    @local.setter
    def local(self, value):
        raise AttributePermissionError("You cannot set local coords this way.")
    
    @property
    def global_(self):
        return self._global
    
    @global_.setter
    def global_(self, value):
        raise AttributePermissionError("You cannot set global coords this way.")
    
    def set_global_start_pnt(self, p: AllplanGeo.Point3D):
        self.global_.start_point = p
        self.global_.end_point   = p + (self.local.end_point - self.local.start_point)

    @property
    def length(self):
        return abs(self.local.end_point.Y - self.local.start_point.Y)
    
    @property
    def width(self):
        return abs(self.local.end_point.X - self.local.start_point.X)
    
    @property
    def height(self):
        return abs(self.local.end_point.Z - self.local.start_point.Z)

    def place(self, other_space: "Space",
              left: float=0, right: float=0,
              top: float=0, bottom: float=0,
              front: float=0, back: float=0,
              center: bool=False):
        other_space.set_global_start_pnt(self.global_.start_point)
        if center:
            if (math.isclose(left, 0) and math.isclose(right, 0)):
                left, right = center_calc(self.global_.start_point.X, 
                                            self.global_.end_point.X,
                                            other_space.width)
            if (math.isclose(front, 0) and math.isclose(back, 0)):
                front, back = center_calc(self.global_.start_point.Y, 
                                            self.global_.end_point.Y,
                                            other_space.width)
            if (math.isclose(top, 0) and math.isclose(bottom, 0)):
                top, bottom = center_calc(self.global_.start_point.Z, 
                                            self.global_.end_point.Z,
                                            other_space.width)
        other_space.global_.move(AllplanGeo.Vector3D(left, front, bottom))    
        other_space.global_.move(AllplanGeo.Vector3D(right, back, top).Reverse())
        self._add_child(other_space)

    def _add_child(self, child_space: "Space"):
        self._children.append(child_space)

    def __eq__(self, other):
        return (self.local == other.local
                and self.global_ == other.global_ 
                and self.length == other.length
                and self.width == other.width
                and self.height == other.height
                and self._visible == other._visible
                and self._union_parent == other._union_parent
                and len(self._children) == len(other._children)
                and all(c1 == c2 for c1, c2 in zip(self._children, other._children)))

    def __repr__(self):
        return f"Space({self.local!r}, {self.global_!r})"
