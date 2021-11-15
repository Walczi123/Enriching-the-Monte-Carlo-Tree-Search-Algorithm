from copy import deepcopy
from tkinter import *
from math import *
from time import *
from random import *

class Board:
	def __init__(self, globalValues, player = 0):
		self.player = player
		self.passed = False
		self.won = False
		self.g = globalValues
		self.placements = create_start_state()
		#Initializing old values
		self.oldplacements = deepcopy(self.placements)

	
	def update(self, i=0):
		""" Redraw the board, animate changes beetween moves, 
			add player possible moves signalization
		"""
		self.g.screen.delete("highlight")
		self.g.screen.delete("tile")
		self.g.screen.delete("player_signalization")
		for x in range(8):
			for y in range(8):
				#Could replace the circles with images later, if I want
				if self.oldplacements[x][y]==0:
					self.g.screen.create_oval(54+50*x,54+50*y,96+50*x,96+50*y,tags="tile {0}-{1}".format(x,y),fill="#aaa",outline="#aaa")
					self.g.screen.create_oval(54+50*x,52+50*y,96+50*x,94+50*y,tags="tile {0}-{1}".format(x,y),fill="#fff",outline="#fff")

				elif self.oldplacements[x][y]==1:
					self.g.screen.create_oval(54+50*x,54+50*y,96+50*x,96+50*y,tags="tile {0}-{1}".format(x,y),fill="#000",outline="#000")
					self.g.screen.create_oval(54+50*x,52+50*y,96+50*x,94+50*y,tags="tile {0}-{1}".format(x,y),fill="#111",outline="#111")
		#Animation of new tiles
		self.g.screen.update()
		sleep(0.12)
		for x in range(8):
			for y in range(8):
				if self.placements[x][y] != self.oldplacements[x][y] and self.placements[x][y] == 0:
					self.g.screen.delete("{0}-{1}".format(x,y))
					#42 is width of tile so 21 is half of that
					#Shrinking
					for i in range(21):
						self.g.screen.create_oval(54+i+50*x,54+i+50*y,96-i+50*x,96-i+50*y,tags="tile animated",fill="#000",outline="#000")
						self.g.screen.create_oval(54+i+50*x,52+i+50*y,96-i+50*x,94-i+50*y,tags="tile animated",fill="#111",outline="#111")
						if i%3==0:
							sleep(0.01)
						self.g.screen.update()
						self.g.screen.delete("animated")
					#Growing
					for i in reversed(range(21)):
						self.g.screen.create_oval(54+i+50*x,54+i+50*y,96-i+50*x,96-i+50*y,tags="tile animated",fill="#aaa",outline="#aaa")
						self.g.screen.create_oval(54+i+50*x,52+i+50*y,96-i+50*x,94-i+50*y,tags="tile animated",fill="#fff",outline="#fff")
						if i%3==0:
							sleep(0.01)
						self.g.screen.update()
						self.g.screen.delete("animated")
					self.g.screen.create_oval(54+50*x,54+50*y,96+50*x,96+50*y,tags="tile",fill="#aaa",outline="#aaa")
					self.g.screen.create_oval(54+50*x,52+50*y,96+50*x,94+50*y,tags="tile",fill="#fff",outline="#fff")
					self.g.screen.update()

				elif self.placements[x][y]!=self.oldplacements[x][y] and self.placements[x][y]==1:
					self.g.screen.delete("{0}-{1}".format(x,y))
					#42 is width of tile so 21 is half of that
					#Shrinking
					for i in range(21):
						self.g.screen.create_oval(54+i+50*x,54+i+50*y,96-i+50*x,96-i+50*y,tags="tile animated",fill="#aaa",outline="#aaa")
						self.g.screen.create_oval(54+i+50*x,52+i+50*y,96-i+50*x,94-i+50*y,tags="tile animated",fill="#fff",outline="#fff")
						if i%3==0:
							sleep(0.01)
						self.g.screen.update()
						self.g.screen.delete("animated")
					#Growing
					for i in reversed(range(21)):
						self.g.screen.create_oval(54+i+50*x,54+i+50*y,96-i+50*x,96-i+50*y,tags="tile animated",fill="#000",outline="#000")
						self.g.screen.create_oval(54+i+50*x,52+i+50*y,96-i+50*x,94-i+50*y,tags="tile animated",fill="#111",outline="#111")
						if i%3==0:
							sleep(0.01)
						self.g.screen.update()
						self.g.screen.delete("animated")

					self.g.screen.create_oval(54+50*x,54+50*y,96+50*x,96+50*y,tags="tile",fill="#000",outline="#000")
					self.g.screen.create_oval(54+50*x,52+50*y,96+50*x,94+50*y,tags="tile",fill="#111",outline="#111")
					self.g.screen.update()
		#Drawing of highlight circles
		#Drawing player sygnalization box
		if self.player == 0:
			sleep(0.02)
			self.g.screen.create_rectangle(60,455,440,465,tags="player_signalization", fill="white")
		if self.player == 1:
			sleep(0.02)
			self.g.screen.create_rectangle(60,455,440,465,tags="player_signalization", fill="black")
			self.g.screen.create_text(250, 480, tags="player_signalization", anchor="c", text="Thinking...",
                            font=("Consolas", 15), fill="black")
	
		for x in range(8):
			for y in range(8):
				if self.player == 0:
					if valid(self.placements, self.player,x,y):
						# helv36 = font.Font(family='Helvetica', size=36, weight='bold')
						# self.g.screen.create_text(68+50*x,68+50*y,32+50*(x+1),32+50*(y+1), anchor=W, font=("Helvetica",60), text="X")
						self.g.screen.create_oval(68+50*x,68+50*y,32+50*(x+1),32+50*(y+1),tags="highlight",fill="grey78")
				elif self.player == 1 and not(self.g.computerMove):
					if valid(self.placements, self.player, x, y):
						self.g.screen.create_oval(68+50*x,68+50*y,32+50*(x+1),32+50*(y+1),tags="highlight",fill="grey30")
		if not self.won:
			#Draw the scoreboard and update the self.g.screen
			self.drawScoreBoard()
			self.g.screen.update()
		else:
			self.g.screen.create_text(250,550,anchor="c",font=("Consolas",15), text="The game is done!")

	def drawScoreBoard(self):
		#Deleting prior score elements
		self.g.screen.delete("score")

		#Scoring based on number of tiles
		player_score = 0
		computer_score = 0
		for x in range(8):
			for y in range(8):
				if self.placements[x][y]==0:
					player_score+=1
				elif self.placements[x][y]==1:
					computer_score+=1

		if self.player%2==0:
			player_colour = "white"
			computer_colour = "black"
		else:
			player_colour = "white"
			computer_colour = "black"

		self.g.screen.create_oval(5,540,25,560,fill=player_colour,outline=player_colour)
		self.g.screen.create_oval(380,540,400,560,fill=computer_colour,outline=computer_colour)

		#Pushing text to screen
		self.g.screen.create_text(30,550,anchor="w", tags="score",font=("Consolas", 50),fill="white",text=player_score)
		self.g.screen.create_text(400,550,anchor="w", tags="score",font=("Consolas", 50),fill="black",text=computer_score)

		moves = player_score+computer_score

	def update_without_animation(self, sleep_time = 0.8):
		""" Redraw the board, animate changes beetween moves, 
			add player possible moves signalization
		"""
		self.g.screen.delete("highlight")
		self.g.screen.delete("tile")
		self.g.screen.delete("player_signalization")
		for x in range(8):
			for y in range(8):
				#Could replace the circles with images later, if I want
				if self.placements[x][y]==0:
					self.g.screen.create_oval(54+50*x,54+50*y,96+50*x,96+50*y,tags="tile {0}-{1}".format(x,y),fill="#aaa",outline="#aaa")
					self.g.screen.create_oval(54+50*x,52+50*y,96+50*x,94+50*y,tags="tile {0}-{1}".format(x,y),fill="#fff",outline="#fff")

				elif self.placements[x][y]==1:
					self.g.screen.create_oval(54+50*x,54+50*y,96+50*x,96+50*y,tags="tile {0}-{1}".format(x,y),fill="#000",outline="#000")
					self.g.screen.create_oval(54+50*x,52+50*y,96+50*x,94+50*y,tags="tile {0}-{1}".format(x,y),fill="#111",outline="#111")
		self.g.screen.update()
		sleep(sleep_time)

