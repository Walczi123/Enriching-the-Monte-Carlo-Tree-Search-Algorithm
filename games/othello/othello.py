import sys
import os

from games.game import Game
from games.othello.common import get_pieces_to_reverse
from games.player import Player

# # Hide Pygame welcome message
os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "hide"
import pygame
from games.othello.ui import UI

class Othello(Game):
    def __init__(self, player1:Player , player2:Player , use_ui:bool = False):
        self.name = "Othello"
        self.use_ui = use_ui

        self.player1 = player1
        self.player2 = player2
        self.turn_state = 1

        self.board = []
        for x in range(8):
            self.board.append([])
            for y in range(8):
                self.board[x].append(None)
        
        self.board[3][3] = 2
        self.board[3][4] = 1
        self.board[4][3] = 1
        self.board[4][4] = 2

        self.winner = None

    def restart(self):
        self.turn_state = 1

        self.board = []
        for x in range(8):
            self.board.append([])
            for y in range(8):
                self.board[x].append(None)
        
        self.board[3][3] = 2
        self.board[3][4] = 1
        self.board[4][3] = 1
        self.board[4][4] = 2

        self.winner = None

    def get_result(self, iteration_state, player):
        return get_result(iteration_state, player)

    def get_all_posible_moves(self, state, player):
        return get_all_posible_moves(state, player)

    def change_player(self, player) -> int:
        return change_player(player)

    def board_move(self, state, move, player):
        return board_move(state, move, player)
        # self.check_and_make_move(state, move, player)
        # return state

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
            if event.type == pygame.MOUSEBUTTONUP or not (self.player1.is_man or self.player2.is_man):
                return self.ui.get_coordiantes(pygame.mouse.get_pos())
        return None

    def swich_player(self):
        # Next turn
        if self.turn_state == 1:
            self.turn_state = 2
            return self.player2
        else:
            self.turn_state = 1
            return self.player1

    def check_for_any_line(self, state, player, x, y, i, j):
        return check_for_any_line(state, player, x, y, i, j)

    def check_and_make_move(self, state, move, player):
        return check_and_make_move(state, move, player)
        
    def move(self, array,  player, x, y):
        """ Make move and reverse all influenced oponnent's disks 

        Returns:
            [type]: array - board after move
        """
        return move(array,  player, x, y)

    def check_move(self, state, move, player):
        return check_move(state, move, player)

    def player_make_move(self, player, clicked = None, all_posible_moves:list = None):
        if player.is_man:
            if clicked is None:
                return None
            args = clicked
        else:
            args = (self.board, self.turn_state, self.get_result, self.get_all_posible_moves, self.change_player, self.board_move, all_posible_moves)
            # args = (self.board, self.turn_state, get_result, get_all_posible_moves, change_player, board_move, all_posible_moves)

        move = player.make_move(args)
        return move

    def get_scores(self):
        s1 = 0 
        s2 = 0
        for x in range(8):
            for y in range(8):
                if self.board[x][y] == 1:
                    s1 += 1
                elif self.board[x][y] == 2:
                    s2 += 1
        return s1, s2

    def print_board(self):
        for x in range(8):
            print(self.board[x])

    def end_condition(self):
        first_pos_moves = self.get_all_posible_moves(self.board, 1)
        second_pos_moves = self.get_all_posible_moves(self.board, 2)
        if len(first_pos_moves) == 0 and len(second_pos_moves) == 0 :
            s1, s2 = self.get_scores()
            self.score_result = (s1, s2)
            if s1 > s2:     
                self.winner = 1
            elif s2 > s1:
                self.winner = 2
            else:
                self.winner = 0
            return True
        return False

    def avg(self, l):
        return sum(l)/len(l)

    def play_with_ui(self):
        pygame.init()
        pygame.display.set_caption("Othello")
        self.ui = UI()

        no_moves_p1 = 0
        no_moves_p2 = 0
        no_blocked_moves_p1 = 0
        no_blocked_moves_p2 = 0
        move_income_p1 = []
        move_income_p2 = []
        current_player = self.player1
        board_scores = []
        while not self.end_condition():
            # print("start player"+str(self.turn_state))
            pos_moves = self.get_all_posible_moves(self.board, self.turn_state)
            self.ui.draw_board(self.board, pos_moves)
            if pos_moves == []:
                if self.turn_state == 1:
                    no_blocked_moves_p1 += 1
                else: 
                    no_blocked_moves_p2 += 1
                current_player = self.swich_player()
                continue

            pygame.display.update()
            self.ui.clock.tick(30)

            clicked = self.handle_events()

            if (current_player.is_man and clicked is not None) or not current_player.is_man:
                move = self.player_make_move(current_player, clicked, pos_moves)
                checked_move = self.check_and_make_move(self.board, move, self.turn_state)
                if checked_move[0]: 
                    s1, s2 = self.get_scores()
                    board_scores.append((s1,s2))
                    if self.turn_state == 1:
                        move_income_p1.append(checked_move[1])
                        no_moves_p1 += 1
                    else: 
                        move_income_p2.append(checked_move[1])
                        no_moves_p2 += 1
                    current_player = self.swich_player()   

        self.ui.draw_board(self.board)
        pygame.display.update()

        print("winner ", self.winner)
        self.wait_for_click()
        pygame.quit()
        return self.winner, (self.score_result, (no_moves_p1, no_moves_p2), (no_blocked_moves_p1, no_blocked_moves_p2), (move_income_p1, move_income_p2), board_scores)
                         
    def play_without_ui(self):
        current_player = self.player1
        no_moves_p1 = 0
        no_moves_p2 = 0
        no_blocked_moves_p1 = 0
        no_blocked_moves_p2 = 0
        move_income_p1 = []
        move_income_p2 = []
        board_scores = []
        while not self.end_condition():
            pos_moves = self.get_all_posible_moves(self.board, self.turn_state)
            print('====================================')
            print('board',self.board)
            print('pos_moves',pos_moves)
            print('turn_state',self.turn_state)
            if pos_moves == []:
                if self.turn_state == 1:
                    no_blocked_moves_p1 += 1
                else: 
                    no_blocked_moves_p2 += 1
                current_player = self.swich_player() 
                continue

            move = self.player_make_move(current_player, pos_moves)
            checked_move = self.check_and_make_move(self.board, move, self.turn_state)
            print('checked_move',checked_move)
            print('move',move)
            print('board',self.board)

            if checked_move[0]:
                s1, s2 = self.get_scores()
                board_scores.append(s1-s2)
                if self.turn_state == 1:
                    move_income_p1.append(checked_move[1])
                    no_moves_p1 += 1
                else: 
                    move_income_p2.append(checked_move[1])
                    no_moves_p2 += 1
                current_player = self.swich_player()  

        return self.winner, (self.score_result, (no_moves_p1, no_moves_p2), (no_blocked_moves_p1, no_blocked_moves_p2), (move_income_p1, move_income_p2), board_scores)

