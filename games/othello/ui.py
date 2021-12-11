from math import floor
import pygame

from games.othello.const import BACKGROUND_COLOR, BOARD_COLOR, FRIST_PLAYER_COLOR, SECONF_PLAYER_COLOR


class UI:
    def __init__(self):
        self.clock = pygame.time.Clock()
        self.screen_size = (500, 500)
        self.screen = pygame.display.set_mode(self.screen_size)

        self.screen.fill(BACKGROUND_COLOR)
        self.fonts = pygame.font.SysFont("Sans", 20)

        self.square_size = int(self.screen_size[0]/8)
        self.circle_size = 0.3 * self.square_size
        self.line = 1

    def draw_board(self, board, possible_moves = []):
        c = self.square_size / 2

        sqr_size = self.square_size - self.line
        for i in range(8):
            for j in range(8):
                #check if current loop value is even
                x = self.square_size*i + self.line
                y = self.square_size*j + self.line
                
                pygame.draw.rect(self.screen, BOARD_COLOR,[x,y,sqr_size,sqr_size])
                if board[i][j] == 1:
                    pygame.draw.circle(self.screen, FRIST_PLAYER_COLOR, (x+c,y+c), self.circle_size)
                elif board[i][j] == 2:
                    pygame.draw.circle(self.screen, SECONF_PLAYER_COLOR, (x+c,y+c), self.circle_size)

                if (i,j) in possible_moves:
                    pygame.draw.circle(self.screen, (100,100,100), (x+c,y+c), self.circle_size/2)


    def get_coordiantes(self, pos):
        x_pos, y_pos = pos
        x = floor(x_pos / self.square_size)
        y = floor(y_pos / self.square_size)
        return (x, y)