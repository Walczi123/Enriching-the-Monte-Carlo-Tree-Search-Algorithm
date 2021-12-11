from games.othello.msi2.start import run_game

from mcts.mcts import mcts

if __name__ == "__main__":
    result = run_game(mcts, mcts,  n_iterations=800, printfinalResult=True, printSteps=True)
    print(result)
