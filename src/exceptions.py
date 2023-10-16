
class AttributePermissionError(AttributeError):

    def __init__(self, msg):
        super().__init__(msg)

class WrongParametersError(TypeError):

    def __init__(self, msg):
        super().__init__(msg)


class AllplanGeometryError(ValueError):

    def __init__(self, msg):
        super().__init__(msg)


class IncorrectAxisValueError(ValueError):

    def __init__(self, msg):
        super().__init__(msg)