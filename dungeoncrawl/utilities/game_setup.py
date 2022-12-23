from typing import Any

from dungeoncrawl.board import Square, Board
from dungeoncrawl.utilities.location import Point

def dict_to_square(d: dict[str,Any]) -> Square:
    return Square(
        Point(*d['position'])
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

def list_to_board(l: list[list[dict]]) -> Board:
    return Board(
        grid=[list(map(dict_to_square, row)) for row in l],
    )