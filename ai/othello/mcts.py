import random
from mcts.nodes import Node
from games.othello.msi2.othello2 import get_all_posible_moves, board_move, change_player


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


def MCTS(initial_state, player, number_of_iteration):
	rootnode = Node(None, None, initial_state, player)
	for _ in range(number_of_iteration):
		node = rootnode
		iteration_state = node.state

		# Selection
		while node.untried_moves == [] and node.child_nodes != []:
			node = select_uct_child(node.child_nodes)

		# Expansion
		if node.untried_moves != []:
			move = random.choice(node.untried_moves)
			_, iteration_state = board_move(iteration_state, node.player, move[0], move[1])
			node = node.add_child(move, iteration_state)

		# Playout
		player = node.player
		while True:          
			all_possible_moves = get_all_posible_moves(iteration_state, player)
			if  all_possible_moves != []:
				move = random.choice(all_possible_moves)
				_, iteration_state = board_move(iteration_state, player, move[0], move[1])
				player = change_player(player)
				continue

			player = change_player(player)
			all_possible_moves = get_all_posible_moves(iteration_state, player)
			if  all_possible_moves != []:
				move = random.choice(all_possible_moves)
				_, iteration_state = board_move(iteration_state, player, move[0], move[1])
				player = change_player(player)
				continue

			break

		# Backpropagation
		node.backpropagation(iteration_state)

	return sorted(rootnode.child_nodes, key=lambda c: c.visits)[-1].move
