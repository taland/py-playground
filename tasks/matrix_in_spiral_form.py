import math
from typing import Any, Generator, List, Tuple


Coordinate = Tuple[int, int]
Matrix = List[List[Any]]


def count_items_on_level(matrix_size: int, depth: int = 1, level: int = 1) -> int:
    if level <= 0:
        raise ValueError("`level` should be great then `0`")
    if level > depth:
        raise ValueError("`level` should not be great then `depth`")
    if depth == level:
        return 1 if depth % 2 == 1 else 4
    item_num = matrix_size - (level - 1)
    return item_num * item_num - 4


def get_item_coord_by_index(matrix_size: int, index: int = 0) -> Coordinate:
    arc_size = matrix_size - 1
    curr_arc = int(index / arc_size)
    item_idx_on_curr_arc = index % arc_size

    if curr_arc == 0:
        return 0, item_idx_on_curr_arc
    if curr_arc == 1:
        if item_idx_on_curr_arc == 0:
            return 0, arc_size
        return item_idx_on_curr_arc, arc_size
    if curr_arc == 2:
        return arc_size, arc_size - item_idx_on_curr_arc
    if curr_arc == 3:
        if item_idx_on_curr_arc == 0:
            return arc_size, 0
        return arc_size - item_idx_on_curr_arc, 0


def get_item_coord_by_index_on_level(matrix_size: int, index: int = 0, level: int = 0) -> Coordinate:
    adjusted_size = math.ceil(matrix_size / level)
    coord = get_item_coord_by_index(adjusted_size, index)
    return coord[0] + (level - 1), coord[1] + (level - 1)


def iter_matrix_in_spiral_form(matrix: Matrix) -> Generator[Coordinate, None, None]:
    size_ = len(matrix)
    depth_ = math.ceil(size_ / 2)
    for level_ in range(1, depth_ + 1):
        items_on_level = count_items_on_level(matrix_size=size_, depth=depth_, level=level_)
        for i in range(0, items_on_level):
            coord = get_item_coord_by_index_on_level(matrix_size=size_, level=level_, index=i)
            yield coord
