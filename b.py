from copy import deepcopy
import time
from ai.nodes import Node
from games.othello.othello import Othello
from games.player import MCTS_Player, Player

import random
from typing import Callable
from numba import njit
from math import log, sqrt
from typing import Callable

def get_result(state, player):
    player1_score = 0
    player2_score = 0
    for x in range(8):
        for y in range(8):  
            if state[x][y] == 1:
                player1_score += 1
            elif state[x][y] == 2:
                    player2_score += 1
    if player1_score == player2_score:
        return 0.5
    if player == 0:
        if player1_score > player2_score :
            return 1
        else :
            return 0
    if player1_score < player2_score :
        return 1
    else :
        return 0

def check_for_any_line(state, player, x, y, i, j):
    """ Check if move creates a line. 
        So if there is a line from (x,y) to another player's colored disk going through the neighbour (i,j), 
        where (i,j) has the opponent's color

    Args:
        colour ([type]): [description]
        x ([type]): move's x coordinate
        i ([type]): neighbour's x coordinate 

    Returns:
        [type]: boolean - true if it forms a correct line
    """
    neighX = i
    neighY = j
    
    #If the neighbour colour is equal to your colour, it doesn't form a line
    #Go onto the next neighbour
    if state[neighX][neighY]==player:
        return False

    #Determine the direction of the line
    deltaX = neighX-x
    deltaY = neighY-y
    tempX = neighX
    tempY = neighY
    
    while 0<=tempX<=7 and 0<=tempY<=7:
        #If an empty space, no line is formed
        if state[tempX][tempY]==None:
            return False
        #If it reaches a piece of the player's colour, it forms a line
        if state[tempX][tempY] == player:
            return True
        #Move the index according to the direction of the line
        tempX+=deltaX
        tempY+=deltaY
    return False

def check_move(state, move, player):
    """ Check if placing disk on (x,y) is a valid move

    Args:
        player ([type]): [description]
        x ([type]): [description]
        y ([type]): [description]

    Returns:
        [type]: [description]
    """
    x, y = move
    #Sets player colour
    colour = player
    #If there's already a piece there, it's an invalid move
    if state[x][y] != None:
        return False
    else:
        #Generating the list of neighbours
        neighbour = False
        neighbours = []
        valid = False
        for i in range(max(0,x-1),min(x+2,8)):
            for j in range(max(0,y-1),min(y+2,8)):
                if state[i][j]!=None:
                    neighbour=True
                    neighbours.append([i,j])
                    if not valid:
                        valid = check_for_any_line(state, colour, x, y, i, j)
        #If there's no neighbours, it's an invalid move
        if not neighbour:
            return False
        else:
            return valid

def get_all_posible_moves(state, player):
    moveList = []
    for x in range(8):
        for y in range(8):
            if check_move(state, (x,y), player):
                moveList.append((x,y))
    return moveList

def change_player(player):
    if player == 2:
        return 1
    else:
        return 2

def get_pieces_to_reverse(array,  player, x, y):
    #Must copy the passedArray so we don't alter the original
    # array = deepcopy(state)
    #Set colour and set the moved location to be that colour
    colour = player
    array[x][y] = colour
    
    #Determining the neighbours to the square
    neighbours = []
    for i in range(max(0,x-1),min(x+2,8)):
        for j in range(max(0,y-1),min(y+2,8)):
            if array[i][j]!=None:
                neighbours.append([i,j])
    
    #Which tiles to convert
    convert = []

    #For all the generated neighbours, determine if they form a line
    #If a line is formed, we will add it to the convert array
    for neighbour in neighbours:
        neighX = neighbour[0]
        neighY = neighbour[1]
        #Check if the neighbour is of a different colour - it must be to form a line
        if array[neighX][neighY]!=colour:
            #The path of each individual line
            path = []
            
            #Determining direction to move
            deltaX = neighX-x
            deltaY = neighY-y

            tempX = neighX
            tempY = neighY

            #While we are in the bounds of the board
            while 0<=tempX<=7 and 0<=tempY<=7:
                path.append([tempX,tempY])
                value = array[tempX][tempY]
                #If we reach a blank tile, we're done and there's no line
                if value==None:
                    break
                #If we reach a tile of the player's colour, a line is formed
                if value==colour:
                    #Append all of our path nodes to the convert array
                    for node in path:
                        convert.append(node)
                    break
                #Move the tile
                tempX+=deltaX
                tempY+=deltaY

    return convert  

def move(array,  player, x, y):
    """ Make move and reverse all influenced oponnent's disks 

    Returns:
        [type]: array - board after move
    """
    convert = get_pieces_to_reverse(array,  player, x, y)
                
    #Convert all the appropriate tiles
    for i,j in convert:
        array[i][j]=player

    # state = array

def check_and_make_move(state, m, player):
    if  check_move(state, m, player):
        # state[move[0]][move[1]] = player
        move(state, player, m[0], m[1])
        
        return True
    return False

def board_move(state, move, player):
    check_and_make_move(state, move, player)
    return state

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

def mcts_numba(initial_state, player, number_of_iteration, get_result:Callable, get_all_posible_moves:Callable, change_player:Callable, board_move:Callable, all_posible_moves:list):
    rootnode = Node(None, None, initial_state, player, get_result, get_all_posible_moves, change_player, all_posible_moves)
    for _ in range(number_of_iteration):
        node = rootnode

        # Selection
        while node.untried_moves == [] and node.child_nodes != []:
            node = select_uct_child(node.child_nodes)
        iteration_state = deepcopy(node.state)

        # Expansion
        if node.untried_moves != []:
            move = random.choice(node.untried_moves)
            board_move(iteration_state, move, node.player)
            node = node.add_child(move, iteration_state)
            iteration_state = deepcopy(iteration_state)
            

        # Playout
        player = node.player
        while 1:      
            all_possible_moves = get_all_posible_moves(iteration_state, player)
            if  all_possible_moves != []:
                move = random.choice(all_possible_moves)
                board_move(iteration_state, move, player)
                player = change_player(player)
                continue

            player = change_player(player)
            all_possible_moves = get_all_posible_moves(iteration_state, player)
            if  all_possible_moves != []:
                move = random.choice(all_possible_moves)
                board_move(iteration_state, move, player)
                player = change_player(player)
                continue

            break

        # Backpropagation
        node.backpropagation(iteration_state)

    return sorted(rootnode.child_nodes, key=lambda c: c.visits)[-1].move


class MCTS1_Player(Player):
    def __init__(self, number_of_iteration: int = 100):
        super().__init__(False)
        self.name = f"mcts{str(number_of_iteration)}"
        self.number_of_iteration = number_of_iteration

    def make_move(self, args):
        (initial_state, player, _, _, _, _, all_posible_moves) = args
        move = mcts_numba(initial_state, player, self.number_of_iteration, get_result, get_all_posible_moves, change_player, board_move, all_posible_moves)
        return move


if __name__ == "__main__":
    start_time = time.time()
    p1 = MCTS1_Player(50)
    p2 = MCTS1_Player(50)

    game = Othello(use_ui=False, player1=p1, player2=p2)
    game.play()
    print("--- %s seconds ---" % (time.time() - start_time))
