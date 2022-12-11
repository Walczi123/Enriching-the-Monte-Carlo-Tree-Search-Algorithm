import itertools
from matplotlib import pyplot as plt
import numpy as np
import pandas as pd
from statistics import mean

from additional_functions import mean_foreach_sep, sign, compose, count_foreach_negative, count_foreach_positive, count_foreach_zero, get_negative_values, get_positive_values, join_lists, mean_foreach, sum_lists_elemnet_wise, get_lenghts_nonnegative_nonpositive_sequences

#Scorre
WIN_SCORE = 1
DRAW_SCORE = 0.5
DEFEAT_SCORE = 0

def process_data(file_path, separator, game_name, omit_errors:bool=False):
    df = read_data_of_game(file_path, separator, game_name)
    check_data(df, omit_errors) 
    result_df = create_result_df(df)
    df_tournament = create_tournament_df(df, list(result_df.index))
    return  df, result_df, df_tournament

def read_data(file_path, separator):
    return pd.read_csv(file_path, sep=separator)

def read_data_of_game(file_path, separator, game_name):
    df = pd.read_csv(file_path, sep=separator, header=None)

    if len(df.columns) == 6:
        df.columns = ['game_type','player1','player2','winner','seed','game_time']
        df = df[df['game_type']==game_name]
        return df
    elif len(df.columns) == 7:
        df.columns = ['game_type','player1','player2','winner','seed','game_time','other']
        df = df[df['game_type']==game_name]
        if game_name == 'othello':
            return transform_other_othello(df)
        elif game_name == 'hex':
            return transform_other_hex(df)
        elif game_name == 'hive': 
            return transform_other_hive(df)

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

def check_additiona_info(df:pd.DataFrame, omit_errors:bool=False):
    if len(df.loc[(df['game_type'] == 'othello')])>0:
        check_additiona_info_othello(df.loc[(df['game_type'] == 'othello')], omit_errors)
    if len(df.loc[(df['game_type'] == 'hex')])>0:
        check_additiona_info_hex(df.loc[(df['game_type'] == 'hex')], omit_errors)
    if len(df.loc[(df['game_type'] == 'hive')])>0:
        check_additiona_info_hive(df.loc[(df['game_type'] == 'hive')], omit_errors)

def is_duplicated_records(df:pd.DataFrame):
    return len(df[df.duplicated()]) == 0

def is_game_number_equal_for_all_players(df:pd.DataFrame):
    return set(df["player2"].unique()) == set(df["player1"].unique())

def create_results_dict(df:pd.DataFrame):
    results_dict = dict()
    players = np.unique(np.concatenate((df["player1"].unique(), df["player2"].unique())))
    for player_name in players:
        results_dict[player_name] = [0,0,0,0]

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
        # avg game time
        results_dict[key][3] = round(np.mean(df.loc[(df['player1'] == key) | (df['player2'] == key)]["game_time"]), 2)

    return results_dict

def create_results_df(results_dict:dict):
    df = pd.DataFrame.from_dict(results_dict, orient='index', columns=['wins', 'draws', 'defeats', 'avg game time'])
    df['score'] = df['wins']*WIN_SCORE+df['draws']*DRAW_SCORE+df['defeats']*DEFEAT_SCORE
    df.sort_values(by=['score', 'wins', 'draws'], inplace=True, ascending=False)
    df['win%'] = df['wins'] / (df['wins'] + df['draws'] + df['defeats']) * 100
    df['draws%'] = df['draws'] / (df['wins'] + df['draws'] + df['defeats']) * 100
    df['defeats%'] = df['defeats'] / (df['wins'] + df['draws'] + df['defeats']) * 100
    df['no games'] = df['wins']+df['draws']+df['defeats']
    # df.drop(columns=['wins', 'draws', 'defeats'], inplace=True)
    return df


def check_data(df:pd.DataFrame, omit_errors:bool=False):
    print(f"Amount data before check: {len(df)}")
    df.drop_duplicates(subset=df.columns.difference(['index','game_time']), inplace=True)
    if not set(df["player2"].unique()) == set(df["player1"].unique()) and not omit_errors:
        raise ValueError('Different players arrays') 
    check_number_players_games(df, omit_errors)
    if len(df.columns) == 7 :
        check_additiona_info(df, omit_errors)
    print(f"Amount data after check: {len(df)}")

def create_result_df(df:pd.DataFrame):
    result_dict = create_results_dict(df)
    return create_results_df(result_dict)

def create_tournament_df(df:pd.DataFrame, players:list=None):
    if players is None:
        players = list(set(df["player1"].unique()))
    arr = [[0 for _ in players] for _ in players]
    # nparr = np.zeros((len(players), len(players), 3))
    for index1, value1 in enumerate(players):
        for index2, value2 in enumerate(players):
            (wins_p1, draws_p1, defeats_p1) = get_results_between_players(df, value1, value2)
            arr[index1][index2] = f'{wins_p1}-{draws_p1}-{defeats_p1}'
            # nparr[index1][index2][0] = wins_p1
            # nparr[index1][index2][1] = draws_p1
            # nparr[index1][index2][2] = defeats_p1
    df = pd.DataFrame(arr, columns=players, index=players)
    return df

