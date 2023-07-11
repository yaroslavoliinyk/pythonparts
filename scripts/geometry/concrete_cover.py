from collections import defaultdict
from typing import Any


class ConcreteCover:

    __match_args__ = ('left', 'right', 'top', 'bottom', 'front', 'back')


    def __init__(self, sides_dict):
        cls = type(self)
        self._sides = defaultdict.fromkeys(cls.__match_args__, 0.0)
        for name, value in sides_dict.items():
            self.__setattr__(name, value)


    def __setattr__(self, __name: str, __value: Any) -> None:
        cls = type(self)
        if __name in cls.__match_args__:
            self._sides[__name] = __value
            self.__check_opposite_sides()
        else:
            super().__setattr__(__name, __value)

    def __getattr__(self, name):
        cls = type(self)
        if name in cls.__match_args__:
            return self._sides[name]
        raise AttributeError(f"Wrong. Attribute does not exist. Try one of the attributes: {' ,'.join(cls.__match_args__)}")

    def __repr__(self):
        return "ConcreteCover({" + ', '.join([f"{name}={value}" for name, value in self._sides.items() if value > 0]) + "})"

    def __check_opposite_sides(self):
        """
            If both opposite sides defined - it's an Error for now. Because then Length of an object is defined.

            Opposite sides: left and right; top and bottom; front and back
        """
        if ((self.left > 0 and self.right > 0) 
            or (self.top > 0  and self.bottom > 0)
            or (self.front > 0 and self.back > 0)):
            raise ValueError("You cannot have both opposite sides to" 
                             f"be positive at same time:" 
                             f"left={self.left}, right={self.right}"
                             f"top={self.top}, bottom={self.bottom}"
                             f"front={self.front}, back={self.back}")
