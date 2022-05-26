import numpy as np
import random
from trueskill import global_env
import itertools
import math
from collections import Counter
import pandas as pd


def get_winner_team(elo_playerA1, elo_playerA2, elo_playerB1, elo_playerB2):

  elo_teamA = np.mean([elo_playerA1, elo_playerA2])
  elo_teamB = np.mean([elo_playerB1, elo_playerB2]) 
  match_result = random.choices(
                  population=[[1], [0]],
                  weights=[elo_teamA/(elo_teamA+elo_teamB), elo_teamB/(elo_teamA+elo_teamB)],
                  k=1
                )
  
  return match_result[0][0]

def simulate_draw(teams):
    """Return the list of games."""
    random.shuffle(teams)
    half_len = int(len(teams)/2)
    arr1 = [i for i in range(half_len)]
    arr2 = [i for i in range(half_len, len(teams))][::-1]
    matches = []
    for i in range(len(teams)-1):
        arr1.insert(1, arr2.pop(0))
        arr2.append(arr1.pop())
        for a, b in zip(arr1, arr2):
            matches.append((teams[a], teams[b]))
    return matches

def win_probability(team1, team2):
    delta_mu = sum(r.mu for r in team1) - sum(r.mu for r in team2)
    sum_sigma = sum(r.sigma ** 2 for r in itertools.chain(team1, team2))
    size = len(team1) + len(team2)
    ts = global_env()
    denom = math.sqrt(size * (ts.beta * ts.beta) + sum_sigma)
    
    return ts.cdf(delta_mu / denom)

def predict_match_result(players, teamA, teamB):
  #Predict match result from players
  teamA_rating = [players[i][-1] for i in teamA]
  teamB_rating = [players[i][-1] for i in teamB]
  if win_probability(teamA_rating, teamB_rating) > 0.5:
    return [1, win_probability(teamA_rating, teamB_rating)]
  else:
    return [0, win_probability(teamA_rating, teamB_rating)]

def get_winner_team_ts(players, teamA, teamB):

  [result, prob] = predict_match_result(players, teamA, teamB)
  match_result = random.choices(
                  population=[[1], [0]],
                  weights=[prob, 1-prob],
                  k=1
                )
  
  return match_result[0][0]

def get_metrics_from_system(champs, points_total):
    trophies = Counter(x for xs in champs for x in set(xs))
    for key in trophies:
        trophies[key] /= 10000

    trophies = trophies.most_common()

    points_total_normalized = {k: v / total for total in (sum(points_total.values())/(2*3),) for k, v in points_total.items()}
    points = sorted(points_total_normalized.items(), key=lambda item: item[1], reverse=True)

    df1 = pd.DataFrame(trophies, columns=['player', 'champ_wr'])
    df2 = pd.DataFrame(points, columns=['player', 'match_wr'])

    df = pd.merge(df1, df2, on='player')

    return df

def print_result(players, teamA, teamB):
    [result, prob] = predict_match_result(players, teamA, teamB)
    if result == 1:
        print(f'Gana {teamA} a {teamB} con probabilidad {prob}')
    else:
        print(f'Gana {teamB} a {teamA} con probabilidad {1-prob}')
