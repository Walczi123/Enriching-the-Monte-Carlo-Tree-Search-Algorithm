import random
from typing import Callable
from ai.nodes import Node


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


def mcts(initial_state, player, number_of_iteration, get_result:Callable, get_all_posible_moves:Callable, change_player:Callable, board_move:Callable, max_depth:int = 3):
	rootnode = Node(None, None, initial_state, player, get_result, get_all_posible_moves, change_player, all_posible_moves = None, max_depth = max_depth)
	for _ in range(number_of_iteration):
		node = rootnode
		iteration_state = node.state

		# Selection
		while node.untried_moves == [] and node.child_nodes != []:
			node = select_uct_child(node.child_nodes)

		# Expansion
		if node.untried_moves != []:
			move = random.choice(node.untried_moves)
			iteration_state = board_move(iteration_state, move, node.player)
			node = node.add_child(move, iteration_state)

		# Playout
		player = node.player
		j = 0
		while (max_depth < 1 or node.depth + j < max_depth):    
			j += 1      
			all_possible_moves = get_all_posible_moves(iteration_state, player)
			if  all_possible_moves != []:
				move = random.choice(all_possible_moves)
				iteration_state = board_move(iteration_state, move, player)
				player = change_player(player)
				continue

			player = change_player(player)
			all_possible_moves = get_all_posible_moves(iteration_state, player)
			if  all_possible_moves != []:
				move = random.choice(all_possible_moves)
				iteration_state = board_move(iteration_state, move, player)
				player = change_player(player)
				continue

			break

		# Backpropagation
		node.backpropagation(iteration_state)

	return sorted(rootnode.child_nodes, key=lambda c: c.visits)[-1].move
