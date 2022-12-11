from cmath import inf
from games.hex.const import BLUE_PLAYER, RED_PLAYER


def get_dijkstra_score(board, color): 
    LOSE = 1000 
    board_size = len(board)
    scores = [[LOSE for x in range(board_size)] for y in range(board_size)] 
    updated = [[True for x in range(board_size)] for y in range(board_size)]

    alignment = (0, 1) if color == 2 else (1, 0)


    for i in range(board_size):
        newcoord = tuple([i * j for j in alignment])

        updated[newcoord[0]][newcoord[1]] = False
        if board[newcoord[0]][newcoord[1]] == color:
            scores[newcoord[0]][newcoord[1]] = 0
        elif board[newcoord[0]][newcoord[1]] == 0:
            scores[newcoord[0]][newcoord[1]] = 1
        else:
            scores[newcoord[0]][newcoord[1]] = LOSE

    scores = dijkstra_update(board, color, scores, updated)
    results = [scores[alignment[0] * i - 1 + alignment[0]][alignment[1]*i - 1 + alignment[1]] for i in range( board_size)] #take "other side" to get the list of distance from end-end on board
    best_result = min(results)
    
    return LOSE - best_result

def dijkstra_update(board, color, scores, updated):
    LOSE = 500
    updating = True
    while updating: 
        updating = False
        for i, row in enumerate(scores):
            for j, point in enumerate(row):
                if not updated[i][j]: 
                    neighborcoords = get_neighbours((i,j), len(board))
                    for neighborcoord in neighborcoords:
                        path_cost = inf
                        if board[neighborcoord[0]][neighborcoord[1]] == 0:
                            path_cost = 1
                        elif board[neighborcoord[0]][neighborcoord[1]] == color:
                            path_cost = 0
                        
                        if scores[neighborcoord[0]][neighborcoord[1]] > scores[i][j] + path_cost:
                            scores[neighborcoord[0]][neighborcoord[1]] = scores[i][j] + path_cost
                            updated[neighborcoord[0]][neighborcoord[1]] = False 
                            updating = True                          
    return scores

def get_neighbours(coordinates, board_size):
    (cx,cy) = coordinates
    neighbors = []
    if cx-1 >= 0: neighbors.append((cx-1,cy))
    if cx+1 < board_size: neighbors.append((cx+1,cy))
    if cx-1 >= 0 and cy+1 <= board_size-1: neighbors.append((cx-1,cy+1))
    if cx+1 < board_size and cy-1 >= 0: neighbors.append((cx+1,cy-1))
    if cy+1 < board_size: neighbors.append((cx,cy+1))
    if cy-1 >= 0: neighbors.append((cx,cy-1))

    return neighbors

def get_possible_moves(board: list):
    free_coordinates = []
    for x in range(len(board)):
        for y in range(len(board)):
            if board[x][y] == 0 :
                free_coordinates.append((x,y))

    return free_coordinates

def is_game_over(player: int, board: list, return_winner:bool = True):
    if not return_winner and not get_possible_moves(board):
        return True

    if player is None:
        for _ in range(len(board)):
            path = traverse((_, 0), BLUE_PLAYER, board, list(), len(board))
            if path:
                return BLUE_PLAYER

            path = traverse((0, _), RED_PLAYER, board, list(), len(board))
            if path:
                return RED_PLAYER           
    else:
        for _ in range(len(board)):
            if player is BLUE_PLAYER:
                border = (_, 0)
            if player is RED_PLAYER:
                border = (0, _)

            path = traverse(border, player, board, list(), len(board))
            if path:
                return player

def is_border(node: tuple, player: int, board_size):
    x, y = node
    if player is BLUE_PLAYER:
        if y == board_size - 1:
            return True
    elif player is RED_PLAYER:
        if x == board_size - 1:
            return True

def traverse(node: tuple, player: int, board: list, visited: list, board_size):
    x, y = node 
    achiachieved_border = False    
    if not ((x, y) in visited) and board[x][y] == player:
        visited.append((x, y))

        if is_border(node, player, board_size):
            achiachieved_border =  True

        neighbours = get_neighbours((x, y), board_size)
        for neighbour in neighbours:
            if traverse(neighbour, player, board, visited, board_size):
                achiachieved_border =  True

    if achiachieved_border:
        return visited