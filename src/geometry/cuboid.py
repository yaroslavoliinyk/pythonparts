import copy

from .space import Space, AllplanGeo


class Cuboid:

    def __init__(self, width, length, height):
        self.space = Space.from_dimensions(width, length, height)

    @property
    def width(self):
        return self.space.width

    @property
    def length(self):
        return self.space.length

    @property
    def height(self):
        return self.space.height

    def place(self, child_cuboid: "Cuboid", center: bool=False, **concov_kwargs):
        self.space.place(child_cuboid.space, concov_dict=concov_kwargs, center=center,)

    def build(self):
        return AllplanGeo.Polyhedron3D.CreateCuboid(self.global_.start_point, self.global_.end_point)

    def __repr__(self):
        return repr(self.space)
