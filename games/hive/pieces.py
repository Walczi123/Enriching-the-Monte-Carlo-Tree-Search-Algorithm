import os
import numpy as np

from games.hive.const import ANT_AMOUNT, ANT_ID, BEETLE_AMOUNT, BEETLE_ID, GRASSHOPPER_AMOUNT, GRASSHOPPER_ID, QUEEN_AMOUNT, QUEEN_ID, SPIDER_AMOUNT, SPIDER_ID
from games.hive.common_functions import cube_to_axial, evenr_to_axial, move_does_not_break_hive, neighbours, find_pieces_around, path_exists
from games.hive.state import State
os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "hide"
import pygame as pg

PIECE_WHITE = (250, 250, 250)
class Piece:

    def __init__(self, color=PIECE_WHITE):
        self.old_pos = None
        self.color = color
        self.amount = 0

    def update_pos(self, pos):
        self.old_pos = pos

    def moves(self, coordinate, state):
        return iter(())


class Queen(Piece):

    def __init__(self, color=PIECE_WHITE):
        super().__init__(color)
        self.amount = QUEEN_AMOUNT

    def draw(self, surface, hex_pos):
        image = \
            pg.image.load('games/hive/images/{}.png'.format(type(self).__name__))
        (x, y) = hex_pos
        pos = (x - 16, y - 14)
        surface.blit(image, pos)

    def moves(self, coordinate, state):
        if len(find_pieces_around(state, coordinate)) < 4:
            return trace_coutour(state, coordinate, steps=1)
        return super().moves(coordinate, state)

class Ant(Piece):

    def __init__(self, color=PIECE_WHITE):
        super().__init__(color)
        self.amount = ANT_AMOUNT

    def draw(self, surface, hex_pos):
        image = \
            pg.image.load('games/hive/images/{}.png'.format(type(self).__name__))
        (x, y) = hex_pos
        pos = (x - 16, y - 17)
        surface.blit(image, pos)

    def moves(self, coordinate, state):
        return [c for c in find_contour(state, exclude=(coordinate,)) if path_exists(state, coordinate, c)]
         
class Spider(Piece):

    def __init__(self, color=PIECE_WHITE):
        super().__init__(color)
        self.amount = SPIDER_AMOUNT

    def draw(self, surface, hex_pos):
        image = \
            pg.image.load('games/hive/images/{}.png'.format(type(self).__name__))
        (x, y) = hex_pos
        pos = (x - 16, y - 17)
        surface.blit(image, pos)

    def moves(self, coordinate, state):
        return trace_coutour(state, coordinate, steps=3)


class Beetle(Piece):

    def __init__(self, color=PIECE_WHITE):
        super().__init__(color)
        self.amount = BEETLE_AMOUNT

    def draw(self, surface, hex_pos):
        image = \
            pg.image.load('games/hive/images/{}.png'.format(type(self).__name__))
        (x, y) = hex_pos
        pos = (x - 16, y - 16)
        surface.blit(image, pos)

    def moves(self, coordinate, state):
        return [n for n in neighbours(coordinate) if move_does_not_break_hive(state, coordinate, n)]

# Hex topology stuff
offsets = [
    (0, -1, 1), (1, -1, 0), (1, 0, -1),
    (0, 1, -1), (-1, 1, 0), (-1, 0, 1)]

def add(c1, c2):
    x1, y1, z1 = c1
    x2, y2, z2 = c2
    return x1 + x2, y1 + y2, z1 + z2

class Grasshopper(Piece):

    def __init__(self, color=PIECE_WHITE):
        super().__init__(color)
        self.amount = GRASSHOPPER_AMOUNT

    def draw(self, surface, hex_pos):
        image = \
            pg.image.load('games/hive/images/{}.png'.format(type(self).__name__))
        (x, y) = hex_pos
        pos = (x - 12, y - 14)
        surface.blit(image, pos)

    def moves(self, coordinate, state):
        c = evenr_to_axial(coordinate)
        for direction in offsets:
            p = add(c, direction)
            # Grasshopper must jump over at least one piece
            if p in state.board.keys():
                while p in state.board.keys():
                    p = add(p, direction)
                yield cube_to_axial(p)


def find_contour(state:State, exclude=None):
        """Returns all contour coordinates of the hive"""
        contour = set()
        # All neighbours
        for coordinate in state.board.keys():
            if coordinate not in exclude:
                for neighbour in neighbours(coordinate):
                    contour.add(neighbour)
        # ...except non-free
        contour.difference_update(set(state.board.keys()))
        return contour

def trace_coutour(state, coordinate, steps=1):
    """Returns the two coordinates n steps away from coordinate along
    the hive contour."""
    contour = find_contour(state, exclude=(coordinate,))
    visited = set()
    todo = [(coordinate, 0)]
    while todo:
        c, n = todo.pop()
        for neighbour in neighbours(c):
            if neighbour in contour and neighbour not in visited:
                visited.add(neighbour)
                if n == steps:
                    yield c
                else:
                    todo.append((neighbour, n + 1))

def id_to_piece(id):
    if id == QUEEN_ID:
        return Queen
    elif id == ANT_ID:
        return Ant
    elif id == GRASSHOPPER_ID:
        return Grasshopper
    elif id == SPIDER_ID:
        return Spider
    elif id == BEETLE_ID:
        return Beetle