class SwitchingMechanism():
    def __init__(self, strategies):
        self.strategies = strategies
        self.b = 4
        self.q_table = None
        self.t_table = None

    def choose_strategy(self):
        return self.strategies[0]

    def get_move_from_strategy(self, moves):
        result = []
        for i in len(self.strategies):
            result.append(self.strategies[i])
        strategy = self.choose_strategy()
        return strategy(moves)
