import math

import NemAll_Python_Geometry as AllplanGeo
import NemAll_Python_Reinforcement as AllplanReinf
import StdReinfShapeBuilder.LinearBarPlacementBuilder as LinearBarBuilder

from StdReinfShapeBuilder.ReinforcementShapeProperties import (
    ReinforcementShapeProperties,
)

from ..geometry.concrete_cover import ConcreteCover
from ..exceptions import AllplanGeometryError, AttributePermissionError
from ..utils import (find_point_on_space,
                     check_correct_axis,)



class Reinforcement:
    pass



class Longbars(Reinforcement):
    
    FRONT_HOOK_CONST = "add_front_hook"
    BACK_HOOK_CONST  = "add_back_hook"
    id = 0

    def __init__(self, 
                 space, 
                 along_axis, 
                 split_by_count=False,
                 split_by_spacing=False,
                 **properties):
        self.parent_space = space
        if not split_by_count and not split_by_spacing:                                             # ! Error prone, because not sure that this'll work 
            raise AllplanGeometryError("Longbars should be split either by count or by spacing")    # ! in combination with space.add_reinforcement implementation
        self.start_concov = ConcreteCover()
        self.end_concov = ConcreteCover()
        self.along_axis = check_correct_axis(along_axis)
        self.split_by_count = split_by_count
        self.split_by_spacing = split_by_spacing
        self.properties = properties
        self.__class__.id += 1

    @property
    def start_point(self):
        return find_point_on_space(self.start_concov, self.parent_space)

    @property
    def end_point(self):
        return find_point_on_space(self.end_concov, self.parent_space)

    @property
    def length(self):
        if self.along_axis == "x":
            return math.fabs(self.end_point.X - self.start_point.X)
        if self.along_axis == "y":
            return math.fabs(self.end_point.Y - self.start_point.Y)
        if self.along_axis == "z":
            return math.fabs(self.end_point.Z - self.start_point.Z)
        

    
    def start(self, **concov) -> "Longbars":
        self.start_concov.update(concov)
        return self
    
    def end(self, **concov) -> "Longbars":
        self.end_concov.update(concov)
        return self

    def fetch_shape(self, shape_properties):
        shape_builder = AllplanReinf.ReinforcementShapeBuilder()
        shape_builder.AddPoints(
            [(AllplanGeo.Point2D(), 0), (AllplanGeo.Point2D(0, self.length), 0), (0)]
        )
        if self.__add_front_hook():
            shape_builder.SetHookStart(self.properties["front_hook_length"],
                                       90.0,
                                       AllplanReinf.HooType.eAngle)
        if self.__add_back_hook():
            shape_builder.SetHookEnd(self.properties["front_hook_length"],
                                       90.0,
                                       AllplanReinf.HooType.eAngle)
        return shape_builder.CreateShape(shape_properties)

    def create(self):
        spacing, count = self.__assign_spacing_count()
        shape_properties = ReinforcementShapeProperties.rebar(
            self.properties["diameter"],
            self.properties["bending_roller"],
            self.properties["steel_grade"],
            self.properties["concrete_grade"],
            AllplanReinf.BendingShapeType.LongitudinalBar,
        )
        longbar_shape = self.fetch_shape(shape_properties)
        return LinearBarBuilder.create_linear_bar_placement_from_by_dist_count(
                self.__class__.id,
                longbar_shape,
                self.start_point,
                self.end_point,
                0,
                spacing,
                count,
            )

    def __add_front_hook(self):
        return self.FRONT_HOOK_CONST in self.properties.keys() and self.properties[self.FRONT_HOOK_CONST]

    def __add_back_hook(self):
        return self.BACK_HOOK_CONST in self.properties.keys() and self.properties(self.BACK_HOOK_CONST)

    def __assign_spacing_count(self):
        if self.split_by_spacing and self.split_by_count:
            return self.properties["spacing"], self.properties["count"]
        if self.split_by_spacing:
            count = int((self.length - self.properties["diameter"]) / self.properties["spacing"]) + 1
            return self.properties["spacing"], count
        if self.split_by_count:
            spacing = (self.length - self.properties["diameter"]) / (self.properties["count"] - 1) if self.properties["count"] != 1 else self.length
            return spacing, self.properties["count"]
        raise AttributePermissionError("Unnown error. Contact Developer. Should not have reached this point.")