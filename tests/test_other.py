import pytest

import pythonparts as pp


# def test_center_calc1():
#     cc1 = pp.src.utils.__center_calc_axis(5, 
#                                         None,
#                                         500.2, 
#                                         300,
#                                         1000,)
#     assert cc1 == 5


# def test_center_calc2():
#     child_len = 300
#     parent_start_point_coord = 1300
#     parent_end_point_coord = 1900
#     cc1 = pp.src.utils.__center_calc_axis(None, 
#                                           None, 
#                                         parent_start_point_coord, 
#                                         parent_end_point_coord,
#                                         child_len,)

#     assert cc1 == 150.0


# def test_center_calc3():
#     child_len = 1000
#     parent_start_point_coord = 1300
#     parent_end_point_coord = 1900
#     cc1 = pp.src.utils.__center_calc_axis(None, 
#                                         None, 
#                                         parent_start_point_coord, 
#                                         parent_end_point_coord,
#                                         child_len,)

#     parent_len = parent_end_point_coord - parent_start_point_coord
#     expected_cc = (parent_len - child_len) / 2.
    
#     assert cc1 == -200.0


def test_child_global_coords_calc1():
    start_coord, end_coord = pp.src.utils.__coords_calc_axis(5, 
                                                            None,
                                                            500.2, 
                                                            300,
                                                            1000,)
    
    assert (start_coord, end_coord) == (505.2, 1505.2) 


def test_child_global_coords_calc2():
    child_len = 300
    parent_start_point_coord = 1300
    parent_end_point_coord = 1900
    start_coord, end_coord = pp.src.utils.__coords_calc_axis(None, 
                                            200, 
                                            parent_start_point_coord, 
                                            parent_end_point_coord,
                                            child_len,)
    
    assert (start_coord, end_coord) == (1400, 1700)


def test_child_global_coords_calc3():
    child_len = 1000
    parent_start_point_coord = 1300
    parent_end_point_coord = 1900
    start_coord, end_coord = pp.src.utils.__coords_calc_axis(None, 
                                            None, 
                                            parent_start_point_coord, 
                                            parent_end_point_coord,
                                            child_len,)
    
    assert (start_coord, end_coord) == (1300, 2300)


# test_center_calc1()