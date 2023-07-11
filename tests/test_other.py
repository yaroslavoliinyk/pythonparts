import pytest

import pythonparts as pp


def test_center_calc1():
    cc1 = pp.scripts.utils.__center_calc_axis(5, 
                                            0,
                                            500.2, 
                                            300,
                                            1000,)
    assert cc1 == 5


def test_center_calc2():
    child_len = 300
    parent_start_point_coord = 1300
    parent_end_point_coord = 1900
    cc1 = pp.scripts.utils.__center_calc_axis(0, 
                                            0, 
                                            parent_start_point_coord, 
                                            parent_end_point_coord,
                                            child_len,)

    assert cc1 == 150.0


def test_center_calc3():
    child_len = 1000
    parent_start_point_coord = 1300
    parent_end_point_coord = 1900
    cc1 = pp.scripts.utils.__center_calc_axis(0, 
                                            0, 
                                            parent_start_point_coord, 
                                            parent_end_point_coord,
                                            child_len,)

    parent_len = parent_end_point_coord - parent_start_point_coord
    expected_cc = (parent_len - child_len) / 2.
    
    assert cc1 == -200.0