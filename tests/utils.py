import pytest
import random

from typing import List, Tuple

from pythonparts import geometry as geo
import NemAll_Python_Geometry as AllplanGeo


MIN_COORD = -1_000_000_000.0
MAX_COORD =  1_000_000_000.0


def random_point():
    randX = random.uniform(MIN_COORD, MAX_COORD)
    randY = random.uniform(MIN_COORD, MAX_COORD)
    randZ = random.uniform(MIN_COORD, MAX_COORD)

    return AllplanGeo.Point3D(randX, randY, randZ)


def unit_point_x():
    return AllplanGeo.Point3D(1, 0, 0)


def unit_point_y():
    return AllplanGeo.Point3D(0, 1, 0)


def unit_point_z():
    return AllplanGeo.Point3D(0, 0, 1)


def random_unit_point():
    random_axis = random.randint(0, 2)
    if random_axis == 0:
        return unit_point_x()
    elif random_axis == 1:
        return unit_point_y()
    elif random_axis == 2:
        return unit_point_z()
    else:
        raise ValueError('Incorrect random value')


def zero_point():
    return AllplanGeo.Point3D(0, 0, 0)


points = [random_point(), 
          unit_point_x(), 
          unit_point_y(), 
          unit_point_z(),
          random_unit_point(),
          zero_point()]
points_combinations = [(p1, p2) for p1, p2 in zip(random.sample(points, len(points)), random.sample(points, len(points)))]

# coords_combinations: List[geo.Coords] = [geo.Coords(p1, p2) for (p1, p2) in points_combinations]
# space_coords_combinations = [geo.SpaceCoords(from_poin(local=local_coords, global_=global_coords) 
#                              for local_coords, global_coords in 
#                              zip(random.sample(coords_combinations, len(coords_combinations)), 
#                                  random.sample(coords_combinations, len(coords_combinations)))]

# def random_coords():
#     return random.choice(coords_combinations)

# def random_space_coords():
#     return random.choice(space_coords_combinations)