from .space import Space, AllplanGeo
from ..properties import com_prop as cp


class Cuboid(Space):
    """
    Essentially a Polyhedron3D that's flexible because of child-parent relations with other ``Cuboid`` s.
    Can be easily adjusted on a ``Scene`` and built or used as space/boundary for other objects(like Reinforcement).
    """

    def __init__(self, width, length, height, global_start_pnt=None, com_prop=None):
        """
        Can be defined with ``width``, ``length`` and ``height`` and placed at a given global point (default == ``Point3D(0, 0, 0)`` )
        Specific ``CommonProperties`` can also be added (default == ``com_prop.GetGlobalProperties()``)
        """
        super().__init__(width, length, height, global_start_pnt)
        if com_prop is None:
            com_prop = cp.global_properties()
        self.__com_prop = com_prop

    @property
    def polyhedron(self):
        return AllplanGeo.Polyhedron3D.CreateCuboid(self.global_.start_point, self.global_.end_point)

    @property
    def com_prop(self):
        """
        Returning the basic set ``CommonProperties`` object of given ``Cuboid``
        """
        return self.__com_prop
