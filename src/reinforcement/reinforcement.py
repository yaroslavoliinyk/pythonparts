import math

from abc import ABC, abstractmethod

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



class Reinforcement(ABC):
    FRONT_HOOK_CONST = "add_front_hook"
    BACK_HOOK_CONST  = "add_back_hook"
    INTERSECT_CENTER = False                   # If False - Longbars will touch aligned side with 1 point
    id = 0                                     # If True - Longbars will be half diameter inside aligned side

    def __init__(self, 
                 space,
                 along_axis,
                 split_by_count,
                 split_by_spacing,
                 intersect_center=INTERSECT_CENTER,
                 **properties,):
        if not split_by_count and not split_by_spacing:                                             
            raise AllplanGeometryError("Reinforcement should be split either by count or by spacing")
        self.parent_space = space
        self.start_concov = ConcreteCover()
        self.end_concov = ConcreteCover()
        self.along_axis = check_correct_axis(along_axis)
        self.split_by_count = split_by_count
        self.split_by_spacing = split_by_spacing
        self.properties = properties
        self.__class__.id += 1
        self.intersect_center = intersect_center


    @property
    def start_point(self):
        return find_point_on_space(self.start_concov, self.parent_space)

    @property
    def end_point(self):
        return find_point_on_space(self.end_concov, self.parent_space)

    @property
    def end_placement_point(self):
        if self.along_axis == "x":
            return AllplanGeo.Point3D(self.start_point.X, 
                                      self.end_point.Y, 
                                      self.end_point.Z)
        if self.along_axis == "y":
            return AllplanGeo.Point3D(self.end_point.X, 
                                      self.start_point.Y, 
                                      self.end_point.Z)
        if self.along_axis == "z":
            return AllplanGeo.Point3D(self.end_point.X, 
                                    self.end_point.Y, 
                                    self.start_point.Z)

    @property
    def length(self):
        axis_upper = self.along_axis.upper()
        return math.fabs(getattr(self.end_point, axis_upper) - getattr(self.start_point, axis_upper))

    @property
    def width(self):
        return self.start_point.GetDistance(self.end_placement_point)
    
    @abstractmethod
    def fetch_shape(self, shape_properties): ...

    @abstractmethod
    def create(self): ...

    def start(self, **concov) -> "Reinforcement":
        self.start_concov.update(concov)
        return self
    
    def end(self, **concov) -> "Reinforcement":
        self.end_concov.update(concov)
        return self

    
    def get_shape_properties(self, shape_type: AllplanReinf.BendingShapeType):
        return ReinforcementShapeProperties.rebar(
            self.properties["diameter"],
            self.properties["bending_roller"],
            self.properties["steel_grade"],
            self.properties["concrete_grade"],
            shape_type,
        )

    def _add_front_hook(self):
        return self.FRONT_HOOK_CONST in self.properties.keys() and self.properties[self.FRONT_HOOK_CONST]

    def _add_back_hook(self):
        return self.BACK_HOOK_CONST in self.properties.keys() and self.properties[self.BACK_HOOK_CONST]

    def _shift_concrete_covers_to_edge(self):
        aligned_side = self._find_aligned_side()
        
        old_start_value = getattr(self.start_concov, aligned_side)
        setattr(self.start_concov, aligned_side, old_start_value + self.diameter/2.)
        old_end_value = getattr(self.end_concov, aligned_side)
        setattr(self.end_concov, aligned_side, old_end_value + self.diameter/2.)

    def _find_aligned_side(self):
        identical_sides = self.start_concov.as_sides_set().intersection(self.end_concov.as_sides_set())
        for side in identical_sides:
            if self.start_concov.as_dict()[side] is not None and \
                self.end_concov.as_dict()[side] is not None and \
                    math.isclose(self.start_concov.as_dict()[side], self.end_concov.as_dict()[side]):
                return side
        raise AllplanGeometryError("No aligned side in Longbars!")

    def _assign_spacing_count(self):
        if self.split_by_spacing and self.split_by_count:
            return self.properties["spacing"], self.properties["count"]
        if self.split_by_spacing:
            count = int((self.width - self.properties["diameter"]) / self.properties["spacing"]) + 1
            return self.properties["spacing"], count
        if self.split_by_count:
            spacing = (self.width - self.properties["diameter"]) / (self.properties["count"] - 1) if self.properties["count"] != 1 else self.width
            return spacing, self.properties["count"]
        raise AttributePermissionError("Unnown error. Contact Developer. Should not have reached this point.")
    

    def __getattr__(self, name):
        if name in self.properties.keys():
            return self.properties[name]
        return self.name



