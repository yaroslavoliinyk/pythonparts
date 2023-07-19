import pythonparts as pp

from typing import Tuple, Union, Optional
from numbers import Real


def create_scene(build_ele):
    return pp.src.geometry.Scene(build_ele)

def create_cuboid(param1, param2=0., param3=0.):
    if isinstance(param1, str):
        return f"Cuboid: build_ele"
    if isinstance(param1, Real) and isinstance(param2, Real) and isinstance(param3, Real):
        width, length, height = param1, param2, param3
        return pp.src.geometry.Cuboid(width, length, height)
    
    raise NotImplemented()
