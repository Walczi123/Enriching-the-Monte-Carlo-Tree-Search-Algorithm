from tkinter import *
from math import *
from time import *
from random import *
from copy import deepcopy
from tkinter import font

class Globals:
    def __init__(self, player1=0, player2=1, board=None, moves=None, depth=None, running1=False, running2=False, nodes=None, computerMove=False):
        self.root = Tk()
        self.screen = Canvas(self.root, width=500, height=600, background="DarkOliveGreen4",highlightthickness=0)
        self.screen.pack()
        self.board = board
        self.moves = moves 
        self.depth = depth
        self.running1 = running1
        self.running2 = running2
        self.nodes = nodes
 
        self.player1 = player1
        self.player2 = player2
        self.computerMove = bool(player1%2) # False # True if (player1 == 2 or player2 == 3) else False

    def switchPlayer(self):
        if self.board.player == self.player1:
            self.board.player = self.player2
            self.computerMove = bool(self.board.player%2)
        else: 
            self.board.player = self.player1
            self.computerMove = bool(self.board.player%2)

    def set_players(self, player1, player2):
        self.player1 = player1
        self.player2 = player2
        self.computerMove = bool(player1 % 2)
