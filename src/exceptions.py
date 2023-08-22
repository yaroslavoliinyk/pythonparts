
class AttributePermissionError(AttributeError):

    def __init__(self, msg):
        super().__init__(msg)


class AllplanGeometryError(ValueError):

    def __init__(self, msg):
        super().__init__(msg)


class IncorrectAxisValueError(ValueError):

    def __init__(self, axis):
        super().__init__(f"Axis value = {axis} is incorrect. Please, state correct axis: x, y, z(or Ox, Oy, Oz)")