from pythonparts import Block


def test_block_coords():
    b = Block(0, 0, 0)
    assert b.x == 0
    assert b.y == 0
    assert b.z == 0


def test_block_coords2():
    b = Block(1, 2, 3)
    assert b.x == 1
    assert b.y == 2
    assert b.z == 3
