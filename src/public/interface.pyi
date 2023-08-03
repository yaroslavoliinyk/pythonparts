import pythonparts as pp

from typing import overload, Tuple


def create_scene(build_ele): 
    """
    The function "create_scene" creates a geometry scene using the input build element.
    
    :param build_ele: The parameter "build_ele" is likely an input that represents the elements or
    objects that will be included in the scene. It could be a list, dictionary, or any other data
    structure that contains information about the objects to be included in the scene
    :return: a pp.src.geometry.Scene object.
    """

@overload
def create_cuboid(width: float, length: float, height: float): 
    """
    The function `create_cuboid` creates a cuboid object with the given dimensions.
    
    :param param1: The first parameter, `param1`, represents the width of the cuboid
    :param param2: The second parameter, `param2`, represents the length of the cuboid
    :param param3: The `param3` parameter represents the height of the cuboid
    :return: The function `create_cuboid` returns a cuboid object from the `pp.src.geometry.Cuboid`
    class if the parameters `param1`, `param2`, and `param3` are all real numbers. 
    """

@overload
def create_cuboid(be_name: str): 
    """
    Create cuboid with build_ele parameters
    """
