from .space import Space, AllplanGeo
from ..properties import com_prop as cp
from ..utils import (check_correct_axis,
                     get_diagonal_plane,)


class Cuboid(Space):
    """
        Essentially a Polyhedron3D that's flexible because of child-parent relations with other ``Cuboid`` .
        Can be easily adjusted on a ``Scene`` and built or used as space/boundary for other objects(like Reinforcement).
    """

    def __init__(self, width, length, height, global_start_pnt=None, visible=True, com_prop=None):
        super().__init__(width, length, height, global_start_pnt=global_start_pnt, visible=visible)
        self.cut_along_axis = None
        self.cut_by_main_diagonal = True
        self.below_diagonal = True
        if com_prop is None:
            com_prop = cp.global_properties()
        self.__com_prop = com_prop

    
    @property
    def polyhedron(self):
        """
            :return: ``AllplanGeo.Polyhedron3D`` created with ``AllplanGeo.Polyhedron3D.CreateCuboid``
        """
        if not self.visible:
            return AllplanGeo.Polyhedron3D()
        cuboid = AllplanGeo.Polyhedron3D.CreateCuboid(self.global_.start_point, self.global_.end_point)
        
        if self.cut_along_axis is not None:
            (is_cut,
            above_plane_polyhedron, 
            below_plane_polyhedron) = \
                AllplanGeo.CutPolyhedronWithPlane(cuboid, 
                                                  get_diagonal_plane(self.global_, 
                                                                     self.cut_along_axis, 
                                                                     self.cut_by_main_diagonal
                                                                     )
                                                )
            if not is_cut:
                raise ValueError("Could not cut Polyhedron. Check cut_diagonally() parameters or contact developer.")
            return below_plane_polyhedron if self.below_diagonal else above_plane_polyhedron
        
        return cuboid  
    
    @property
    def polyhedron_transformed(self):
        """
            :return: ``AllplanGeo.Polyhedron3D`` created with ``AllplanGeo.Polyhedron3D.CreateCuboid``
        """
        polyhedron = self.polyhedron
        tfs_reversed = [] if not self.transformations else self.transformations[::-1]
        for tf in tfs_reversed:
            polyhedron = tf.transform(polyhedron)
        return polyhedron

    @property
    def com_prop(self):
        """
        Returning the basic set ``CommonProperties`` object of given ``Cuboid``
        """
        return self.__com_prop

    def cut_cuboid_diagonally(self, along_axis: str, main_diagonal: bool=True, below_diagonal: bool=True):
        """
            :along_axis: Along which axis to cut: Ox, Oy, Oz
            :diagonal: Either 0 or 1. If 0, Cut by the main diagonal. If 1 - cut by the other diagonal. 
        """
        self.cut_along_axis = check_correct_axis(along_axis)
        self.cut_by_main_diagonal   = main_diagonal
        self.below_diagonal = below_diagonal

    def get_face(self, side_name):
        return self.polyhedron.GetFace(0)

    def __str__(self):
        return f"Cuboid(width={self.width}, length={self.length}, height={self.height})"
