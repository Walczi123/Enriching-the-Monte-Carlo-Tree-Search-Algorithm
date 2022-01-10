from copy import deepcopy
from math import inf
from typing import Union

import numpy as np

from games.hex.const import BLUE_PLAYER, COLOR_BLUE, COLOR_RED, RED_PLAYER

NEIGHBOURS = [(-1, 0), (0, -1), (1, -1), (1, 0), (0, 1), (-1, 1)]

class Logic:
    def __init__(self, ui, board_size):
        self.ui = ui
        self.board_size = board_size

        self.GAME_OVER = False
        self.MCTS_GAME_OVER = False
        self.logger = np.zeros(shape=(self.board_size, self.board_size))

        self.distance_board_player1 = np.full((self.board_size, self.board_size), np.inf)     
        self.distance_board_player2 = np.full((self.board_size, self.board_size), np.inf)   

        # for i in range(self.board_size):
        #     self.distance_board_player1 = self.update_distance(self.distance_board_player1, i, 0, 1)
        #     self.distance_board_player1 = self.update_distance(self.distance_board_player1, i, self.board_size-1, 1)
        # for i in range(self.board_size):
        #     self.distance_board_player2 = self.update_distance(self.distance_board_player2, 0, i, 1)
        #     self.distance_board_player2 = self.update_distance(self.distance_board_player2, self.board_size-1, i, 1)



    def get_possible_moves(self, board: np.ndarray):
        x, y = np.where(board == 0)
        free_coordinates = [(i, j) for i, j in zip(x, y)]

        return free_coordinates

    def update_distance(self, board, x, y, value):
        if not (x > -1 and y > -1 and x < self.board_size and y < self.board_size):
            return board
            
        if board[x][y] > value:
            board[x][y] = value
        else:
            return board

        for a,b in NEIGHBOURS:
            board = self.update_distance(board, x+a, y+b, value+1)
        
        return board


    def manhattan_distance(self, board, player):
        if player == 1:
            distance_board = deepcopy(self.distance_board_player1)
        else:
            distance_board = deepcopy(self.distance_board_player2)
        distance_board[board == (player%2)+1] = None
        result = np.where(self.logger == player)
        for r in range(len(result[0])):
            distance_board = self.update_distance(distance_board, result[0][r], result[1][r], 0)

        return distance_board
        



    def make_move(self, coordinates: tuple, player: Union[int, None]):
        x, y = coordinates
        node = x * self.board_size + y

        if self.ui is not None:
            if player is None and self.ui.color[node] == 0:
                self.ui.color[node] = self.ui.green
            else:
                self.ui.color[node] = COLOR_BLUE if player is BLUE_PLAYER else COLOR_RED

    def is_game_over(self, player: int, board: np.ndarray, mcts_mode: bool = False):
        """
        Sets GAME_OVER to True if there are no more moves to play.
        Returns the winning player.
        """
        if not self.get_possible_moves(board):
            if not mcts_mode:
                self.GAME_OVER = True

        for _ in range(self.board_size):
            if player is BLUE_PLAYER:
                border = (_, 0)
            if player is RED_PLAYER:
                border = (0, _)

            path = self.traverse(border, player, board, {}, mcts_mode)
            if path:
                if not mcts_mode:
                    # Highlights the winning path in green
                    for step in path.keys():
                        self.make_move(step, None)

                return player
        


    def is_border(self, node: tuple, player: int):
        x, y = node
        if player is BLUE_PLAYER:
            if y == self.board_size - 1:
                return True
        elif player is RED_PLAYER:
            if x == self.board_size - 1:
                return True

    def traverse(self, node: tuple, player: int, board: np.ndarray, visited: dict, mcts_mode: bool):
        x, y = node
        neighbours = self.get_neighbours((x, y))

        try:
            if visited[(x, y)]:
                pass
        except KeyError:
            if board[x][y] == player:
                visited[(x, y)] = 1

                if self.is_border(node, player):
                    if not mcts_mode:
                        self.GAME_OVER = True
                    # else:
                    #     self.MCTS_GAME_OVER = True

                for neighbour in neighbours:
                    self.traverse(neighbour, player, board, visited, mcts_mode)

        if self.GAME_OVER or self.MCTS_GAME_OVER:
            return visited

    def get_neighbours(self, coordinates: tuple):
        x, y = coordinates
        neighbours = []
        for row in range(-1, 2):
            for col in range(-1, 2):
                if row != col:
                    node = (x + row, y + col)
                    if self.is_valid(node):
                        neighbours.append(node)

        return neighbours

    def is_valid(self, coordinates: tuple):
        """
        Returns True if node exists.
        """
        return all(0 <= _ < self.board_size for _ in coordinates)

    def is_node_free(self, coordinates: tuple, board: np.ndarray):
        """
        Returns True if node is free.
        """
        x, y = coordinates

        return True if not board[x][y] else False

    def check_and_make_action(self, player: int, coordinates: tuple) -> int:
        (x, y) = coordinates
   
        assert self.is_node_free((x, y), self.logger), "node is busy"
        self.make_move((x, y), player)
        self.logger[x][y] = player

        return self.is_game_over(player, self.logger)

