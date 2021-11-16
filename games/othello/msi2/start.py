import games.othello.msi2.othello2 as ot
import games.othello.msi2.globals as cdf
import copy 

from time import *

WAIT_TIME = 0.5

g = cdf.Globals()
DEPTH = 800

def run_game(f1, f2, n_iterations=DEPTH, printfinalResult=False, printSteps=False):
    """[summary]

    Args:
        f1 (function name with library): AI function name (must take three arguments: gamestate table, player (0 or 1), iterations amount) \n \t
        f2 (function name with library): AI function name (must take three arguments: gamestate table, player (0 or 1), iterations amount) \n \t
        printfinalResult (bool): Indicates whether the final state of the game should be displayed \n \t
        printSteps (bool): Indicates whether every move of the game should be displayed \n

    Returns:
        int: Number of the winner
    """

    if printfinalResult or printSteps:
        drawGridBackground()

    g.board = ot.Board(g)
    passed_1 = False
    passed_2 = False
    moves_amount = 0

    while not(passed_2 and passed_1):
        passed_1 = False
        passed_2 = False

        if not(ot.must_pass(g.board.placements, g.board.player)):
            placements_to_pass = copy.deepcopy(g.board.placements)
            x, y = f1(placements_to_pass, g.board.player, n_iterations, ot.get_result, ot.get_all_posible_moves, ot.change_player, ot.board_move2)

            g.board.oldplacements, g.board.placements = ot.board_move(g.board.placements, g.board.player, x, y)
            if printSteps:
                print("0 " , x,y)
                g.board.update()
                sleep(WAIT_TIME)
        else:
            passed_1 = True

        g.switchPlayer()  #player2

        if not(ot.must_pass(g.board.placements, g.board.player)):
            placements_to_pass = copy.deepcopy(g.board.placements)
            x, y = f2(placements_to_pass, g.board.player, n_iterations, ot.get_result, ot.get_all_posible_moves, ot.change_player, ot.board_move2)
            g.board.oldplacements, g.board.placements = ot.board_move(g.board.placements, g.board.player, x, y)
            if printSteps:
                print("1 ", x, y)
                g.board.update()
                sleep(WAIT_TIME)
            g.switchPlayer()  # player1
        else:
            passed_2 = True
            g.switchPlayer()  # player1
            if ot.must_pass(g.board.placements, g.board.player):
                passed_1 = True
        moves_amount += 1

    if printfinalResult:
        g.board.update_without_animation(sleep_time = 10*WAIT_TIME)

    if ot.get_result(g.board.placements, g.board.player):
        return g.board.player, moves_amount
    else:
        g.switchPlayer()
        return g.board.player, moves_amount
    
    


#Method for drawing the gridlines
def drawGridBackground(outline=True):
	#If we want an outline on the board then draw one
	if outline:
		g.screen.create_rectangle(50, 50, 450, 450, outline="#111")

	#Drawing the intermediate lines
	for i in range(7):
		lineShift = 50+50*(i+1)

		#Horizontal line
		g.screen.create_line(50, lineShift, 450, lineShift, fill="#111")

		#Vertical line
		g.screen.create_line(lineShift, 50, lineShift, 450, fill="#111")

	g.screen.update()


# if __name__ == "__main__":
#     # result = run_game(MCTS_RAVE, MCTS_MAST,  n_iterations=800, printfinalResult=True, printSteps=True)
#     # print(result)

#     start()