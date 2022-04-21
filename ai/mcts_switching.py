from copy import deepcopy
import random
from typing import Callable
from ai.nodes import Node
from ai.switching_mechanism import SwitchingMechanism

def select_uct_child(childNodes):
	bestChildren = list()
	bestScore = - float("inf")

	for childNode in childNodes:
		score = childNode.get_uct_score()
		if score > bestScore:
			bestScore = score
			bestChildren = [childNode]
		elif score == bestScore:
			bestChildren.append(childNode)

	return random.choice(bestChildren)


def mcts_switching(initial_state, player, number_of_iteration, get_result:Callable, get_all_posible_moves:Callable, change_player:Callable, board_move:Callable, strategies:list, max_depth:int = -1):
	switching_mechanism = SwitchingMechanism(strategies)
	rootnode = Node(None, None, initial_state, player, get_result, get_all_posible_moves, change_player)
	for i in range(number_of_iteration):
		node = rootnode

		# Selection
		while node.untried_moves == [] and node.child_nodes != []:
			node = select_uct_child(node.child_nodes)
		iteration_state = node.state

		# Expansion
		if node.untried_moves != []:
			# move = switching_mechanism.get_move_from_strategy(node.untried_moves)
			move = random.choice(node.untried_moves)
			iteration_state = board_move(iteration_state, move, node.player)
			node = node.add_child(move, iteration_state)

		# Playout
		player = node.player
		strategy = switching_mechanism.choose_strategy(i)
		j = 0
		while (max_depth < 1 or j < max_depth):    
			j += 1         
			all_possible_moves = get_all_posible_moves(iteration_state, player)
			if  all_possible_moves != []:
				move = strategy(all_possible_moves, iteration_state, board_move, get_all_posible_moves, player, change_player)
				iteration_state = board_move(iteration_state, move, player)
				player = change_player(player)
				continue

			player = change_player(player)
			all_possible_moves = get_all_posible_moves(iteration_state, player)
			if  all_possible_moves != []:
				move = strategy(all_possible_moves, iteration_state, board_move, get_all_posible_moves, player, change_player)
				iteration_state = board_move(iteration_state, move, player)
				player = change_player(player)
				continue

			break

		# Backpropagation
		node.backpropagation(iteration_state)
		switching_mechanism.update_strategy_result(strategy, get_result(iteration_state, player))

	return sorted(rootnode.child_nodes, key=lambda c: c.visits)[-1].move
