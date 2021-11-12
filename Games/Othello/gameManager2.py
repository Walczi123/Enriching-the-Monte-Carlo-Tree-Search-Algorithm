from tkinter import *
from math import *
from time import *
from random import *
from copy import deepcopy
from tkinter import font
import Game.othello2 as ot
import Game.globals as cdf

from AI.Heuristic import heu
from AI.MCTS import MCTS
from AI.MCTS_MAST import MCTS_MAST
from AI.MCTS_RAVE import MCTS_RAVE


g = cdf.Globals()
algorithm = None
TREE_ITERATIONS = 5
player_first = False

algorithmNames={
	'heu': 'Heuristic',
	'MCTS': 'MCTS',
	'MCTS_MAST': 'MAST',
	'MCTS_RAVE': 'RAVE',
}

def clickHandle(event):
	""" Player's engine - handles click, checks move correctness and switches to computer's turn
		If clicked just after begginging chooses gameplay mode.
	"""
	global player_first
	xMouse = event.x
	yMouse = event.y
	if g.running1:
		if g.running2:
			if not(g.computerMove):
				if xMouse >= 450 and yMouse <= 50:
					g.root.destroy()
				elif xMouse <= 50 and yMouse <= 50:
					runGame()
				else:
					if not(ot.must_pass(g.board.placements, g.board.player)):
						# Delete the highlights
						x = int((event.x-50)/50)
						y = int((event.y-50)/50)
						# Determine the grid index for where the mouse was clicked

						# If the click is inside the bounds and the move is valid, move to that location
						if 0 <= x <= 7 and 0 <= y <= 7:
							if ot.valid(g.board.placements, g.board.player, x, y):
								# g.board.update("2")
								g.board.oldplacements, g.board.placements = ot.board_move(
									g.board.placements, g.board.player, x, y)
								g.switchPlayer()
								g.board.update()
								doValidComputerMove()
					else: 
						g.switchPlayer()
						if ot.must_pass(g.board.placements, g.board.player):
							print("Game won")
							gameWonBoard()
						else:
							doValidComputerMove()
			else:
				doValidComputerMove()
		else:
			# Gametype clicking
			g.running2 = True
			
			if 40 <= xMouse <= 250 and 360 <= yMouse <= 405:
				alg = MCTS
			elif 260 <= xMouse <= 470 and 360 <= yMouse <= 405:
				alg = MCTS_RAVE
			elif 40 <= xMouse <= 250 and 415 <= yMouse <= 460:
				alg = MCTS_MAST
			elif 260 <= xMouse <= 470 and 415 <= yMouse <= 460:
				alg = heu
				
			if player_first:
				playGamevsAlgorithm(alg)
			else:
				playAlgorithmvsGame(alg)
	else:
		if 40 <= xMouse <= 250:
			player_first = True
			#Two star
		elif 260 <= xMouse <= 470:
			player_first = False
		g.running1 = True
		setAlgorithm()



def doValidComputerMove():
	#todo
	if g.computerMove:
		if not(ot.must_pass(g.board.placements, g.board.player)):
			placements = deepcopy(g.board.placements)
			x, y = eval(
				str(algorithm(placements, g.board.player, TREE_ITERATIONS)))
			sleep(0.5)
			g.board.oldplacements, g.board.placements = ot.board_move(
				g.board.placements, g.board.player, x, y)
			g.switchPlayer()
			g.board.update()
			if ot.must_pass(g.board.placements, g.board.player):
				print("Game won")
				gameWonBoard()
				
			# g.computerMove = False
		else: 
			g.switchPlayer()
			if ot.must_pass(g.board.placements, g.board.player):
				print("Game won")
				gameWonBoard()
			else:
				doValidComputerMove()


def playAlgorithmvsGame(alg):
	global algorithm
	algorithm = alg

	g.running = True
	g.screen.delete(ALL)
	create_buttons()
	# Draw the background
	drawGridBackground()
	markPlayers(alg)

	g.set_players(1,0)
	g.board = ot.Board(g, g.player1)
	g.board.update()
	doValidComputerMove()

def playGamevsAlgorithm(alg):
	global algorithm
	algorithm = alg
	g.running = True
	g.screen.delete(ALL)
	create_buttons()
	# Draw the background
	drawGridBackground()
	markPlayers(alg)
	
	g.set_players(0,1)
	g.board = ot.Board(g, g.player1)
	g.board.update()


def markPlayers(alg):
	g.screen.create_text(30, 500, anchor="w", tags="score_player", font=(
		"Consolas", 15), fill="white", text="Player")
	g.screen.create_text(400, 500, anchor="w", tags="score_player", font=(
		"Consolas", 15), fill="black", text=algorithmNames[alg.__name__])
	g.screen.update()

def gameWonBoard():
	sleep(0.4)
	g.screen.delete(ALL)

	g.running2 = False
	g.board.drawScoreBoard()
	markPlayers(algorithm)
	g.screen.create_text(250, 220, anchor="c", font=(
		"Consolas", 30), text="The game is done!")

