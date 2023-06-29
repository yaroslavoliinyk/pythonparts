
class Point3D:

    def __init__(self, x: float, y: float, z: float):
        self._x = x
        self._y = y
        self._z = z

    @property
    def x(self):
        return self._x
    
    @property
    def y(self):
        return self._y
    
    @property
    def z(self):
        return self._z

    def __iadd__(self, other_point: 'Point3D'):
        self._x += other_point.x
        self._y += other_point.y
        self._z += other_point.z
        return self

    def __repr__(self):
        return f"Point3D({self.x!r}, {self.y!r}, {self.z!r},)"
