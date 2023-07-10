import pytest
import random

from pythonparts import geometry as geo, AttributePermissionError

import NemAll_Python_Geometry as AllplanGeo

import utils


class TestSpace:
    def test_create_init(self):
        with pytest.raises(TypeError):
            sample_point = random.choice(utils.points)
            space = geo.Space(sample_point, sample_point)

    def test_create_from_classmethod_equal(self):
        end_pnt = random.choice(utils.points)
        space1 = geo.Space.from_dimensions(length=end_pnt.Y, 
                                           width=end_pnt.X, 
                                           height=end_pnt.Z)

        assert space1 == geo.Space.from_dimensions_global_point(length=end_pnt.Y, 
                                                                width=end_pnt.X, 
                                                                height=end_pnt.Z, 
                                                                global_start_pnt=AllplanGeo.Point3D(0, 0, 0)
                                                                )

    def test_from_points_set_global(self):
        end_pnt          = random.choice(utils.points)
        global_start_pnt = random.choice(utils.points)
        space1 = geo.Space.from_dimensions_global_point(length=end_pnt.Y, 
                                                        width=end_pnt.X, 
                                                        height=end_pnt.Z, 
                                                        global_start_pnt=global_start_pnt)

        space2 = geo.Space.from_dimensions(length=end_pnt.Y, 
                                            width=end_pnt.X, 
                                            height=end_pnt.Z,)
        space2.set_global_start_pnt(global_start_pnt)

        assert space1 == space2

    def test_length_width_height(self):
        end_pnt = random.choice(utils.points)
        global_start_pnt = random.choice(utils.points)
        space1 = geo.Space.from_dimensions_global_point(length=end_pnt.Y, 
                                                        width=end_pnt.X, 
                                                        height=end_pnt.Z, 
                                                        global_start_pnt=global_start_pnt)

        assert space1.length == abs(end_pnt.Y)
        assert space1.width == abs(end_pnt.X)
        assert space1.height == abs(end_pnt.Z)

    def test_set_lengt_width_height(self):
        end_pnt = random.choice(utils.points)
        global_start_pnt = random.choice(utils.points)
        space1 = geo.Space.from_dimensions_global_point(length=end_pnt.Y, 
                                                        width=end_pnt.X, 
                                                        height=end_pnt.Z, 
                                                        global_start_pnt=global_start_pnt)

        with pytest.raises(AttributePermissionError):
            space1.length = 1
        with pytest.raises(AttributePermissionError):
            space1.width = 1
        with pytest.raises(AttributePermissionError):
            space1.height = 1

    def test_place1(self):
        pass

    def test_place2(self):
        pass

    def test_add_child(self):
        pass