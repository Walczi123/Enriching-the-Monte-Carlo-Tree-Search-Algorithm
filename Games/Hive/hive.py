from os import stat
import pygame
from tile import Tile, initialize_grid, draw_drag
from move_checker import is_valid_move, game_is_over, \
    player_has_no_moves
from menus import start_menu, end_menu, no_move_popup
from game_state import Game_State
from inventory_frame import Inventory_Frame
from turn_panel import Turn_Panel
from settings import BACKGROUND, WIDTH, HEIGHT

class Hive():
    def __init__(self, use_ui):
        self.use_ui = use_ui
        self.name = "Hive"

    def init_ui(self):
        pygame.font.init()

        # Create the screen

        screen = pygame.display.set_mode((WIDTH, HEIGHT))
        background = pygame.Surface(screen.get_size())

        # Title and Icon

        pygame.display.set_caption('Hive')
        icon = pygame.image.load('games/hive/images/icon.png')
        pygame.display.set_icon(icon)

        state = Game_State(initialize_grid(HEIGHT - 200, WIDTH, radius=20))
        white_inventory = Inventory_Frame((0, 158), 0, white=True)
        black_inventory = Inventory_Frame((440, 158), 1, white=False)

        return screen, background, state, white_inventory, black_inventory

    def ui_menu(self, screen, state):
        while state.menu_loop:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    state.quit()
                    break
                start_menu(screen, state, event)
    
    def ui_move_popup(self,screen, state, background):
        while state.move_popup_loop:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    state.quit()
                    break
                no_move_popup(screen, background, state, event)

    def ui_end_game(self, screen, state):
        while state.end_loop:
            end_menu(screen, state, event)  # drawing takes precedence over the close window button
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    state.quit()
                    break

    def play_with_ui(self):
        print(f'{self.name} starts')
        # current_player = self.player1
        # while not self.endCondition():
        #     move = current_player.make_move()
        #     self.animate(move)
        #     self.swich_player()

        # def Hive():

        screen, background, state, white_inventory, black_inventory = self.init_ui()
       
        while state.running:
            self.ui_menu(screen, state)
            self.ui_move_popup(screen, state, background)
           

            while state.main_loop:
                pos = pygame.mouse.get_pos()
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        state.quit()
                        break
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            state.quit()
                            break
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        state.click()
                    if event.type == pygame.MOUSEBUTTONUP:
                        state.unclick()
                        if state.moving_piece and state.is_player_turn():
                            old_tile = next(tile for tile in
                                    state.board_tiles if tile.has_pieces()
                                    and tile.pieces[-1]
                                    == state.moving_piece)
                            new_tile = next((tile for tile in
                                    state.board_tiles
                                    if tile.under_mouse(pos)), None)
                            if is_valid_move(state, old_tile, new_tile):
                                old_tile.move_piece(new_tile)
                                state.next_turn()
                                if player_has_no_moves(state):
                                    state.open_popup()

                        state.remove_moving_piece()

                # only animate once each loop

                background.fill(BACKGROUND)
                white_inventory.draw(background, pos)
                black_inventory.draw(background, pos)
                for tile in state.board_tiles:
                    if state.clicked:
                        tile.draw(background, pos, state.clicked)
                        if tile.under_mouse(pos) and state.moving_piece \
                            is None and tile.has_pieces():
                            state.add_moving_piece(tile.pieces[-1])
                    else:
                        tile.draw(background, pos)
                if state.moving_piece:
                    draw_drag(background, pos, state.moving_piece)
                state.turn_panel.draw(background, state.turn)
                screen.blit(background, (0, 0))
                pygame.display.flip()

                if game_is_over(state):
                    state.end_game()

            self.ui_end_game(screen, state)
        
        return state.play_new_game


    def play_without_ui(self):
        print("play_without_ui")

    def play(self):
        if self.use_ui:
            self.play_with_ui()
        else:
            self.play_without_ui()
