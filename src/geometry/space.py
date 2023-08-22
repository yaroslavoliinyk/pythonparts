import math
import copy

from abc import ABC, abstractmethod, abstractproperty
from typing import Optional, List, Dict

import NemAll_Python_BasisElements as AllplanBasisElements    # type: ignore

from .space_state import State
from .coords import Coords, AllplanGeo
from .concrete_cover import ConcreteCover
from ..exceptions import AttributePermissionError, AllplanGeometryError
from ..config import TOLERANCE
from ..utils import (center_calc,
                    child_global_coords_calc,
                    equal_points, 
                    get_rotation_matrix,
                    transform,)


# The `Space` class represents a three-dimensional space with width, length, and height, and provides
# methods for positioning child spaces within it.
class Space(ABC):
    """
    Abstract class for representing objects in *Allplan PythonParts*.

    Contains general logics for interaction with other :py:class:`Space <pythonparts.geometry.Space>` objects.
    You can :py:func:`place child <pythonparts.geometry.Space.place>`  ``Space`` objects with 
    different :py:class:`Concrete cover <pythonparts.geometry.ConcreteCover>` idents.

    From any :py:class:`Space <pythonparts.geometry.Space>` object you can make 
    
    :py:func:`an AllplanGeo.Polyhedron3D <pythonparts.geometry.Space.polyhedron>` and get 
    
    :py:func:`AllplanBaseElements.CommonProperties <pythonparts.geometry.Space.com_prop>`

    You can also :py:func:`build <pythonparts.geometry.Space.build>` an ``AllplanBasisElements.ModelElement3D``
    object to represent it in ``Allplan``.

    """

    def __init__( 
        self, width, length, height, global_start_pnt=None, visible=True,
    ):
        """
        Assignes *width*, *length* and *height* of child objects :py:class:`pythonparts.geometry.Scene`,
        :py:class:`pythonparts.geometry.Cuboid`

        In future versions you will be able to *hide* or *subtract* ``Space`` objects

        :param width: Set a width of an object.
        :type width: float value >= 0.
        :param length: Set a length of an object.
        :type length: float value >= 0. 
        :param height: Set a length of an object.
        :type height: float value >= 0.
        :param global_start_pnt: Set Global Start Point on coordinate axis. If not set, it will be ``AllplanGeo.Point3D(0, 0, 0)`` 
        :type global_start_pnt: ``None`` or ``AllplanGeo.Point3D``
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
        """Inner attribute that contains list of ``Space`` that were :py:func:`placed <pythonparts.geometry.Space.place>`."""
        
        self._state                                       = State.PLACE
        self.visible                                      = visible
        self.rotation_matrices: List[AllplanGeo.Matrix3D] = []

    @abstractproperty
    def polyhedron(self) -> AllplanGeo.Polyhedron3D: ...
    
    @abstractproperty
    def com_prop(self): ...

    @property
    def local(self) -> Coords:
        """
            :return: Local coordinates of this ``Space`` object.
            :rtype: :py:class:`pythonparts.geometry.coords.Coords`
        """
        return self._local
    
    @local.setter
    def local(self, value):
        raise AttributePermissionError("You cannot set local coords this way.")
    
    @property
    def global_(self) -> Coords:
        """
            :return: Global coordinates of this ``Space`` object.
            :rtype: :py:class:`pythonparts.geometry.coords.Coords`
        """
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

    @property
    def state(self):
        return self._state
    
    @state.setter
    def state(self, value):
        raise AttributePermissionError("You cannot set union of Space with another Space. Use union() function instead")
    
    # @property
    # def visible(self):
    #     return self.visible
    
    # @visible.setter
    # def visible(self, value):
    #     raise AttributePermissionError("You cannot set visiblity. Please set it when you either create or place object")
    # @visible.setter
    # def state(self, value):
    #     self.visible = value

    def update_global_coords(self, parent_global_coords: Coords):
        """
        Set new Global coordinates for this ``Space`` object and all its :py:func:`children <pythonparts.geometry.Space._children>`
        
        :param parent_global_coords: An instance of the Coords class.
            It represents the global coordinates of the parent object.
        :type parent_global_coords: Coords
        """
        start_point, end_point = child_global_coords_calc(self._concov, parent_global_coords, self)
        self._global           = Coords(start_point, end_point)
        for child in self._children:
            child.update_global_coords(self._global)  
    
    def build(self) -> List[AllplanBasisElements.ModelElement3D]:
        """
        Recursively builds a list of `AllplanBasisElements.ModelElement3D` objects for itselt
        and all its :py:func:`children <pythonparts.geometry.Space._children>`
        :return: a list of AllplanBasisElements.ModelElement3D objects.
        """
        self._update_rotation_matrices(self.rotation_matrices)
        model_ele_list       = self.__build_all()

        # return [AllplanBasisElements.ModelElement3D(self.com_prop, placed_poly) for placed_poly in polyhedrons]
        return model_ele_list

    def place(self, child_space: "Space", center: bool=False, **concov_sides,):
        """
        Position a child space inside a parent space, with options for
        centering and specifying the position of each side.

        :info: If you don't define *center* and *sides* , child global start point will be
            equal parent global start point.

        :param child_space: Represents the space that will be placed inside the parent space
        :type child_space: "Space"
        :param center: A boolean value indicating whether the child space should be centered within the
            parent space. If set to True, the left, front, and bottom shifts will be redefined by the
            center_calc function, defaults to False
        :type center: bool (optional)
        :type sides: 6 different sides that you can add to place child space inside parent:
            - left
            - right
            - front
            - back
            - top
            - bottom
        :type sides: float (optional)

        :warning: Opposite sides(*left* and *right*; *front* and *back*; *top* and *bottom*) 
            are not allowed to have values at same time.
        """
        concov = ConcreteCover(concov_sides)
        if center:
            concov.left, concov.front, concov.bottom = center_calc(concov, self.global_, child_space)
        child_space._concov.update(concov.as_dict())
        child_space.update_global_coords(self.global_)
        self._children.append(child_space)
        # child_space._update_rotation_matrices(self.rotation_matrices)

    def union(self, child_space: "Space", center: bool=False, **concov_sides,):
        self.place(child_space, center, **concov_sides)
        child_space._state = State.UNION

    def subtract(self, child_space: "Space", center: bool=False, **concov_sides,):
        self.place(child_space, center, **concov_sides)
        child_space._state = State.SUBTRACT

    def rotate(self, degree: float, along_axis: str="x", center: bool=False, **point_props,):
        """
        :type sides: 6 different sides that you can add to place child space inside parent:
            - left
            - right
            - front
            - back
            - top
            - bottom
        :type sides: float (optional)
        """
        # We don't actually rotate here. But user doesn't need to know that. 
        # We just set rotation matrix and the very rotation will happen 
        # at the point of creating model_ele_list
        props = ConcreteCover(point_props)
        if center:
            props.left, props.front, props.bottom = center_calc(props, self.global_, self)
        rotation_space = copy.copy(self)
        rotation_space._concov.update(props.as_dict())
        rotation_space.update_global_coords(self.global_)
        
        local_rotation_matrix = get_rotation_matrix(degree, along_axis, rotation_space.global_.start_point)
        self.rotation_matrices.append(local_rotation_matrix)
        # self._update_rotation_matrices([local_rotation_matrix])

    def _update_rotation_matrices(self, rotation_matrices):
        """
        The function spreads a parent rotation matrix to all its children by inserting it at the
        beginning of each child's rotation matrix list and recursively calling itself on each child.
        
        :param parent_rotation_matrix: The parent_rotation_matrix is a 3x3 matrix representing the
        rotation transformation applied to the parent object
        """
        for child in self._children:
            child.rotation_matrices[:0] = rotation_matrices
            child._update_rotation_matrices(child.rotation_matrices)

    def __build_all(self, resulted_polyhedron=None):
        polyhedrons = []

        if resulted_polyhedron is not None and self.state == State.UNION:
            err, resulted_polyhedron = AllplanGeo.MakeUnion(resulted_polyhedron, self.polyhedron)
            if err:
                raise AllplanGeometryError(f"You cannot make union of {resulted_polyhedron} and {self.polyhedron}.\n{err}")
        elif resulted_polyhedron is not None and self.state == State.SUBTRACT:
            err, resulted_polyhedron = AllplanGeo.MakeSubtraction(resulted_polyhedron, self.polyhedron)
            if err:
                raise AllplanGeometryError(f"You cannot subtract from {resulted_polyhedron} the following polyhedron {self.polyhedron}.\n{err}")
        else:
            resulted_polyhedron = self.polyhedron

        for child in self._children:
            polyhedrons.extend(child.__build_all(resulted_polyhedron))
        
        if not resulted_polyhedron == AllplanGeo.Polyhedron3D():        # If the resulted_polyhedron not empty
            if not any(child.state in (State.UNION, State.SUBTRACT) for child in self._children):
                model  = AllplanBasisElements.ModelElement3D(self.com_prop, transform(resulted_polyhedron, self.rotation_matrices))
                polyhedrons.append(model)
        
        return polyhedrons

    def __copy__(self):
        # Create a new instance of the Space class with the same attributes
        copied_instance = self.__class__(
            width=self.width,
            length=self.length,
            height=self.height,
            global_start_pnt=self.global_.start_point if self._global != Coords.from_empty() else None,
            visible=self.visible
        )
        
        # Copy any additional attributes as needed
        copied_instance._concov = copy.copy(self._concov)
        copied_instance._children = copy.copy(self._children)
        copied_instance.rotation_matrices = copy.copy(self.rotation_matrices)
        
        # You might need to update the global coordinates of the copied instance
        copied_instance.update_global_coords(copied_instance._global)
        
        return copied_instance


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
                and self.visible == other.visible
                and self._state == other._state
                and len(self._children) == len(other._children)
                and all(c1 == c2 for c1, c2 in zip(self._children, other._children)))

    def __repr__(self):
        return f"Space({self.local!r}, {self.global_!r})"
