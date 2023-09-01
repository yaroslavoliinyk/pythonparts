from collections import defaultdict
from typing import Any


# The `ConcreteCover` class represents a concrete cover with sides defined by the `left`, `right`,
# `top`, `bottom`, `front`, and `back` attributes, and provides methods for updating and accessing
# these attributes.
class ConcreteCover:

    __match_args__ = ('left', 'right', 'top', 'bottom', 'front', 'back')


    def __init__(self, sides_dict=None):
        """
        The function initializes an object with a dictionary of sides and their values.
        
        :param sides_dict: The `sides_dict` parameter is a dictionary that contains the sides of an
        object. The keys of the dictionary represent the names of the sides, and the values represent
        the lengths of the sides
        """
        cls = type(self)
        self._sides = defaultdict.fromkeys(cls.__match_args__, None)
        if sides_dict is not None:
            self.update(sides_dict)

    @classmethod
    def from_sides(cls, **sides):
        """
        The above function is a class method that creates an instance of the class using the provided
        sides as arguments.
        
        :param cls: cls is a reference to the class itself. It is used to create a new instance of the
        class
        :return: The method is returning an instance of the class.
        """
        return cls(sides)


    def update(self, sides_dict):
        """
        The `update` function updates the attributes of an object with the values provided in the
        `sides_dict` dictionary.
        
        :param sides_dict: A dictionary containing the names of the sides as keys and their corresponding
        values as values
        """
        for name, value in sides_dict.items():
            self.__setattr__(name, value)

    def as_dict(self):
        """
        The function `as_dict` returns the `_sides` attribute as a dictionary.
        :return: The method `as_dict` is returning the value of the variable `_sides`.
        """
        return self._sides


    def __setattr__(self, __name: str, __value: Any) -> None:
        """
        The `__setattr__` function is used to set attribute values for an object, with special handling for
        certain attributes.
        
        :param __name: The `__name` parameter is a string that represents the name of the attribute being
        set
        :type __name: str
        :param __value: The __value parameter is the value that you want to set for the attribute
        :type __value: Any
        """
        cls = type(self)
        if __name in cls.__match_args__:
            self._sides[__name] = __value
            self.__check_opposite_sides()
        else:
            super().__setattr__(__name, __value)

    def __getattr__(self, name):
        """
        The `__getattr__` function is used to handle attribute access for a class, raising an error if the
        attribute does not exist.
        
        :param name: The name parameter is the name of the attribute that is being accessed
        :return: If the `name` is found in `cls.__match_args__`, then `self._sides[name]` is returned.
        Otherwise, an `AttributeError` is raised with a message indicating that the attribute does not exist
        and suggesting the available attributes from `cls.__match_args__`.
        """
        cls = type(self)
        if name in cls.__match_args__:
            return self._sides[name]
        raise AttributeError(f"Wrong. Attribute does not exist. Try one of the attributes: {' ,'.join(cls.__match_args__)}")

    def __repr__(self):
        return "ConcreteCover({" + ', '.join([f"{name}={value}" for name, value in self._sides.items() if value is not None]) + "})"

    def __check_opposite_sides(self):
        """
            If both opposite sides defined - it's an Error for now. Because then Length of an object is defined.

            Opposite sides: left and right; top and bottom; front and back
        """
        cls = type(self)
        if ((self.left is not None and self.right is not None) 
            or (self.top is not None and self.bottom is not None)
            or (self.front is not None and self.back is not None)):
            raise ValueError("You cannot have both opposite sides to" 
                             f"be positive at same time: "
                             f"{(side + '=' + self.__getattr__[side] + ',' for side in cls.__match_args__)}")
