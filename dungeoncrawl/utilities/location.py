import heapq
import math
from dataclasses import dataclass
from functools import singledispatch
import re
from typing import Generator

def clean_name(name):
    name = re.sub(r'([a-z])([A-Z])', r'\1 \2', name)
    return name.replace('_', ' ').title()
    
@dataclass
class Point:
    x: int
    y: int

    def __repr__(self)->str:
        return f"({self.x}, {self.y})"

    def __tuple__(self)->tuple[int, int]:
        return (self.x, self.y)

    def __getitem__(self, key):
        return (self.x, self.y)[key]

    def __hash__(self):
        return hash(self.__tuple__())
    
    def __iter__(self):
        yield self.x
        yield self.y

@singledispatch
def distance_between(a: Point|tuple[int,int], b: Point|tuple[int,int]) -> float:
    if isinstance(a, tuple):
        a = Point(*a)
    if isinstance(b, tuple):
        b = Point(*b)
    return ((a.x - b.x)**2 + (a.y - b.y)**2)**0.5

@distance_between.register
def _(x1:int, y1:int, x2:int, y2:int) -> float:
    return distance_between(Point(x1, y1), Point(x2, y2))

@singledispatch
def behinds(x1:int, y1:int, x2:int, y2:int) -> tuple[Point, Point, Point]:
    x3 = x1 - x2
    y3 = y1 - y2

    xb = x3 + x1
    yb = y3 + y1

    if x1 == x2 and y1 != y2: # Orthog from side
        return Point(xb-1, yb), Point(xb, yb), Point(xb+1, yb)
    elif x1 != x2 and y1 == y2: # Orthog from top/bottom
        return Point(xb, yb+1), Point(xb, yb), Point(xb, yb-1)

    elif xb < x1 and yb < y1: # Diag down left
        return Point(xb, yb+1), Point(xb, yb), Point(xb+1, yb)
    elif xb > x1 and yb < y1:  # Diag down right
        return Point(xb-1, yb), Point(xb, yb), Point(xb, yb+1)
    elif xb < x1 and yb > y1: # Diag up left
        return Point(xb, yb-1), Point(xb, yb), Point(xb+1, yb)
    else: #xb > x1 and yb > y1: Diag up right
        return Point(xb-1, yb), Point(xb, yb), Point(xb, yb-1)

@behinds.register
def _(location: Point, facing: Point) -> tuple[Point, Point, Point]:
    return behinds(location.x, location.y, facing.x, facing.y)

@singledispatch
def angle_between(x1, y1, x2, y2):
    x3 = x2 - x1
    y3 = y2 - y1
    return math.degrees(math.atan2(y3, x3))

@angle_between.register
def _(location: Point, facing: Point):
    return angle_between(location.x, location.y, facing.x, facing.y)

@singledispatch
def angle_behind(x1, y1, x2, y2):
    return angle_between(x2, y2, x1, y1)

@angle_behind.register
def _(location: Point, facing: Point):
    return angle_behind(location.x, location.y, facing.x, facing.y)

def bresenham(origin: Point, destination: Point) -> Generator[Point, None, None]:
    x1, y1 = origin.x, origin.y
    x2, y2 = destination.x, destination.y
    dx = abs(x2 - x1)
    dy = abs(y2 - y1)
    sx = 1 if x1 < x2 else -1
    sy = 1 if y1 < y2 else -1
    err = dx - dy

    while True:
        if x1 == x2 and y1 == y2:
            break
        e2 = 2 * err
        if e2 > -dy:
            err = err - dy
            x1 = x1 + sx
        if e2 < dx:
            err = err + dx
            y1 = y1 + sy
        yield Point(x1, y1)
