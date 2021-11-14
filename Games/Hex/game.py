import sys

import pygame
from rich.console import Console
from rich.table import Table
from Games.game import BaseGame

from logic import Logic
from ui import UI


class Game(BaseGame):
    def __init__(self, board_size: int, itermax: int, mode: str, blue_starts: bool = True):
        # Select mode
        self.modes = {"cpu_vs_cpu": 0,
                      "man_vs_cpu": 0,
                      "man_vs_man": 0}
        self.modes[mode] = 1
        # Instantiate classes
        self.ui = UI(board_size)
        self.logic = Logic(self.ui, itermax)

        # Initialize variables
        self.node = None
        self.winner = 0
        self.turn = {True: self.ui.BLUE_PLAYER, False: self.ui.RED_PLAYER}

        # BLUE player starts
        self.turn_state = blue_starts

    def get_game_info(self, args):
        console = Console()

        table = Table(title="Hex Game", show_header=True, header_style="bold magenta")
        table.add_column("Parameters", justify="center")
        table.add_column("Value", justify="right")
        table.add_row("Board size", str(args[0]))
        table.add_row("MCTS itermax", str(args[1]))
        table.add_row("Mode", str(args[2]))
        table.add_row("Game", str(args[3]))

        console.print(table)

    def handle_events(self):
        if self.modes["man_vs_cpu"]:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONUP or self.modes["cpu_vs_cpu"]:
                    self.run_turn()

        if self.modes["cpu_vs_cpu"]:
            self.run_turn()

    def run_turn(self):
        if self.modes["cpu_vs_cpu"]:
            node = None
        if self.modes["man_vs_cpu"]:
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
            self.winner = self.logic.get_action(node, player)
        except AssertionError:
            return False

        # Next turn
        self.turn_state = not self.turn_state

        # If there is a winner, break the loop
        if self.get_winner():
            return False

        return True

    def get_winner(self):
        if self.winner:
            print("Player {} wins!".format(self.winner))
            return True

    def play_with_ui(self):
        self.ui.draw_board()

        if self.modes["man_vs_cpu"] or self.modes["man_vs_man"]:
            self.node = self.ui.get_node_hover()

        pygame.display.update()
        self.ui.clock.tick(30)
        self.handle_events()

    def play_without_ui(self):
        pass

        
