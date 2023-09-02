from typing import List

import NemAll_Python_BasisElements as AllplanBasisElements

from PythonPartUtil import PythonPartUtil
from CreateElementResult import CreateElementResult
from PythonPart import View2D3D, PythonPart

from .space import Space, AllplanGeo
from .cuboid import Cuboid
from .coords import Coords
from .concrete_cover import ConcreteCover
from ..reinforcement import Reinforcement
from ..utils import center_scene_calc
from ..properties import com_prop as cp



# The `Scene` class represents a 3D scene and provides methods for adding model elements and
# reinforcement elements to the scene.
class Scene:

    MAX_AXIS_UNIT = 1_000_000_000_000

    def __init__(self, build_ele):
        self.scene_space = Cuboid(self.MAX_AXIS_UNIT, self.MAX_AXIS_UNIT, self.MAX_AXIS_UNIT)
        self.build_ele = build_ele

    @property
    def model_ele_list(self) -> List[AllplanBasisElements.ModelElement3D]:
        """
        :return: Returns a list of AllplanBasisElements.ModelElement3D objects.
        """
        model_ele_list = []
        for model in self.scene_space._children:
            if isinstance(model, Cuboid):
                model_ele_list.extend(model.build())
        return model_ele_list

    @property
    def reinf_ele_list(self):
        """
        :return: a list of reinforcement elements.
        """
        reinf_ele_list = []
        for reinf in self.scene_space._children:
            if isinstance(reinf, Reinforcement):
                reinf_ele_list.extend(reinf.build())
        return reinf_ele_list

    @property
    def pythonpart(self):
        """
        Creates a Python part by adding 2D/3D views and reinforcement elements to
        the model element list and then creating the Python part using the build element.
        :return: an instance of the PythonPart.
        """
        
        ppart = self.PythonPart()
        return ppart.create(self.build_ele, self.model_ele_list, self.reinf_ele_list, cp.global_properties())

    @property
    def handles(self):
        handles = []
        for model in self.scene_space._children:
            handles.extend(model.build_handles(self))
        return handles

    @property
    def global_(self):
        return self.scene_space.global_

    # def update_child_global_coords(self, parent_global_coords: Coords):
    #     print("Updating!", parent_global_coords)
    #     self.scene_space.update_child_global_coords(parent_global_coords)

    def place(self, child_space: Space, center=False, visible=True, **concov_sides):
        """
        See explanation in :py:func:`pythonparts.geometry.Space.place`
        """
        concov = ConcreteCover(concov_sides)
        concov.right = None
        concov.top   = None
        concov.back  = None
        if center:
            concov.left, concov.front, concov.bottom = center_scene_calc(concov, child_space)
        self.scene_space.place(child_space, visible=visible, left=concov.left, front=concov.front, bottom=concov.bottom)
        # self.update_child_global_coords(self.scene_space.global_)


    class PythonPart:

        def create(self, build_ele, model_ele_list, reinf_ele_list, com_prop):
            """
            Create Object Pythonpart

            """
            pythonpart = PythonPart(
                str(self.__class__.__name__),
                parameter_list=build_ele.get_params_list(),
                hash_value=build_ele.get_hash(),
                python_file=build_ele.pyp_file_name,
                views=[View2D3D(model_ele_list)],
                reinforcement=reinf_ele_list,
                common_props=com_prop,
            )

            return pythonpart.create()


    def __repr__(self):
        return f"Scene(build_ele={self.build_ele!r})"

    def __str__(self):
        return f"Scene(children={[child for child in self.scene_space._children]})"

