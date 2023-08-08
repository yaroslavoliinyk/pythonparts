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
        self, width, length, height, global_start_pnt=None,
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
        
        self._visible               = True
        self._union_parent          = True

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
        builded = [AllplanBasisElements.ModelElement3D(self.com_prop, self.polyhedron)]
        for child in self._children:
            builded.extend(child.build())
        return builded

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
        
        :Example:

            Let's first create two cubes. One with sides 200x200x200, another 1000x1000x1000
            >>> import pythonparts as pp
            >>> small_cube = pp.create_cuboid(200, 200, 200)
            >>> big_cube = pp.create_cuboid(1000, 1000, 1000)

            And place small cube inside big one with left shift = 300

            >>> big_cube.place(small_cube, left=300)

            After creating scene inside ``create_element()`` and returning pythonpart, we 
            will obtain the following result:

            >>> def create_element(build_ele, doc):
            >>>     scene  = pp.create_scene(build_ele)
            >>>     scene.place(big_cube)
            >>>     return scene.pythonpart

            .. image:: images/place_001.png
                :alt: Resulting image with shift left=300

        :Example:

            If we place small cube inside very center, we will obtain the following:

            >>> big_cube.place(small_cube, center=True)

            ** Other code is the same **

            .. image:: images/place_002.png
                :alt: Centered cube
            
        :Example:

            Placing center and shift right=20 will give us:

            >>> big_cube.place(small_cube, center=Ture, right=20)

            ** Other code is the same **

            .. image:: images/place_003.png
                :alt: Center + right=20

        :Example:

            You can also adjust starting point, placing main object on a scene with parameters:

            >>> scene.place(big_cube, center=True, bottom=0)

            ** Other code is the same **

            .. image:: images/place_004_1.png
                :alt: Perspective view scene place settings

            .. image:: images/place_004_2.png
                :alt: Profile view scene place settings
            
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
