
class AttributePermissionError(AttributeError):

    def __init__(self, msg):
        super().__init__(msg)


class AllplanGeometryError(ValueError):

    def __init__(self, msg):
        super().__init__(msg)