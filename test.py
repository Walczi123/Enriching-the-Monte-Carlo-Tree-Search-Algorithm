import random
from config import RESULTS_FILE_PATH
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
            if game_limit is not None and self.game_type == Hive:
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
        if self.game_type == Hive:
            game = self.game_type(self.player1, self.player2, round_limit=self.game_limit)
        else:
            game = self.game_type(self.player1, self.player2)
            
        if self.seed is not None:
            random.seed(self.seed)
        start_time = time.time()
        r, additional_params = game.play()
        game_time = time.time() - start_time
        result = (r, additional_params, self.seed, game_time)
        print(f"saving {self.name}")
        self.save_to_global_file(result)

    # def save_to_file(self, results):
    #     file_path = f'./tests/results/{str(self.game_type.__name__).lower()}/{self.name}'
    #     f = open(file_path, "w")
    #     print("saving", self.name)
    #     f.write(f"Game NO{SEPARATHOR}Winner\n")
    #     results = [f'{str(results[i][0])}{SEPARATHOR}{str(results[i][1])}\n' for i in range(
    #         len(results))]
    #     f.writelines(results)
    #     f.close

    def get_result_csv(self, result):
        # game_type, player1, player2, winner, seed, game_time, additional params
        p1 = self.player1.name
        p2 = self.player2.name
        return (str(self.game_type.__name__).lower(),
                      p1, p2, result[0], result[2], result[3], result[1])

    def save_to_global_file(self, result):
        file_path = RESULTS_FILE_PATH
        result_csv = self.get_result_csv(result)

        with open(file_path, 'a', newline='') as file:
            file_writer = writer(file)
            file_writer.writerow(result_csv)
            file.close()

    def is_in_data_frame(self, df):
        return ((df['game_type'] == str(self.game_type.__name__).lower()) & (df['player1'] == self.player1.name) & (df['player2'] == self.player2.name) & (df['seed'] == self.seed)).any()

    def is_done(self, done_tests):
        x = (str(self.game_type.__name__).lower(), self.player1.name, self.player2.name, str(self.seed)) in done_tests
        return x 
