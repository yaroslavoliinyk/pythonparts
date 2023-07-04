from .space import Space, AllplanGeo
from .coords import Coords, SpaceCoords
from .cuboid import Cuboid
from ..reinforcement import Reinforcement


class Scene(Space):
    build_ele = None
    _instance = None

    @classmethod
    def get_instance(cls, build_ele):
        if not cls._instance:
            cls.build_ele = build_ele
            cls._instance = cls()
        return cls._instance

    def __init__(self):
        if not self._instance:
            local_coords = Coords(AllplanGeo.Point3D(), AllplanGeo.Point3D())
            global_coords = Coords(AllplanGeo.Point3D(), AllplanGeo.Point3D())
            self.__model_ele_list = []
            self.__reinf_ele_list = []
            super().__init__(SpaceCoords(local_coords, global_coords))
        else:
            raise TypeError("Singleton implementation. Cannot create one more object.")

    @property
    def model_ele_list(self):
        return self.__model_ele_list

    @property
    def reinf_ele_list(self):
        return self.__reinf_ele_list

    def _add_child(self, child_space: "Space"):
        super()._add_child(child_space)
        if isinstance(child_space, Cuboid):
            self.__model_ele_list.append(child_space)
        elif isinstance(child_space, Reinforcement):
            self.__reinf_ele_list.append(child_space)
        else:
            raise TypeError("Child has to be either Cuboid or Reinforcement.")
