import math
import re

from abc import ABC, abstractmethod, abstractproperty
from typing import Union, Optional, List, Dict

import NemAll_Python_BasisElements as AllplanBasisElements    # type: ignore

from HandleProperties import HandleProperties                  # type: ignore

from .space_state import State
from .coords import Coords, AllplanGeo
from .concrete_cover import ConcreteCover
from ..handles import Handle
from ..reinforcement import Longbars, Stirrups
from ..exceptions import (AttributePermissionError, 
                          AllplanGeometryError,
                          IncorrectAxisValueError,)
from ..config import TOLERANCE
from ..utils import (child_global_coords_calc,
                    equal_points, 
                    check_correct_axis,
                    to_radians,
                    unit_vector,)


# The `Space` class represents a three-dimensional space with width, length, and height, and provides
# methods for positioning child spaces within it.
class Space:
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
    
    @classmethod
    def from_space_no_children(cls, other_space: "Space"):
        gspnt = AllplanGeo.Point3D(other_space.global_.start_point)
        space = cls(other_space.width, other_space.length, other_space.height, global_start_pnt=gspnt, visible=other_space.visible)
        space._state = other_space.state
        # ? space.com_prop = other_space.com_prop
        return space

    @classmethod
    def from_dimentions_global_point(cls, width, length, height, global_pnt):
        return cls(width, length, height, global_pnt)

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
        self.transformations: List[Union[Rotation, Reflection]] = []
        self.handles                                      = []
        self.longbars                                     = []
        self.stirrups                                     = []


    def polyhedron(self) -> AllplanGeo.Polyhedron3D: 
        raise NotImplementedError()
    
    def polyhedron_transformed(self) -> AllplanGeo.Polyhedron3D: 
        raise NotImplementedError()
    
    def com_prop(self):
        raise NotImplementedError()

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
    
    # @check_update_transformations
    def build(self) -> List[AllplanBasisElements.ModelElement3D]:
        """
        Recursively builds a list of `AllplanBasisElements.ModelElement3D` objects for itselt
        and all its :py:func:`children <pythonparts.geometry.Space._children>`
        :return: a list of AllplanBasisElements.ModelElement3D objects.
        """
        self._update_child_transformations(self.transformations)
        model_ele_list       = self.__build_all()

        # return [AllplanBasisElements.ModelElement3D(self.com_prop, placed_poly) for placed_poly in polyhedrons]
        return model_ele_list

    # @check_update_transformations
    def build_handles(self, scene) -> List[HandleProperties]:
        handles_allplan: List[HandleProperties] = [handle.create(scene) for handle in self.handles]
        handles_transformed: List[HandleProperties] = []
        tfs_reversed = [] if not self.transformations else self.transformations[::-1]
        
        for handle_prop in handles_allplan:
            for tf in tfs_reversed:
                handle_prop.transform(tf.get_matrix())
            handles_transformed.append(handle_prop)
        
        for model in self._children:
            handles_transformed.extend(model.build_handles(scene))
        return handles_transformed

    def build_reinforcement(self):
        reinforcement_allplan = [longbar.create() for longbar in self.longbars]
        reinforcement_allplan.extend([stirrup.create() for stirrup in self.stirrups])
        
        reinforcement_transformed = []
        tfs_reversed = [] if not self.transformations else self.transformations[::-1]

        for reinf in reinforcement_allplan:
            for tf in tfs_reversed:
                reinf.Transform(tf.get_matrix())
            reinforcement_transformed.append(reinf)

        for model in self._children:
            reinforcement_transformed.extend(model.build_reinforcement())
        return reinforcement_transformed

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
            concov.x_sides.center(self.local, child_space.local)
            concov.y_sides.center(self.local, child_space.local)
            concov.z_sides.center(self.local, child_space.local)
            # concov.left, concov.front, concov.bottom = center_calc(concov, self.global_, child_space)
        child_space._concov.update(concov.as_dict())
        child_space.update_child_global_coords(self.global_)
        self._children.append(child_space)

    def union(self, child_space: "Space", center: bool=False, **concov_sides,):
        self.place(child_space, center, **concov_sides)
        child_space._state = State.UNION

    def subtract(self, child_space: "Space", center: bool=False, **concov_sides,):
        self.place(child_space, center, **concov_sides)
        child_space._state = State.SUBTRACT

    def rotate(self, degree: float, along_axis: str="x", center: bool=False, **point_props,):
        # We don't actually rotate here. But user doesn't need to know that. 
        # We just set rotation matrix and the very rotation will happen 
        # at the point of creating model_ele_list
        self.transformations.append(Rotation(self, degree, along_axis, center, **point_props))
    
    def reflect(self, along_axis1: str="x", along_axis2: str="y", center: bool=False, **point_props,):
        self.transformations.append(Reflection(self, along_axis1, along_axis2, center, **point_props))

    def add_longbars(self, along_axis="x", **longbars_kwargs) -> Longbars:
        longbars = Longbars(self, check_correct_axis(along_axis), **longbars_kwargs)
        self.longbars.append(longbars)
        return longbars

    def add_stirrups(self, stirrup_shape: Stirrups.Shape, along_axis="x", **stirrups_kwargs) -> Stirrups:
        stirrups = Stirrups(self, stirrup_shape, check_correct_axis(along_axis), **stirrups_kwargs)
        self.stirrups.append(stirrups)
        return stirrups
    
    def add_handle(self, param_name) -> Handle:
        handle = Handle(self, param_name)
        self.handles.append(handle)
        return handle

    def update_child_global_coords(self, parent_global_coords: Coords):
        """
        Set new Global coordinates for this ``Space`` object and all its :py:func:`children <pythonparts.geometry.Space._children>`
        
        :param parent_global_coords: An instance of the Coords class.
            It represents the global coordinates of the parent object.
        :type parent_global_coords: Coords
        """
        start_point, end_point = child_global_coords_calc(self._concov, parent_global_coords, self)
        self._global           = Coords(start_point, end_point)
        for child in self._children:
            child.update_child_global_coords(self._global)  

    def _update_child_transformations(self, parent_transformations):
        """
        The function spreads a parent rotation matrix to all its children by inserting it at the
        beginning of each child's rotation matrix list and recursively calling itself on each child.
        
        :param parent_rotation_matrix: The parent_rotation_matrix is a 3x3 matrix representing the
        rotation transformation applied to the parent object
        """
        for child in self._children:
            child.transformations[:0] = parent_transformations
            child._update_child_transformations(child.transformations)

    def __build_all(self, resulted_polyhedron=None):
        polyhedrons = []

        if resulted_polyhedron is not None and self.state == State.UNION:
            err, resulted_polyhedron = AllplanGeo.MakeUnion(resulted_polyhedron, self.polyhedron_transformed)
            if err:
                raise AllplanGeometryError(f"Error while making Union.\n{err}")
        elif resulted_polyhedron is not None and self.state == State.SUBTRACT:
            err, resulted_polyhedron = AllplanGeo.MakeSubtraction(resulted_polyhedron, self.polyhedron_transformed)
            if err:
                raise AllplanGeometryError(f"Error while making Subtraction.\n{err}")
        else:
            resulted_polyhedron = self.polyhedron_transformed

        for child in self._children:
            polyhedrons.extend(child.__build_all(resulted_polyhedron))
        
        if not resulted_polyhedron == AllplanGeo.Polyhedron3D():                                     # If the resulted_polyhedron not empty
            if not any(child.state in (State.UNION, State.SUBTRACT) for child in self._children):    # If we don't need more unions or subtractions
                # tfs_reversed = [] if not self.transformations else self.transformations[::-1]
                # for tf in tfs_reversed:
                #     resulted_polyhedron = tf.transform(resulted_polyhedron)
                model  = AllplanBasisElements.ModelElement3D(self.com_prop, resulted_polyhedron)
                polyhedrons.append(model)
        
        return polyhedrons

    def __len__(self):
        return len(self._children)
    
    def __getitem__(self, index):
        return self._children[index]

    def __hash__(self):
        hashable_attributes = frozenset([
            self.local, self.global_, self.length, self.width, self.height,
            self.visible, self._state, *self._children
        ])
        return hash(hashable_attributes)

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


