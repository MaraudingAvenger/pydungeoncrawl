import json
import copy
from typing import Any, Dict, List

try:
    import importlib.resources as resources
except ImportError:
    # Try backported to PY<37 `importlib_resources`.
    import importlib_resources as resources # type: ignore

from . import base_maps

from ..entities.board import Square, Board
from .location import Point


_TILE_MAP = {
    (0, 0, 0):{'symbol': '⬛', 'impassable': True, 'is_burning': False, 'is_lava': False, 'is_water': False, 'damage': 0}, # Black - Void/Impassable/Walls
    (255, 0, 0):{'symbol': '🟥', 'impassable': False, 'is_burning': False, 'is_lava': True, 'is_water': False, 'damage': 500}, # Red - Lava
    (0, 255, 0):{'symbol': '🟢', 'impassable': False, 'is_burning': False, 'is_lava': False, 'is_water': False, 'damage': 0}, # Green - Party Start
    (100, 100, 100):{'symbol':'🔴', 'impassable': False, 'is_burning': False, 'is_lava': False, 'is_water': False, 'damage': 0}, # Gray - Boss Start
    (0, 0, 255):{'symbol': '🟦', 'impassable': False, 'is_burning': False, 'is_lava': False, 'is_water': True, 'damage': 0}, # Blue - Water
    (255, 255, 0):{'symbol': '🟨', 'impassable': False, 'is_burning': True, 'is_lava': False, 'is_water': False, 'damage': 10}, # Yellow - Burning
    (255, 255, 255):{'symbol': '⬜', 'impassable': False, 'is_burning': False, 'is_lava': False, 'is_water': False, 'damage': 0}, # White - Floor
    (80, 50, 0):{'symbol': '🟫', 'impassable': True, 'is_burning': False, 'is_lava': False, 'is_water': False, 'damage': 0}, # Brown - Tree Trunk/Wooden object
    (0, 100, 0):{'symbol': '🟩', 'impassable': True, 'is_burning': False, 'is_lava': False, 'is_water': False, 'damage': 0}, # Green Square - Tree Leaves/Dense Foliage
}



def dict_to_square(d: Dict[str,Any]) -> Square:
    return Square(
        position=Point(*d['position']),
        symbol=d['symbol'],
        impassable=d['impassable'],
        is_burning=d['is_burning'],
        is_lava=d['is_lava'],
        is_water=d['is_water'],
        damage=d['damage'],
    )

def square_to_dict(s: Square) -> Dict[str,Any]:
    return {
        'position': [s.position.x, s.position.y],
        'symbol': s.symbol,
        'impassable': s.impassable,
        'is_burning': s.is_burning,
        'is_lava': s.is_lava,
        'is_water': s.is_water,
        'damage': s.damage,
    }

def json_to_board(json_str: str) -> Board:
    squares = json.loads(json_str)
    grid = []
    for _ in range(len(squares)):
        grid.append([])

    for row in squares:
        for square_dict in row:
            grid[square_dict['position'][1]].append(dict_to_square(square_dict))

    return Board(grid=grid)


def tiff_to_dict(read_loc: str, save: bool=False, save_loc: str='') -> List[Dict]:
    from PIL import Image

    im = Image.open(read_loc, 'r')
    width, height = im.size
    picture = im.load()
    js = []
    for y in range(height):
        row = []
        for x in range(width):
            square = copy.deepcopy(_TILE_MAP[picture[x,y]]) # type: ignore
            square.update({'position':(x,(height-y)-1)})
            row.append(square)

        js.append(row)
    
    if save and save_loc:
        with open(save_loc, 'w', encoding='utf8') as file:
            json.dump(js, file, ensure_ascii=False, indent=4)
    
    return js


def get_map(map_name: str) -> Board:
    """Returns a Board object for the given map name.

    :param map_name: the name of the map to load
    :return: a Board object for the given map
    """
    return json_to_board(resources.read_text(base_maps, map_name))