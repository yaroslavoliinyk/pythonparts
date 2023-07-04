import pytest


def test_coords():
    from pythonparts import geometry as geo
    import NemAll_Python_Geometry as AllplanGeo

    p1 = AllplanGeo.Point3D(0, 0, 0)
    p2 = AllplanGeo.Point3D(1, 0, 0)

    coords = geo.Coords(p1, p2)

    assert repr(coords) == "Coords(start_point=Point3D(0, 0, 0), end_point=Point3D(1, 0, 0))"


def test_coords_start_point():
    from pythonparts import geometry as geo
    import NemAll_Python_Geometry as AllplanGeo

    p1 = AllplanGeo.Point3D(15, 22, -4)
    p2 = AllplanGeo.Point3D(1, 0, 0)

    coords = geo.Coords(p1, p2)

    assert coords.start_point == AllplanGeo.Point3D(15, 22, -4)


def test_coords_end_point():
    from pythonparts import geometry as geo
    import NemAll_Python_Geometry as AllplanGeo

    p1 = AllplanGeo.Point3D(15, 22, -4)
    p2 = AllplanGeo.Point3D(12, 110, 1110)

    coords = geo.Coords(p1, p2)

    assert coords.end_point == AllplanGeo.Point3D(12, 110, 1110)


def test_coords_start_point_None():
    from pythonparts import geometry as geo
    import NemAll_Python_Geometry as AllplanGeo

    p1 = AllplanGeo.Point3D(15, 22, -4)
    p2 = AllplanGeo.Point3D(12, 110, 1110)

    coords = geo.Coords(p1, p2)
    with pytest.raises(TypeError):
        coords.start_point = None


def test_coords_end_point_None():
    from pythonparts import geometry as geo
    import NemAll_Python_Geometry as AllplanGeo

    p1 = AllplanGeo.Point3D(15, 22, -4)
    p2 = AllplanGeo.Point3D(12, 110, 1110)

    coords = geo.Coords(p1, p2)
    with pytest.raises(TypeError):
        coords.end_point = None


def test_coords_end_point_other():
    from pythonparts import geometry as geo
    import NemAll_Python_Geometry as AllplanGeo

    p1 = AllplanGeo.Point3D(15, 22, -4)
    p2 = AllplanGeo.Point3D(12, 110, 1110)

    coords = geo.Coords(p1, p2)
    with pytest.raises(TypeError):
        coords.end_point = "1, 2, 4"


# def test_coords_start_point_move():
#     from pythonparts import geometry as geo
#     import NemAll_Python_Geometry as AllplanGeo

#     p1 = AllplanGeo.Point3D(15, 22, -4)
#     p2 = AllplanGeo.Point3D(12, 110, 1110)

#     coords = geo.Coords(p1, p2)
#     coords.move_start_point(AllplanGeo.Vector3D(40, 0, -40))
    
#     assert coords.start_point == AllplanGeo.Point3D(55, 22, -44)


# def test_coords_start_point_move_err():
#     from pythonparts import geometry as geo
#     import NemAll_Python_Geometry as AllplanGeo

#     p1 = AllplanGeo.Point3D(15, 22, -4)
#     p2 = AllplanGeo.Point3D(12, 110, 1110)

#     coords = geo.Coords(p1, p2)
#     with pytest.raises(TypeError):
#         coords.move_start_point(AllplanGeo.Point3D(40, 0, -40))
    

# def test_coords_end_point_move():
#     from pythonparts import geometry as geo
#     import NemAll_Python_Geometry as AllplanGeo

#     p1 = AllplanGeo.Point3D(15, 22, -4)
#     p2 = AllplanGeo.Point3D(12, 110, 1110)

#     coords = geo.Coords(p1, p2)
#     coords.move_end_point(AllplanGeo.Vector3D(4, 50, -40))
    
#     assert coords.end_point == AllplanGeo.Point3D(16, 160, 1070)


# def test_coords_end_point_move_err():
#     from pythonparts import geometry as geo
#     import NemAll_Python_Geometry as AllplanGeo

#     p1 = AllplanGeo.Point3D(15, 22, -4)
#     p2 = AllplanGeo.Point3D(12, 110, 1110)

#     coords = geo.Coords(p1, p2)
#     with pytest.raises(TypeError):
#         coords.move_end_point(AllplanGeo.Point3D(40, 0, -40))
    