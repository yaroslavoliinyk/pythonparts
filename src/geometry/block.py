from typing import List


class Block:

    def __init__(self, x: float, y: float, z: float):
        self._x = x
        self._y = y
        self._z = z
        self.children: List[Block] = list()

    def add_child(self):
        pass