import pythonparts as pp

from typing import overload, Tuple


def create_scene(build_ele) -> pp.geometry.Scene: ...

@overload
def create_cuboid(width: float, length: float, height: float) -> pp.geometry.Cuboid: ...

@overload
def create_cuboid(be_name: str) -> pp.geometry.Cuboid: ...
