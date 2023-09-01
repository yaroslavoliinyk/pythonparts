import pythonparts as pp


class Register:

    build_ele = None
    scene     = None

    def set_build_ele(self, build_ele):
        cls = type(self)
        cls.build_ele = build_ele

    def get_build_ele(self):
        cls = type(self)
        return cls.build_ele

    def set_scene(self, scene):
        cls = type(self)
        cls.scene = scene

    def get_scene(self):
        cls = type(self)
        return cls.scene