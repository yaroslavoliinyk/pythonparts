import abc

from typing import List

from ..utils.point import Point3D


class Block:

    def __init__(self, x: float, y: float, z: float):
        self._x = x
        self._y = y
        self._z = z
        self.children: List['Block'] = list()
        self.reference_point: Point3D = Point3D(0, 0, 0)

    @property
    def x(self) -> float:
        return self._x

    @property
    def y(self) -> float:
        return self._y
    
    @property
    def z(self) -> float:
        return self._z

    def add_child(self, child_block: 'Block'):
        pass

    def __repr__(self):
        return f"Block({self.x!r}, {self.y!r}, {self.z!r})"

    def __str__(self):
        return f"Block with coords ({self.x}, {self.y}, {self.z})"
