from typing import List

import NemAll_Python_BasisElements as AllplanBasisElements

from PythonPartUtil import PythonPartUtil

from .space import Space, AllplanGeo
from .cuboid import Cuboid
from ..reinforcement import Reinforcement


class Scene:

    MAX_AXIS_UNIT = 1_000_000_000_000

    build_ele = None
    _instance = None

    @classmethod
    def get_instance(cls, build_ele):
        if not cls._instance:
            cls.build_ele = build_ele
            return cls()
        return cls._instance

    def __init__(self):
        self.scene_space = Cuboid(self.MAX_AXIS_UNIT, self.MAX_AXIS_UNIT, self.MAX_AXIS_UNIT)
        self.place = self.scene_space.place    # Assigning a Space method here(Monkey patching)

        cls = type(self)
        if cls._instance:
            raise TypeError("Singleton implementation. Cannot create one more object.")
        cls._instance = self

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

        model_ele_list = pyp_util.create_pythonpart(self.build_ele)   # TODO: Add build_ele
        handle_list = []
        return model_ele_list, handle_list

    # def place(self, child_space, concov_dict, center=False,):
    #     self.scene_space.place(child_space, concov_dict, center)

    def __repr__(self):
        cls = type(self)
        return f"Scene(build_ele={cls.build_ele!r})"