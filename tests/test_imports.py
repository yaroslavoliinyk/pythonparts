import pytest


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


# def test_coords_import():
#     try:
#         from pythonparts.