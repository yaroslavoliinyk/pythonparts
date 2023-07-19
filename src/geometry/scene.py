from typing import List

import NemAll_Python_BasisElements as AllplanBasisElements

from PythonPartUtil import PythonPartUtil
from CreateElementResult import CreateElementResult

from .space import Space, AllplanGeo
from .cuboid import Cuboid
from .concrete_cover import ConcreteCover
from ..reinforcement import Reinforcement
from ..utils import center_scene_calc


class Scene:

    MAX_AXIS_UNIT = 1_000_000_000_000

    def __init__(self, build_ele):
        self.scene_space = Cuboid(self.MAX_AXIS_UNIT, self.MAX_AXIS_UNIT, self.MAX_AXIS_UNIT)
        self.build_ele = build_ele

    @property
    def model_ele_list(self) -> List[AllplanBasisElements.ModelElement3D]:
        model_ele_list = []
        for model in self.scene_space._children:
            if isinstance(model, Cuboid):
                model_ele_list.extend(model.build())
        return model_ele_list

    @property
    def reinf_ele_list(self):
        reinf_ele_list = []
        for reinf in self.scene_space._children:
            if isinstance(reinf, Reinforcement):
                reinf_ele_list.extend(reinf.build())
        return reinf_ele_list

    @property
    def pythonpart(self):
        pyp_util = PythonPartUtil()
        pyp_util.add_pythonpart_view_2d3d(self.model_ele_list)
        pyp_util.add_reinforcement_elements(self.reinf_ele_list)

        return CreateElementResult(pyp_util.create_pythonpart(self.build_ele))


    def place(self, child_space: Space, center=False, **concov_sides):
        """
            In this method, parameter 'center' will act differently.
            If center is True => put child_space in the very middle of Axis

            Sides 'right', 'top', 'back' will not be taken into account.
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