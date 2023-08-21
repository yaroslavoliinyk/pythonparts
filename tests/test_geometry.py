import pytest
import random

from pythonparts.src import geometry as geo, AttributePermissionError, utils as pp_utils
from pythonparts import create_cuboid, create_scene

import NemAll_Python_Geometry as AllplanGeo
import utils


class TestSpace:

    def test_create_from_classmethod_equal(self):
        end_pnt = random.choice(utils.points)
        space1 = geo.Cuboid(
                            width=end_pnt.X, 
                            length=end_pnt.Y, 
                            height=end_pnt.Z)

        assert space1 == geo.Cuboid(
                                    width=end_pnt.X, 
                                    length=end_pnt.Y, 
                                    height=end_pnt.Z, 
                                    global_start_pnt=AllplanGeo.Point3D(0, 0, 0)
                                    )

    def test_length_width_height(self):
        end_pnt = random.choice(utils.points)
        global_start_pnt = random.choice(utils.points)
        space1 = geo.Cuboid(length=end_pnt.Y, 
                                                        width=end_pnt.X, 
                                                        height=end_pnt.Z, 
                                                        global_start_pnt=global_start_pnt)

        assert space1.length == abs(end_pnt.Y)
        assert space1.width == abs(end_pnt.X)
        assert space1.height == abs(end_pnt.Z)

    def test_set_lengt_width_height(self):
        end_pnt = random.choice(utils.points)
        global_start_pnt = random.choice(utils.points)
        space1 = geo.Cuboid(length=end_pnt.Y, 
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
        parent_space = geo.Cuboid(length=end_pnt.Y, 
                                width=end_pnt.X, 
                                height=end_pnt.Z, 
                                global_start_pnt=global_start_pnt)

        end_pnt          = utils.random_point()
        child_space = geo.Cuboid(length=end_pnt.Y, 
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
        assert pp_utils.equal_points(parent_space[0].global_.start_point, expected_child_global_start_pnt)
        assert pp_utils.equal_points(parent_space[0].global_.end_point, expected_child_global_end_pnt)

    def test_place2(self):
        end_pnt          = utils.random_point()
        global_start_pnt = utils.random_point()
        parent_space = geo.Cuboid(length=end_pnt.Y, 
                                                            width=end_pnt.X, 
                                                            height=end_pnt.Z, 
                                                            global_start_pnt=global_start_pnt)

        end_pnt          = utils.random_point()
        child_space = geo.Cuboid(length=end_pnt.Y, 
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

        parent_space.place(child_space, center=False, left=200., bottom=15.)

        # ------------ child space 2 place ---------------
        end_pnt          = utils.random_point()
        child_space2 = geo.Cuboid(length=end_pnt.Y, 
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

        parent_space.place(child_space2, center=True, front=200., left=1000.,)

        assert len(parent_space) == 2
        assert len(child_space) == 0
        assert len(child_space2) == 0
        assert pp_utils.equal_points(parent_space[0].global_.start_point, expected_child_global_start_pnt)
        assert pp_utils.equal_points(parent_space[0].global_.end_point, expected_child_global_end_pnt)
        assert pp_utils.equal_points(parent_space[1].global_.start_point, expected_child_global_start_pnt2)
        assert pp_utils.equal_points(parent_space[1].global_.end_point, expected_child_global_end_pnt2)

    # def test_build(self):
    #     pass

    # def test_union(self):
    #     pass


class TestConcreteCover:

    def test_init(self):
        with pytest.raises(TypeError):
            cc = geo.ConcreteCover()

    def test_from_kwargs(self):
        cc = geo.ConcreteCover.from_sides(left=200, top=-100)
        
        assert cc.left == 200
        assert cc.top == -100

    def test_opposite_sides(self):
        with pytest.raises(ValueError):
            cc = geo.ConcreteCover.from_sides(left=100, right=200)
    
    def test_opposite_sides2(self):
        # No exception should be here.
        cc = geo.ConcreteCover.from_sides(left=100, right=None)
        assert True


class TestCuboid:

    def test_init(self):
        cuboid = geo.Cuboid(10, 20, 30)
        assert cuboid.width == 10
        assert cuboid.length == 20
        assert cuboid.height == 30


class TestScene:

    def test_elements_number(self):
        scene = create_scene('empty_build_ele')
        column = create_cuboid(10, 10, 1000)
        slab   = create_cuboid(200, 200, 12)

        column.union(slab, bottom=300)
        scene.place(column)

        assert len(scene.model_ele_list) == 1

    def test_elements_number2(self):
        scene = create_scene('empty_build_ele')
        column = create_cuboid(10, 10, 1000)
        slab   = create_cuboid(200, 200, 12)

        column.place(slab, bottom=300)
        scene.place(column)

        assert len(scene.model_ele_list) == 2

    def test_elements_number3(self):
        scene = create_scene('empty_build_ele')
        column = create_cuboid(10, 10, 1000)
        slab   = create_cuboid(200, 200, 12)
        small_cube = create_cuboid(5, 5, 5)
        small_slab = create_cuboid(10, 10, 3)

        slab.union(small_cube, right=slab.length-2)
        slab.place(small_slab, bottom=-2)
        column.place(slab, bottom=300)
        scene.place(column)

        assert len(scene.model_ele_list) == 3
    
    def test_elements_number4(self):
        scene = create_scene('empty_build_ele')
        column = create_cuboid(10, 10, 1000)
        slab   = create_cuboid(200, 200, 12)
        small_cube = create_cuboid(5, 5, 5)
        small_slab = create_cuboid(10, 10, 3)

        slab.union(small_cube, right=slab.length-2)
        slab.place(small_slab, bottom=-2)
        column.union(slab, bottom=300)
        scene.place(column)

        assert len(scene.model_ele_list) == 2
    
    
    def test_elements_union_subtract(self):
        scene  = create_scene('build_ele')
        cuboid = create_cuboid(100, 100, 100)
        mini_cuboid = create_cuboid(10, 10, 300)
        cuboid.subtract(mini_cuboid)
        slab = create_cuboid(2000, 1300, 90)
        slab.place(cuboid, left=400)
        
        box = create_cuboid(250, 250, 400)
        roof = create_cuboid(500, 500, 50)

        box.union(roof, center=True, top=0)

        scene.place(slab, center=True)
        scene.place(box)

        assert len(scene.model_ele_list) == 3


    # def test_elements_visible(self):
    #     scene  = create_scene('build_ele')
       
    #     box = create_cuboid(250, 250, 400, visible=False)
    #     roof = create_cuboid(500, 500, 50)

    #     box.place(roof, center=True, top=0)

    #     scene.place(box)

    #     assert len(scene.model_ele_list) == 3


# ts = TestScene()
# ts.test_elements_visible()