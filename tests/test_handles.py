import pytest
import random

from pythonparts.src import geometry as geo, AttributePermissionError, utils as pp_utils
from pythonparts import create_cuboid, create_scene

import NemAll_Python_Geometry as AllplanGeo
import utils


class TestConcreteHandles:

    """
        We need real build_ele. Without it we cannot test handles.
        But I still can test to some point.
    """

    def test_start_end(self):
        scene = create_scene('build_ele')

        column = create_cuboid(10, 200, 500)
        slab = create_cuboid(width=400, 
                            length=200, 
                            height=50,
        )
        column.union(slab, top=0)
        column.add_handle('SlabDist').start(right=0).end(right=0, top=slab.height)

        scene.place(column)
        print(column.handles[0].start_point)
        print(column.handles[0].end_point)
        assert True


# tch = TestConcreteHandles()
# tch.test_start_end()