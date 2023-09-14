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
    INTERSECT_CENTER = False                   # If False - Longbars will touch aligned side with 1 point
    id = 0                                     # If True - Longbars will be half diameter inside aligned side

    def __init__(self, 
                 space, 
                 along_axis, 
                 split_by_count=False,
                 split_by_spacing=False,
                 intersect_center=INTERSECT_CENTER,
                 **properties):
        self.parent_space = space
        if not split_by_count and not split_by_spacing:                                             
            raise AllplanGeometryError("Longbars should be split either by count or by spacing")
        self.start_concov = ConcreteCover()
        self.end_concov = ConcreteCover()
        self.along_axis = check_correct_axis(along_axis)
        if self.along_axis == "z":
            raise ValueError("Allplan does not allow creation of Longbars along axis Z!")
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
    

    def start(self, **concov) -> "Longbars":
        self.start_concov.update(concov)
        return self
    
    def end(self, **concov) -> "Longbars":
        self.end_concov.update(concov)
        return self

    def fetch_shape(self, shape_properties):
        shape_builder = AllplanReinf.ReinforcementShapeBuilder()
        # shape_builder.AddPoint(AllplanGeo.Point3D(), 0, self.properties["bending_roller"])
        # shape_builder.AddPoint(self.end_point - self.end_placement_point, 0, self.properties["bending_roller"])
        shape_builder.AddPoints(
            [(AllplanGeo.Point3D(), 0), (self.end_point - self.end_placement_point, 0), (0)]
        )
        if self.__add_front_hook():
            shape_builder.SetHookStart(self.properties["front_hook_length"],
                                       90.0,
                                       AllplanReinf.HookType.eAngle)
        if self.__add_back_hook():
            shape_builder.SetHookEnd(self.properties["front_hook_length"],
                                       90.0,
                                       AllplanReinf.HookType.eAngle)
        return shape_builder.CreateShape(shape_properties)

    def create(self):
        if not self.intersect_center:
            self.__shift_concrete_covers_to_edge()
        spacing, count = self.__assign_spacing_count()
        shape_properties = ReinforcementShapeProperties.rebar(
            self.properties["diameter"],
            self.properties["bending_roller"],
            self.properties["steel_grade"],
            self.properties["concrete_grade"],
            AllplanReinf.BendingShapeType.LongitudinalBar,
        )
        longbar_shape = self.fetch_shape(shape_properties)
        rebars = LinearBarBuilder.create_linear_bar_placement_from_by_dist_count(
                self.__class__.id,
                longbar_shape,
                self.start_point,
                self.end_placement_point,
                0,
                spacing,
                count,
            )
        return rebars
    

    def __getattr__(self, name):
        if name in self.properties.keys():
            return self.properties[name]
        return self.name

    def __add_front_hook(self):
        return self.FRONT_HOOK_CONST in self.properties.keys() and self.properties[self.FRONT_HOOK_CONST]

    def __add_back_hook(self):
        return self.BACK_HOOK_CONST in self.properties.keys() and self.properties[self.BACK_HOOK_CONST]

    def __assign_spacing_count(self):
        if self.split_by_spacing and self.split_by_count:
            return self.properties["spacing"], self.properties["count"]
        if self.split_by_spacing:
            count = int((self.width - self.properties["diameter"]) / self.properties["spacing"]) + 1
            return self.properties["spacing"], count
        if self.split_by_count:
            spacing = (self.width - self.properties["diameter"]) / (self.properties["count"] - 1) if self.properties["count"] != 1 else self.width
            return spacing, self.properties["count"]
        raise AttributePermissionError("Unnown error. Contact Developer. Should not have reached this point.")
    
    def __shift_concrete_covers_to_edge(self):
        aligned_side = self.__find_aligned_side()
        
        old_start_value = getattr(self.start_concov, aligned_side)
        setattr(self.start_concov, aligned_side, old_start_value + self.diameter/2.)
        old_end_value = getattr(self.end_concov, aligned_side)
        setattr(self.end_concov, aligned_side, old_end_value + self.diameter/2.)

    def __find_aligned_side(self):
        identical_sides = self.start_concov.as_sides_set().intersection(self.end_concov.as_sides_set())
        for side in identical_sides:
            if self.start_concov.as_dict()[side] is not None and \
                self.end_concov.as_dict()[side] is not None and \
                    math.isclose(self.start_concov.as_dict()[side], self.end_concov.as_dict()[side]):
                return side
        raise AllplanGeometryError("No aligned side in Longbars!")