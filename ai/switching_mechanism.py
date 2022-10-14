from math import log, sqrt
import random

class SwitchingMechanism():
    def __init__(self, strategies):
        self.strategies = strategies
        self.b = 5 # wczesniej 4
        self.q_table = [0] * len(strategies)
        self.t_table = [0] * len(strategies)
        self.selected_strategies = [0] * len(strategies)

    def __t_table__(self, i):
        if self.t_table[i] != 0:
            return self.t_table[i]
        return 1

    def choose_strategy(self, n):
        if self.t_table.count(0) > 0:
            index_list = [index for index, value in enumerate(self.t_table) if value == 0]
            index = random.choice(index_list)
            self.selected_strategies[index] += 1
            return self.strategies[index]
        result = []
        for i in range(len(self.strategies)):
            result.append((self.q_table[i]/self.__t_table__(i)) + self.b * sqrt(log(n)/self.__t_table__(i)))
        index = result.index(max(result))
        self.selected_strategies[index] += 1
        return self.strategies[index]

    def update_strategy_result(self, strategy, result):
        index = self.strategies.index(strategy)
        self.t_table[index] += 1
        self.q_table[index] += result

    def get_stats(self):
        return self.selected_strategies

