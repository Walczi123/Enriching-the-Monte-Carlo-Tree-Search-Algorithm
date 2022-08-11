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
            child = Node(self, move, state, player, self.get_result, self.get_all_posible_moves, self.change_player, all_posible_moves)

        self.child_nodes.append(child)
        self.untried_moves.remove(move)
        return child

    def backpropagation(self, state):
        self.visits +=1          
        if self.parent is not None:
            self.wins += self.get_result(state, self.parent.player)     
            self.parent.backpropagation(state)                

class RAVENode:
    def __init__(self, parent, move, state, player, get_result:Callable, get_all_posible_moves:Callable, change_player:Callable, all_posible_moves = None):
        self.get_result = get_result
        self.get_all_posible_moves = get_all_posible_moves
        self.change_player = change_player

        self.rave_wins = 0
        self.rave_visits = 0
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

    def add_child(self, move, state):
        player = self.change_player(self.player)
        all_posible_moves = self.get_all_posible_moves(state, player)
        if all_posible_moves == []:
            p = self.change_player(player)
            all_posible_moves = self.get_all_posible_moves(state, p)
            if all_posible_moves != []:
                child = RAVENode(self, move, state, p, self.get_result, self.get_all_posible_moves, self.change_player, all_posible_moves)
            else :
                child = RAVENode(self, move, state, player, self.get_result, self.get_all_posible_moves, self.change_player, all_posible_moves)
        else:
            child = RAVENode(self, move, state, player, self.get_result, self.get_all_posible_moves, self.change_player, all_posible_moves = all_posible_moves)

        self.child_nodes.append(child)
        self.untried_moves.remove(move)
        return child

    def get_rave_score(self, c: float = sqrt(2), k: int = 1000):
        b = sqrt(k/((3*self.visits)+k))
        stat1 = 0
        if self.rave_visits != 0 :
            stat1 = (b * (self.rave_wins/self.rave_visits)) 
        stat2 = ((1-b) * (self.wins/self.visits))
        return stat1 + stat2 + (c * sqrt(log(self.parent.visits) / self.visits))

    def backpropagation(self, state, moves):
        update_children = [child for child in self.child_nodes if (child.move, child.player) in moves]
        for child in update_children:
            child.rave_wins += self.get_result(state, child.parent.player)
            child.rave_visits +=1

        self.visits +=1          
        if self.parent is not None:
            self.wins += self.get_result(state, self.parent.player)     
            self.parent.backpropagation(state, moves)    
