import os
from mcts import MCTS
from player import MCTS_Player, Man_Player

from player import Player

# # Hide Pygame welcome message
os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "hide"
import pygame

from hex import Hex
from game import Game

if __name__ == "__main__":
    BOARD_SIZE = 7
    ITERMAX = 20
    GAME_COUNT, N_GAMES = 0, 200

    # pygame.init()
    # pygame.display.set_caption("Hex")

    # p2 = Man_Player()
    p1 = Man_Player()
    p2 = MCTS_Player()

    game = Hex(board_size=BOARD_SIZE, use_ui=True, player1=p1, player2=p2)
    # game = Game(board_size=BOARD_SIZE, use_ui=True, player1=p1, player2=p2, itermax=ITERMAX)
    game.get_game_info([BOARD_SIZE, ITERMAX, GAME_COUNT])
    game.play()