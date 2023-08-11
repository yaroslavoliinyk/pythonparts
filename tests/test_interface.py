import pytest
import random

import pythonparts as pp


class TestInterface:

    def test_attribute_exception(self):
        with pytest.raises(AttributeError):
            cube = pp.create_cuboid_from_pyp('Cuboid')
