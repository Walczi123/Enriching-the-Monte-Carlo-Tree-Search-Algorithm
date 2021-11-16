from math import log, sqrt
from typing import Callable

class Node:
    def __init__(self, parent, move, state, player, get_result:Callable, get_all_posible_moves:Callable, change_player:Callable, all_posible_moves = None):
        self.get_result = get_result
        self.get_all_posible_moves = get_all_posible_moves
        self.change_player = change_player
        
        self.wins = 0
        self.visits = 0
        self.parent = parent
        self.state = state
        self.child_nodes = []
        self.player = player
        self.move = move
        if all_posible_moves is None:
            all_posible_moves = get_all_posible_moves(state, player)
        self.untried_moves = all_posible_moves

    def get_uct_score(self, c: float = sqrt(2)):
        return self.wins / self.visits + c * \
            sqrt(log(self.parent.visits) / self.visits)

    def add_child(self, move, state):
        player = self.change_player(self.player)
        all_posible_moves = self.get_all_posible_moves(state, player)
        if all_posible_moves == []:
            p = self.change_player(player)
            all_posible_moves = self.get_all_posible_moves(state, p)
            if all_posible_moves != []:
                child = Node(self, move, state, p, self.get_result, self.get_all_posible_moves, self.change_player, all_posible_moves)
            else:
                child = Node(self, move, state, player, self.get_result, self.get_all_posible_moves, self.change_player, all_posible_moves)
        else:
            child = Node(self, move, state, player, self.get_result, self.get_all_posible_moves, self.change_player, all_posible_moves = all_posible_moves)

        self.child_nodes.append(child)
        self.untried_moves.remove(move)
        return child

    def backpropagation(self, state):
        self.visits +=1          
        if self.parent is not None:
            self.wins += self.get_result(state, self.parent.player)     
            self.parent.backpropagation(state)                