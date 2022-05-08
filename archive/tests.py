import random
import numpy as np
from datetime import datetime
from csv import writer
import time


from games.game import Game
from games.player import Player

SEPARATHOR = '\t'

class Tests:
    def __init__(self, game_type:Game, player1:Player, player2:Player, n_repetition:int = 1, name:str = None, seed=None):
        self.game_type = game_type
        self.player1 = player1
        self.player2 = player2
        self.n_repetition = n_repetition
        self.seed = seed

        if name is None:
            timestr = time.strftime("%d_%m_%Y-%H_%M")
            p1 = player1.__name__.split('_')[0].lower()
            p2 = player2.__name__.split('_')[0].lower()
            if seed is None:
                name = f'test_{str(self.game_type.__name__).lower()}_{p1}_{p2}-{timestr}'
            else:
                name = f'test_{str(self.game_type.__name__).lower()}_{p1}_{p2}_{seed}-{timestr}'    
        self.name = name
            

    def start(self):
        results = []
        game = self.game_type(self.player1(), self.player2())
        for i in range(self.n_repetition):
            if self.seed is not None:
                random.seed(self.seed + i)
                # np.random.seed(self.seed + i)
            game.restart()
            r = game.play()
            results.append((r,self.seed + i))
        print("saving")
        # self.save_to_file(results)
        self.save_to_global_file(results)

    def save_to_file(self, results):
        file_path = f'./tests/results/{str(self.game_type.__name__).lower()}/{self.name}'
        f = open(file_path, "w")
        print("saving", self.name)
        f.write(f"Game NO{SEPARATHOR}Winner\n")
        results = [f'{str(results[i][0])}{SEPARATHOR}{str(results[i][1])}\n' for i in range(len(results))]
        f.writelines(results)
        f.close

    def save_to_global_file(self, results):
        file_path = './tests/all_results.csv'
        results_csv = []
        # game_type, player1, player2, winner, seed
        p1 = self.player1.__name__.split('_')[0].lower()
        p2 = self.player2.__name__.split('_')[0].lower()
        for result in results:
            results_csv.append((str(self.game_type.__name__).lower(), p1, p2, result[0], result[1]))
        with open(file_path, 'a', newline='') as file:  
            file_writer = writer(file)
            file_writer.writerows(results_csv) 
            file.close()
        # with open(file_path, 'a', newline='') as file:  
        #     file_writer = writer(file)
        #     file_writer.writerow(results_csv) 
        #     file.close()