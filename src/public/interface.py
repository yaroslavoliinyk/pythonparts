import pythonparts as pp

from typing import Tuple, Union, Optional
from numbers import Real


def create_scene(build_ele):
    """
    The function "create_scene" creates a geometry scene using the input build element.
    
    :param build_ele: The parameter "build_ele" is likely an input that represents the elements or
    objects that will be included in the scene. It could be a list, dictionary, or any other data
    structure that contains information about the objects to be included in the scene
    :return: a pp.src.geometry.Scene object.
    """
    return pp.src.geometry.Scene(build_ele)

def create_cuboid(param1, param2=0., param3=0.):
    """
    The function `create_cuboid` creates a cuboid object with the given dimensions or returns a string
    if the first parameter is a string.
    
    :param param1: The first parameter, `param1`, represents the width of the cuboid
    :param param2: param2 is an optional parameter that represents the length of the cuboid. If no value
    is provided for param2, it defaults to 0
    :param param3: The `param3` parameter represents the height of the cuboid
    :return: The function `create_cuboid` returns a cuboid object from the `pp.src.geometry.Cuboid`
    class if the parameters `param1`, `param2`, and `param3` are all real numbers. If `param1` is a
    string, it returns the string "Cuboid: build_ele". If none of these conditions are met, it raises a
    `NotImplemented
    """
    if isinstance(param1, str):
        return f"Cuboid: build_ele"
    if isinstance(param1, Real) and isinstance(param2, Real) and isinstance(param3, Real):
        width, length, height = param1, param2, param3
        return pp.src.geometry.Cuboid(width, length, height)
    
    raise NotImplemented()