class Rotation:

    def __init__(self, space_transformed: Space, degree: float, along_axis: str, center: bool, **point_props):
        self.space = space_transformed
        self.degree = degree
        self.axis = check_correct_axis(along_axis)
        self.center = center
        self.props = ConcreteCover(point_props)

    def transform(self, polyhedron):
        return AllplanGeo.Transform(polyhedron, self.get_matrix())
    
    def get_matrix(self):
        # if self.center:
        #     self.props.left, self.props.front, self.props.bottom = center_calc(self.props, self.space.global_, self.space)
        rotation_space = Space.from_space_no_children(self.space)
        rotation_space._concov.update(self.props.as_dict())
        rotation_space.update_child_global_coords(self.space.global_)
        
        matrix = self.__get_matrix_by_point(rotation_space.global_.start_point)
        return matrix


    def __get_matrix_by_point(self, rotation_point):
        axis_line = self.__get_axis_line(rotation_point)
        rotation_matrix = AllplanGeo.Matrix3D()
        rotation_matrix.Rotation(axis_line,
                                to_radians(self.degree))
        return rotation_matrix
    
    def __get_axis_line(self, rotation_point: AllplanGeo.Point3D):
        return AllplanGeo.Line3D(rotation_point, rotation_point + unit_vector(along_axis=self.axis))


