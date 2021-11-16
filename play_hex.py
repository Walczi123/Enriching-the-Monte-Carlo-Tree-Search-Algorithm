import os

from games.hex.player import MCTS_Player, Man_Player

# # Hide Pygame welcome message
os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "hide"
import pygame

from games.hex.hex import Hex

if __name__ == "__main__":
    BOARD_SIZE = 7
    ITERMAX = 20
    GAME_COUNT, N_GAMES = 0, 200

    # pygame.init()
    # pygame.display.set_caption("Hex")

    # p2 = Man_Player()
    p1 = Man_Player()
    p2 = MCTS_Player(100)

    game = Hex(board_size=BOARD_SIZE, use_gui=True, player1=p1, player2=p2)
    # game = Game(board_size=BOARD_SIZE, use_ui=True, player1=p1, player2=p2, itermax=ITERMAX)
    game.get_game_info([BOARD_SIZE, ITERMAX, GAME_COUNT])
    game.play()