import os
import random

from games.hex.player import Man_Player
from games.player import MCTS_Player, MCTSRAVE_Player

# # Hide Pygame welcome message
os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "hide"
import pygame

from games.hex.hex import Hex

if __name__ == "__main__":
    random.seed(10)
    BOARD_SIZE = 7
    ITERMAX = 10
    GAME_COUNT, N_GAMES = 0, 200

    # pygame.init()
    # pygame.display.set_caption("Hex")

    # p2 = Man_Player()
    # p1 = MCTS_Player(ITERMAX)
    # p2 = MCTS_Player(ITERMAX)
    # p1 = MCTS_Player(ITERMAX)
    # p2 = MCTSRAVE_Player(ITERMAX)
    p1 = Man_Player()
    p2 = Man_Player()

    game = Hex(board_size=BOARD_SIZE, use_ui=True, player1=p1, player2=p2)
    # game = Game(board_size=BOARD_SIZE, use_ui=True, player1=p1, player2=p2, itermax=ITERMAX)
    game.get_game_info([BOARD_SIZE, ITERMAX, GAME_COUNT])
    print(game.play())