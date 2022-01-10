from copy import deepcopy
import sys
from tkinter.constants import NO
import os

os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "hide"
import pygame
from rich.console import Console
from rich.table import Table
from games.game import Game
from games.hex.const import BLUE_PLAYER, RED_PLAYER
from games.hex.player import Player

from games.hex.logic import Logic
from games.hex.ui import UI

# from mcts import MCTS


class Hex(Game):
    def __init__(self, player1:Player, player2:Player, use_ui: bool = False, board_size: int = 11):
        self.name = "Hex"
        
        # Mode
        self.player1=player1
        self.player2=player2
        self.turn_state = 1

        use_ui = use_ui or player1.is_man or player2.is_man

        # Instantiate classes
        self.use_ui = use_ui
        self.ui = None
        if use_ui:
            pygame.init()
            pygame.display.set_caption("Hex")
            self.ui = UI(board_size)
        self.logic = Logic(self.ui, board_size)
        self.board_size = board_size

        # Initialize variables
        self.node = None
        self.winner = 0
        self.turn_state = BLUE_PLAYER
        
    def restart(self):
        self.turn_state = 1
        self.logic = Logic(self.ui, self.board_size)

        # Initialize variables
        self.node = None
        self.winner = 0
        self.turn_state = BLUE_PLAYER

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
            # if self.winner:
            #     print('win')
        except AssertionError:
            print("invalid move")
            return False

        return True

    def player_make_move(self, player, node = None):
        if player.is_man:
            if node is None:
                return None
            args = (self.ui, node)
        else:
            # args = (self.logic, self.ui, self.logic.logger, 1, 20, True, True)
            # args = (self.logic.logger, player, 20, self.logic.is_game_over, self.logic.get_possible_moves, self.logic.change_player, self.logic.check_and_make_action2)
            args = (self.logic.logger, self.turn_state, self.get_result, self.get_all_posible_moves, self.change_player, self.board_move)
            
        move = player.make_move(args)
        return move

    def end_condition(self):
        return self.winner

    def swich_player(self):
        # Next turn
        if self.turn_state == 1:
            self.turn_state = 2
            return self.player2
        else:
            self.turn_state = 1
            return self.player1

    def get_winner(self):
        if self.winner:
            # print("Player {} wins!".format(self.winner))
            return True

    def play_with_ui(self):
        # print(f'{self.name} starts')
        node = None
        current_player = self.player1
        while not self.end_condition():
            dist_board = self.logic.manhattan_distance(self.logic.logger, self.turn_state)
            self.ui.draw_board(dist_board)
    
            if current_player.is_man:
                node = self.ui.get_node_hover()
                         
            pygame.display.update()
            self.ui.clock.tick(30)

            cliced = self.handle_events()

            if (current_player.is_man and cliced) or not current_player.is_man:
                move = self.player_make_move(current_player, node)
                if self.check_move(move, self.turn_state):  
                    current_player = self.swich_player()  
        self.ui.draw_board()
        pygame.display.update()
        self.get_winner()
        print("Player {} wins!".format(self.winner))
        self.wait_for_click()
        return self.winner
    
    def play_without_ui(self):
        # print(f'{self.name} starts')
        current_player = self.player1
        while not self.end_condition():
            # move = current_player.make_move()
            move = self.player_make_move(current_player)
            self.check_move(move, self.turn_state)
            current_player = self.swich_player()

        self.get_winner()
        return self.winner

    def get_result(self, state, player) -> int:
        result = self.logic.is_game_over(player, state, True)
        if result is None:
            result = 0.5
        return result

    def get_all_posible_moves(self, iteration_state, player = None) -> list:
        moves = self.logic.get_possible_moves(iteration_state)
        return moves

    def change_player(self, player) -> int:
        if player == 2:
            return 1
        else:
            return 2

    def board_move(self, state, move, player):
        (x, y) = move

        assert self.logic.is_node_free((x, y), state), "node is busy"

        copy_state = deepcopy(state)
        copy_state[x][y] = player

        return copy_state

        
