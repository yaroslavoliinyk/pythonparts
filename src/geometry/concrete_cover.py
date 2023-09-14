from collections import defaultdict, namedtuple
from typing import Any, Tuple, Optional, Dict
from copy import copy

from ..utils import check_correct_axis





class Sides:


    class Info:

        def __init__(self, name, value, axis, set_by_user):
            self.name = name
            self.value = value
            self.axis = axis
            self.set_by_user = set_by_user


    # SideInfo = namedtuple('SideInfo', ['name', 'value', 'axis', 'set_by_user'])

    def __init__(self, adjacent_side_name, opposite_side_name, along_axis):
        along_axis = check_correct_axis(along_axis)
        self.adjacent = self.Info(adjacent_side_name, 0, along_axis, False)
        self.opposite = self.Info(opposite_side_name, None, along_axis, False)
        self.along_axis = along_axis
        

    def get_sides_names(self) -> Tuple[str, str]:
        if not ('adjacent') in dir(self) or not ('opposite') in dir(self):
            return '', ''
        return self.adjacent.name, self.opposite.name

    def get_sides_dict(self):
        return {self.adjacent.name:self,
                self.opposite.name:self}

    def get_side_by_name(self, name):
        if name == self.adjacent.name:
            return self.adjacent
        elif name == self.opposite.name:
            return self.opposite
        else:
            raise ValueError(f"No such side name {name}")

    def opposite_to(self, name):
        if name == self.adjacent.name:
            return self.opposite
        elif name == self.opposite.name:
            return self.adjacent
        else:
            raise ValueError(f"No such side name {name}")

    def center(self, parent_coords, child_coords):
        if not self.adjacent.set_by_user and not self.opposite.set_by_user:
            start_parent_coord = getattr(parent_coords.start_point, self.along_axis.upper())
            end_parent_coord = getattr(parent_coords.end_point, self.along_axis.upper())
            parent_len = abs(end_parent_coord - start_parent_coord)
            
            start_child_coord = getattr(child_coords.start_point, self.along_axis.upper())
            end_child_coord = getattr(child_coords.end_point, self.along_axis.upper())
            child_len = abs(end_child_coord - start_child_coord)
            
            shift = (parent_len - child_len)/2.
            self.adjacent.value = shift
            self.adjacent.set_by_user = True
            

    def __setattr__(self, name, value):
        if value is None:
            return
        # if value is None:
        #     raise ValueError("You cannot manually set side to None.")
        if name in self.get_sides_names():
            if self.opposite_to(name).set_by_user:
                raise ValueError(f"You cannot have {name}={value} and {self.opposite_to(name).name}={self.opposite_to(name).value}."
                                    f"Opposite sides are not allowed to be set for the same object.")
            self.get_side_by_name(name).value = value
            self.get_side_by_name(name).set_by_user = True
            self.opposite_to(name).value = None             # Make impossible to use opposite value
            self.opposite_to(name).set_by_user = False
        else:
            super().__setattr__(name, value)


    # def __getattr__(self, name):
    #     # if name not in self.get_sides_names():
    #     #     raise AttributeError(f"No such side {name}!")
    #     if name == self.adjacent.name:
    #         return self.adjacent
    #     elif name == self.opposite.name:
    #         return self.opposite
    #     else:
    #         return super().__getattr__(name)
        
    def __repr__(self):
        return f"Sides(adjacent={self.adjacent.name!r}, opposite={self.opposite.name!r}, axis={self.along_axis!r})"


# The `ConcreteCover` class represents a concrete cover with sides defined by the `left`, `right`,
# `top`, `bottom`, `front`, and `back` attributes, and provides methods for updating and accessing
# these attributes.
class ConcreteCover:

    __match_args__ = ('left', 'right', 'front', 'back', 'bottom', 'top',)
   
    # __match_args__ = (x_sides.get_sides_names(), y_sides.get_sides_names(), z_sides.get_sides_names())


    def __init__(self, sides_dict: Optional[Dict]=None):
        """
        The function initializes an object with a dictionary of sides and their values.
        
        :param sides_dict: The `sides_dict` parameter is a dictionary that contains the sides of an
        object. The keys of the dictionary represent the names of the sides, and the values represent
        the lengths of the sides
        """
        self.x_sides = Sides('left', 'right', 'x')
        self.y_sides = Sides('front', 'back', 'y')
        self.z_sides = Sides('bottom', 'top', 'z')

        self._sides_cache = {**self.x_sides.get_sides_dict(), **self.y_sides.get_sides_dict(), **self.z_sides.get_sides_dict()}

        if sides_dict is not None:
            for name, value in sides_dict.items():
                setattr(self, name, value)
        # self._sides = dict()
        # if sides_dict is not None:
        #     for name, value in sides_dict.items():
        #         setattr(name, value)
        # cls = type(self)
        # self._sides = defaultdict.fromkeys(cls.__match_args__, None)
        # if sides_dict is not None:
        #     self.update(sides_dict)

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
        # sides_dict = {}
        # for side_name, obj in self._sides_cache.items():
        #     side_info = obj.get_side_by_name(side_name)
        #     if side_info.value is not None and side_info.se
        sides_dict = {side_name:obj.get_side_by_name(side_name).value for side_name, obj in self._sides_cache.items() if obj.get_side_by_name(side_name).value is not None}
        return sides_dict


    def as_sides_set(self):
        sides_set = set(side_name for side_name, obj in self._sides_cache.items() if obj.get_side_by_name(side_name).value is not None)
        return sides_set


    def __setattr__(self, name: str, value: Any) -> None:
        """
        The `__setattr__` function is used to set attribute values for an object, with special handling for
        certain attributes.
        
        :param name: The `name` parameter is a string that represents the name of the attribute being
        set
        :type name: str
        :param value: The value parameter is the value that you want to set for the attribute
        :type value: Any
        """
        if '_sides_cache' in dir(self) and name in self._sides_cache.keys():
            setattr(self._sides_cache[name], name, value)
        else:
            super().__setattr__(name, value)


    def __getattr__(self, name):
        """
        The `__getattr__` function is used to handle attribute access for a class, raising an error if the
        attribute does not exist.
        
        :param name: The name parameter is the name of the attribute that is being accessed
        :return: If the `name` is found in `cls.__match_args__`, then `self._sides[name]` is returned.
        Otherwise, an `AttributeError` is raised with a message indicating that the attribute does not exist
        and suggesting the available attributes from `cls.__match_args__`.
        """
        if name in self._sides_cache.keys():
            return self._sides_cache[name].get_side_by_name(name).value
           
        # cls = type(self)
        # if name in cls.__match_args__:
        #     return self._sides[name]
        raise AttributeError(f"Wrong. Attribute does not exist. Try one of the attributes: {' ,'.join(self._sides_cache.keys())}")

    def __repr__(self):
        return "ConcreteCover({" + ', '.join([f"{name}={value}" for name, value in self.as_dict().items() if value is not None]) + "})"

    # def __check_opposite_sides(self):
    #     """
    #         If both opposite sides defined - it's an Error for now. Because then Length of an object is defined.

    #         Opposite sides: left and right; top and bottom; front and back
    #     """
    #     cls = type(self)
    #     if ((self.left is not None and self.right is not None) 
    #         or (self.top is not None and self.bottom is not None)
    #         or (self.front is not None and self.back is not None)):
    #         raise ValueError("You cannot have both opposite sides to" 
    #                          f"be positive at same time: "
    #                          f"{(side + '=' + self.__getattr__[side] + ',' for side in cls.__match_args__)}")
