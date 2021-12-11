from math import ceil, floor
import numpy as np
import pygame
from games.hive.pieces import Ant, Beetle, Grasshopper, Queen, Spider

from games.othello.const import BACKGROUND_COLOR, BOARD_COLOR, FRIST_PLAYER_COLOR, SECONF_PLAYER_COLOR


class UI:
    def __init__(self):
        self.clock = pygame.time.Clock()
        self.hex_radius = 20
        self.board_height = 600
        self.board_width = 700 
        self.inv_height = 200
        self.screen_size = (self.board_width, self.board_height + self.inv_height)
        self.screen = pygame.display.set_mode(self.screen_size)

        self.screen.fill(BACKGROUND_COLOR)
        self.fonts = pygame.font.SysFont("Sans", 10)

        # location of the tiles in pygame/cartesian pixels
        self.pixel_y = list(reversed(range(self.board_height + self.hex_radius, 0, -2 * self.hex_radius + 6)))
        self.len_pixel_y = len(self.pixel_y)
        self.pixel_x = list(range(0, self.board_width + self.hex_radius, 2 * self.hex_radius))
        self.len_pixel_x = len(self.pixel_x)
        self.center_x = self.len_pixel_x//2 - 1
        self.center_y = self.len_pixel_y//2 - 1

        self.border = 2
        self.pieces = list([Queen(), Ant(), Grasshopper(), Spider(), Beetle()])


    def draw_board(self, board:dict, amount_available_white_pieces, amount_available_black_pieces):
        # Board
        for j in range(0, self.len_pixel_y):
            for k in range(0, self.len_pixel_x):
                if j % 2 == 1:
                    coordinates = (self.pixel_x[k] + self.hex_radius, self.pixel_y[j])
                else:
                    coordinates = (self.pixel_x[k], self.pixel_y[j])
     
                pygame.draw.polygon(self.screen, (255,255,255), self.get_hex_points(coordinates))
                # print coordiantes
                # self.screen.blit(self.fonts.render(f'({k - self.center_x}, {j - self.center_y})', True, (150,150,150)), (coordinates[0] - 13, coordinates[1] - 6 ))
                if (k - self.center_x, j - self.center_y) in board.keys():
                    board[k - self.center_x, j - self.center_y].draw(self.screen, coordinates)
                    
        # Inventory
        pygame.draw.rect(self.screen, (50, 50, 50), [0, self.board_height, self.board_width, self.inv_height])
        
        # White
        white_inv = [self.border,self.board_height + self.border,self.board_width//2 - self.border,self.inv_height - self.border]
        pygame.draw.rect(self.screen, (125, 125, 125), white_inv)
        white_inv_border = (white_inv[0] + self.border, white_inv[1] + self.border)


        # Black
        black_inv = [self.board_width//2 + self.border ,self.board_height + self.border ,self.board_width//2 - (2*self.border),self.inv_height - (2*self.border)]
        pygame.draw.rect(self.screen, (125, 125, 125), black_inv)
        black_inv_border = (black_inv[0] + self.border, black_inv[1] + self.border)

        pieces_amount = len(self.pieces)

        for i in range(pieces_amount):
            piece_amount = self.pieces[i].amount

            w_coordinates = [white_inv_border[0] + (i * white_inv[2] // pieces_amount), white_inv_border[1], white_inv[2] // pieces_amount - self.border, white_inv[3] - self.border]
            pygame.draw.rect(self.screen, (220, 220, 220), w_coordinates)    
            for j in range(1, amount_available_white_pieces[i] + 1):
                self.pieces[i].draw(self.screen, (w_coordinates[0] + white_inv[2] //(pieces_amount*2), w_coordinates[1] + (j * (white_inv[3] // (piece_amount + 1)))))

            b_coordinates = [white_inv_border[0] + (i * white_inv[2] // pieces_amount) + self.board_width//2, white_inv_border[1], white_inv[2] // pieces_amount - self.border, white_inv[3] - self.border]
            pygame.draw.rect(self.screen, (50, 50, 50), b_coordinates)
            for j in range(1, amount_available_black_pieces[i] + 1):
                self.pieces[i].draw(self.screen, (b_coordinates[0] + white_inv[2] //(pieces_amount*2), b_coordinates[1] + (j * (white_inv[3] // (piece_amount + 1)))))


    def get_hex_points(self, coord_pair):
        (x, y) = coord_pair
        radius = self.hex_radius + 1

        return (  # has to be in counterclockwise order for drawing
            (x, y + radius),  # top
            (x - ((radius * np.sqrt(3))/2), y + (radius / 2)),  # top-left
            (x - ((radius * np.sqrt(3))/2), y - (radius / 2)),  # bottom-left
            (x, y - radius),  # bottom
            (x + ((radius * np.sqrt(3))/2), y - (radius / 2)),  # bottom-right
            (x + ((radius * np.sqrt(3))/2), y + (radius / 2))  # top-right
        )

    def distance(self, pair_one, pair_two):
        (x1, y1) = pair_one
        (x2, y2) = pair_two
        return np.sqrt((x1 - x2) * (x1 - x2) + (y1 - y2) * (y1 - y2))

    def get_coordiantes(self, pos):
        x_pos, y_pos = pos
        x = min(range(self.len_pixel_x), key=lambda i: abs(self.pixel_x[i]-x_pos))
        y = min(range(self.len_pixel_y), key=lambda i: abs(self.pixel_y[i]-y_pos))
        return x, y