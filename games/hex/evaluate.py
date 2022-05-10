import numpy as np
from games.hex.common import get_dijkstra_score


def hex_evaluate(state, player):
    return get_dijkstra_score(state, player)

def get_dijkstra_score(board, color): 
    """gets the dijkstra score for a certain color, differs from dijkstra eval in that it only considers the passed color
    Args:
        color (Hexboard.Color): What color to evaluate
    Returns:
        int: score of how many (shortest) path-steps remain to victory
    """
    LOSE = 1000 # Choose win value higher than possible score but lower than INF

    board_size = len(board)
    scores = np.array([[LOSE for i in range(board_size)] for j in range(board_size)])
    updated = np.array([[True for i in range(board_size)] for j in range(board_size)]) #Start updating at one side of the board 

    #alignment of color (blue = left->right so (1,0))
    alignment = (0, 1) if color == 2 else (1, 0)


    for i in range(board_size):
        newcoord = tuple([i * j for j in alignment]) #iterate over last row or column based on alignment of current color

        updated[newcoord] = False
        if board[newcoord] == color: #if same color --> path starts at 0
            scores[newcoord] = 0
        elif board[newcoord] == 0: #if empty --> costs 1 move to use this path 
            scores[newcoord] = 1
        else: #If other color --> can't use this path
            scores[newcoord] = LOSE

    scores = dijkstra_update(board, color, scores, updated)

    #self.board.print_dijkstra(scores)

    results = [scores[alignment[0] * i - 1 + alignment[0]][alignment[1]*i - 1 + alignment[1]] for i in range( board_size)] #take "other side" to get the list of distance from end-end on board
    best_result = min(results)
    
    # if best_result == 0:
    #     best_result = -500
    
    # log.debug("Best score for color {}: {}".format(color, best_result))
    return LOSE - best_result #return minimum distance to get current score

def dijkstra_update(board, color, scores, updated):
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
                    neighborcoords = get_neighbors((i,j), len(board))
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

def get_neighbors(coordinates, board_size):
    """Gets all the neighbouring cells of a given cell
    Args:
        coordinates (tuple): Cell (x, y) coordinates
    Returns:
        list: List of neighbouring cell coordinates tuples
    """
    (cx,cy) = coordinates
    neighbors = []
    if cx-1 >= 0: neighbors.append((cx-1,cy))
    if cx+1 < board_size: neighbors.append((cx+1,cy))
    if cx-1 >= 0 and cy+1 <= board_size-1: neighbors.append((cx-1,cy+1))
    if cx+1 < board_size and cy-1 >= 0: neighbors.append((cx+1,cy-1))
    if cy+1 < board_size: neighbors.append((cx,cy+1))
    if cy-1 >= 0: neighbors.append((cx,cy-1))

    return neighbors

