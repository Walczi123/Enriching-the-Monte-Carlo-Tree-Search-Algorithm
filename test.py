import random
import numpy as np
from datetime import datetime
from csv import writer
import time

from games.game import Game
from games.hive.hive import Hive
from games.player import Player

SEPARATHOR = '\t'


class Test:
    def __init__(self, game_type: Game, player1: Player, player2: Player, name: str = None, seed=None, game_limit:int = None):
        self.game_type = game_type
        self.player1 = player1
        self.player2 = player2
        self.seed = seed
        self.game_limit = game_limit

        if name is None:
            if game_limit is not None and isinstance(self.game_type, Hive):
                game_name = f"{str(self.game_type.__name__).lower()}{game_limit}"
            else:
                game_name = f"{str(self.game_type.__name__).lower()}"
            p1 = self.player1.name
            p2 = self.player2.name
            if seed is None:
                name = f'test_{game_name}_{p1}_{p2}'
            else:
                name = f'test_{game_name}_{p1}_{p2}_{seed}'
        self.name = name

    def start(self):
        if isinstance(self.game_type, Hive):
            print(f"HIVEEEEEE   {self.name}")
            game = self.game_type(self.player1, self.player2, game_limit=self.game_limit)
        else:
            game = self.game_type(self.player1, self.player2)
        if self.seed is not None:
            random.seed(self.seed)
        try:
            r = game.play()
        except Exception as e:
            print(f"ERRROOOORRRR {self.name}")
            raise e
        result = (r, self.seed)
        print(f"saving {self.name}")
        self.save_to_global_file(result)


    def save_to_file(self, results):
        file_path = f'./tests/results/{str(self.game_type.__name__).lower()}/{self.name}'
        f = open(file_path, "w")
        print("saving", self.name)
        f.write(f"Game NO{SEPARATHOR}Winner\n")
        results = [f'{str(results[i][0])}{SEPARATHOR}{str(results[i][1])}\n' for i in range(
            len(results))]
        f.writelines(results)
        f.close

    def save_to_global_file(self, result):
        file_path = './tests/all_results.csv'
        results_csv = []
        # game_type, player1, player2, winner, seed
        p1 = self.player1.name
        p2 = self.player2.name
        result_csv = (str(self.game_type.__name__).lower(),
                      p1, p2, result[0], result[1])

        # results_csv = results_csv + results_csv
        print(result)
        print(result_csv)

        with open(file_path, 'a', newline='') as file:
            print("saving")
            file_writer = writer(file)
            file_writer.writerow(result_csv)
            file.close()


# with open('./tests/all_results.csv', 'a', newline='') as file:
#     file_writer = writer(file)
#     file_writer.writerow((1,2,3,4,5))
#     file.close()
