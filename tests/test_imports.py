def test_import_NemAll_Python_Geometry():
    try:
        import pythonparts      # Without pythonparts import, path to NemAll_Python_Geometry is undefined
        import NemAll_Python_Geometry as AllplanGeo
    except ModuleNotFoundError:
        assert False, "No such module: NemAll_Python_Geometry"
    except ImportError:
        assert False, "Failed to import AllplanGeo from NemAll_Python_Geometry"
    assert True


def test_import_NemAll_Python_BaseElements():
    try:
        import pythonparts      # Without pythonparts import, path to NemAll_Python_BaseElements is undefined
        import NemAll_Python_BaseElements as AllplanBaseElements
    except ModuleNotFoundError:
        assert False, "No such module: AllplanBaseElements"
    except ImportError:
        assert False, "Failed to import AllplanBaseElements from NemAll_Python_BaseElements"
    assert True



def test_import_pythonparts():
    try:
        import pythonparts
    except ModuleNotFoundError:
        assert False, "No such module: pythonparts"


def test_import_geometry():
    try:
        from pythonparts import geometry
    except ModuleNotFoundError:
        assert False, "No such module: pythonparts"
    except ImportError:
        assert False, "Failed to import geometry from pythonparts"
    assert True


def test_import_geometry_coords():
    try:
        from pythonparts import geometry as geo 
        coords = geo.Coords()
    except ModuleNotFoundError:
        assert False, "No such module: geometry"
    except ImportError:
        assert False, "Failed to import geometry from pythonparts"
    assert True


def test_import_geometry_space_coords():
    try:
        from pythonparts import geometry as geo 
        coords = geo.SpaceCoords(geo.Coords(), geo.Coords())
    except ModuleNotFoundError:
        assert False, "No such module: geometry"
    except ImportError:
        assert False, "Failed to import geometry from pythonparts"
    assert True