def get_results_between_players(df:pd.DataFrame, player1, player2):
    df_tmp = get_games_between_two_players(df, player1, player2)
    wins_p1 = 0
    draws_p1 = 0
    defeats_p1 = 0
    # wins
    wins_p1 += len(df_tmp.loc[(df_tmp['player1'] == player1) & (df_tmp['winner'] == 1)])
    # wins_p1 += len(df_tmp.loc[(df_tmp['player2'] == player1) & (df_tmp['winner'] == 2)])
    # draws
    draws_p1 += len(df_tmp.loc[(df_tmp['winner'] == 0)])
    # defeat
    defeats_p1 += len(df_tmp.loc[(df_tmp['player1'] == player1) & (df_tmp['winner'] == 2)])
    # defeats_p1 += len(df_tmp.loc[(df_tmp['player2'] == player1) & (df_tmp['winner'] == 1)])
    return (wins_p1, draws_p1, defeats_p1)


def get_all_games_of_player(df:pd.DataFrame, player:str):
    df1 = df.loc[(df['player1'] == player)]
    df2 = df.loc[(df['player2'] == player) & (df['player1'] != player)]
    return pd.concat([df1, df2])

def get_games_between_two_players(df:pd.DataFrame, player1:str, player2:str):
    df = df.loc[(df['player1'] == player1) & (df['player2'] == player2)]
    return df

def get_all_games_between_two_players(df:pd.DataFrame, player1:str, player2:str):
    df1 = df.loc[(df['player1'] == player1) & (df['player2'] == player2)]
    if player1 == player2:
        return df1
    df2 = df.loc[(df['player1'] == player2) & (df['player2'] == player1)]
    return pd.concat([df1, df2])


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

def transform_other_othello(df:pd.DataFrame):
    d_tmp = dict()
    columns = ['score_result','score_result_diff', 'no_moves_p1','no_moves_p2','no_blocked_moves_p1','no_blocked_moves_p2','move_income_p1','move_income_p2','board_scores','switching_stats_p1','switching_stats_p2']

    for c in columns:
        d_tmp[c] = list()

    for r in df['other']:
        d = r[1:-1].replace('(', '').split("),")

        d1 = d[1].strip().split(",")
        d2 = d[2].strip().split(",")
        d3 = d[3].strip()[1:-1].split("], [")
        d4 = d[4].split("],",1)
        d4_1 = d4[1].strip().replace("None", '[[]]').strip().split(']], [[')

        d_tmp['score_result'].append(d[0].replace(',', ':'))
        a,b = d[0].split(',')
        d_tmp['score_result_diff'].append(int(a) - int(b))
        d_tmp['no_moves_p1'].append(int(d1[0]))
        d_tmp['no_moves_p2'].append(int(d1[1]))
        d_tmp['no_blocked_moves_p1'].append(int(d2[0]))
        d_tmp['no_blocked_moves_p2'].append(int(d2[1]))
        d_tmp['move_income_p1'].append(tuple((int(elem) for elem in d3[0].split(','))))
        d_tmp['move_income_p2'].append(tuple((int(elem) for elem in d3[1].split(','))))
        d_tmp['board_scores'].append(tuple((int(elem) for elem in d4[0].strip()[1:].split(','))))
        # d_tmp['move_income_p1'].append(d3[0])
        # d_tmp['move_income_p2'].append(d3[1])
        # d_tmp['board_scores'].append(d4[0].strip()[1:])
        # d_tmp['switching_stats_p1'].append(d4_1[0][1:]+']' if d4_1[0] != '[[' else None)
        # d_tmp['switching_stats_p2'].append('['+d4_1[1][:-1] if d4_1[1] != ']]' else None)

        if d4_1[0] != '[[':
            switching_stats = tuple((tuple(([int(elem2) for elem2 in elem.split(',') ])) for elem in d4_1[0][2:].replace(' ','').split('],[')))
            d_tmp['switching_stats_p1'].append(switching_stats)
        else:           
            d_tmp['switching_stats_p1'].append(None)

        if d4_1[1] != ']]':
            switching_stats = tuple((tuple(([int(elem2) for elem2 in elem.split(',') ])) for elem in d4_1[1][:-2].replace(' ','').split('],[')))
            d_tmp['switching_stats_p2'].append(switching_stats)
        else:
            d_tmp['switching_stats_p2'].append(None)


    df1 = df.drop('other', axis=1).reset_index()
    df2 = pd.concat([df1, pd.DataFrame(d_tmp)], axis=1)
    df2.insert(16, "board_scores_monotonicity", df2["board_scores"].apply(lambda x : tuple(([1 if x[i] < x[i+1] else -1 for i in range(len(x)-1)]))))
    df2.insert(17, "board_scores_leader_change", df2["board_scores"].apply(lambda x : tuple(([1 if (x[i]>0 and x[i+1]<0) or (x[i]<0 and x[i+1]>0) else 0 for i in range(len(x)-1)]))))
    df2.insert(18, "board_scores_leading", df2["board_scores"].apply(lambda x : tuple(([sign(y) for y in x]))))
    return df2

