import pytest
import random

from pythonparts import geometry as geo

import NemAll_Python_Geometry as AllplanGeo

import utils


points_combinations = utils.points_combinations
points              = utils.points


@pytest.mark.parametrize('p1, p2', points_combinations)
class TestCoords:

    def test_coords(self, p1, p2):
        coords = geo.Coords(p1, p2)
        assert repr(coords) == f"Coords(start_point={p1!r}, end_point={p2!r})"

    def test_coords_start_point(self, p1, p2):
        coords = geo.Coords(p1, p2)
        assert coords.start_point == p1

    def test_coords_end_point(self, p1, p2):
        coords = geo.Coords(p1, p2)
        assert coords.end_point == p2

    def test_coords_start_point_None(self, p1, p2):
        coords = geo.Coords(p1, p2)
        with pytest.raises(TypeError):
            coords.start_point = None

    def test_coords_end_point_None(self, p1, p2):
        coords = geo.Coords(p1, p2)
        with pytest.raises(TypeError):
            coords.end_point = None

    def test_coords_end_point_other(self, p1, p2):
        coords = geo.Coords(p1, p2)
        with pytest.raises(TypeError):
            coords.end_point = "1, 2, 4"

    def test_coords_start_point_move(self, p1, p2):
        coords = geo.Coords(p1, p2)
        vec = AllplanGeo.Vector3D(40, 0, -40)
        coords.move_start_point(vec)
        
        assert coords.start_point == p1 + vec

    def test_coords_start_point_move_err(self, p1, p2):
        coords = geo.Coords(p1, p2)
        with pytest.raises(TypeError):
            coords.move_start_point(AllplanGeo.Point3D(40, 0, -40))
        
    def test_coords_end_point_move(self, p1, p2):
        coords = geo.Coords(p1, p2)
        vec = AllplanGeo.Vector3D(4, 50, -40)
        coords.move_end_point(vec)
        
        assert coords.end_point == p2 + vec

    def test_coords_end_point_move_err(self, p1, p2):
        coords = geo.Coords(p1, p2)
        with pytest.raises(TypeError):
            coords.move_end_point(AllplanGeo.Point3D(40, 0, -40))
        
    def test_move_points(self, p1, p2):
        coords = geo.Coords(p1, p2)
        vec = AllplanGeo.Vector3D(100, 200, 300)
        coords.move(vec)
        
        assert coords.start_point == p1 + vec
        assert coords.end_point   == p2 + vec

    def test_move_points2(self, p1, p2):
        coords = geo.Coords(p1, p2)
        coords.move(AllplanGeo.Vector3D(0, 0, 0))
        
        assert coords.start_point == p1
        assert coords.end_point   == p2

    def test_move_incorrect_param(self, p1, p2):
        coords = geo.Coords(p1, p2)

        with pytest.raises(TypeError):
            coords.move(AllplanGeo.Point3D(10, 10, 10))

    def test_coords_equal(self, p1, p2):
        coords = geo.Coords(p1, p2)
        coords2 = geo.Coords(p1, p2)

        assert coords == coords2

    def test_coords_equal2(self, p1, p2):
        coords = geo.Coords(p1, p2)
        coords2             = geo.Coords(None, None)
        coords2.start_point = p1
        coords2.end_point   = p2

        assert coords == coords2

    def test_from_empty(self, p1, p2):
        coords = geo.Coords.from_empty()
        assert geo.Coords(None, None) == coords


    def test_coords_equal_move(self, p1, p2):
        coords = geo.Coords(p1, p2)
        vec = AllplanGeo.Vector3D(1, -10, -100)
        coords.move(vec)

        assert coords == geo.Coords(p1 + vec, p2 + vec)


# @pytest.mark.parametrize('p1, p2', points_combinations)
# class TestSpaceCoords:

#     def test_create_space_coords_directly(self, p1, p2):
#         lcoords = geo.Coords(p1, p2)
#         gcoords = geo.Coords(p1, p2)
        
#         with pytest.raises(TypeError):
#             space_coords = geo.SpaceCoords(local=lcoords, global_=gcoords)

#     def test_space_coords_equal(self, p1, p2):
#         space_coords = geo.SpaceCoords.from_local_points(p1, p2)

#         assert space_coords == geo.SpaceCoords.from_local_points(p1, p2)

#     def test_space_coords_equal_global(self, p1, p2):
#         global_pnt = random.choice(points)
#         space_coords = geo.SpaceCoords.from_points(p1, p2, global_pnt)
        
#         space_coords2 = geo.SpaceCoords.from_local_points(p1, p2)
#         space_coords2.set_global_start_pnt(global_pnt)

#         assert space_coords == space_coords2
