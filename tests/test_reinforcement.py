
import pytest
import random

from pythonparts.src import geometry as geo, AttributePermissionError, utils as pp_utils
from pythonparts import create_cuboid, create_scene, create_stirrup_shape

import NemAll_Python_Geometry as AllplanGeo
import utils


class TestLongbars:

    def test_add_longbars(self):
        scene = create_scene(build_ele="build_ele")

        column = create_cuboid(width=400, 
                                length=2000, 
                                height=800,
        )
        slab = create_cuboid(width=1000, 
                                length=2000, 
                                height=200,
        )

        column.union(slab, top=0)
        # invoke identificator when min/max value is set
     
        column.add_longbars(along_axis="y",
                            concrete_grade=4,
                            steel_grade=4,
                            bending_roller=4.0,
                            diameter=8.0,
                            split_by_count=True,
                            # split_by_spacing=False,
                            count=10,
                            add_back_hook=True,
                            back_hook_length=100,
                            add_front_hook=True,
                            front_hook_length=50).\
        start(top=0, left=0, front=15.).\
        end(bottom=0, left=0, back=10.)

        scene.place(column)
        # pp, handles = scene.pythonpart, scene.handles
        assert True
    
    
    def test_add_longbars2(self):
        scene = create_scene(build_ele="build_ele")

        column = create_cuboid(width=400, 
                                length=2000, 
                                height=800,
        )
        slab = create_cuboid(width=1000, 
                                length=2000, 
                                height=200,
        )

        column.union(slab, top=0)
        # invoke identificator when min/max value is set
     
        column.add_longbars(along_axis="y",
                            concrete_grade=4,
                            steel_grade=4,
                            bending_roller=4.0,
                            diameter=8.0,
                            split_by_count=True,
                            # split_by_spacing=False,
                            count=10,
                            add_back_hook=True,
                            back_hook_length=100,
                            add_front_hook=True,
                            front_hook_length=50).\
        start(right=0, front=15.).\
        end(top=0, right=0, back=10.)

        scene.place(column)
        # pp, handles = scene.pythonpart, scene.handles
        assert True


class TestStirrups:

    def test_add_stirrups(self):
        scene = create_scene(build_ele="build_ele")

        column = create_cuboid(width=400, 
                                length=2000, 
                                height=800,
        )
        slab = create_cuboid(width=1000, 
                                length=2000, 
                                height=200,
        )

        column.union(slab, top=0)

        stirrup_shape = create_stirrup_shape()
        stirrup_shape.add_point(AllplanGeo.Point3D(0, 0, column.height))
        stirrup_shape.add_point(AllplanGeo.Point3D(0, 0, 0))
        stirrup_shape.add_point(AllplanGeo.Point3D(column.width, 0, 0))
        stirrup_shape.add_point(AllplanGeo.Point3D(column.width, 0, column.height))

        column.add_stirrups(stirrup_shape,
                            along_axis="y",
                            concrete_grade=4,
                            steel_grade=4,
                            bending_roller=4.0,
                            diameter=8.0,
                            split_by_count=True,
                            # split_by_spacing=False,
                            count=10,).\
        start(top=0, left=0, front=15.).\
        end(bottom=0, left=0, back=10.)

        scene.place(column)
        # pp, handles = scene.pythonpart, scene.handles
        assert True

# ts = TestStirrups()
# ts.test_add_stirrups()