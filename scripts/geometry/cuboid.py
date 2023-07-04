import copy

from .space import Space, AllplanGeo
from .coords import Coords, SpaceCoords


class Cuboid(Space):

    def __init__(self, width, length, height):
        global_coords = Coords(AllplanGeo.Point3D(), AllplanGeo.Point3D(width, length, height))
        local_coords = Coords(AllplanGeo.Point3D(), AllplanGeo.Point3D(width, length, height))
        space_coords = SpaceCoords(local_coords, global_coords)
        super().__init__(space_coords)

    def build(self):
        return AllplanGeo.Polyhedron3D.CreateCuboid(self.coords.global_.start_point, self.coords.global_.end_point)