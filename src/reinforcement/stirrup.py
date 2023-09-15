import itertools
from typing import List

import NemAll_Python_Geometry as AllplanGeo
import NemAll_Python_Reinforcement as AllplanReinf

from StdReinfShapeBuilder.ReinforcementShapeProperties import (
    ReinforcementShapeProperties,
)

from .reinforcement import Reinforcement



class Stirrups(Reinforcement):

    class Shape:

        def __init__(self):
            self.points: List[AllplanGeo.Point2D] = []

        def add_point(self, point: AllplanGeo.Point2D):
            self.points.append(point)

    def __init__(self, 
                 space,
                 stirrup_shape: "Shape", 
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
        self.stirrup_shape = stirrup_shape

    def fetch_shape(self, shape_properties):
        shape_builder = AllplanReinf.ReinforcementShapeBuilder()
        shape_builder.AddPoints(
            [(point, zero) for point, zero in zip(self.stirrup_shape, itertools.repeat(0, len(self.stirrup_shape)))]
        )
        return shape_builder.CreateShape(shape_properties)

    def create(self):
        spacing, count = self._assign_spacing_count()
        shape_properties = self.get_shape_properties(AllplanReinf.BendingShapeType.OpenStirrup)
        stirrup_shape = self.fetch_shape(shape_properties)
        
        stirrups = self.__get_bar_placement(
            self.__class__.id,
            stirrup_shape,
            self.start_point,
            self.end_placement_point,
            spacing,
            count,
        )
        return stirrups

       
    
    def __get_bar_placement(self,
                            id,
                            shape,
                            start_point,
                            end_placement_point,
                            spacing,
                            count):
        dist_vec = AllplanGeo.Vector3D(start_point, end_placement_point)
        start_shape = AllplanReinf.BendingShape(shape)
        start_shape.Move(AllplanGeo.Vector3D(start_point))
        dist_vec.Normalize(spacing)
        
        return AllplanReinf.BarPlacement(
            id,
            count,
            dist_vec,
            start_point,
            end_placement_point,
            start_shape,
        )

