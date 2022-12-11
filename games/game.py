import os
import sys
os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "hide"
import pygame
from pygame.constants import KEYDOWN, QUIT
from games.player import Player


class Game():
    def __init__(self, player1:Player , player2:Player , use_ui:bool = False):
        self.announcement = 'Don\'t use base class.'
        self.name = "Base Game Class"
        self.use_ui = use_ui
        self.player1 = player1
        self.player2 = player2

    def wait_for_click(self):
        while 1:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == KEYDOWN or event.type == pygame.MOUSEBUTTONUP:
                    return

    def restart(self):
        raise ValueError(self.announcement)

    def play_with_ui(self):
        raise ValueError(self.announcement)

    def play_without_ui(self):
        raise ValueError(self.announcement)

    def play(self):
        # print(f'{self.name} starts')
        if self.use_ui:
            return self.play_with_ui()
        else:
            return self.play_without_ui()

    def get_result(self, state, player) -> int:
        raise ValueError(self.announcement)

    def get_all_posible_moves(self, iteration_state, player) -> list:
        raise ValueError(self.announcement)

    def change_player(self, player) -> int:
        raise ValueError(self.announcement)

    def board_move(self, state, move, player):
        raise ValueError(self.announcement)