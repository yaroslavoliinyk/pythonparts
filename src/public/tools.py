import pythonparts as pp


class Register:

    build_ele = None

    def set(self, build_ele):
        cls = type(self)
        cls.build_ele = build_ele

    def get(self):
        cls = type(self)
        return cls.build_ele
