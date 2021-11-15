import os

# # Hide Pygame welcome message
os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "hide"
import pygame

from game import Game

if __name__ == "__main__":
    BOARD_SIZE = 7
    ITERMAX = 20
    MODE = "man_vs_cpu"
    GAME_COUNT, N_GAMES = 0, 200

    pygame.init()
    pygame.display.set_caption("Hex")

    game = Game(board_size=BOARD_SIZE, itermax=ITERMAX, mode=MODE, blue_starts=True)
    game.get_game_info([BOARD_SIZE, ITERMAX, MODE, GAME_COUNT])
    game.play()