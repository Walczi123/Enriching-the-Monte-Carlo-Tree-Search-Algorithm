import sys

import pygame
from rich.console import Console
from rich.table import Table
from const import BLUE_PLAYER, RED_PLAYER
from player import Player

from logic import Logic
from ui import UI

from mcts import MCTS


class Hex():
    def __init__(self, board_size: int, player1:Player, player2:Player, use_ui: bool = True):
        self.name = "Hex"
        
        # Mode
        self.player1=player1
        self.player2=player2

        use_ui = use_ui or player1.is_man or player2.is_man

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
        self.turn_state = BLUE_PLAYER

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
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONUP or not (self.player1.is_man or self.player2.is_man):
                return True
        return False

    def check_move(self, move, player):
        # Forbid playing on already busy node
        try:
            self.winner = self.logic.check_and_make_action(player, move)
        except AssertionError:
            return False

        return True

    def player_make_move(self, player, node = None):
        if player.is_man:
            if node is None:
                return None
            args = (self.ui, node)
        else:
            args = (self.logic, self.ui, self.logic.logger, 1, 20, True, True)
        move = player.make_move(args)
        return move

    def end_condition(self):
        return self.winner

    def swich_player(self):
        # Next turn
        if self.turn_state is BLUE_PLAYER:
            self.turn_state = RED_PLAYER
            return self.player2
        else:
            self.turn_state = BLUE_PLAYER
            return self.player1

    def get_winner(self):
        if self.winner:
            print("Player {} wins!".format(self.winner))
            return True

    def play_with_ui(self):
        print(f'{self.name} starts')
        node = None
        current_player = self.player1
        while not self.end_condition():
            self.ui.draw_board()
    
            if current_player.is_man:
                node = self.ui.get_node_hover()
                         
            pygame.display.update()
            self.ui.clock.tick(30)

            cliced = self.handle_events()

            if (current_player.is_man and cliced) or not current_player.is_man:
                move = self.player_make_move(current_player, node)
                self.check_move(move, self.turn_state)
                current_player = self.swich_player()  
        self.get_winner()
    
            

    def play_without_ui(self):
        print(f'{self.name} starts')
        current_player = self.player1
        while not self.end_condition():
            # move = current_player.make_move()
            move = self.player_make_move(current_player)
            self.check_move(move, self.turn_state)
            current_player = self.swich_player()

        self.get_winner()

    def play(self):
        if self.use_ui:
            self.play_with_ui()
        else:
            self.play_without_ui()

        
