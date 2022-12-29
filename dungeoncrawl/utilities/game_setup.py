import json
from os import PathLike
from typing import Any

from dungeoncrawl.board import Square, Board
from dungeoncrawl.utilities.location import Point

# {
# "position": [0, 0],
# "symbol": "@",
# 
# }

def dict_to_square(d: dict[str,Any]) -> Square:
    return Square(
        Point(*d['position']),
        d['symbol'],
        d['impassable'],
        d['is_burning'],
        d['is_lava'],
        d['damage'],
    )

def square_to_dict(s: Square) -> dict[str,Any]:
    return {
        'position': [s.position.x, s.position.y],
        'symbol': s.symbol,
        'impassable': s.impassable,
        'is_burning': s.is_burning,
        'is_lava': s.is_lava,
        'damage': s.damage,
    }

def json_to_board(json_loc:str|PathLike) -> Board:
    squares = json.load(open(json_loc, encoding='utf-8'))
    grid = []
    for _ in range(len(squares)):
        grid.append([])

    for row in squares:
        for square_dict in row:
            grid[square_dict['position'][1]].append(dict_to_square(square_dict))

    return Board(grid=grid)