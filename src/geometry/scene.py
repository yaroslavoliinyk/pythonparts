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
        :return: Returns a list of AllplanBasisElements.ModelElement3D objects.
        """
        model_ele_list = []
        for model in self.scene_space._children:
            if isinstance(model, Cuboid):
                model_ele_list.extend(model.build())
        return model_ele_list

    @property
    def reinf_ele_list(self):
        """
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
        Creates a Python part by adding 2D/3D views and reinforcement elements to
        the model element list and then creating the Python part using the build element.
        :return: an instance of the PythonPart.
        """
        pyp_util = PythonPartUtil()
        pyp_util.add_pythonpart_view_2d3d(self.model_ele_list)
        pyp_util.add_reinforcement_elements(self.reinf_ele_list)

        return CreateElementResult(pyp_util.create_pythonpart(self.build_ele))


    def place(self, child_space: Space, center=False, **concov_sides):
        """
        See explanation in :py:func:`pythonparts.geometry.Space.place`
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