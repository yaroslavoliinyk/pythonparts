import copy

from .space import Space, AllplanGeo


class Cuboid(Space):

    def __init__(self, width, length, height):
        space_coords = Space.from_points(AllplanGeo.Point3D(), AllplanGeo.Point3D(width, length, height), AllplanGeo.Point3D())
        super().__init__(space_coords)

    def build(self):
        return AllplanGeo.Polyhedron3D.CreateCuboid(self.global_.start_point, self.global_.end_point)