def transform_other_hex(df:pd.DataFrame):
    d_tmp = dict()
    columns = ['no_moves_p1','no_moves_p2', 'dikstra_scores_p1', 'dikstra_scores_p2', 'switching_stats_p1','switching_stats_p2']

    for c in columns:
        d_tmp[c] = list()

    for r in df['other']:
        d = r[1:-1].replace('(', '').split("),")

        d0=d[0].strip().split(",")
        d1=d[1].strip().split("], [")
        d2=d[2].strip().replace("None", '[[]]').strip().split(']], [[')

        d_tmp['no_moves_p1'].append(int(d0[0]))
        d_tmp['no_moves_p2'].append(int(d0[1]))
        d_tmp['dikstra_scores_p1'].append(tuple(([int(elem) for elem in d1[0][1:].split(",")])))
        d_tmp['dikstra_scores_p2'].append(tuple(([int(elem) for elem in d1[1][:-1].split(",")])))


        if d2[0] != '[[':
            switching_stats = tuple((tuple(([int(elem2) for elem2 in elem.split(',') ])) for elem in d2[0][2:].replace(' ','').split('],[')))
            d_tmp['switching_stats_p1'].append(switching_stats)
        else:           
            d_tmp['switching_stats_p1'].append(None)

        if d2[1] != ']]':
            switching_stats = tuple((tuple(([int(elem2) for elem2 in elem.split(',') ])) for elem in d2[1][:-2].replace(' ','').split('],[')))
            d_tmp['switching_stats_p2'].append(switching_stats)
        else:
            d_tmp['switching_stats_p2'].append(None)

    df1 = df.drop('other', axis=1).reset_index()
    df2 = pd.concat([df1, pd.DataFrame(d_tmp)], axis=1)
    df2.insert(11, "dikstra_scores_diff_values_p1", df2['dikstra_scores_p1'].apply(lambda x : tuple(([x[i+1]-x[i] for i in range(len(x)-1)]))))
    df2.insert(12, "dikstra_scores_diff_values_p2", df2['dikstra_scores_p2'].apply(lambda x : tuple(([x[i+1]-x[i] for i in range(len(x)-1)]))))
    return df2

def transform_other_hive(df:pd.DataFrame):
    d_tmp = dict()
    columns = ['queens_neighbours_count_player1', 'queens_neighbours_count_player2',
        'player1_unsed_pieces','player2_unsed_pieces','player1_pos_moves','player2_pos_moves',
        'switching_stats_p1', 'switching_stats_p2']

    for c in columns:
        d_tmp[c] = list()

    for r in df['other']:
        try:
            d = r[1:-1].strip().split(")], [(")

            d0 = d[0][3:-1].split(")), ((")
            d1 = d[1].split("]), ([")
            d20 = d[2].split("],",1)[0]
            d21 = d[2].split("],",1)[1].strip().replace("None", '[[]]').split(']], [[')
            
            l1 = list()
            l2 = list()
            for x in d0:
                y = x.split('), (')
                y1 = tuple(([int(z) for z in y[0].strip().split(',')]))
                y2 = tuple(([int(z) for z in y[1].strip().split(',')]))

                l1.append(y1)
                l2.append(y2)
            d_tmp['queens_neighbours_count_player1'].append(tuple((l1)))
            d_tmp['queens_neighbours_count_player2'].append(tuple((l2)))

            l1 = list()
            l2 = list()
            for x in d1[1:-1]:
                y = x.split('], [')
                y1 = tuple(([int(z) for z in y[0].strip().split(',')]))
                y2 = tuple(([int(z) for z in y[1].strip().split(',')]))

                l1.append(y1)
                l2.append(y2)
            d_tmp['player1_unsed_pieces'].append(tuple((l1)))
            d_tmp['player2_unsed_pieces'].append(tuple((l2)))

            l1 = list()
            l2 = list()
            for x in d20[:-1].split('), ('):
                y = x.split(',')
                l1.append(int(y[0]))
                l2.append(int(y[1]))
            d_tmp['player1_pos_moves'].append(tuple((l1)))
            d_tmp['player2_pos_moves'].append(tuple((l2)))

            if d21[0] != '[[':
                switching_stats = tuple((tuple(([int(elem2) for elem2 in elem.split(',') ])) for elem in d21[0][2:].replace(' ','').split('],[')))
                d_tmp['switching_stats_p1'].append(switching_stats)
            else:           
                d_tmp['switching_stats_p1'].append(None)

            if d21[1] != ']]':
                switching_stats = tuple((tuple(([int(elem2) for elem2 in elem.split(',') ])) for elem in d21[1][:-2].replace(' ','').split('],[')))
                d_tmp['switching_stats_p2'].append(switching_stats)
            else:
                d_tmp['switching_stats_p2'].append(None)
        except Exception as e:
            print(r)
            return r

    df1 = df.drop('other', axis=1).reset_index()
    df2 = pd.concat([df1, pd.DataFrame(d_tmp)], axis=1)
    return df2

