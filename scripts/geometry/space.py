import math

from abc import ABC
from typing import Optional, List

from .coords import Coords, SpaceCoords, AllplanGeo
from ..utils import center_calc


class Space:
    
    def __init__(
        self, space_coords: Optional[SpaceCoords]=None
    ):
        self._coords                = space_coords
        self._children: List[Space] = []
        self._visible               = True
        self._union_parent          = True

    @property
    def coords(self):
        return self._coords

    @property
    def length(self):
        return abs(self.coords.local.end_point.Y - self.coords.local.start_point.Y)
    
    @property
    def width(self):
        return abs(self.coords.local.end_point.X - self.coords.local.start_point.X)
    
    @property
    def height(self):
        return abs(self.coords.local.end_point.Z - self.coords.local.start_point.Z)

    def place(self, other_space: "Space",
              left: float=0, right: float=0,
              top: float=0, bottom: float=0,
              front: float=0, back: float=0,
              center: bool=False):
        other_space.coords.set_global_start_pnt(self.coords.global_.start_point)
        if center:
            if (math.isclose(left, 0) and math.isclose(right, 0)):
                left, right = center_calc(self.coords.global_.start_point.X, 
                                            self.coords.global_.end_point.X,
                                            other_space.width)
            if (math.isclose(front, 0) and math.isclose(back, 0)):
                front, back = center_calc(self.coords.global_.start_point.Y, 
                                            self.coords.global_.end_point.Y,
                                            other_space.width)
            if (math.isclose(top, 0) and math.isclose(bottom, 0)):
                top, bottom = center_calc(self.coords.global_.start_point.Z, 
                                            self.coords.global_.end_point.Z,
                                            other_space.width)
        other_space.coords.global_.move(AllplanGeo.Vector3D(left, front, bottom))    
        other_space.coords.global_.move(AllplanGeo.Vector3D(right, back, top).Reverse())
        self._add_child(other_space)

    def _add_child(self, child_space: "Space"):
        self._children.append(child_space)

    def __eq__(self, other):
        return (self.coords == other.coords 
                and self.length == other.length
                and self.width == other.width
                and self.height == other.height
                and self._visible == other._visible
                and self._union_parent == other._union_parent
                and len(self._children) == len(other._children)
                and all(c1 == c2 for c1, c2 in zip(self._children, other._children)))

    def __repr__(self):
        return f"Space({self.coords!r})"
