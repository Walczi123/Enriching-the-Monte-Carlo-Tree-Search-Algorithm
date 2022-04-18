from math import log, sqrt

class SwitchingMechanism():
    def __init__(self, strategies):
        self.strategies = strategies
        self.b = 4
        self.q_table = [0] * len(strategies)
        self.t_table = [0] * len(strategies)

    def __t_table__(self, i):
        if self.t_table[i] != 0:
            return self.t_table[i]
        return 1

    def choose_strategy(self, n):
        result = []
        for i in range(len(self.strategies)):
            result.append(self.q_table[i] + self.b * sqrt(log(n+1)/self.__t_table__(i)))
        index = result.index(max(result))
        return self.strategies[index]

    def update_strategy_result(self, strategy, result):
        index = self.strategies.index(strategy)
        self.t_table[index] += 1
        self.q_table[index] += result
