from games.hive.const import ANT_AMOUNT, BEETLE_AMOUNT, GRASSHOPPER_AMOUNT, QUEEN_AMOUNT, SPIDER_AMOUNT


class State:
    def __init__(self):
        self.board = dict()
        # Queen, Ant, Grasshopper, Spider, Beetle
        self.amount_available_white_pieces = [QUEEN_AMOUNT, ANT_AMOUNT, GRASSHOPPER_AMOUNT, SPIDER_AMOUNT, BEETLE_AMOUNT]
        self.amount_available_black_pieces = [QUEEN_AMOUNT, ANT_AMOUNT, GRASSHOPPER_AMOUNT, SPIDER_AMOUNT, BEETLE_AMOUNT]
        self.round_counter = 1
        self.turn_state = 1

    def add_to_board(self, coordinate, piece):
        if coordinate in self.board.keys():
            self.board[coordinate].append(piece)
        else:
            self.board[coordinate] = [piece]

    def remove_from_board(self, coordinate, piece):
        if not coordinate in self.board.keys():
            raise 'Invalid coordinates'
        
        if len(self.board[coordinate]) > 1:
            self.board[coordinate].remove(piece)
        else:
            del self.board[coordinate]