def check_additiona_info_othello(df:pd.DataFrame, omit_errors:bool=False):
    df_temp=pd.concat([df['score_result'].str.split(':',1,expand=True).astype(int),df['winner']],axis=1)
    for r in pd.concat([df_temp.iloc[:,0:2].idxmax(axis=1)+1 == df["winner"],df_temp[0]==df_temp[1], df_temp['winner']==0],axis=1).values:
        if not (r[0] or (r[1]and r[2])):
            if not omit_errors: raise ValueError('Additional info Othello - invalid score_result or winner')

    df_tmp = df["no_moves_p1"].apply(lambda x : int(x)>0)
    invalid_indexies = df_tmp[df_tmp==False].index
    if len(invalid_indexies)>0:
        if not omit_errors: raise ValueError(f'Additional info Othello - no player 1 moves ({invalid_indexies[0]})')
    df_tmp = df["no_moves_p2"].apply(lambda x : int(x)>0)
    invalid_indexies = df_tmp[df_tmp==False].index
    if len(invalid_indexies)>0:
        if not omit_errors: raise ValueError(f'Additional info Othello - no player 2 moves ({invalid_indexies[0]})')
    
    df_tmp = df[df["board_scores"]==""]
    if not all((df['no_moves_p1'].astype(int)+df['no_blocked_moves_p1'].astype(int))-(df['no_moves_p2'].astype(int)+df['no_blocked_moves_p2'].astype(int))<2):
        if not omit_errors: raise ValueError('Additional info Othello - Sum of players moves diff is bigger then 1')

    df_tmp = df[df["board_scores"]==""]
    if len(df_tmp)>0:
        if not omit_errors: raise ValueError(f'Additional info Othello - invalid board scores ({df_tmp.index[0]})')
        df = df.drop(df_tmp.index)

    df_monotonic = df["board_scores_monotonicity"] 
    if not all(df_monotonic.apply(lambda x: abs(sum([el for el in x if el>0 ])) + 1).astype(int) == df["no_moves_p1"].astype(int)):
        if not omit_errors: raise ValueError(f'Additional info Othello - invalid board scores or no player 1 moves ({df[df_monotonic.apply(lambda x: abs(sum([el for el in x if el>0 ])) + 1).astype(int) == df["no_moves_p1"].astype(int)].index[0]})')   
    if not all(df_monotonic.apply(lambda x: abs(sum([el for el in x if el<0]))).astype(int)== df["no_moves_p2"].astype(int)):
        if not omit_errors: raise ValueError(f'Additional info Othello - invalid board scores or no player 2 moves ({df[df_monotonic.apply(lambda x: abs(sum([el for el in x if el<0]))).astype(int)!= df["no_moves_p2"].astype(int)].index[0]})')

    if not all(df_monotonic.apply(lambda x : sum([1 if x[i] == -1 and x[i+1] == -1 else 0 for i in range(len(x)-1)])).astype(int)==df['no_blocked_moves_p1'].astype(int)):
        index = df[df_monotonic.apply(lambda x : sum([1 if x[i] == -1 and x[i+1] == -1 else 0 for i in range(len(x)-1)])).astype(int)!=df['no_blocked_moves_p1'].astype(int)].index[0]
        if not omit_errors: raise ValueError(f'Additional info Othello - invalid board scores or no player 1 blocked moves ({index})')
        
    if not all(df_monotonic.apply(lambda x : sum([1 if x[i] == 1 and x[i+1] == 1 else 0 for i in range(len(x)-1)])).astype(int)==df['no_blocked_moves_p2'].astype(int)):
        index = df[df_monotonic.apply(lambda x : sum([1 if x[i] == 1 and x[i+1] == 1 else 0 for i in range(len(x)-1)])).astype(int)!=df['no_blocked_moves_p2'].astype(int)].index[0]
        if not omit_errors: raise ValueError(f'Additional info Othello - invalid board scores or no player 2 blocked moves ({index})')

    df_tmp = df[df['player1'].str.contains('mctsstrategies')].reset_index()
    if not all(df_tmp['switching_stats_p1'].apply(lambda x: len(x)).astype(int) == df_tmp['no_moves_p1'].astype(int)):
        if not omit_errors: raise ValueError('Additional info Othello - invalid switching stats for player 1')

    df_tmp2 = df_tmp.dropna(subset=["switching_stats_p1"])
    df_tmp2 = df_tmp2[df_tmp2["player1"].str.contains('mctsstrategies')]
    df_tmp2 = df_tmp2[["switching_stats_p1",'player1']]
    df_tmp2['no'] = df_tmp2['player1'].str.replace('mctsstrategies','').apply(lambda x: x.split('(')[0]).astype(int)
    if not all(df_tmp2['switching_stats_p1'].apply(lambda x: all([all(sum(y) == df_tmp2['no']) for y in x]))):
        if not omit_errors: raise ValueError('Additional info Othello - invalid switching stats for player 1 (switching stats sum is incorrect')

    df_tmp = df[df['player2'].str.contains('mctsstrategies')].reset_index()
    if not all(df_tmp['switching_stats_p2'].apply(lambda x: len(x)).astype(int) == df_tmp['no_moves_p2'].astype(int)):
        if not omit_errors: raise ValueError('Additional info Othello - invalid switching stats for player 2')

    df_tmp2 = df_tmp.dropna(subset=["switching_stats_p2"])
    df_tmp2 = df_tmp2[df_tmp2["player2"].str.contains('mctsstrategies')]
    df_tmp2 = df_tmp2[["switching_stats_p2",'player2']]
    df_tmp2['no'] = df_tmp2['player2'].str.replace('mctsstrategies','').apply(lambda x: x.split('(')[0]).astype(int)
    if not all(df_tmp2['switching_stats_p2'].apply(lambda x: all([all(sum(y) == df_tmp2['no']) for y in x]))):
        if not omit_errors: raise ValueError('Additional info Othello - invalid switching stats for player 2 (switching stats sum is incorrect')
    
