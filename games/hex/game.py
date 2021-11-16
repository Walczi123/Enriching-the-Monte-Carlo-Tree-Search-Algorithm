import sys

import pygame
from rich.console import Console
from rich.table import Table
from const import BLUE_PLAYER, RED_PLAYER
from player import Player

from logic import Logic
from ui import UI

from mcts import MCTS


class Game():
    def __init__(self, board_size: int, itermax: int, player1:Player, player2:Player, blue_starts: bool = True, use_ui: bool = True):
        # Mode
        self.player1=player1
        self.player2=player2

        self.itermax = itermax

        # Instantiate classes
        self.ui = None
        if use_ui:
            pygame.init()
            pygame.display.set_caption("Hex")
            self.ui = UI(board_size)
        self.logic = Logic(self.ui, board_size)

        # Initialize variables
        self.node = None
        self.winner = 0
        self.turn = {True: BLUE_PLAYER, False: RED_PLAYER}

        # BLUE player starts
        self.turn_state = blue_starts
        self.use_ui = use_ui

    def get_game_info(self, args):
        console = Console()

        table = Table(title="Hex Game", show_header=True, header_style="bold magenta")
        table.add_column("Parameters", justify="center")
        table.add_column("Value", justify="right")
        table.add_row("Board size", str(args[0]))
        table.add_row("MCTS itermax", str(args[1]))
        table.add_row("Game", str(args[2]))

        console.print(table)

    def handle_events(self):
        if self.player1.is_man or self.player2.is_man:
            # pass
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

                # if event.type == pygame.MOUSEBUTTONUP or not (self.player1.is_man or self.player2.is_man):
                #     self.run_turn()

        if not (self.player1.is_man or self.player2.is_man):
            self.run_turn()

    def run_turn(self):
        if not (self.player1.is_man or self.player2.is_man):
            node = None
        if self.player1.is_man or self.player2.is_man:
            node = self.node

        # BLUE player's turn
        if not self.check_move(node, self.turn[self.turn_state]):
            return
        # RED player's turn (AI)
        else:
            if not self.check_move(None, self.turn[self.turn_state]):
                return

    def check_move(self, node, player):
        # Forbid playing on already busy node
        try:
            coordinates = self.player_make_move(player, node)
            print('coordinates',coordinates)
            self.winner = self.logic.get_action(player, coordinates)
        except AssertionError:
            return False

        # Next turn
        self.turn_state = not self.turn_state

        # If there is a winner, break the loop
        if self.get_winner():
            return False

        return True

    def player_make_move(self, player, node):
        # Human player
        if player is BLUE_PLAYER:
            if self.player1.is_man:
                x, y = self.ui.get_true_coordinates(node)
            else:
                # args = (self.logic, self.ui, self.logic.logger, 1, self.logic.itermax, True, True)
                # x,y = self.player1(args)
                self.mcts = MCTS(logic=self.logic, ui=self.ui, board_state=self.logic.logger, starting_player=1)
                x, y = self.mcts.start(itermax=self.logic.itermax, verbose=True, show_predictions=True)
            # Debug: random player
            # x, y = choice(self.get_possible_moves(self.logger))
            # self.mcts = MCTS(logic=self, ui=self.ui, board_state=self.logger, starting_player=self.ui.BLUE_PLAYER)
            # x, y = self.mcts.start(itermax=self.itermax, verbose=False)


        # AI player
        if player is RED_PLAYER:
            if self.player2.is_man:
                x, y = self.ui.get_true_coordinates(node)
            else:
                # args = (self.logic, self.ui, self.logic.logger, 2, self.logic.itermax, True, True)
                # x,y = self.player1(args)
                self.mcts = MCTS(logic=self.logic, ui=self.ui, board_state=self.logic.logger, starting_player=2)
                x, y = self.mcts.start(itermax=self.itermax, verbose=True, show_predictions=True)
            # Debug: random player
            # x, y = choice(self.get_possible_moves(self.logger))
            # MCTS player
        return (x,y)


    def get_winner(self):
        if self.winner:
            print("Player {} wins!".format(self.winner))
            return True

    def play_with_ui(self):     
        while not self.winner:
            print("loop")
            self.ui.draw_board()
            
            # if self.player1.is_man or self.player2.is_man:
            #     self.node = self.ui.get_node_hover()

            pygame.display.update()
            self.ui.clock.tick(30)
            self.handle_events()

    def play_without_ui(self):
        while not self.winner:
            # self.ui.draw_board()

            # if self.modes["man_vs_cpu"] or self.modes["man_vs_man"]:
            #     self.node = self.ui.get_node_hover()

            # pygame.display.update()
            # self.ui.clock.tick(30)

            self.handle_events()

    def play(self):
        if self.use_ui:
            self.play_with_ui()
        else:
            self.play_without_ui()

        
