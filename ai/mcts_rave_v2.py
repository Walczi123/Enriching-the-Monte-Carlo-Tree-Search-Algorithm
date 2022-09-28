from copy import deepcopy
import random
from typing import Callable

from ai.nodes import RAVENode, RAVENodev2



def select_rave_child(childNodes):
    bestChildren = list()
    bestScore = - float("inf")

    for childNode in childNodes:
        score = childNode.get_rave_score()
        if score > bestScore:
            bestScore = score
            bestChildren = [childNode]
        elif score == bestScore:
            bestChildren.append(childNode)

    return random.choice(bestChildren)
    
def mcts_rave_v2(initial_state, player, number_of_iteration, get_result:Callable, get_all_posible_moves:Callable, change_player:Callable, board_move:Callable, all_posible_moves:list):
    rootnode = RAVENodev2(None, None, initial_state, player, get_result, get_all_posible_moves, change_player, all_posible_moves)
    for _ in range(number_of_iteration):
        node = rootnode
        moves = []

        # Selection
        while node.untried_moves == [] and node.child_nodes != []:
            node = select_rave_child(node.child_nodes)
            moves.append((node.move, node.player))
        iteration_state = deepcopy(node.state)

        # Expansion
        if node.untried_moves != []:
            move = random.choice(node.untried_moves)
            iteration_state = board_move(iteration_state, move, node.player)
            node = node.add_child(move, iteration_state)
            moves.append((node.move, node.player))
            iteration_state = deepcopy(node.state)

        # Playout
        player = node.player
        while 1:          
            all_possible_moves = get_all_posible_moves(iteration_state, player)
            if  all_possible_moves != []:
                move = random.choice(all_possible_moves)
                board_move(iteration_state, move, player)
                moves.append((move, player))
                player = change_player(player)
                continue

            player = change_player(player)
            all_possible_moves = get_all_posible_moves(iteration_state, player)
            if  all_possible_moves != []:
                move = random.choice(all_possible_moves)
                board_move(iteration_state, move, player)
                moves.append((move, player))
                player = change_player(player)
                continue

            break

        # Backpropagation
        node.backpropagation(iteration_state, moves)
    return sorted(rootnode.child_nodes, key=lambda c: c.visits)[-1].move