def get_result(state, player):
    player1_score = 0
    player2_score = 0
    for x in range(8):
        for y in range(8):  
            if state[x][y] == 1:
                player1_score += 1
            elif state[x][y] == 2:
                    player2_score += 1
    if player1_score == player2_score:
        return 0.5
    if player == 1:
        if player1_score > player2_score :
            return 1
        else :
            return 0
    if player1_score < player2_score :
        return 1
    else :
        return 0

def check_for_any_line(state, player, x, y, i, j):
    """ Check if move creates a line. 
        So if there is a line from (x,y) to another player's colored disk going through the neighbour (i,j), 
        where (i,j) has the opponent's color

    Args:
        colour ([type]): [description]
        x ([type]): move's x coordinate
        i ([type]): neighbour's x coordinate 

    Returns:
        [type]: boolean - true if it forms a correct line
    """
    neighX = i
    neighY = j
    
    if state[neighX][neighY]==player:
        return False

    #Determine the direction of the line
    deltaX = neighX-x
    deltaY = neighY-y
    tempX = neighX
    tempY = neighY
    
    while 0<=tempX<=7 and 0<=tempY<=7:
        #If an empty space, no line is formed
        if state[tempX][tempY]==None:
            return False
        #If it reaches a piece of the player's colour, it forms a line
        if state[tempX][tempY] == player:
            return True
        #Move the index according to the direction of the line
        tempX+=deltaX
        tempY+=deltaY
    return False

def check_move(state, move, player):
    """ Check if placing disk on (x,y) is a valid move

    Args:
        player ([type]): [description]
        x ([type]): [description]
        y ([type]): [description]

    Returns:
        [type]: [description]
    """
    x, y = move
    #Sets player colour
    colour = player
    #If there's already a piece there, it's an invalid move
    if state[x][y] != None:
        return False
    else:
        #Generating the list of neighbours
        neighbour = False
        neighbours = []
        valid = False
        for i in range(max(0,x-1),min(x+2,8)):
            for j in range(max(0,y-1),min(y+2,8)):
                if state[i][j]!=None:
                    neighbour=True
                    neighbours.append([i,j])
                    valid = valid or check_for_any_line(state, colour, x, y, i, j)
        #If there's no neighbours, it's an invalid move
        if not neighbour:
            return False
        else:
            return valid

def get_all_posible_moves(state, player):
    moveList = []
    for x in range(8):
        for y in range(8):
            if check_move(state, (x,y), player):
                moveList.append((x,y))
    return moveList

def change_player(player):
    if player == 2:
        return 1
    else:
        return 2

def move(array,  player, x, y):
    """ Make move and reverse all influenced oponnent's disks 

    Returns:
        [type]: array - board after move
    """
    convert = get_pieces_to_reverse(array,  player, x, y)
                
    #Convert all the appropriate tiles
    for i,j in convert:
        array[i][j]=player

    return len(convert)

def check_and_make_move(state, m, player):
    if  check_move(state, m, player):
        # state[move[0]][move[1]] = player
        l = move(state, player, m[0], m[1])
        
        return True, l
    return False, 0

def board_move(state, move, player):
    check_and_make_move(state, move, player)
    return state
