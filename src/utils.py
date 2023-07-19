import math

from typing import Optional

import NemAll_Python_Geometry as AllplanGeo    # type: ignore

from .config import TOLERANCE


def child_global_coords_calc(concov, global_, child_space):
    start_X, end_X = __coords_calc_axis(concov.left, 
                                        concov.right, 
                                        global_.start_point.X, 
                                        global_.end_point.X,
                                        child_space.width,)
    
    start_Y, end_Y = __coords_calc_axis(concov.front, 
                                        concov.back, 
                                        global_.start_point.Y, 
                                        global_.end_point.Y,
                                        child_space.length,)

    start_Z, end_Z = __coords_calc_axis(concov.bottom,
                                        concov.top, 
                                        global_.start_point.Z, 
                                        global_.end_point.Z,
                                        child_space.height,)
    
    child_global_start_pnt = AllplanGeo.Point3D(start_X, start_Y, start_Z)
    child_global_end_pnt   = AllplanGeo.Point3D(end_X, end_Y, end_Z)

    return child_global_start_pnt, child_global_end_pnt


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


def center_scene_calc(concov, child_space):
    yield -child_space.width/2. if concov.left is None else None
    yield -child_space.length/2. if concov.front is None else None
    yield -child_space.height/2. if concov.bottom is None else None


def equal_points(p1: Optional[AllplanGeo.Point3D], p2: Optional[AllplanGeo.Point3D]):
    if (p1 is None) and (p2 is None):
        return True
    if (p1 is None) or (p2 is None):
        return False
 
    return  (math.isclose(p1.X, p2.X, rel_tol=TOLERANCE, abs_tol=TOLERANCE)  
            and math.isclose(p1.Y, p2.Y, rel_tol=TOLERANCE, abs_tol=TOLERANCE)
            and math.isclose(p1.Z, p2.Z, rel_tol=TOLERANCE, abs_tol=TOLERANCE)
    )


def __coords_calc_axis(cc_start, cc_end, parent_global_start_point, parent_global_end_point, child_len):
    if cc_start is not None:
        child_global_start_point = parent_global_start_point + cc_start
        child_global_end_point   = child_global_start_point + child_len
    elif cc_end is not None:
        child_global_end_point   = parent_global_end_point - cc_end
        child_global_start_point = child_global_end_point - child_len
    else:
        child_global_start_point = parent_global_start_point
        child_global_end_point   = child_global_start_point + child_len

    return child_global_start_point, child_global_end_point


def __center_calc_axis(cc_start, cc_end, parent_global_start_point, parent_global_end_point, child_len):
    if not (cc_start is None and cc_end is None):
        return cc_start
    parent_len = abs(parent_global_end_point - parent_global_start_point)
    shift = (parent_len - child_len) / 2.
    return shift


