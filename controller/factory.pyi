import typing


class Factory:
    """
        A Factory of all methods for end user
    
    """

    def create_scene(build_ele):
        """
            Creating a Scene with start global point (0, 0, 0) 
        """
        
    @typing.overload
    def create_cuboid(self, be_name):
        """
            Create Cuboid fetching all parameters from pyp file.
        """
    
    @typing.overload
    def create_cuboid(self, width: float, height: float, length: float):
        """
            Create Cuboid with parameters explicitly.    
        """
