import NemAll_Python_Geometry as AllplanGeo    # type: ignore


from HandleDirection import HandleDirection    # type: ignore
from HandleProperties import HandleProperties  # type: ignore



class Handle:

    id = 0

    def __init__(self, space, handle_point: AllplanGeo.Point3D, ref_point: AllplanGeo.Point3D, param_name: str):
        self.parent_space = space
        self.handle_point = handle_point
        self.ref_point = ref_point
        self.param_name = param_name

    def __call__(self):
        return HandleProperties(
                self.__class__.id,
                self.handle_point,
                self.ref_point,
                [(self.param_name, HandleDirection.point_dir, True)],
                HandleDirection.point_dir,
                True,
        )

