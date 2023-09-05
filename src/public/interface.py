import pythonparts as pp

from numbers import Real

import NemAll_Python_Geometry as AllplanGeo     # type: ignore

from .tools import Register
from ..utils import equal_points


def create_scene(build_ele):
    """
    Creates a canvas. All objects should be placed on Scene.

    :param build_ele: Given by Allplan ``BuildingElement`` object

    :return: :class:`Scene <Scene>` object

    Usage:

        >>> import pythonparts as pp
        >>> c = pp.create_cuboid(200, 1000, 100)
        >>> scene = pp.create_scene('build_ele')
        >>> scene.place(c)
        >>> scene
        Scene(children=[Cuboid(width=200, length=1000, height=100)]) 
    """
    register = Register()
    register.set_build_ele(build_ele)
    scene = pp.src.geometry.Scene(build_ele)
    try:
        scene_start_point = getattr(build_ele, "scene_start_point")
        scene.global_.move_start_point(AllplanGeo.Vector3D(scene_start_point))
    except AttributeError:
        print("No handle move that influences input point of scene")
    register.set_scene(scene)
    
    return scene


def create_cuboid(width, length, height, visible=True):
    """
    Constructs :class:`Cuboid <Cuboid>` object with start global point = ``Point3D(0, 0, 0)``.

    :param width: Width of Cuboid. Goes along X axis in Allplan.
    :param length: Length of Cuboid. Goes along Y axis in Allplan.
    :param height: Height of Cuboid. Goes along Z axis in Allplan.

    :return: :class:`Cuboid <Cuboid>` object
    :rtype: pythonparts.Cuboid

    Usage:

        >>> import pythonparts as pp
        >>> c = pp.create_cuboid(200, 1000, 100)
        >>> c
        Cuboid(width=200, length=1000, height=100) 
    """
    if isinstance(width, Real) and isinstance(length, Real) and isinstance(height, Real):
        return pp.src.geometry.Cuboid(width, length, height, visible=visible)
    
    raise NotImplemented()


def create_cuboid_from_pyp(pyp_name, visible=True):
    """
    Constructs :class:`Cuboid <Cuboid>` object fetching 
    width, length, and height from the according pyp file.

    :param pyp_name: According pyp file has to have three following parameters: 
    
                                - *pyp_name + 'Width'*
                                - *pyp_name + 'Length'*
                                - *pyp_name + 'Height'*

    :return: :class:`Cuboid <Cuboid>` object
    :rtype: pythonparts.Cuboid

    Inside pyp file::

        <Parameter>
            <Name>ColumnWidth</Name>
            <Text>Column Width</Text>
            <Value>200.</Value>
            <ValueType>Length</ValueType>
        </Parameter>
        
        <Parameter>
            <Name>ColumnLength</Name>
            <Text>Column Length</Text>
            <Value>1000.</Value>
            <ValueType>Length</ValueType>
        </Parameter>
        
        <Parameter>
            <Name>ColumnHeight</Name>
            <Text>Column Height</Text>
            <Value>100.</Value>
            <ValueType>Length</ValueType>
        </Parameter>

    Usage:

        >>> import pythonparts as pp
        >>> c = pp.create_cuboid_from_pyp('Column')
        >>> c
        Cuboid(width=200, length=1000, height=100)   
    """
    register = Register()
    build_ele = register.get_build_ele()
    
    width  = getattr((build_ele), f"{pyp_name}Width").value
    length = getattr((build_ele), f"{pyp_name}Length").value
    height = getattr((build_ele), f"{pyp_name}Height").value

    return pp.src.geometry.Cuboid(width, length, height, visible=visible)


def move_handle(build_ele, handle_prop, input_pnt, doc, create):
    register = Register()
    register.set_build_ele(build_ele)
    scene = register.get_scene()

    handle_param_property = getattr(build_ele, handle_prop.parameter_data[0].param_prop_name)

    delta = handle_prop.ref_point.GetDistance(input_pnt) - float(handle_param_property.constant)
    parameter_property = getattr(build_ele, handle_param_property.param_name)
    parameter_property.value = delta

    if handle_prop.move_scene is not None:
        scene.global_.move_start_point_along_axis(AllplanGeo.Vector3D(scene.global_.start_point, input_pnt), 
                                                  axis=handle_prop.move_scene)
        build_ele.scene_start_point = scene.global_.start_point

    return create(build_ele, doc)


def modify_element_property(build_ele, name, value):
    if name.startswith(pp.src.handles.Handle.name):
        handle_param_property = getattr(build_ele, name)
        param_prop  = getattr(build_ele, handle_param_property.param_name)
        param_prop.value = value - float(handle_param_property.constant)
        return True


def initialize_control_properties(build_ele, ctrl_prop_util, doc,) -> None:
    for handle_param_name in filter(lambda prop_name: prop_name.startswith(pp.src.handles.Handle.name), dir(build_ele)):
        handle_param_property = getattr(build_ele, handle_param_name)
        if hasattr(handle_param_property, "min_value"):
            ctrl_prop_util.set_min_value(handle_param_property.param_name, handle_param_property.min_value)
        if hasattr(handle_param_property, "max_value"):
            ctrl_prop_util.set_min_value(handle_param_property.param_name, handle_param_property.max_value)
