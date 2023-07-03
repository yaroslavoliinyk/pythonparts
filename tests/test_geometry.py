import pytest


def test_coords():
    from pythonparts import geometry as geo
    import NemAll_Python_Geometry as AllplanGeo

    p1 = AllplanGeo.Point3D(0, 0, 0)
    p2 = AllplanGeo.Point3D(1, 0, 0)

    coords = geo.Coords(p1, p2)

    assert repr(coords) == "Coords(start_point=Point3D(0, 0, 0), end_point=Point3D(1, 0, 0))"