def create_start_state():
	iteration_state = []
	for x in range(8):
		iteration_state.append([])
		for y in range(8):
			iteration_state[x].append(None)

	iteration_state[3][3] = 1
	iteration_state[3][4] = 0
	iteration_state[4][3] = 0
	iteration_state[4][4] = 1

	return iteration_state


def get_all_posible_moves(iteration_state, player):
	moveList = []
	for x in range(8):
		for y in range(8):
				if valid(iteration_state, player,x,y):
					moveList.append((x,y))
	return moveList

def get_all_moves(iteration_state):
	moveList = []
	for x in range(8):
		for y in range(8):
			if iteration_state[x][y] == None:
				moveList.append((x,y))
	return moveList

def board_move(iteration_state, player,x,y):
	""" Moves to position and updates 'oldplacements' table
	"""
	#Move and update self.g.screen
	oldplacements = deepcopy(iteration_state)
	# print("something")
	if player%2 == 0 :
		oldplacements[x][y]=0 #change
	else:
		oldplacements[x][y]=1 #change
	iteration_state = move(iteration_state, player, x,y)
	
	return oldplacements, iteration_state

def must_pass(iteration_state, player):
	""" 
	Tests if player must pass this round

	Returns:
		[type]: boolean
	"""
	must_pass = True
	for x in range(8):
		for y in range(8):
			if valid(iteration_state, player,x,y):
				must_pass=False
	return must_pass