class Reflection:

    def __init__(self, space_transformed: Space, along_axis1: str, along_axis2: str, center: bool, **point_props):
        self.space = space_transformed
        self.axis1 = check_correct_axis(along_axis1)
        self.axis2 = check_correct_axis(along_axis2)
        self.center = center
        self.props = ConcreteCover(point_props)

    def transform(self, polyhedron):
        # if self.center:
        #     self.props.left, self.props.front, self.props.bottom = center_calc(self.props, self.space.global_, self.space)
        reflection_space = Space.from_space_no_children(self.space)
        reflection_space._concov.update(self.props.as_dict())
        reflection_space.update_child_global_coords(self.space.global_)

        return AllplanGeo.Mirror(polyhedron, self.__get_reflection_plane(reflection_space.global_.start_point))
    
    def get_matrix(self):
        # if self.center:
        #     self.props.left, self.props.front, self.props.bottom = center_calc(self.props, self.space.global_, self.space)
        reflection_space = Space.from_space_no_children(self.space)
        reflection_space._concov.update(self.props.as_dict())
        reflection_space.update_child_global_coords(self.space.global_)
        
        matrix = self.__get_matrix_by_point(reflection_space.global_.start_point)
        return matrix

    def __get_matrix_by_point(self, reflection_point):
        plane = self.__get_reflection_plane(reflection_point)
        reflection_matrix = AllplanGeo.Matrix3D()
        reflection_matrix.Reflection(plane)

        return reflection_matrix

    def __get_reflection_plane(self, reflection_point):
        if self.axis1 == self.axis2:
            raise IncorrectAxisValueError(f"You should enter two different axis. You entered: along_axis1={self.axis1}, along_axis2={self.axis2}")
        normal_vector = AllplanGeo.Vector3D(1, 1, 1)
        if "x" in self.axis1 + self.axis2:
            normal_vector.X = 0
        if "y" in self.axis1 + self.axis2:
            normal_vector.Y = 0
        if "z" in self.axis1 + self.axis2:
            normal_vector.Z = 0
        
        plane = AllplanGeo.Plane3D(reflection_point, normal_vector)
        return plane 