def runGame():
	""" Start game, create game board, let the player choose gameplay mode
	"""
	g.screen.delete(ALL)
	g.running1 = False
	# Title and shadow
	g.screen.create_text(250, 203, anchor="c", text="Othello", font=(
		"Consolas", 50), fill="dark slate gray")
	g.screen.create_text(250, 200, anchor="c", text="Othello",
						 font=("Consolas", 50), fill="white smoke")

	# Creating the play buttons, 1- two players, 2- player vs computer, 3- computer vs computerfor i in range(3):
	# Background
	# i=1
	# g.screen.create_rectangle(
	# 	25+155*i, 310, 155+155*i, 355, fill="dark slate gray", outline="dark slate gray")
	# g.screen.create_rectangle(25+155*i, 300, 155+155*i,
	# 						  350, fill="cadet blue", outline="cadet blue")

	# # Creating the difficulty buttons
	g.screen.create_rectangle(
		40, 360, 250, 405, fill="dark slate gray", outline="#000")
	g.screen.create_rectangle(
		40, 350, 250, 400, fill="cadet blue", outline="#111")

	g.screen.create_rectangle(
		260, 360, 470, 405, fill="dark slate gray", outline="#000")
	g.screen.create_rectangle(
		260, 350, 470, 400, fill="cadet blue", outline="#111")
	
	g.screen.create_text(250, 330, anchor="c", text="Who should be the first player?",
                      font=("Consolas", 20), fill="white smoke")
	g.screen.create_text(145, 375, anchor="c",
	                     text="Me", font=("Consolas", 20), fill="gainsboro")
	g.screen.create_text(365, 375, anchor="c",
	                     text="Algorithm", font=("Consolas", 20), fill="gainsboro")

def setAlgorithm():
	g.screen.delete(ALL)
	g.running2 = False
	# Title and shadow
	g.screen.create_text(250, 203, anchor="c", text="Othello", font=(
		"Consolas", 50), fill="dark slate gray")
	g.screen.create_text(250, 200, anchor="c", text="Othello",
                      font=("Consolas", 50), fill="white smoke")

	# # Creating the difficulty buttons
	g.screen.create_rectangle(
		40, 360, 250, 405, fill="dark slate gray", outline="#000")
	g.screen.create_rectangle(
		40, 350, 250, 400, fill="cadet blue", outline="#111")

	g.screen.create_rectangle(
		260, 360, 470, 405, fill="dark slate gray", outline="#000")
	g.screen.create_rectangle(
		260, 350, 470, 400, fill="cadet blue", outline="#111")
	
	g.screen.create_rectangle(
		40, 415, 250, 460, fill="dark slate gray", outline="#000")
	g.screen.create_rectangle(
		40, 410, 250, 455, fill="cadet blue", outline="#111")

	g.screen.create_rectangle(
		260, 415, 470, 460, fill="dark slate gray", outline="#000")
	g.screen.create_rectangle(
		260, 410, 470, 455, fill="cadet blue", outline="#111")

	g.screen.create_text(250, 330, anchor="c", text="Which algorithm would you like to test?",
                      font=("Consolas", 15), fill="white smoke")
	g.screen.create_text(145, 375, anchor="c",
	                     text="MCTS", font=("Consolas", 20), fill="gainsboro")
	g.screen.create_text(365, 375, anchor="c",
	                     text="RAVE", font=("Consolas", 20), fill="gainsboro")
	g.screen.create_text(145, 430, anchor="c",
	                     text="MAST", font=("Consolas", 20), fill="gainsboro")
	g.screen.create_text(365, 430, anchor="c",
	                     text="Heur.", font=("Consolas", 20), fill="gainsboro")

#Method for drawing the gridlines
def drawGridBackground(outline=True):
	#If we want an outline on the board then draw one
	if outline:
		g.screen.create_rectangle(50,50,450,450,outline="#111")

	#Drawing the intermediate lines
	for i in range(7):
		lineShift = 50+50*(i+1)

		#Horizontal line
		g.screen.create_line(50,lineShift,450,lineShift,fill="#111")

		#Vertical line
		g.screen.create_line(lineShift,50,lineShift,450,fill="#111")

	g.screen.update()

def create_buttons():
		#Restart button
		#Background/shadow
		g.screen.create_rectangle(0,5,50,55,fill="#000033", outline="#000033")
		g.screen.create_rectangle(0,0,50,50,fill="#000088", outline="#000088")

		#Arrow
		g.screen.create_arc(5,5,45,45,fill="#000088", width="2",style="arc",outline="white",extent=300)
		g.screen.create_polygon(33,38,36,45,40,39,fill="white",outline="white")

		#Quit button
		#Background/shadow
		g.screen.create_rectangle(450,5,500,55,fill="#330000", outline="#330000")
		g.screen.create_rectangle(450,0,500,50,fill="#880000", outline="#880000")
		#"X"
		g.screen.create_line(455,5,495,45,fill="white",width="3")
		g.screen.create_line(495,5,455,45,fill="white",width="3")
		

if __name__ == "__main__":
	
	runGame()

	# # Binding, setting
	g.screen.bind("<Button-1>", clickHandle)
	# g.screen.bind("<Key>", keyHandle)
	g.screen.focus_set()

	# Run forever
	g.root.wm_title("Not othello")
	g.root.mainloop()
