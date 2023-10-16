import math

import NemAll_Python_Geometry as AllplanGeo
import NemAll_Python_Reinforcement as AllplanReinf
import StdReinfShapeBuilder.LinearBarPlacementBuilder as LinearBarBuilder

from StdReinfShapeBuilder.ReinforcementShapeProperties import (
    ReinforcementShapeProperties,
)

from .reinforcement import Reinforcement
from ..geometry.concrete_cover import ConcreteCover
from ..exceptions import AllplanGeometryError, AttributePermissionError
from ..utils import (find_point_on_space,
                     check_correct_axis,)






class Longbars(Reinforcement):
    
    def __init__(self, 
                 space, 
                 along_axis, 
                 split_by_count=False,
                 split_by_spacing=False,
                 intersect_center=Reinforcement.INTERSECT_CENTER,
                 **properties):
        super().__init__(space, 
                         along_axis, 
                         split_by_count=split_by_count,
                         split_by_spacing=split_by_spacing,
                         intersect_center=intersect_center,
                         **properties)
        if self.along_axis == "z":
            raise ValueError("Allplan does not allow creation of Longbars along axis Z!")
        
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


    def fetch_shape(self, shape_properties):
        shape_builder = AllplanReinf.ReinforcementShapeBuilder()
        shape_builder.AddPoints(
            [(AllplanGeo.Point3D(), 0), (self.end_point - self.end_placement_point, 0), (0)]
        )
        if self.front_hook.enabled:
            shape_builder.SetHookStart(self.front_hook.length,
                                       90.0,
                                       AllplanReinf.HookType.eAngle)
        if self.back_hook.enabled:
            shape_builder.SetHookEnd(self.back_hook.length,
                                       90.0,
                                       AllplanReinf.HookType.eAngle)
        return shape_builder.CreateShape(shape_properties)

    def create(self):
        if not self.intersect_center:
            self._shift_concrete_covers_to_edge()
        spacing, count = self._assign_spacing_count()
        shape_properties = self.get_shape_properties(AllplanReinf.BendingShapeType.LongitudinalBar)
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
    


