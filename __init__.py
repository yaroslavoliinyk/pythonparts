import sys
# This is the location of NemAll Allplan scripts like NemAll_Python_Geometry, etc.
sys.path.append("C:\\Program Files\\Allplan\\Allplan\\2023\\Prg")    # TODO: Change it looking for libs and paths inside Redistry.

import NemAll_Python_Geometry as AllplanGeo    # type: ignore

from .src import geometry
from .src import AttributePermissionError
from .src import create_scene, create_cuboid
