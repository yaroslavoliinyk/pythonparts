import typing

from ..scripts import geometry


class Factory:

    def create_scene(build_ele):
        return geometry.Scene.get_instance(build_ele)
    
   
    def create_cuboid(self, be_name):
        return geometry.Cuboid(be_name)
    
    @typing.overload
    def create_cuboid(self, width: float, height: float, length: float):
        return geometry.Cuboid(width, height, length)