def get_result(iteration_state, player):
	player1_score = 0
	player2_score = 0
	for x in range(8):
		for y in range(8):  
			if iteration_state[x][y] == 0 :
				player1_score += 1
			elif iteration_state[x][y] == 1:
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

		
def move(iteration_state,  player, x, y):
		""" Make move and reverse all influenced oponnent's disks 

		Returns:
			[type]: array - board after move
		"""
		#Must copy the passedArray so we don't alter the original
		array = deepcopy(iteration_state)
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
					
		#Convert all the appropriate tiles
		for i,j in convert:
			array[i][j]=colour

		return array


def check_for_any_line(iteration_state, player, x, y, i, j):
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
	if iteration_state[neighX][neighY]==player:
		return False

	#Determine the direction of the line
	deltaX = neighX-x
	deltaY = neighY-y
	tempX = neighX
	tempY = neighY
	
	while 0<=tempX<=7 and 0<=tempY<=7:
		#If an empty space, no line is formed
		if iteration_state[tempX][tempY]==None:
			return False
		#If it reaches a piece of the player's colour, it forms a line
		if iteration_state[tempX][tempY] == player:
			return True
		#Move the index according to the direction of the line
		tempX+=deltaX
		tempY+=deltaY
	return False

#Checks if a move is valid for a given array.
def valid(iteration_state, player, x, y):
	""" Check if placing disk on (x,y) is a valid move

	Args:
		player ([type]): [description]
		x ([type]): [description]
		y ([type]): [description]

	Returns:
		[type]: [description]
	"""
	#Sets player colour
	colour = player
	#If there's already a piece there, it's an invalid move
	if iteration_state[x][y] != None:
		return False

	else:
		#Generating the list of neighbours
		neighbour = False
		neighbours = []
		valid = False
		for i in range(max(0,x-1),min(x+2,8)):
			for j in range(max(0,y-1),min(y+2,8)):
				if iteration_state[i][j]!=None:
					neighbour=True
					neighbours.append([i,j])
					valid = valid or check_for_any_line(iteration_state,colour, x, y, i, j)
		#If there's no neighbours, it's an invalid move
		if not neighbour:
			return False
		else:
			return valid

def change_player(player):
	return (player+1)%2
