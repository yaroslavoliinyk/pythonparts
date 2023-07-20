from .space import Space, AllplanGeo
from ..properties import com_prop as cp


# The Cuboid class represents a three-dimensional cuboid shape and includes methods for creating a
# cuboid polyhedron and accessing its common properties.
class Cuboid(Space):

    def __init__(self, width, length, height, global_start_pnt=None, com_prop=cp.global_properties()):
        super().__init__(width, length, height, global_start_pnt)
        self.__com_prop = com_prop

    @property
    def polyhedron(self):
        """
        The function creates a cuboid polyhedron using the start and end points.
        :return: The code is returning a polyhedron object created using the
        AllplanGeo.Polyhedron3D.CreateCuboid method.
        """
        return AllplanGeo.Polyhedron3D.CreateCuboid(self.global_.start_point, self.global_.end_point)

    @property
    def com_prop(self):
        """
        The above code defines a property called "com_prop" that returns the value of a private
        attribute "__com_prop".
        :return: The property `com_prop` is being returned.
        """
        return self.__com_prop
