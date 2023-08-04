from typing import List

import NemAll_Python_BasisElements as AllplanBasisElements

from PythonPartUtil import PythonPartUtil
from CreateElementResult import CreateElementResult

from .space import Space, AllplanGeo
from .cuboid import Cuboid
from .concrete_cover import ConcreteCover
from ..reinforcement import Reinforcement
from ..utils import center_scene_calc


# The `Scene` class represents a 3D scene and provides methods for adding model elements and
# reinforcement elements to the scene.
class Scene:

    MAX_AXIS_UNIT = 1_000_000_000_000

    def __init__(self, build_ele):
        self.scene_space = Cuboid(self.MAX_AXIS_UNIT, self.MAX_AXIS_UNIT, self.MAX_AXIS_UNIT)
        self.build_ele = build_ele

    @property
    def model_ele_list(self) -> List[AllplanBasisElements.ModelElement3D]:
        """
        The function `model_ele_list` returns a list of 3D model elements from a scene space.
        :return: The method is returning a list of AllplanBasisElements.ModelElement3D objects.
        """
        model_ele_list = []
        for model in self.scene_space._children:
            if isinstance(model, Cuboid):
                model_ele_list.extend(model.build())
        return model_ele_list

    @property
    def reinf_ele_list(self):
        """
        The function `reinf_ele_list` returns a list of reinforcement elements by iterating through the
        children of `self.scene_space` and adding any instances of `Reinforcement` to the list.
        :return: a list of reinforcement elements.
        """
        reinf_ele_list = []
        for reinf in self.scene_space._children:
            if isinstance(reinf, Reinforcement):
                reinf_ele_list.extend(reinf.build())
        return reinf_ele_list

    @property
    def pythonpart(self):
        """
        The function `pythonpart` creates a Python part by adding 2D/3D views and reinforcement elements to
        the model element list and then creating the Python part using the build element.
        :return: an instance of the PythonPart.
        """
        pyp_util = PythonPartUtil()
        pyp_util.add_pythonpart_view_2d3d(self.model_ele_list)
        pyp_util.add_reinforcement_elements(self.reinf_ele_list)

        return CreateElementResult(pyp_util.create_pythonpart(self.build_ele))


    def place(self, child_space: Space, center=False, **concov_sides):
        """
        The `place` function is used to position a child space within a scene space, with the option to
        center it. Sides 'right', 'top', 'back' will not be taken into account. In this method, parameter 
        'center' will act differently. If center is True => put child_space in the very middle of Axis
        
        :param child_space: The child_space parameter is an instance of the Space class that represents
        the space to be placed within the scene_space
        :type child_space: Space
        :param center: A boolean parameter that determines whether the child_space should be placed in
        the center of the Axis or not. If set to True, the child_space will be placed in the center. If
        set to False, the child_space will be placed according to the other parameters, defaults to
        False (optional)
        """
        concov = ConcreteCover(concov_sides)
        concov.right = None
        concov.top   = None
        concov.back  = None
        if center:
            concov.left, concov.front, concov.bottom = center_scene_calc(concov, child_space)
        self.scene_space.place(child_space, left=concov.left, front=concov.front, bottom=concov.bottom)


    def __repr__(self):
        return f"Scene(build_ele={self.build_ele!r})"