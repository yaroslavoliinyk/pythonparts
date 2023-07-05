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


def test_coords_start_point_move():
    from pythonparts import geometry as geo
    import NemAll_Python_Geometry as AllplanGeo

    p1 = AllplanGeo.Point3D(15, 22, -4)
    p2 = AllplanGeo.Point3D(12, 110, 1110)

    coords = geo.Coords(p1, p2)
    coords.move_start_point(AllplanGeo.Vector3D(40, 0, -40))
    
    assert coords.start_point == AllplanGeo.Point3D(55, 22, -44)


def test_coords_start_point_move_err():
    from pythonparts import geometry as geo
    import NemAll_Python_Geometry as AllplanGeo

    p1 = AllplanGeo.Point3D(15, 22, -4)
    p2 = AllplanGeo.Point3D(12, 110, 1110)

    coords = geo.Coords(p1, p2)
    with pytest.raises(TypeError):
        coords.move_start_point(AllplanGeo.Point3D(40, 0, -40))
    

def test_coords_end_point_move():
    from pythonparts import geometry as geo
    import NemAll_Python_Geometry as AllplanGeo

    p1 = AllplanGeo.Point3D(15, 22, -4)
    p2 = AllplanGeo.Point3D(12, 110, 1110)

    coords = geo.Coords(p1, p2)
    coords.move_end_point(AllplanGeo.Vector3D(4, 50, -40))
    
    assert coords.end_point == AllplanGeo.Point3D(16, 160, 1070)


def test_coords_end_point_move_err():
    from pythonparts import geometry as geo
    import NemAll_Python_Geometry as AllplanGeo

    p1 = AllplanGeo.Point3D(15, 22, -4)
    p2 = AllplanGeo.Point3D(12, 110, 1110)

    coords = geo.Coords(p1, p2)
    with pytest.raises(TypeError):
        coords.move_end_point(AllplanGeo.Point3D(40, 0, -40))
    

def test_move_points():
    from pythonparts import geometry as geo
    import NemAll_Python_Geometry as AllplanGeo

    p1 = AllplanGeo.Point3D(15, 22, -4)
    p2 = AllplanGeo.Point3D(12, 110, 1110)
    coords = geo.Coords(p1, p2)

    coords.move(AllplanGeo.Vector3D(100, 200, 300))
    
    assert coords.start_point == AllplanGeo.Point3D(115, 222, 296)
    assert coords.end_point   == AllplanGeo.Point3D(112, 310, 1410)


def test_move_points2():
    from pythonparts import geometry as geo
    import NemAll_Python_Geometry as AllplanGeo

    p1 = AllplanGeo.Point3D(15, 22, -4)
    p2 = AllplanGeo.Point3D(12, 110, 1110)
    coords = geo.Coords(p1, p2)

    coords.move(AllplanGeo.Vector3D(0, 0, 0))
    
    assert coords.start_point == AllplanGeo.Point3D(15, 22, -4)
    assert coords.end_point   == AllplanGeo.Point3D(12, 110, 1110)


def test_move_incorrect_param():
    from pythonparts import geometry as geo
    import NemAll_Python_Geometry as AllplanGeo

    p1 = AllplanGeo.Point3D(15, 22, -4)
    p2 = AllplanGeo.Point3D(12, 110, 1110)
    coords = geo.Coords(p1, p2)

    with pytest.raises(TypeError):
        coords.move(AllplanGeo.Point3D(10, 10, 10))


def test_coords_equal():
    from pythonparts import geometry as geo
    import NemAll_Python_Geometry as AllplanGeo

    p1 = AllplanGeo.Point3D(15, 22, -4)
    p2 = AllplanGeo.Point3D(12, 110, 1110)
    coords = geo.Coords(p1, p2)

    coords2 = geo.Coords(p1, p2)

    assert coords == coords2


