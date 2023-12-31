from typing import Tuple

import NemAll_Python_Geometry as AllplanGeo     # type: ignore

from HandleDirection import HandleDirection     # type: ignore
from HandleProperties import HandleProperties   # type: ignore
from ParameterProperty import ParameterProperty # type: ignore

from ..geometry.coords import Coords
from ..geometry.concrete_cover import ConcreteCover
from ..utils import (find_point_on_space,
                     equal_points,
                     move_scene_along_axis,)



class Handle:

    name = "PP_Handle"
    id = 0

    def __init__(self, space, param_name: str):
        self.parent_space = space
        self.param_name = param_name
        self.start_concov = ConcreteCover()
        self.end_concov = ConcreteCover()
        self.__id = self.__class__.id
        self.__handle_name = f"{self.name}{self.__id}"
        self.__class__.id += 1


    @property
    def start_point(self):
        return find_point_on_space(self.start_concov, self.parent_space)

    @property
    def end_point(self):
        return find_point_on_space(self.end_concov, self.parent_space)


    def start(self, **concov_sides) -> "Handle":
        self.start_concov.update(concov_sides)
        return self

    def end(self, **concov_sides) -> "Handle":
        self.end_concov.update(concov_sides)
        return self

    def create(self, scene):
        param_property: ParameterProperty = getattr(scene.build_ele, self.param_name)
        constant = self.end_point.GetDistance(self.start_point) - getattr(scene.build_ele, self.param_name).value
        
        handle_param_property = param_property.deep_copy()                      # Creation of special Paramater Property for handle values
        handle_param_property.name = self.__handle_name
        handle_param_property.value = self.end_point.GetDistance(self.start_point)
        handle_param_property.param_name = self.param_name
        handle_param_property.constant   = constant

        param_property = getattr(scene.build_ele, self.param_name)
        param_property.value = param_property.value
        setattr(scene.build_ele, self.__handle_name, handle_param_property)

        handle_property = HandleProperties(
            self.__handle_name,
            self.end_point,
            self.start_point,
            [(self.__handle_name, HandleDirection.point_dir, True)],
            HandleDirection.point_dir,
        )
        
        handle_property.move_scene = move_scene_along_axis(self.start_point, self.end_point, scene.global_.start_point)
        handle_property.scene_start_point = scene.global_.start_point
        
        return handle_property
