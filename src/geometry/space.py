import math

from abc import ABC, abstractmethod, abstractproperty
from typing import Optional, List, Dict

import NemAll_Python_BasisElements as AllplanBasisElements    # type: ignore

from .coords import Coords, AllplanGeo
from .concrete_cover import ConcreteCover
from ..utils import center_calc, child_global_coords_calc, equal_points
from ..exceptions import AttributePermissionError
from ..config import TOLERANCE


# The `Space` class represents a three-dimensional space with width, length, and height, and provides
# methods for positioning child spaces within it.
class Space(ABC):
    """
        Abstract class for representing objects in *Allplan PythonPart*s.
    """

    def __init__( 
        self, width, length, height, global_start_pnt=None,
    ):
        """
        The function initializes an object with width, length, height, and optional global start point
        coordinates, and sets up local and global coordinates based on the input.
        
        :param width: The width of the object
        :param length: The `length` parameter represents the length of an object or space
        :param height: The `height` parameter represents the height of an object or space. It is used to
        define the dimensions of the object or space in the `__init__` method of a class
        :param global_start_pnt: The `global_start_pnt` parameter is the starting point of the global
        coordinates. It is an optional parameter that defaults to `None`. If a value is provided for
        `global_start_pnt`, the global coordinates will be calculated based on this point and the width,
        length, and height parameters
        """
        local    = Coords(AllplanGeo.Point3D(), AllplanGeo.Point3D(width, length, height))
        
        if global_start_pnt is not None:
            global_ = Coords(global_start_pnt, global_start_pnt + AllplanGeo.Vector3D(width, length, height))
        else:
            global_  = Coords(AllplanGeo.Point3D(), AllplanGeo.Point3D(width, length, height))

        if (global_ != Coords.from_empty() and 
            not equal_points(local.end_point - local.start_point, global_.end_point - global_.start_point)):
            raise ValueError(f"Incorrect global or local coordinates!\nlocal={local}\nglobal={global_}")
        
        self._concov = ConcreteCover.from_sides()
        self._local  = local
        self._global = global_
        self._children: List[Space] = []
        self._visible               = True
        self._union_parent          = True

    @abstractproperty
    def polyhedron(self): ...
    
    @abstractproperty
    def com_prop(self): ...

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

    def update_global_coords(self, parent_global_coords: Coords):
        """
        The function updates the global coordinates of an object and its children based on the parent's
        global coordinates.
        
        :param parent_global_coords: The parent_global_coords parameter is an instance of the Coords class.
        It represents the global coordinates of the parent object
        :type parent_global_coords: Coords
        """
        start_point, end_point = child_global_coords_calc(self._concov, parent_global_coords, self)
        self._global           = Coords(start_point, end_point)
        for child in self._children:
            child.update_global_coords(self._global)

    def build(self) -> List[AllplanBasisElements.ModelElement3D]:
        """
        The `build` function recursively builds a list of `ModelElement3D` objects by appending the current
        object and calling the `build` function on each child object.
        :return: a list of AllplanBasisElements.ModelElement3D objects.
        """
        builded = [AllplanBasisElements.ModelElement3D(self.com_prop, self.polyhedron)]
        for child in self._children:
            builded.extend(child.build())
        return builded

    def place(self, child_space: "Space", center: bool=False, **concov_sides,):
        """
        The `place` function is used to position a child space inside a parent space, with options for
        centering and specifying the position of each side.
        Places child Space inside parent Space according to given settings.

        Opposite sides are not allowed to have positive values at same time.
        
        E.g. left and right shifts == 0 and center == True,
        then left and right shifts will be redefined by center_calc.
        Same for top and bottom; front and back.
        
        :param child_space: The `child_space` parameter is an instance of the "Space" class. It represents
        the space that will be placed inside the parent space
        :type child_space: "Space"
        :param center: A boolean value indicating whether the child space should be centered within the
        parent space. If set to True, the left, front, and bottom shifts will be redefined by the
        center_calc function, defaults to False
        :type center: bool (optional)
        """
        """
            
        """
        concov = ConcreteCover(concov_sides)
        if center:
            concov.left, concov.front, concov.bottom = center_calc(concov, self.global_, child_space)
        child_space._concov.update(concov.as_dict())
        child_space.update_global_coords(self.global_)
        self._children.append(child_space)

    def __len__(self):
        return len(self._children)
    
    def __getitem__(self, index):
        return self._children[index]

    def __eq__(self, other):
        return (self.local == other.local
                and self.global_ == other.global_ 
                and math.isclose(self.length, other.length, rel_tol=TOLERANCE, abs_tol=TOLERANCE) 
                and math.isclose(self.width, other.width, rel_tol=TOLERANCE, abs_tol=TOLERANCE) 
                and math.isclose(self.height, other.height, rel_tol=TOLERANCE, abs_tol=TOLERANCE)
                and self._visible == other._visible
                and self._union_parent == other._union_parent
                and len(self._children) == len(other._children)
                and all(c1 == c2 for c1, c2 in zip(self._children, other._children)))

    def __repr__(self):
        return f"Space({self.local!r}, {self.global_!r})"
