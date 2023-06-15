from typing import List


class Block:

    def __init__(self, x: float, y: float, z: float):
        self._x = x
        self._y = y
        self._z = z
        self.children: List['Block'] = list()

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

    def __str__(self):
        return f"Block with coords ({self.x}, {self.y}, {self.z})"
