import pythonparts as pp

import NemAll_Python_Geometry as AllplanGeo     # type: ignore


from ControlPropertiesUtil import ControlPropertiesUtil
from BuildingElement import BuildingElement
from ParameterProperty import ParameterProperty
from HandleDirection import HandleDirection
from HandleProperties import HandleProperties
import NemAll_Python_IFW_ElementAdapter as AllplanElementAdapter


def check_allplan_version(build_ele, version):
    # Delete unused arguments
    del build_ele
    del version

    return True


def create_element(build_ele, doc):
    scene = pp.create_scene(build_ele=build_ele)

    column = pp.create_cuboid(width=build_ele.ColumnWidth.value, 
                              length=build_ele.ColumnLength.value, 
                              height=build_ele.SlabDist.value + build_ele.SlabHeight.value,)
    slab = pp.create_cuboid(width=build_ele.SlabWidth.value, 
                            length=build_ele.ColumnLength.value, 
                            height=build_ele.SlabHeight.value,)
    
    column.union(slab, top=0)
    

    column.add_handle('SlabDist').start(top=0).end()
    column.add_handle('SlabDist').start(right=0).end(right=0, top=slab.height)
    column.add_handle('ColumnLength').start(back=0, top=0).end(top=0)
    slab.add_handle('SlabWidth').start(left=column.width).end(right=0)
    slab.add_handle('SlabHeight').start(right=0).end(right=0, top=0)
    
    stirrup_shape = pp.create_stirrup_shape()
    stirrup_shape.add_point(AllplanGeo.Point2D(0, column.height))
    stirrup_shape.add_point(AllplanGeo.Point2D(0, 0))
    stirrup_shape.add_point(AllplanGeo.Point2D(column.width, 0))
    stirrup_shape.add_point(AllplanGeo.Point2D(column.width, column.height))


    stirrups = column.add_stirrups(stirrup_shape,
                        along_axis="y",
                        concrete_grade=4,
                        steel_grade=4,
                        bending_roller=4.0,
                        diameter=8.0,
                        split_by_count=True,
                        count=10,).\
    start().\
    end(back=10.)

    slab.add_longbars(along_axis="y",
                    concrete_grade=build_ele.ColumnReinfConcreteGrade.value,
                    steel_grade=build_ele.ColumnReinfSteelGrade.value,
                    bending_roller=build_ele.ColumnReinfBendingRoller.value,
                    diameter=build_ele.ColumnHorLongbarsBotDiameter.value,
                    split_by_count=True,
                    split_by_spacing=False,
                    count=build_ele.ColumnHorLongbarsBotCount.value,).\
        start().end(bottom=0, right=0, back=0)
                    
 
    column.add_longbars(along_axis="x",
                        concrete_grade=build_ele.ColumnReinfConcreteGrade.value,
                        steel_grade=build_ele.ColumnReinfSteelGrade.value,
                        bending_roller=build_ele.ColumnReinfBendingRoller.value,
                        diameter=build_ele.ColumnHorLongbarsBotDiameter.value,
                        split_by_count=True,
                        split_by_spacing=False,
                        count=build_ele.ColumnHorLongbarsBotCount.value + 2,).\
        start(bottom=0).\
        end(top=0, right=0)
    
    if build_ele.SelectShape.value == 1:
        column.reflect(along_axis1="z", along_axis2="y")
    if build_ele.SelectShape.value == 2:
        column.reflect(along_axis1="z", along_axis2="y")
        column.reflect(along_axis1="x", along_axis2="y")
    if build_ele.SelectShape.value == 3:
        column.reflect(along_axis1="x", along_axis2="y")
 

    scene.place(column)
    return scene.pythonpart, scene.handles

def move_handle(build_ele, handle_prop, input_pnt, doc):
    return pp.move_handle(build_ele, handle_prop, input_pnt, doc, create_element)


def modify_element_property(build_ele, name, value):
    pp.modify_element_property(build_ele, name, value)

