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
        # self.logger = np.zeros(shape=(self.board_size, self.board_size)) 
        self.logger = [[0 for x in range(self.board_size)] for y in range(self.board_size)] 

    def get_possible_moves(self, board: list):
        free_coordinates = []
        for x in range(self.board_size):
            for y in range(self.board_size):
                if board[x][y] == 0 :
                    free_coordinates.append((x,y))

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
        
    def get_dijkstra_score(self, board, color): 
        """gets the dijkstra score for a certain color, differs from dijkstra eval in that it only considers the passed color
        Args:
            color (Hexboard.Color): What color to evaluate
        Returns:
            int: score of how many (shortest) path-steps remain to victory
        """
        LOSE = 1000 # Choose win value higher than possible score but lower than INF

        board_size = self.board_size
        scores = np.array([[LOSE for i in range(board_size)] for j in range(board_size)])
        updated = np.array([[True for i in range(board_size)] for j in range(board_size)]) #Start updating at one side of the board 

        #alignment of color (blue = left->right so (1,0))
        alignment = (0, 1) if color == 1 else (1, 0)


        for i in range(board_size):
            newcoord = tuple([i * j for j in alignment]) #iterate over last row or column based on alignment of current color

            updated[newcoord] = False
            if board[newcoord] == color: #if same color --> path starts at 0
                scores[newcoord] = 0
            elif board[newcoord] == 0: #if empty --> costs 1 move to use this path 
                scores[newcoord] = 1
            else: #If other color --> can't use this path
                scores[newcoord] = LOSE

        scores = self.dijkstra_update(board, color, scores, updated)

        #self.board.print_dijkstra(scores)

        results = [scores[alignment[0] * i - 1 + alignment[0]][alignment[1]*i - 1 + alignment[1]] for i in range( board_size)] #take "other side" to get the list of distance from end-end on board
        best_result = min(results)
        
        # if best_result == 0:
        #     best_result = -500
        
        # log.debug("Best score for color {}: {}".format(color, best_result))
        return best_result #return minimum distance to get current score

    def dijkstra_update(self, board, color, scores, updated):
        """Updates the given dijkstra scores array for given color
        Args:
            color (HexBoard.color): color to evaluate
            scores (int array): array of initial scores
            updated (bool array): array of which nodes are up-to-date (at least 1 should be false for update to do something)
        Returns:
            the updated scores
        """
        LOSE = 1000 # Choose win value higher than possible score but lower than INF
        # log.debug("Starting dijkstra algorithm")
        updating = True
        while updating: 
            updating = False
            for i, row in enumerate(scores): #go over rows
                for j, point in enumerate(row): #go over points 
                    if not updated[i][j]: 
                        neighborcoords = self.get_neighbors((i,j))
                        for neighborcoord in neighborcoords:
                            target_coord = tuple(neighborcoord)
                            path_cost = LOSE #1 for no color, 0 for same color, INF for other color 
                            if board[target_coord] == 0:
                                path_cost = 1
                            elif board[target_coord] == color:
                                path_cost = 0
                            
                            if scores[target_coord] > scores[i][j] + path_cost: #if new best path to this neighbor
                                scores[target_coord] = scores[i][j] + path_cost #update score
                                updated[target_coord] = False #This neighbor should be updated
                                updating = True #make sure next loop is started
                                
        return scores

    def get_neighbors(self, coordinates):
        """Gets all the neighbouring cells of a given cell
        Args:
            coordinates (tuple): Cell (x, y) coordinates
        Returns:
            list: List of neighbouring cell coordinates tuples
        """
        (cx,cy) = coordinates
        neighbors = []
        if cx-1 >= 0: neighbors.append((cx-1,cy))
        if cx+1 < self.board_size: neighbors.append((cx+1,cy))
        if cx-1 >= 0 and cy+1 <= self.board_size-1: neighbors.append((cx-1,cy+1))
        if cx+1 < self.board_size and cy-1 >= 0: neighbors.append((cx+1,cy-1))
        if cy+1 < self.board_size: neighbors.append((cx,cy+1))
        if cy-1 >= 0: neighbors.append((cx,cy-1))

        return neighbors

    def make_move(self, coordinates: tuple, player: Union[int, None]):
        x, y = coordinates
        node = x * self.board_size + y

        if self.ui is not None:
            if player is None and self.ui.color[node] == 0:
                self.ui.color[node] = self.ui.green
            else:
                self.ui.color[node] = COLOR_BLUE if player is BLUE_PLAYER else COLOR_RED

    def is_game_over(self, player: int, board: list, show_path: bool = True, return_winner:bool = True):
        if not return_winner and not self.get_possible_moves(board):
            return True

        if player is None:
            for _ in range(self.board_size):
                path = self.traverse((_, 0), BLUE_PLAYER, board, list())
                if path:
                    if show_path and self.ui:
                        for step in path:
                            x, y = step
                            node = x * self.board_size + y
                            self.ui.color[node] = self.ui.green

                    return BLUE_PLAYER

                path = self.traverse((0, _), RED_PLAYER, board, list())
                if path:
                    if show_path and self.ui:
                        for step in path:
                            x, y = step
                            node = x * self.board_size + y
                            self.ui.color[node] = self.ui.green

                    return RED_PLAYER           
        else:
            for _ in range(self.board_size):
                if player is BLUE_PLAYER:
                    border = (_, 0)
                if player is RED_PLAYER:
                    border = (0, _)

                path = self.traverse(border, player, board, list())
                if path:
                    if show_path and self.ui:
                        for step in path:
                            x, y = step
                            node = x * self.board_size + y
                            self.ui.color[node] = self.ui.green

                    return player

    def is_border(self, node: tuple, player: int):
        x, y = node
        if player is BLUE_PLAYER:
            if y == self.board_size - 1:
                return True
        elif player is RED_PLAYER:
            if x == self.board_size - 1:
                return True

    def traverse(self, node: tuple, player: int, board: list, visited: list):
        x, y = node 
        achiachieved_border = False    
        if not ((x, y) in visited) and board[x][y] == player:
            visited.append((x, y))

            if self.is_border(node, player):
                achiachieved_border =  True

            neighbours = self.get_neighbours((x, y))
            for neighbour in neighbours:
                if self.traverse(neighbour, player, board, visited):
                    achiachieved_border =  True

        if achiachieved_border:
            return visited

    def get_neighbours(self, coordinates: tuple):
        x, y = coordinates
        neighbours = []
        for row in range(-1, 2):
            for col in range(-1, 2):
                if row != col:
                    node = (x + row, y + col)
                    if 0 <= x + row < self.board_size and 0 <= y + col < self.board_size:
                        neighbours.append(node)

        return neighbours

    def check_and_make_action(self, player: int, coordinates: tuple) -> int:
        (x, y) = coordinates
   
        if self.logger[x][y] : raise("node is busy")
        self.make_move((x, y), player)
        self.logger[x][y] = player

        return self.is_game_over(player, self.logger)

