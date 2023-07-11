import math


def center_calc(concov, global_, child_space):
    yield __center_calc_axis(concov.left, 
                             concov.right, 
                             global_.start_point.X, 
                             global_.end_point.X,
                             child_space.width)
    
    yield __center_calc_axis(concov.front, 
                             concov.back, 
                             global_.start_point.Y, 
                             global_.end_point.Y,
                             child_space.length)

    yield __center_calc_axis(concov.bottom,
                             concov.top, 
                             global_.start_point.Z, 
                             global_.end_point.Z,
                             child_space.height)


def __center_calc_axis(shift1, shift2, parent_start_point_coord, parent_end_point_coord, child_len):
    if not (math.isclose(shift1, 0) and math.isclose(shift2, 0)):
        return shift1
    parent_len = abs(parent_end_point_coord - parent_start_point_coord)
    shift = (parent_len - child_len) / 2.
    return shift