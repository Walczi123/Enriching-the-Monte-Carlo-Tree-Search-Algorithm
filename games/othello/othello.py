from copy import deepcopy
import sys
import os

from games.game import Game
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
        self.turn_state = 2

        self.board = []
        for x in range(8):
            self.board.append([])
            for y in range(8):
                self.board[x].append(None)
        
        self.board[3][3] = 1
        self.board[3][4] = 2
        self.board[4][3] = 2
        self.board[4][4] = 1

        self.winner = None

    def restart(self):
        self.turn_state = 2

        self.board = []
        for x in range(8):
            self.board.append([])
            for y in range(8):
                self.board[x].append(None)
        
        self.board[3][3] = 1
        self.board[3][4] = 2
        self.board[4][3] = 2
        self.board[4][4] = 1

        self.winner = None

    def get_result(self, iteration_state, player):
        player1_score = 0
        player2_score = 0
        for x in range(8):
            for y in range(8):  
                if iteration_state[x][y] == 0 :
                    player1_score += 1
                elif iteration_state[x][y] == 1:
                        player2_score += 1
        if player1_score == player2_score:
            return 0.5
        if player == 0:
            if player1_score > player2_score :
                return 1
            else :
                return 0
        if player1_score < player2_score :
            return 1
        else :
            return 0

    def get_all_posible_moves(self, state, player):
        moveList = []
        for x in range(8):
            for y in range(8):
                    if self.check_move(state, (x,y), player):
                        moveList.append((x,y))
        return moveList

    def change_player(self, player) -> int:
        if player == 2:
            return 1
        else:
            return 2

    def board_move(self, state, move, player):
        s = deepcopy(state)
        self.check_and_make_move(s, move, player)
        return s

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
        
        #If the neighbour colour is equal to your colour, it doesn't form a line
        #Go onto the next neighbour
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

    def check_and_make_move(self, state, move, player):
        if  self.check_move(state, move, player):
            # state[move[0]][move[1]] = player
            self.move(state, player, move[0], move[1])
            
            return True
        return False
        
    def move(self, array,  player, x, y):
        """ Make move and reverse all influenced oponnent's disks 

        Returns:
            [type]: array - board after move
        """
        #Must copy the passedArray so we don't alter the original
        # array = deepcopy(state)
        #Set colour and set the moved location to be that colour
        colour = player
        array[x][y] = colour
        
        #Determining the neighbours to the square
        neighbours = []
        for i in range(max(0,x-1),min(x+2,8)):
            for j in range(max(0,y-1),min(y+2,8)):
                if array[i][j]!=None:
                    neighbours.append([i,j])
        
        #Which tiles to convert
        convert = []

        #For all the generated neighbours, determine if they form a line
        #If a line is formed, we will add it to the convert array
        for neighbour in neighbours:
            neighX = neighbour[0]
            neighY = neighbour[1]
            #Check if the neighbour is of a different colour - it must be to form a line
            if array[neighX][neighY]!=colour:
                #The path of each individual line
                path = []
                
                #Determining direction to move
                deltaX = neighX-x
                deltaY = neighY-y

                tempX = neighX
                tempY = neighY

                #While we are in the bounds of the board
                while 0<=tempX<=7 and 0<=tempY<=7:
                    path.append([tempX,tempY])
                    value = array[tempX][tempY]
                    #If we reach a blank tile, we're done and there's no line
                    if value==None:
                        break
                    #If we reach a tile of the player's colour, a line is formed
                    if value==colour:
                        #Append all of our path nodes to the convert array
                        for node in path:
                            convert.append(node)
                        break
                    #Move the tile
                    tempX+=deltaX
                    tempY+=deltaY
                    
        #Convert all the appropriate tiles
        for i,j in convert:
            array[i][j]=colour

        # state = array


    def check_move(self, state, move, player):
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
                        valid = valid or self.check_for_any_line(state, colour, x, y, i, j)
            #If there's no neighbours, it's an invalid move
            if not neighbour:
                return False
            else:
                return valid

    def player_make_move(self, player, clicked = None):
        if player.is_man:
            if clicked is None:
                return None
            args = clicked
        else:
            # args = (self.logic, self.ui, self.logic.logger, 1, 20, True, True)
            # args = (self.logic.logger, player, 20, self.logic.is_game_over, self.logic.get_possible_moves, self.logic.change_player, self.logic.check_and_make_action2)
            args = (self.board, self.turn_state, self.get_result, self.get_all_posible_moves, self.change_player, self.board_move)
            
        move = player.make_move(args)
        return move

    def get_scores(self):
        s1 = 0 
        s2 = 0
        for x in range(8):
            for y in range(8):
                if self.board[x][y] == 1:
                    s1 += 1
                if self.board[x][y] == 2:
                    s2 += 1
        return s1, s2

    def print_board(self):
        for x in range(8):
            print(self.board[x])


    def end_condition(self):
        first_pos_moves = self.get_all_posible_moves(self.board, 1)
        second_pos_moves = self.get_all_posible_moves(self.board, 2)
        if len(first_pos_moves) != 0 or len(second_pos_moves) != 0 :
            return True
        s1, s2 = self.get_scores()
        if s1 > s2:     
            self.winner = 1
        elif s2 > s1:
            self.winner = 2
        else:
            self.winner = 0
        return False

    def play_with_ui(self):
        pygame.init()
        pygame.display.set_caption("Othello")
        self.ui = UI()

        current_player = self.player1
        while self.end_condition():
            pos_moves = self.get_all_posible_moves(self.board, self.turn_state)
            self.ui.draw_board(self.board, pos_moves)
            if len(pos_moves) == 0:
                current_player = self.swich_player()
                continue

            pygame.display.update()
            self.ui.clock.tick(30)

            clicked = self.handle_events()

            if (current_player.is_man and clicked is not None) or not current_player.is_man:
                move = self.player_make_move(current_player, clicked)
                if self.check_and_make_move(self.board, move, self.turn_state):  
                    current_player = self.swich_player()  

        self.ui.draw_board(self.board)
        pygame.display.update()

        print("winner ", self.winner)
        while 1: 
            pygame.event.wait() 
            self.handle_events()
        pygame.quit()
        return self.winner
                         

    def play_without_ui(self):
        current_player = self.player1
        while self.end_condition():
            pos_moves = self.get_all_posible_moves(self.board, self.turn_state)
            if len(pos_moves) == 0:
                current_player = self.swich_player() 
                continue

            move = self.player_make_move(current_player)
            if self.check_and_make_move(self.board, move, self.turn_state):  
                current_player = self.swich_player()  

        # print("winner ", self.winner)
        return self.winner


    # def play(self):
    #     if self.use_ui:
    #         self.play_with_ui()
    #     else:
    #         self.play_without_ui()

