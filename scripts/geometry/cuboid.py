import copy

from .space import Space, AllplanGeo


class Cuboid:

    def __init__(self, width, length, height):
        self.space = Space.from_points(AllplanGeo.Point3D(), AllplanGeo.Point3D(width, length, height), AllplanGeo.Point3D())

    def build(self):
        return AllplanGeo.Polyhedron3D.CreateCuboid(self.global_.start_point, self.global_.end_point)
