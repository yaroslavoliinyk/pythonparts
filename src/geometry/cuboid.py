from .space import Space, AllplanGeo
from ..properties import com_prop as cp


class Cuboid(Space):

    def __init__(self, width, length, height, global_start_pnt=None, com_prop=cp.global_properties()):
        super().__init__(width, length, height, global_start_pnt)
        self.__com_prop = com_prop

    @property
    def polyhedron(self):
        return AllplanGeo.Polyhedron3D.CreateCuboid(self.global_.start_point, self.global_.end_point)

    @property
    def com_prop(self):
        return self.__com_prop
