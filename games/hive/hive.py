from collections import defaultdict
from copy import deepcopy
import sys
import os

from games.hive.const import ANT_AMOUNT, ANT_ID, BEETLE_AMOUNT, BEETLE_ID, GRASSHOPPER_AMOUNT, GRASSHOPPER_ID, QUEEN_AMOUNT, QUEEN_ID, SPIDER_AMOUNT, SPIDER_ID

from games.hive.pieces import Ant, Beetle, Grasshopper, Queen, Spider
from games.hive.move_checker import check_move
from games.hive.common_functions import neighbours, one_hive
from games.hive.state import State

# # Hide Pygame welcome message
os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "hide"
import pygame
from games.hive.ui import UI

class Hive():
    def __init__(self, use_ui, player1, player2, round_limit:int = 1000):
        self.name = "Hive"
        self.use_ui = use_ui

        self.player1 = player1
        self.player2 = player2

        self.state = State()

        self.winner = 0
        self.round_limit = round_limit

    def get_result(self, iteration_state, player):
        if self.is_looser(iteration_state.board, player):
            return 0
        elif self.is_looser(iteration_state.board, self.change_player(player)):
            return 1
        else: 
            return 0.5

    def change_player(self, player) -> int:
        if player == 2:
            return 1
        else:
            return 2

    def board_move(self, state:State, move, player):
        s = deepcopy(state)
        s.turn_state = player
        self.check_and_make_move(s, move)
        return s

    def enumerate_hand(self, state: State, coordinates, player):
        """Fora given iterable of coordinates, enumerate all avilable tiles"""
        result = []
        if player == 1:
            for x in range(len(state.amount_available_white_pieces)):
                if state.amount_available_white_pieces[x] > 0:
                    for c in coordinates:
                        result.append(((True, (0,x)), c))
        else:
            for x in range(len(state.amount_available_black_pieces)):
                if state.amount_available_black_pieces[x] > 0:
                    for c in coordinates:
                        result.append(((True, (1,x)), c))
        return result

    def placeable(self, state, current_player):
        """Returns all coordinates where the given player can
        _place_ a tile."""
        players = defaultdict(set)
        for coordinate, pieces in state.board.items():
            for piece in pieces:
                player = 2 - piece.color[0]//128
                for n in neighbours(coordinate):
                    if not n in state.board.keys():
                        players[player].add(n)
        # All neighbours to any tile placed by current player...
        coordinates = players[current_player]
        # ...except where the opponent is neighbour...
        for p in players:
            if p != current_player:
                coordinates.difference_update(players[p])
        # ...and you cannot place on top of another tile.
        coordinates.difference_update(state.board.keys())      

        return coordinates   

    def movements(self, state:State, player):
        result = []
        for coordinate, pieces in state.board.items():
            piece = pieces[-1]
            if 2 - piece.color[0]//128 == player:
                coordinates = set(state.board.keys())
                coordinates.remove(coordinate)
                if one_hive(coordinates):
                    for target in piece.moves(coordinate, state):
                        result.append(((False, coordinate), target))

        for r in result:
            if r[0][1] == r[1]:
                raise Exception

        return result

    def get_all_posible_moves(self, state:State, player=None):
        if not state.board:
            # Empty board
            anywhere = (0, 0)
            return self.enumerate_hand(state, [anywhere], player)
        if len(state.board) == 1:
            # If single tile is placed, opponent places at neighbour
            start_tile = next(iter(state.board))
            return self.enumerate_hand(state, list(neighbours(start_tile)), player)
        
        placements = self.placeable(state, player)
        if not len(placements):
            return []

        # If queen is still on hand...
        if player == 1:
            hand = state.amount_available_white_pieces
        else:
            hand = state.amount_available_black_pieces
        if hand[0] > 0:
            # ...it must be placed on round 4
            if state.round_counter + 1 == 4:
                return [(('True', (player-1, QUEEN_ID)), c) for c in placements]
            # ...otherwise only placements...
            return list(self.enumerate_hand(state, placements, player))
        # ...but normally placements and movements
        available = list(self.enumerate_hand(state, placements, player)) + list(self.movements(state, player))
        if not available:
            return []
        return available
    
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
            # if event.type == pygame.MOUSEBUTTONDOWN :
                return self.ui.get_coordiantes(pygame.mouse.get_pos())
        return None

    def id_to_piece(self, id):
        if id == QUEEN_ID:
            return Queen
        elif id == ANT_ID:
            return Ant
        elif id == GRASSHOPPER_ID:
            return Grasshopper
        elif id == SPIDER_ID:
            return Spider
        elif id == BEETLE_ID:
            return Beetle

    def find(self, player, piece_id, board:dict):
        piece = self.id_to_piece(piece_id)
        return [k for k in board.keys() if isinstance(board[k][-1], piece) and 2 - board[k][-1].color[0]//128 == player]

    def is_looser(self, board:dict, player):
        queen_coordinate = self.find(player, QUEEN_ID, board)
        if queen_coordinate:
            if all(n in board.keys() for n in neighbours(queen_coordinate[0])):
                return True
        return False

    def end_condition(self):
        if self.is_looser(self.state.board, 1):
            self.winner = 2
            return False
        if self.is_looser(self.state.board, 2):
            self.winner = 1
            return False
        return True
    
    def player_make_move(self, player, selected_piece = None, coordinates = None):
        if player.is_man:
            args = (selected_piece, coordinates)
        else:
            args = (self.state, self.state.turn_state, self.get_result, self.get_all_posible_moves, self.change_player, self.board_move)
            
        move = player.make_move(args)
        return move

    def get_piece(self, piece, turn_state):
        if turn_state == 1:
            color = (250, 250, 250)
        else:
            color = (50, 50, 50)

        return self.id_to_piece(piece)(color)
 
    def make_move(self, state:State, move):
        if move[0][0]:
            state.add_to_board(move[1], self.get_piece(move[0][1][1], state.turn_state))
            if state.turn_state == 1:
                state.amount_available_white_pieces[move[0][1][1]] -= 1
            else:
                state.amount_available_black_pieces[move[0][1][1]] -= 1
        else:
            piece = state.board[move[0][1]][-1]
            state.add_to_board(move[1], piece)
            state.remove_from_board(move[0][1], piece)

    def swich_player(self):
        # Next turn
        if self.state.turn_state == 1:
            self.state.turn_state = 2
            return self.player2
        else:
            self.state.turn_state = 1
            self.state.round_counter += 1
            return self.player1

    def check_and_make_move(self, state:State, move):
        if check_move(state, move):
            self.make_move(state, move)
            return True
        print("invalid move")
        print(state.turn_state)
        print(self.state.board)
        print(move)
        raise Exception('invalid move')
        return False

    def select_piece_and_coordinates(self, clicked, selected_piece, coordinates):
        if clicked[0] and selected_piece is not None:
            coordinates = deepcopy(clicked[1])
        elif clicked[0] and clicked[1] in self.state.board.keys():
            piece = self.state.board[clicked[1]][-1]
            if piece.color[0]//128 == 2 - self.state.turn_state:
                if selected_piece is not None and selected_piece[1] == clicked[1]:
                    selected_piece = None
                else:
                    selected_piece = (False, deepcopy(clicked[1]))
        elif not clicked[0]:
            if clicked[1][0] + 1 == self.state.turn_state:
                if selected_piece is not None and selected_piece[1] == clicked[1]:
                    selected_piece = None
                else:
                    selected_piece = (True, deepcopy(clicked[1]))   

        return selected_piece, coordinates      
     
    def play_with_ui(self):
        pygame.init()
        pygame.display.set_caption(self.name)
        self.ui = UI()

        selected_piece = None
        coordinates = None
        available_moves_checked = False
        current_player = self.player1
        self.state.turn_state = 1
        round_counter = 0
        while self.end_condition():
            round_counter += 1
            self.ui.draw_board(self.state.board, self.state.amount_available_white_pieces, self.state.amount_available_black_pieces, selected_piece)

            pygame.display.update()
            self.ui.clock.tick(30)

            clicked = self.handle_events()

            if (current_player.is_man and clicked is not None) or not current_player.is_man:
                if clicked is not None and current_player.is_man:
                    selected_piece, coordinates = self.select_piece_and_coordinates(clicked, selected_piece, coordinates)    
                if (selected_piece is not None and coordinates is not None) or not current_player.is_man:
                    move = self.player_make_move(current_player, selected_piece, coordinates)
                    if (move is not None and self.check_and_make_move(self.state, move)) or (not current_player.is_man and move is None): 
                        selected_piece = None
                        coordinates = None
                        available_moves_checked = False
                        current_player = self.swich_player()  
            
            if not available_moves_checked and current_player.is_man:
                if len(self.get_all_posible_moves(self.state)) == 0:
                    print("No available moves for current player")
                    selected_piece = None
                    coordinates = None
                    current_player = self.swich_player()  
                else:
                    available_moves_checked = True

            if round_counter >= self.round_limit:
                break


        self.ui.draw_board(self.state.board, self.state.amount_available_white_pieces, self.state.amount_available_black_pieces, selected_piece)
        pygame.display.update()
        pygame.quit()

        print(f"Player {self.winner} wins!")
        return self.winner
                         
    def play_without_ui(self):
        current_player = self.player1
        self.state.turn_state = 1
        round_counter = 0
        while self.end_condition():
            pos_moves = self.get_all_posible_moves(self.state, current_player)
            if len(pos_moves) == 0:
                current_player = self.swich_player() 
                continue

            round_counter += 1

            move = self.player_make_move(current_player)
            if self.check_and_make_move(self.state, move):
                current_player = self.swich_player()

            if round_counter >= self.round_limit:
                break

        return self.winner

    def play(self):
        if self.use_ui:
            return self.play_with_ui()
        else:
            return self.play_without_ui()

