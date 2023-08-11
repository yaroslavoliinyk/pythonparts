import pythonparts as pp



class BuildElement:

    def __set_name__(self, owner, name):
        self.storage_name = name

    def __set__(self, instance, value):
        cls = type(self)
        cls.registered_build_ele = value

    def __get__(self, instance, owner):
        cls = type(self)
        if ('registered_build_ele' in cls.__dict__):
            return cls.registered_build_ele
        else:
            raise AttributeError('Build_ele is not registered!')