import pytest
import random

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
          zero_point()]

# print(points)
print(list(zip(random.sample(points, len(points)), random.sample(points, len(points)))))