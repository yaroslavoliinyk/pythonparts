import math

from abc import ABC
from typing import Optional, List

from .coords import Coords, AllplanGeo
from .concrete_cover import ConcreteCover
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
            (local.end_point - local.start_point) != (global_.end_point - global_.start_point)):
            raise ValueError(f"Incorrect global or local coordinates!\nlocal={local}\nglobal={global_}")
        self._local  = local
        self._global = global_
        self._children: List[Space] = []
        self._visible               = True
        self._union_parent          = True
        self.__created_with_classmethod = False

    @classmethod
    def from_dimensions(cls, length, width, height):
        local_coords  = Coords(AllplanGeo.Point3D(), AllplanGeo.Point3D(width, length, height))
        global_coords = Coords(AllplanGeo.Point3D(), AllplanGeo.Point3D(width, length, height))
        cls.__created_with_classmethod = True
        return cls(local_coords, global_coords)

    @classmethod
    def from_dimensions_global_point(cls, length, width, height, global_start_pnt):
        local_coords = Coords(AllplanGeo.Point3D(), AllplanGeo.Point3D(width, length, height))
        global_coords = Coords(global_start_pnt, global_start_pnt + AllplanGeo.Vector3D(width, length, height))
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
        self.global_.end_point   = self.global_.start_point + AllplanGeo.Vector3D(self.width, self.length, self.height)
    
    def setup_global_coords(self, parent_global_coords: Coords, concov: ConcreteCover):
        pass

    @property
    def length(self):
        return abs(self.local.end_point.Y - self.local.start_point.Y)
    
    @length.setter
    def length(self, value):
        raise AttributePermissionError("You cannot set length of Space.")

    @property
    def width(self):
        return abs(self.local.end_point.X - self.local.start_point.X)
    
    @width.setter
    def width(self, value):
        raise AttributePermissionError("You cannot set width of Space.")

    @property
    def height(self):
        return abs(self.local.end_point.Z - self.local.start_point.Z)

    @height.setter
    def height(self, value):
        raise AttributePermissionError("You cannot set height of Space.")

    def place(self, child_space: "Space",
              center: bool=False, **concov_kwargs
              ):
        """
            Places child Space inside parent Space according to given settings.

            Opposite sides are not allowed to have positive values at same time.
            
            E.g. left and right shifts == 0 and center == True,
            then left and right shifts will be redefined by center_calc.
            Same for top and bottom; front and back.
        """
        concov = ConcreteCover(concov_kwargs)
        if center:
            left, front, bottom = center_calc(concov, self.global_, child_space)
        child_space.setup_global_coords(self.global_, concov)
        self._add_child(child_space)


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
