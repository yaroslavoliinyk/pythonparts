from PythonPartUtil import PythonPartUtil

from .space import Space, AllplanGeo
from .cuboid import Cuboid
from ..reinforcement import Reinforcement


class Scene:
    build_ele = None
    _instance = None

    @classmethod
    def get_instance(cls, build_ele):
        if not cls._instance:
            cls.build_ele = build_ele
            return cls()
        return cls._instance

    def __init__(self):
        cls = type(self)
        if cls._instance:
            raise TypeError("Singleton implementation. Cannot create one more object.")
        self.__model_spaces = []
        self.__reinf_spaces = []
        self.space = Space.from_dimensions(0, 0, 0)
        cls._instance = self

    @property
    def model_ele_list(self):
        return self.__model_spaces

    @property
    def reinf_ele_list(self):
        return self.__reinf_spaces

    def build(self):
        pyp_util = PythonPartUtil()
        self.__model_ele_list
        pyp_util.add_pythonpart_view_2d3d()

    def _add_child(self, child_space: "Space"):
        self.space._add_child(child_space)
        if isinstance(child_space, Cuboid):
            self.__model_spaces.append(child_space)
        elif isinstance(child_space, Reinforcement):
            self.__reinf_spaces.append(child_space)
        else:
            raise TypeError("Child has to be either Cuboid or Reinforcement.")