def check_additiona_info_hex(df:pd.DataFrame, omit_errors:bool=False):
    if not all(df['dikstra_scores_p1'].apply(lambda x : len(x)).astype(int)==df['no_moves_p1'].astype(int)):
        if not omit_errors: raise ValueError('Additional info Hex - invalid dikstra scores or no player 1 moves')
    if not all(df['dikstra_scores_p2'].apply(lambda x : len(x)).astype(int)==df['no_moves_p2'].astype(int)):
        if not omit_errors: raise ValueError('Additional info Hex - invalid dikstra scores or no player 2 moves')

    df_tmp = df[df['player1'].str.contains('mctsstrategies')].reset_index()
    if not all(df_tmp['switching_stats_p1'].apply(lambda x: len(x)).astype(int) == df_tmp['no_moves_p1'].astype(int)):
        if not omit_errors: raise ValueError('Additional info Hex - invalid switching stats for player 1')
    
    df_tmp2 = df_tmp.dropna(subset=["switching_stats_p1"])
    df_tmp2 = df_tmp2[df_tmp2["player1"].str.contains('mctsstrategies')]
    df_tmp2 = df_tmp2[["switching_stats_p1",'player1']]
    df_tmp2['no'] = df_tmp2['player1'].str.replace('mctsstrategies','').apply(lambda x: x.split('(')[0]).astype(int)
    if not all(df_tmp2['switching_stats_p1'].apply(lambda x: all([all(sum(y) == df_tmp2['no']) for y in x]))):
        if not omit_errors: raise ValueError('Additional info Othello - invalid switching stats for player 1 (switching stats sum is incorrect')
    
    df_tmp = df[df['player2'].str.contains('mctsstrategies')].reset_index()
    if not all(df_tmp['switching_stats_p2'].apply(lambda x: len(x)).astype(int) == df_tmp['no_moves_p2'].astype(int)):
        if not omit_errors: raise ValueError('Additional info Hex - invalid switching stats for player 2')

    df_tmp2 = df_tmp.dropna(subset=["switching_stats_p2"])
    df_tmp2 = df_tmp2[df_tmp2["player2"].str.contains('mctsstrategies')]
    df_tmp2 = df_tmp2[["switching_stats_p2",'player2']]
    df_tmp2['no'] = df_tmp2['player2'].str.replace('mctsstrategies','').apply(lambda x: x.split('(')[0]).astype(int)
    if not all(df_tmp2['switching_stats_p2'].apply(lambda x: all([all(sum(y) == df_tmp2['no']) for y in x]))):
        if not omit_errors: raise ValueError('Additional info Othello - invalid switching stats for player 2 (switching stats sum is incorrect')


