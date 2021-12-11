from copy import deepcopy
import sys
import os
from games.hive.const import ANT_AMOUNT, BEETLE_AMOUNT, GRASSHOPPER_AMOUNT, QUEEN_AMOUNT, SPIDER_AMOUNT

from games.hive.pieces import Beetle, Queen

# # Hide Pygame welcome message
os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "hide"
import pygame
from games.hive.ui import UI

class Hive():
    def __init__(self, use_ui, player1, player2):
        self.name = "Hive"
        self.use_ui = use_ui

        self.player1 = player1
        self.player2 = player2

        self.board = dict()
        self.board[(0,0)] = Queen()
        # Queen, Ant, Grasshopper, Spider, Beetle
        self.amount_available_white_pieces = [QUEEN_AMOUNT - 1, ANT_AMOUNT, GRASSHOPPER_AMOUNT, SPIDER_AMOUNT, BEETLE_AMOUNT]
        self.amount_available_black_pieces = [QUEEN_AMOUNT, ANT_AMOUNT - 2, GRASSHOPPER_AMOUNT, SPIDER_AMOUNT, BEETLE_AMOUNT]

        self.winner = None

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()
            elif self.winner is not None and event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                pygame.quit()
                sys.exit()
            if (self.player1.is_man or self.player2.is_man) and event.type == pygame.MOUSEBUTTONDOWN :
                return self.ui.get_coordiantes(pygame.mouse.get_pos())
        return None

    def end_condition(self):
        return True

    def play_with_ui(self):
        pygame.init()
        pygame.display.set_caption(self.name)
        self.ui = UI()

        current_player = self.player1
        while self.end_condition():
            self.ui.draw_board(self.board, self.amount_available_white_pieces, self.amount_available_black_pieces)

            pygame.display.update()
            self.ui.clock.tick(30)

            clicked = self.handle_events()
            if clicked is not None:
                print("clicked ", clicked)


        self.ui.draw_board(self.board)
        pygame.display.update()
        pygame.quit()
                         

    def play_without_ui(self):
        pass

    def play(self):
        if self.use_ui:
            self.play_with_ui()
        else:
            self.play_without_ui()

