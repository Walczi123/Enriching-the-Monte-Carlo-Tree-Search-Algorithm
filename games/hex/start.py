from player import MCTS_Player, Man_Player
from hex import Hex

if __name__ == "__main__":
    BOARD_SIZE = 7
    ITERMAX = 20
    GAME_COUNT, N_GAMES = 0, 200

    # pygame.init()
    # pygame.display.set_caption("Hex")

    # p2 = Man_Player()
    p1 = Man_Player()
    p2 = MCTS_Player()

    game = Hex(board_size=BOARD_SIZE, use_ui=True, player1=p1, player2=p2)
    # game = Game(board_size=BOARD_SIZE, use_ui=True, player1=p1, player2=p2, itermax=ITERMAX)
    game.get_game_info([BOARD_SIZE, ITERMAX, GAME_COUNT])
    game.play()