def check_additiona_info_hive(df:pd.DataFrame, omit_errors:bool=False):
    if not all(df['queens_neighbours_count_player1'].apply(lambda x : [(y[0]+y[1])>=0 and (y[0]+y[1])<=6 for y in x])):
        if not omit_errors: raise ValueError('Additional info Hive - invalid queens neighbour count for player1')

    if not all(df['queens_neighbours_count_player2'].apply(lambda x : [(y[0]+y[1])>=0 and (y[0]+y[1])<=6 for y in x])):
        if not omit_errors: raise ValueError('Additional info Hive - invalid queens neighbour count for player2')

    s_p1_pos_m = set(df['player1_pos_moves'].apply(lambda x : len(x)))
    s_p2_pos_m = set(df['player1_pos_moves'].apply(lambda x : len(x)))
    s_p1_queen_n = set(df['queens_neighbours_count_player1'].apply(lambda x : len(x)))
    s_p2_queen_n = set(df['queens_neighbours_count_player2'].apply(lambda x : len(x)))
    
    if not max(s_p1_pos_m) == max(s_p2_pos_m) == max(s_p1_queen_n) == max(s_p2_queen_n):
        if not omit_errors: raise ValueError('Additional info Hive - max count of other data is invalid')
    
    if not min(s_p1_pos_m) == min(s_p2_pos_m) == min(s_p1_queen_n) == min(s_p2_queen_n):
        if not omit_errors: raise ValueError('Additional info Hive - min count of other data is invalid')

    df_tmp = df[df['player1'].str.contains('mctsstrategies')].reset_index()
    if not all(df_tmp['switching_stats_p1'].apply(lambda x: len(x)).astype(int) == df_tmp['no_moves_p1'].astype(int)):
        if not omit_errors: raise ValueError('Additional info Hex - invalid switching stats for player 1')
    
    df_tmp2 = df_tmp.dropna(subset=["switching_stats_p1"])
    df_tmp2 = df_tmp2[df_tmp2["player1"].str.contains('mctsstrategies')]
    df_tmp2 = df_tmp2[["switching_stats_p1",'player1']]
    df_tmp2['no'] = df_tmp2['player1'].str.replace('mctsstrategies','').apply(lambda x: x.split('(')[0]).astype(int)
    if not all(df_tmp2['switching_stats_p1'].apply(lambda x: all([all(sum(y) == df_tmp2['no']) for y in x]))):
        if not omit_errors: raise ValueError('Additional info Othello - invalid switching stats for player 1 (switching stats sum is incorrect')
    
    df_tmp = df[df['player2'].str.contains('mctsstrategies')].reset_index()
    if not all(df_tmp['switching_stats_p2'].apply(lambda x: len(x)).astype(int) == df_tmp['no_moves_p2'].astype(int)):
        if not omit_errors: raise ValueError('Additional info Hex - invalid switching stats for player 2')

    df_tmp2 = df_tmp.dropna(subset=["switching_stats_p2"])
    df_tmp2 = df_tmp2[df_tmp2["player2"].str.contains('mctsstrategies')]
    df_tmp2 = df_tmp2[["switching_stats_p2",'player2']]
    df_tmp2['no'] = df_tmp2['player2'].str.replace('mctsstrategies','').apply(lambda x: x.split('(')[0]).astype(int)
    if not all(df_tmp2['switching_stats_p2'].apply(lambda x: all([all(sum(y) == df_tmp2['no']) for y in x]))):
        if not omit_errors: raise ValueError('Additional info Othello - invalid switching stats for player 2 (switching stats sum is incorrect')

def transform_games_into_players_stats(df:pd.DataFrame):
    l = list()
    for row in df.values:
        try:
            p1 = [row[1],row[2], row[4] == 1, row[5], row[6], row[8],  row[9], row[10], row[11], row[12], row[13], row[14], row[15], [int(a) for a in row[16].split(',')], row[17], row[18]]
            p2 = [row[1],row[3], row[4] == 2, row[5], row[6], row[8], -row[9], row[11], row[10], row[13], row[12], row[15], row[14], [-int(a) for a in row[16].split(',')], row[18], row[17]]
        except:
            print(row[0])
            continue
        l.append(p1)
        l.append(p2)
    df_cols= df.columns
    cols = [df_cols[1],df_cols[2], 'is_winner', df_cols[5], df_cols[6], df_cols[8],  df_cols[9], 'player_no_moves', 'opponent_no_moves', 'player_no_blocked_moves', 'opponent_no_blocked_moves', 'player_move_income', 'opponent_move_income', df_cols[16], 'player_swithching_stats', 'opponent_swithching_stats']
    return pd.DataFrame(l, columns=cols)

def create_data_agg_by_player_othello(df:pd.DataFrame):
    l = list()
    for row in df.values:
        p1 = [row[1],row[2], row[4] == 1, row[5], row[6], row[7],  row[8], row[9], row[10], row[11], row[12], row[13], row[14], [int(a) for a in row[15]], [int(a) for a in row[16]], row[17], [int(a) for a in row[18]], row[19] if row[19] != None else [], row[20] if row[20] != None else []]
        p2 = [row[1],row[3], row[4] == 2, row[5], row[6], row[7], -row[8], row[10], row[9], row[12], row[11], row[14], row[13], [-int(a) for a in row[15]], [-int(a) for a in row[16]], row[17], [-int(a) for a in row[18]],row[20] if row[20] != None else [], row[19] if row[19] != None else []]
        l.append(p1)
        l.append(p2)
    df_cols= df.columns
    return pd.DataFrame(l, columns=[df_cols[1],'player', 'is_winner', df_cols[5], df_cols[6], df_cols[7],  df_cols[8], 'player_no_moves', 'opponent_no_moves', 'player_no_blocked_moves', 'opponent_no_blocked_moves', 'player_move_income', 'opponent_move_income', df_cols[15], df_cols[16], df_cols[17], df_cols[18], 'player_switching_stats', 'opponent_switching_stats'])

