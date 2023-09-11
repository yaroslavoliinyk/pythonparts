

class Reinforcement:
    pass



class Longbars(Reinforcement):
    
    def __init__(self, 
                 space, 
                 along_axis, 
                 split_by_count=False,
                 split_by_spacing=False,
                 **properties):
        self.parent_space = space
        self.along_axis = along_axis
        self.split_by_count = split_by_count
        self.split_by_spacing = split_by_spacing
        self.properties = properties


    def start(self, **concov) -> "Longbars":
        return self
    
    def end(self, **concov) -> "Longbars":
        return self
