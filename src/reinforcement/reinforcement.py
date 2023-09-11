import NemAll_Python_Geometry as AllplanGeo
import NemAll_Python_Reinforcement as AllplanReinf
import StdReinfShapeBuilder.LinearBarPlacementBuilder as LinearBarBuilder

from StdReinfShapeBuilder.ReinforcementShapeProperties import (
    ReinforcementShapeProperties,
)

from ..exceptions import AllplanGeometryError
from ..utils import find_point_on_space



class Reinforcement:
    pass



class Longbars(Reinforcement):
    
    def __init__(self, 
                 space, 
                 along_axis, 
                 split_by_count=False,
                 split_by_spacing=False,
                 **properties):
        self.parent_space = space
        if not split_by_count and not split_by_spacing:                                             # ! Error prone, because not sure that this'll work 
            raise AllplanGeometryError("Longbars should be split either by count or by spacing")    # ! in combination with space.add_reinforcement implementation
        self.along_axis = along_axis
        self.split_by_count = split_by_count
        self.split_by_spacing = split_by_spacing
        self.properties = properties


    @property
    def start_point(self):
        return find_point_on_space(self.start_concov, self.parent_space)

    @property
    def end_point(self):
        return find_point_on_space(self.end_concov, self.parent_space)

    @property
    def length(self):
        raise NotImplementedError()

    

    def start(self, **concov) -> "Longbars":
        return self
    
    def end(self, **concov) -> "Longbars":
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
                1,
                longbar_shape,
                self.start_point,
                self.end_point,
                0,
                spacing,
                count,
            )

    
    def __add_front_hook(self):
        pass

    def __add_back_hook(self):
        pass

    def __assign_spacing_count(self):
        raise NotImplementedError