from games.hive.const import ANT_AMOUNT, BEETLE_AMOUNT, GRASSHOPPER_AMOUNT, QUEEN_AMOUNT, SPIDER_AMOUNT


class State:
    def __init__(self):
        self.board = dict()
        # self.board[(0,0)] = Queen()
        # self.board[(2,2)] = Queen((0,0,0))
        # Queen, Ant, Grasshopper, Spider, Beetle
        self.amount_available_white_pieces = [QUEEN_AMOUNT, ANT_AMOUNT, GRASSHOPPER_AMOUNT, SPIDER_AMOUNT, BEETLE_AMOUNT]
        self.amount_available_black_pieces = [QUEEN_AMOUNT, ANT_AMOUNT, GRASSHOPPER_AMOUNT, SPIDER_AMOUNT, BEETLE_AMOUNT]
        self.round_counter = 0
        self.turn_state = 1

