import pytest
import random
import copy

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
        end_pnt          = utils.random_point()
        global_start_pnt = utils.random_point()
        parent_space = geo.Space.from_dimensions_global_point(length=end_pnt.Y, 
                                                            width=end_pnt.X, 
                                                            height=end_pnt.Z, 
                                                            global_start_pnt=global_start_pnt)

        end_pnt          = utils.random_point()
        child_space = geo.Space.from_dimensions(length=end_pnt.Y, 
                                                width=end_pnt.X, 
                                                height=end_pnt.Z,)
        
        expected_child_global_start_pnt = AllplanGeo.Point3D(parent_space.global_.start_point)
        expected_child_global_end_pnt = AllplanGeo.Point3D(parent_space.global_.end_point)
        child_width = child_space.width
        child_length = child_space.length
        child_height = child_space.height
        
        parent_space.place(child_space, center=False, left=200., bottom=15.,)

        expected_child_global_start_pnt.X = parent_space.global_.start_point.X + 200.
        expected_child_global_end_pnt.X   = expected_child_global_start_pnt.X + child_width
        expected_child_global_start_pnt.Z = parent_space.global_.start_point.Z + 15
        expected_child_global_end_pnt.Z   = expected_child_global_start_pnt.Z + child_height
        expected_child_global_start_pnt.Y = parent_space.global_.start_point.Y
        expected_child_global_end_pnt.Y   = expected_child_global_start_pnt.Y + child_length

        assert len(parent_space) == 1
        assert len(child_space) == 0
        assert parent_space[0].global_.start_point == expected_child_global_start_pnt
        assert parent_space[0].global_.end_point == expected_child_global_end_pnt

    def test_place2(self):
        end_pnt          = utils.random_point()
        global_start_pnt = utils.random_point()
        parent_space = geo.Space.from_dimensions_global_point(length=end_pnt.Y, 
                                                            width=end_pnt.X, 
                                                            height=end_pnt.Z, 
                                                            global_start_pnt=global_start_pnt)

        end_pnt          = utils.random_point()
        child_space = geo.Space.from_dimensions(length=end_pnt.Y, 
                                                width=end_pnt.X, 
                                                height=end_pnt.Z,)
        
        # ------------ child space 1 place ---------------
        expected_child_global_start_pnt = AllplanGeo.Point3D(parent_space.global_.start_point)
        expected_child_global_end_pnt = AllplanGeo.Point3D(parent_space.global_.end_point)
        child_width = child_space.width
        child_length = child_space.length
        child_height = child_space.height
        
        expected_child_global_start_pnt.X = parent_space.global_.start_point.X + 200.
        expected_child_global_end_pnt.X   = expected_child_global_start_pnt.X + child_width
        expected_child_global_start_pnt.Z = parent_space.global_.start_point.Z + 15
        expected_child_global_end_pnt.Z   = expected_child_global_start_pnt.Z + child_height
        expected_child_global_start_pnt.Y = parent_space.global_.start_point.Y
        expected_child_global_end_pnt.Y   = expected_child_global_start_pnt.Y + child_length

        parent_space.place(child_space, center=False, left=200., bottom=15.,)

        # ------------ child space 2 place ---------------
        end_pnt          = utils.random_point()
        child_space2 = geo.Space.from_dimensions(length=end_pnt.Y, 
                                                width=end_pnt.X, 
                                                height=end_pnt.Z,)
        expected_child_global_start_pnt2 = AllplanGeo.Point3D(parent_space.global_.start_point)
        expected_child_global_end_pnt2 = AllplanGeo.Point3D(parent_space.global_.end_point)
        child_width = child_space2.width
        child_length = child_space2.length
        child_height = child_space2.height

        expected_child_global_start_pnt2.X = parent_space.global_.start_point.X + 1000.
        expected_child_global_end_pnt2.X   = expected_child_global_start_pnt2.X + child_width
        expected_child_global_start_pnt2.Y = parent_space.global_.start_point.Y + 200.
        expected_child_global_end_pnt2.Y   = expected_child_global_start_pnt2.Y + child_length

        parent_z_delta = parent_space.height/2.
        child_z_delta  = child_height/2.
        expected_child_global_start_pnt2.Z = parent_space.global_.start_point.Z + (parent_z_delta - child_z_delta)
        expected_child_global_end_pnt2.Z   = expected_child_global_start_pnt2.Z + child_height

        parent_space.place(child_space2, center=True, front=200., left=1000.)

        assert len(parent_space) == 2
        assert len(child_space) == 0
        assert len(child_space2) == 0
        assert parent_space[0].global_.start_point == expected_child_global_start_pnt
        assert parent_space[0].global_.end_point == expected_child_global_end_pnt
        assert parent_space[1].global_.start_point == expected_child_global_start_pnt2
        assert parent_space[1].global_.end_point == expected_child_global_end_pnt2

    def test_add_child(self):
        end_pnt          = utils.random_point()
        global_start_pnt = utils.random_point()
        parent_space = geo.Space.from_dimensions_global_point(length=end_pnt.Y, 
                                                            width=end_pnt.X, 
                                                            height=end_pnt.Z, 
                                                            global_start_pnt=global_start_pnt)
        
        end_pnt1          = utils.random_point()
        child_space1 = geo.Space.from_dimensions(length=end_pnt1.Y, 
                                                width=end_pnt1.X, 
                                                height=end_pnt1.Z,)
        
        end_pnt2          = utils.random_point()
        child_space2 = geo.Space.from_dimensions(length=end_pnt2.Y, 
                                                width=end_pnt2.X, 
                                                height=end_pnt2.Z,)
        
        end_pnt3          = utils.random_point()
        grandchild_space3 = geo.Space.from_dimensions(length=end_pnt3.Y, 
                                                width=end_pnt3.X, 
                                                height=end_pnt3.Z,)
        
        child_space2._add_child(grandchild_space3)
        parent_space._add_child(child_space1)
        parent_space._add_child(child_space2)

        # ------------------------- Expected values ---------------------
        expected_child_space2 = geo.Space.from_dimensions(length=end_pnt2.Y, 
                                                        width=end_pnt2.X, 
                                                        height=end_pnt2.Z,)
        expected_grandchild_space3 = geo.Space.from_dimensions(length=end_pnt3.Y, 
                                                width=end_pnt3.X, 
                                                height=end_pnt3.Z,)
        expected_child_space1 = geo.Space.from_dimensions(length=end_pnt1.Y, 
                                                width=end_pnt1.X, 
                                                height=end_pnt1.Z,)
        expected_parent_space = geo.Space.from_dimensions_global_point(length=end_pnt.Y, 
                                                            width=end_pnt.X, 
                                                            height=end_pnt.Z, 
                                                            global_start_pnt=global_start_pnt)
        
        expected_child_space2._add_child(expected_grandchild_space3)
        expected_parent_space._add_child(expected_child_space1)
        expected_parent_space._add_child(expected_child_space2)

        assert len(parent_space) == 2
        assert len(child_space1) == 0
        assert len(child_space2) == 1
        assert parent_space == expected_parent_space
        assert child_space1 == expected_child_space1
        assert child_space2 == expected_child_space2
        assert grandchild_space3 == expected_grandchild_space3



class TestConcreteCover:

    def test_init(self):
        with pytest.raises(TypeError):
            cc = geo.ConcreteCover()

    def test_from_kwargs(self):
        cc = geo.ConcreteCover.from_kwargs(left=200, top=-100)
        
        assert cc.left == 200
        assert cc.top == -100

    def test_opposite_sides(self):
        with pytest.raises(ValueError):
            cc = geo.ConcreteCover.from_kwargs(left=100, right=200)
    
    def test_opposite_sides2(self):
        # No exception should be here.
        cc = geo.ConcreteCover.from_kwargs(left=100, right=0.0)
        assert True


class TestCuboid:

    def test_init(self):
        cuboid = geo.Cuboid(10, 20, 30)
        assert cuboid.width == 10
        assert cuboid.length == 20
        assert cuboid.height == 30


class TestScene:

    def test_get_instance(self, clear_scene):
        scene = geo.Scene.get_instance("build_element")
        assert len(scene.model_ele_list) == 0

    def test_two_scenes_create(self, clear_scene):
        scene1 = geo.Scene()
        with pytest.raises(TypeError):
            scene2 = geo.Scene()

 
    