def create_aggregate_datas_othello(df:pd.DataFrame):
    df_player = create_data_agg_by_player_othello(df)
    agg_dict = {'is_winner': 'sum',
                'game_type': 'count',
                'score_result_diff':'mean',
                'player_no_moves':'mean',
                'opponent_no_blocked_moves':'mean',
                'player_move_income': [('mean_playerr_income', compose(mean, join_lists))],
                'board_scores': [('mean_board_scores',compose(mean, join_lists)), 
                                ('mean_positive_board_scores',compose(mean, get_positive_values, join_lists)), 
                                ('mean_negative_board_scores',compose(mean, get_negative_values, join_lists))],
                'board_scores_leader_change': [('mean', mean_foreach)],
                'board_scores_leading': [('winning', count_foreach_positive),
                                    ('draw', count_foreach_zero),
                                    ('losing', count_foreach_negative)],
                'player_switching_stats': [('strategies stats',compose(sum_lists_elemnet_wise,join_lists))]    
                }
    df_agg_by_player = df_player.groupby(by=['player'], as_index=True).agg(agg_dict)
    # columns = ['win_games_count', 'all_games_count', 'mean_score_result_diff', 'mean_player_moves', 'mean_opponent_blocked_moves', 'mean_player_income', 'mean_board_score', 'mean_winning_board_scores', 'mean_losing_board_scores','mean_leader_changes_per_game', 'mean_board_winning_states_per_game', 'mean_board_draw_states_per_game', 'mean_board_losing_states_per_game','player_switching_stats']
    # df_agg_by_player.columns = columns
    df_agg_by_player.columns = ['_'.join(col) for col in df_agg_by_player.columns.values]
    df_agg_by_player_winner = df_player.groupby(by=['player','is_winner'], as_index=True).agg(agg_dict)
    # df_agg_by_player_winner.columns = columns
    df_agg_by_player_winner.columns = ['_'.join(col) for col in df_agg_by_player_winner.columns.values]
    return df_player, df_agg_by_player, df_agg_by_player_winner

def create_data_agg_by_player_hex(df:pd.DataFrame):
    l = list()
    for row in df.values:
        p1 = [row[1],row[2], row[4] == 1, row[5], row[6], row[7], row[8], row[9], row[10], row[11], row[12], row[13] if row[13] != None else [], row[14] if row[14] != None else []]
        p2 = [row[1],row[3], row[4] == 2, row[5], row[6], row[8], row[7], row[10], row[9], row[12], row[11], row[14] if row[14] != None else [], row[13] if row[13] != None else []]
        l.append(p1)
        l.append(p2)
    df_cols= df.columns
    df_player = pd.DataFrame(l, columns=[df_cols[1],'player', 'is_winner', df_cols[5], df_cols[6], 'player_no_moves', 'opponent_no_moves', 'player_dikstra_scores', 'opponent_dikstra_scores', 'player_dikstra_scores_diff_values', 'opponent_dikstra_scores_diff_values', 'player_switching_stats', 'opponent_switching_stats'])
    lenghts_nonnegative_nonpositive_sequences = df_player['player_dikstra_scores_diff_values'].apply(lambda x : get_lenghts_nonnegative_nonpositive_sequences(x))
    df_player.insert(11, "nonnegative_sequences", [x[0] for x in lenghts_nonnegative_nonpositive_sequences])
    df_player.insert(12, "nonpositive_sequences", [x[1] for x in lenghts_nonnegative_nonpositive_sequences])
    df_player["count_nonnegative_sequences"] = df_player['nonnegative_sequences'].apply(lambda x : len(x))
    df_player["count_nonpositive_sequences"] = df_player['nonpositive_sequences'].apply(lambda x : len(x))
    return df_player

def create_aggregate_datas_hex(df:pd.DataFrame):
    df_player = create_data_agg_by_player_hex(df)
    agg_dict = {'is_winner': 'sum',
                'game_type': 'count',
                'player_no_moves':'mean',
                'opponent_no_moves':'mean',
                'player_dikstra_scores_diff_values':[('mean_diff_value_after_player_move', compose(mean,join_lists)),
                                                ('mean_diff_value_after_player_move_per_game', mean_foreach_sep)],
                'opponent_dikstra_scores_diff_values':[('mean_diff_value_after_opponent_move', compose(mean,join_lists)),
                                                ('mean_diff_value_after_opponent_move_per_game', mean_foreach_sep)],
                'nonnegative_sequences' : [('mean_nonnegative_sequences_lenght', compose(mean,join_lists))],
                'nonpositive_sequences' : [('mean_nonpositive_sequences_lenght', compose(mean,join_lists))],
                'count_nonnegative_sequences' : [('mean'), ('count', lambda x : len([z for z in x if z == 0]))], 
                'count_nonpositive_sequences' : [('mean'), ('count', lambda x : len([z for z in x if z == 0]))],                            
                'player_switching_stats': [('strategies stats', compose(sum_lists_elemnet_wise,join_lists))]    
                }
    df_agg_by_player = df_player.groupby(by=['player'], as_index=True).agg(agg_dict)
    # columns = ['win_games_count', 'all_games_count', 'mean_player_moves', 'mean_opponent_moves', 'mean_of_all_diff_after_player_moves', 'mean_of_means_of_each_game_diff_after_player_moves', 'mean_of_all_diff_after_opponent_moves', 'mean_of_means_of_each_game_diff_after_oponent_moves', 'mean_nonnegative_sequences_lenght', 'mean_nonpositive_sequences_lenght', 'mean_count_nonnegative_sequences', 'count_games_with_none_nonnegative_sequences', 'mean_count_nonpositive_sequences', 'count_games_with_none_nonpositive_sequences', 'player_switching_stats']
    # df_agg_by_player.columns = columns
    df_agg_by_player.columns = ['_'.join(col) for col in df_agg_by_player.columns.values]
    df_agg_by_player_winner = df_player.groupby(by=['player', 'is_winner'], as_index=True).agg(agg_dict)
    # df_agg_by_player_winner.columns = columns
    df_agg_by_player_winner.columns = ['_'.join(col) for col in df_agg_by_player_winner.columns.values]
    return df_player, df_agg_by_player, df_agg_by_player_winner

