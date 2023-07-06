import pytest
import random

from pythonparts import geometry as geo

import NemAll_Python_Geometry as AllplanGeo

import utils


class TestSpace:
    def test_equal(self):
        local_coords = random.choice(utils.coords_combinations)
        global_pnt = random.choice(utils.points_combinations)
        sc1 = geo.from_points(local_coords, global_pnt)
        space = geo.Space(sc1)

        assert space == geo.Space(geo.SpaceCoords(local_coords, global_coords))

    def test_coords(self):
        local_coords = random.choice(utils.coords_combinations)
        global_coords = random.choice(utils.coords_combinations)
        sc1 = geo.SpaceCoords(local_coords, global_coords)
        space = geo.Space(sc1)

        assert space.coords == sc1

    def test_length(self):
        sc = utils.random_space_coords()
        space = geo.Space(sc)

        assert space.length == sc.local.start_point

    def test_width(self):
        pass

    def test_height(self):
        pass

    def test_place1(self):
        pass

    def test_place2(self):
        pass

    def test_add_child(self):
        pass