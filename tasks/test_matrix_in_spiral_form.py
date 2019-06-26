import pytest
from matrix_in_spiral_form import (
    count_items_on_level,
    get_item_coord_by_index,
    get_item_coord_by_index_on_level,
    iter_matrix_in_spiral_form,
)


@pytest.mark.parametrize("matrix_size,depth,level,expected_result", [
    (4, 2, 1, 12),
])
def test_count_items_on_level(matrix_size, depth, level, expected_result):
    actual_num = count_items_on_level(matrix_size, depth, level)
    assert expected_result == actual_num


def test_exception_when_level_is_invalid():
    with pytest.raises(ValueError):
        count_items_on_level(4, depth=3, level=4)


def test_exception_when_level_is_zero():
    with pytest.raises(ValueError):
        count_items_on_level(4, depth=3, level=0)


@pytest.mark.parametrize("matrix_size,index,expected_result", [
    (4, 0,  (0, 0)),
    (4, 1,  (0, 1)),
    (4, 2,  (0, 2)),
    (4, 3,  (0, 3)),
    (4, 4,  (1, 3)),
    (4, 5,  (2, 3)),
    (4, 6,  (3, 3)),
    (4, 7,  (3, 2)),
    (4, 8,  (3, 1)),
    (4, 9,  (3, 0)),
    (4, 10, (2, 0)),
    (4, 11, (1, 0)),
])
def test_get_item_coord_by_index(matrix_size, index, expected_result):
    coords = get_item_coord_by_index(matrix_size, index)
    assert expected_result == coords


def test_exception_when_coord_is_out_of_scope():
    # todo:
    with pytest.raises(ValueError):
        raise ValueError()


@pytest.mark.parametrize("matrix_size,index,level,expected_result", [
    (4, 0, 1,  (0, 0)),
    (4, 1, 1,  (0, 1)),
    (4, 2, 1,  (0, 2)),
    (4, 3, 1,  (0, 3)),
    (4, 4, 1,  (1, 3)),
    (4, 5, 1,  (2, 3)),
    (4, 6, 1,  (3, 3)),
    (4, 7, 1,  (3, 2)),
    (4, 8, 1,  (3, 1)),
    (4, 9, 1,  (3, 0)),
    (4, 10, 1, (2, 0)),
    (4, 11, 1, (1, 0)),

    (4, 0, 2, (1, 1)),
    (4, 1, 2, (1, 2)),
    (4, 2, 2, (2, 2)),
    (4, 3, 2, (2, 1)),
])
def test_get_item_coord_by_index_on_level(matrix_size, index, level, expected_result):
    coords = get_item_coord_by_index_on_level(matrix_size, index, level)
    assert expected_result == coords


def test_iter_matrix_in_spiral_form():
    m = [
        [1, 2, 3, 4],
        [12, 13, 14, 5],
        [11, 16, 15, 6],
        [10, 9, 8, 7],
    ]
    rs = [m[coord[0]][coord[1]] for coord in iter_matrix_in_spiral_form(m)]
    assert rs == list(range(1, 17))