def test_coords_equal2():
    from pythonparts import geometry as geo
    import NemAll_Python_Geometry as AllplanGeo

    p1 = AllplanGeo.Point3D(15, 22, -4)
    p2 = AllplanGeo.Point3D(12, 110, 1110)
    coords = geo.Coords(p1, p2)

    coords2             = geo.Coords(None, None)
    coords2.start_point = p1
    coords2.end_point   = p2

    assert coords == coords2


def test_from_empty():
    from pythonparts import geometry as geo
    import NemAll_Python_Geometry as AllplanGeo

    coords = geo.Coords.from_empty()

    assert geo.Coords(None, None) == coords


def test_coords_equal_move():
    from pythonparts import geometry as geo
    import NemAll_Python_Geometry as AllplanGeo

    p1 = AllplanGeo.Point3D(15, 22, -4)
    p2 = AllplanGeo.Point3D(12, 110, 1110)
    coords = geo.Coords(p1, p2)

    coords.move(AllplanGeo.Vector3D(1, -10, -100))

    assert coords == geo.Coords(AllplanGeo.Point3D(16, 12, -104), AllplanGeo.Point3D(13, 100, 1010))

def test_space_coords_equal():
    from pythonparts import geometry as geo
    import NemAll_Python_Geometry as AllplanGeo

    p1 = AllplanGeo.Point3D(15, 22, -4)
    p2 = AllplanGeo.Point3D(12, 110, 1110)
    lcoords = geo.Coords(p1, p2)
    gcoords = geo.Coords(p1, p2)
    space_coords = geo.SpaceCoords(local=lcoords, global_=gcoords)

    lcoords2 = geo.Coords(p1, p2)
    gcoords2 = geo.Coords(p1, p2)
    space_coords2 = geo.SpaceCoords(lcoords2, gcoords2)

    assert space_coords == space_coords2


def test_space_coords():
    from pythonparts import geometry as geo
    import NemAll_Python_Geometry as AllplanGeo

    p1 = AllplanGeo.Point3D(15, 22, -4)
    p2 = AllplanGeo.Point3D(30, 110, 1110)
    lcoords = geo.Coords(p1, p2)
    gcoords = geo.Coords(p1, p2)
    
    space_coords = geo.SpaceCoords(local=lcoords, global_=gcoords)
    
    global_pnt = AllplanGeo.Point3D(100, 0, 10)
    space_coords.set_global_start_pnt(global_pnt)

    lcoords = geo.Coords(p1, p2)
    gcoords = geo.Coords(global_pnt, p2 + (global_pnt - p1))
    space_coords2 = geo.SpaceCoords(lcoords, gcoords)

    assert space_coords == space_coords2


def test_space_coords_from_local():
    from pythonparts import geometry as geo
    import NemAll_Python_Geometry as AllplanGeo

    p1 = AllplanGeo.Point3D(15, 22, -4)
    p2 = AllplanGeo.Point3D(30, 110, 1110)
    space_coords = geo.SpaceCoords.from_local_points(p1, p2)
    global_pnt   = AllplanGeo.Point3D(-100, -400, 35)
    space_coords.set_global_start_pnt(global_pnt)

    lcoords = geo.Coords(p1, p2)
    gcoords = geo.Coords(global_pnt, p2 + (global_pnt - p1))
    space_coords2 = geo.SpaceCoords(lcoords, gcoords)

    assert space_coords == space_coords2
    

def test_space_coords_from_points():
    from pythonparts import geometry as geo
    import NemAll_Python_Geometry as AllplanGeo

    p1 = AllplanGeo.Point3D(15, 22, -4)
    p2 = AllplanGeo.Point3D(30, 110, 1110)
    global_pnt   = AllplanGeo.Point3D(-100, -400, 35)
    space_coords = geo.SpaceCoords.from_points(p1, p2, global_pnt)
    
    lcoords = geo.Coords(p1, p2)
    gcoords = geo.Coords(global_pnt, p2 + (global_pnt - p1))
    space_coords2 = geo.SpaceCoords(lcoords, gcoords)

    assert space_coords == space_coords2