def create_data_agg_by_player_hive(df:pd.DataFrame):
    l = list()
    for row in df.values:
        p1 = [row[1],row[2], row[4] == 1, row[4] == 0, row[5], row[6], [x[0] for x in row[7]], [x[1] for x in row[7]], [x[0] for x in row[8]], [x[1] for x in row[8]], row[9], row[10], row[11], row[12], row[13] if row[13] != None else [], row[14] if row[14] != None else []]
        p2 = [row[1],row[3], row[4] == 2, row[4] == 0, row[5], row[6], [x[0] for x in row[8]], [x[1] for x in row[8]], [x[0] for x in row[7]], [x[1] for x in row[7]], row[10], row[9], row[12], row[11], row[14] if row[14] != None else [], row[13] if row[13] != None else []]
        l.append(p1)
        l.append(p2)
    df_cols= df.columns
    df1 = pd.DataFrame(l, columns=[df_cols[1],'player', 'is_winner', 'is_draw', df_cols[5], df_cols[6], 'player_queens_neighbours_count_p', 'player_queens_neighbours_count_o',  'opponent_queens_neighbours_count_o', 'opponent_queens_neighbours_count_p', 'player_unsed_pieces', 'opponent_unsed_pieces', 'player_pos_moves', 'opponent_pos_moves', 'player_switching_stats', 'opponent_switching_stats'])
    df1.insert(5, "player_queens_neighbours_count", df1['player_queens_neighbours_count_p']+df1['player_queens_neighbours_count_o'])
    df1.insert(8, "opponent_queens_neighbours_count", df1['opponent_queens_neighbours_count_p']+df1['opponent_queens_neighbours_count_o'])
    return df1

def create_aggregate_datas_hive(df:pd.DataFrame):
    df_player = create_data_agg_by_player_hive(df)
    agg_dict = {'is_winner': 'sum',
            'is_draw': 'sum',
            'game_type': 'count',
            'player_queens_neighbours_count': mean_foreach_sep,
            'player_queens_neighbours_count_p':mean_foreach_sep,
            'player_queens_neighbours_count_o':mean_foreach_sep,
            'opponent_queens_neighbours_count': mean_foreach_sep,
            'opponent_queens_neighbours_count_p':mean_foreach_sep,
            'opponent_queens_neighbours_count_o':mean_foreach_sep,
            'player_pos_moves':[('mean', compose(mean,join_lists)),('mean_foreach_sep', mean_foreach_sep)],
            'opponent_pos_moves':[('mean', compose(mean,join_lists)),('mean_foreach_sep', mean_foreach_sep)],
            'player_unsed_pieces': [('sum_element_wise', compose(sum_lists_elemnet_wise,join_lists))],
            'opponent_unsed_pieces': [('sum_element_wise', compose(sum_lists_elemnet_wise,join_lists))],
            'player_switching_stats': [('strategies stats', compose(sum_lists_elemnet_wise,join_lists))]
            }
    df_agg_by_player = df_player.groupby(by=['player'], as_index=True).agg(agg_dict)
    # columns = ['win_games_count', 'all_games_count', 'mean_player_moves', 'mean_opponent_moves', 'mean_of_all_diff_after_player_moves', 'mean_of_means_of_each_game_diff_after_player_moves', 'mean_of_all_diff_after_opponent_moves', 'mean_of_means_of_each_game_diff_after_oponent_moves', 'mean_nonnegative_sequences_lenght', 'mean_nonpositive_sequences_lenght', 'mean_count_nonnegative_sequences', 'count_games_with_none_nonnegative_sequences', 'mean_count_nonpositive_sequences', 'count_games_with_none_nonpositive_sequences', 'player_switching_stats']
    # df_agg_by_player.columns = columns
    df_agg_by_player.columns = ['_'.join(col) for col in df_agg_by_player.columns.values]
    df_agg_by_player_winner = df_player.groupby(by=['player', 'is_winner'], as_index=True).agg(agg_dict)
    # df_agg_by_player_winner.columns = columns
    df_agg_by_player_winner.columns = ['_'.join(col) for col in df_agg_by_player_winner.columns.values]
    return df_player, df_agg_by_player, df_agg_by_player_winner

def get_switching_stats(df_player, player_name):
    df_strategies = df_player[df_player['player']==player_name]
    switching_stats=df_strategies['player_switching_stats']
    switching_stats_l = switching_stats.tolist()
    one_switching_stats_l = list(itertools.chain.from_iterable(switching_stats_l))
    switching_stats_arr = np.array(one_switching_stats_l).T

    players= [x.replace('_strategy','') for x in player_name.split('(',1)[1][:-1].split(":")]
    df = pd.DataFrame()
    for i in range(len(players)):
        df[str(players[i])] = switching_stats_arr[i]
    return df