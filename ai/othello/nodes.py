from math import log, sqrt
from games.othello.msi2.othello2 import get_result, get_all_posible_moves, change_player

class Node:
    def __init__(self, parent, move, state, player, all_posible_moves = None):
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
        player = change_player(self.player)
        all_posible_moves = get_all_posible_moves(state, player)
        if all_posible_moves == []:
            p = change_player(player)
            all_posible_moves = get_all_posible_moves(state, p)
            if all_posible_moves != []:
                child = Node(self, move, state, p, all_posible_moves)
            else :
                child = Node(self, move, state, player, all_posible_moves)
        else:
            child = Node(self, move, state, player, all_posible_moves = all_posible_moves)

        self.child_nodes.append(child)
        self.untried_moves.remove(move)
        return child

    def backpropagation(self, state):
        self.visits +=1          
        if self.parent is not None:
            self.wins += get_result(state, self.parent.player)     
            self.parent.backpropagation(state)                


class RAVENode:
    def __init__(self, parent, move, state, player, all_posible_moves = None):
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
        player = change_player(self.player)
        all_posible_moves = get_all_posible_moves(state, player)
        if all_posible_moves == []:
            p = change_player(player)
            all_posible_moves = get_all_posible_moves(state, p)
            if all_posible_moves != []:
                child = RAVENode(self, move, state, p, all_posible_moves)
            else :
                child = RAVENode(self, move, state, player, all_posible_moves)
        else:
            child = RAVENode(self, move, state, player, all_posible_moves = all_posible_moves)

        self.child_nodes.append(child)
        self.untried_moves.remove(move)
        return child

    def get_rave_score(self, k: int = 1000):
        b = sqrt(k/((3*self.visits)+k))
        stat1 = 0
        if self.rave_visits != 0 :
            stat1 = (b * (self.rave_wins/self.rave_visits)) 
        stat2 = ((1-b) * (self.wins/self.visits))
        return stat1 + stat2

    def backpropagation(self, state, moves):
        update_children = [child for child in self.child_nodes if (child.move, child.player) in moves]
        for child in update_children:
            child.rave_wins += get_result(state, child.parent.player)
            child.rave_visits +=1

        self.visits +=1          
        if self.parent is not None:
            self.wins += get_result(state, self.parent.player)     
            self.parent.backpropagation(state, moves)    

class MASTNode:
    def __init__(self, parent, move, state, player, all_posible_moves = None):
        self.state = state
        self.parent = parent
        self.child_nodes = []
        self.player = player
        self.move = move
        if all_posible_moves is None:
            all_posible_moves = get_all_posible_moves(state, player)
        self.untried_moves = all_posible_moves


    def add_child(self, move, state):
        player = change_player(self.player)
        all_posible_moves = get_all_posible_moves(state, player)
        if all_posible_moves == []:
            p = change_player(player)
            all_posible_moves = get_all_posible_moves(state, p)
            if all_posible_moves != []:
                child = Node(self, move, state, p, all_posible_moves)
            else :
                child = Node(self, move, state, player, all_posible_moves)
        else:
            child = Node(self, move, state, player, all_posible_moves = all_posible_moves)

        self.child_nodes.append(child)
        self.untried_moves.remove(move)
        return child
