import os
import sys

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

# This is the location of NemAll Allplan scripts like NemAll_Python_Geometry, etc.
sys.path.append("C:\\Program Files\\Allplan\\Allplan\\2023\\Prg")    # TODO: Change it looking for libs and paths inside Redistry.

from scripts import geometry

scene = geometry.Scene.get_instance('my build_ele')
print(scene)

column = geometry.Cuboid(10, 20, 100)
print(column)
scene.place(column, left=20, back=200, bottom=1000)
print(column)

slab = geometry.Cuboid(5, 20, 30)
print(slab)
column.place(slab, left=10, front=50)
print(slab)