from games.hex.common import get_dijkstra_score, is_game_over


def hex_evaluate(state, player):
    winner = is_game_over(None, state, False)
    if not winner:
        return get_dijkstra_score(state, player)
    else:
        if winner == player:
            return 1000
        else:
            return -1000

