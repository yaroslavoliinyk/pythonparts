import pytest

import random

from pythonparts import geometry as geo
import NemAll_Python_Geometry as AllplanGeo


pytest.mark.debug_this = pytest.mark.marker('debug_this')    # type: ignore


@pytest.fixture()
def clear_scene():
    print('Clearing Scene')
    geo.Scene._instance = None
    geo.Scene.build_ele = None

    yield

    print('After Scene Test')

# @pytest.fixture()
# def random_point(scope='function'):
#     randX = random.uniform(MIN_COORD, MAX_COORD)
#     randY = random.uniform(MIN_COORD, MAX_COORD)
#     randZ = random.uniform(MIN_COORD, MAX_COORD)

#     return AllplanGeo.Point3D(randX, randY, randZ)
