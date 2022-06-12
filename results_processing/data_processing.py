from msilib.schema import Error
from matplotlib import pyplot as plt
import numpy as np
import pandas as pd

#Scorre
WIN_SCORE = 1
DRAW_SCORE = 1
DEFEAT_SCORE = 1

def read_data(file_path, separator):
    return pd.read_csv(file_path, sep=separator)

def read_data_of_game(file_path, separator, game_name):
    df = pd.read_csv(file_path, sep=separator, header=None)
    df.columns = ['game_type','player1','player2','winner','seed','game_time']
    return df[df['game_type']==game_name]

def check_number_players_games(df:pd.DataFrame, omit_errors:bool=False):
    n_games1 = len(df.loc[(df['player1'] == df["player1"].unique()[0])])
    for player1 in df["player1"].unique():
        if not n_games1 == len(df.loc[(df['player1'] == player1)]):
            if not omit_errors:
                raise ValueError('Different games player by first players')
            return False

    n_games2 = len(df.loc[(df['player2'] == df["player2"].unique()[0])])
    for player2 in df["player2"].unique():
        if not n_games2 == len(df.loc[(df['player2'] == player2)]):
            if not omit_errors:
                raise ValueError('Different games player by second players')
            return False

    if not n_games2 == n_games1:
        if not omit_errors:
            raise ValueError('Different games player by players')
        return False
    return True

def is_duplicated_records(df:pd.DataFrame):
    return len(df[df.duplicated()]) == 0

def is_game_number_equal_for_all_players(df:pd.DataFrame):
    return set(df["player2"].unique()) == set(df["player1"].unique())

def create_results_dict(df:pd.DataFrame):
    results_dict = dict()
    players = np.unique(np.concatenate((df["player1"].unique(), df["player2"].unique())))
    for player_name in players:
        results_dict[player_name] = [0,0,0]

    for key in results_dict.keys():
        # wins
        results_dict[key][0] += len(df.loc[(df['player1'] == key) & (df['winner'] == 1)])
        results_dict[key][0] += len(df.loc[(df['player2'] == key) & (df['winner'] == 2)])
        # draws
        results_dict[key][1] += len(df.loc[(df['player1'] == key) & (df['winner'] == 0)])
        results_dict[key][1] += len(df.loc[(df['player2'] == key) & (df['winner'] == 0)])
        # defeat
        results_dict[key][2] += len(df.loc[(df['player1'] == key) & (df['winner'] == 2)])
        results_dict[key][2] += len(df.loc[(df['player2'] == key) & (df['winner'] == 1)])
    return results_dict

def create_results_df(results_dict:dict):
    df = pd.DataFrame.from_dict(results_dict, orient='index', columns=['wins', 'draws', 'defeats'])
    df['score'] = df['wins']*WIN_SCORE+df['draws']*DRAW_SCORE+df['defeats']*DEFEAT_SCORE
    df.sort_values(by=['score', 'wins', 'draws'], inplace=True, ascending=False)
    df['win%'] = df['wins'] / (df['wins'] + df['draws'] + df['defeats']) * 100
    df['draws%'] = df['draws'] / (df['wins'] + df['draws'] + df['defeats']) * 100
    df['defeats%'] = df['defeats'] / (df['wins'] + df['draws'] + df['defeats']) * 100
    df.drop(columns=['wins', 'draws', 'defeats'], inplace=True)
    return df

def check_data_and_create_result_df(df:pd.DataFrame, omit_errors:bool=False):
    df.drop_duplicates(subset=df.columns.difference(['game_time']))
    if not set(df["player2"].unique()) == set(df["player1"].unique()) and not omit_errors:
        raise ValueError('Different players arrays') 
    check_number_players_games(df, omit_errors)
    result_dict = create_results_dict(df)
    return create_results_df(result_dict)


def show_results_bar_plot(results_dict:dict):
    # set width of bar
    barWidth = 0.15
    fig = plt.subplots(figsize =(20, 6))
    
    # set height of bar
    wins = [v[0] for v in results_dict.values()]
    draws = [v[1] for v in results_dict.values()]
    losses = [v[2] for v in results_dict.values()]

    names = results_dict.keys()
    
    # Set position of bar on X axis
    br1 = np.arange(len(wins))
    br2 = [x + barWidth for x in br1]
    br3 = [x + barWidth for x in br2]
    
    # Make the plot
    plt.bar(br1, wins, color ='g', width = barWidth,
            edgecolor ='grey', label ='wins')
    plt.bar(br2, draws, color ='grey', width = barWidth,
            edgecolor ='grey', label ='draws')
    plt.bar(br3, losses, color ='r', width = barWidth,
            edgecolor ='grey', label ='losses')
    
    # Adding Xticks
    plt.xlabel('Algorithm', fontweight ='bold', fontsize = 15)
    plt.xticks([r + barWidth for r in range(len(wins))], names)
    plt.title("Othello results")
    
    plt.legend()
    plt.show()

def rename(current_names, alg_names):
    result = []
    for name in current_names:
        if name == 0:
            result.append('draw')
        elif name == 1 or name == 2:
            result.append(alg_names[name - 1])
        else:
            result.append('error')
    return result

def draw_graphs(df):
    players = np.unique(np.concatenate((df["player1"].unique(), df["player2"].unique())))
    for player1 in players:
        df_player1 = df.loc[(df['player1'] == player1)]
        for player2 in players:
            df_player2 = df_player1.loc[(df_player1['player2'] == player2)]
            values = df_player2['winner']
            v_counts = values.value_counts()
            v_counts.index = rename(v_counts.index, [player1, player2])
            total = len(values)

            fig = plt.figure()
            plt.title(f"{player1} vs {player2}")
            plt.pie(v_counts, labels=v_counts.index, autopct=lambda x : '{:.2f}%\n({:.0f})'.format(x, total*x/100), shadow=True)