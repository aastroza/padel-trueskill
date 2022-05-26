from multielo import MultiElo
import numpy as np
from trueskill import rate, Rating


elo = MultiElo()

def update_ELO(players, playerA1, playerA2, playerB1,  playerB2, result):
  #Update ELO rating from players
  if result == 1:#TeamA wins
    resultsA1 = elo.get_new_ratings(np.array([players[playerA1][-1], 
                                              np.mean([players[playerB1][-1],players[playerB2][-1]])]))
    resultsA2 = elo.get_new_ratings(np.array([players[playerA2][-1], 
                                              np.mean([players[playerB1][-1],players[playerB2][-1]])]))
    resultsB1 = elo.get_new_ratings(np.array([np.mean([players[playerA1][-1], players[playerA2][-1]]), 
                                              players[playerB1][-1]]))
    resultsB2 = elo.get_new_ratings(np.array([np.mean([players[playerA1][-1], players[playerA2][-1]]), 
                                              players[playerB2][-1]]))
    
    players[playerA1].append(resultsA1[0])
    players[playerA2].append(resultsA2[0])
    players[playerB1].append(resultsB1[1])
    players[playerB2].append(resultsB2[1])
  else:#TeamB wins
    resultsA1 = elo.get_new_ratings(np.array([np.mean([players[playerB1][-1],players[playerB2][-1]]), 
                                             players[playerA1][-1]]))
    resultsA2 = elo.get_new_ratings(np.array([np.mean([players[playerB1][-1],players[playerB2][-1]]), 
                                             players[playerA2][-1]]))
    resultsB1 = elo.get_new_ratings(np.array([players[playerB1][-1], 
                                             np.mean([players[playerA1][-1],players[playerA2][-1]])]))
    resultsB2 = elo.get_new_ratings(np.array([players[playerB2][-1], 
                                             np.mean([players[playerA1][-1],players[playerA2][-1]])]))

    players[playerA1].append(resultsA1[1])
    players[playerA2].append(resultsA2[1])
    players[playerB1].append(resultsB1[0])
    players[playerB2].append(resultsB2[0])

  return 'Partido Procesado'

def update_TrueSkill(players, playerA1, playerA2, playerB1,  playerB2, result):
  #Update TrueSkill rating from match result
  t1 = [players[playerA1][-1], players[playerA2][-1]]
  t2 = [players[playerB1][-1], players[playerB2][-1]]
  if result == 1:#TeamA wins
    (new_r1, new_r2), (new_r3, new_r4) = rate([t1, t2], ranks=[0, 1])
  else:
    (new_r1, new_r2), (new_r3, new_r4) = rate([t1, t2], ranks=[1, 0])
  players[playerA1].append(new_r1)
  players[playerA2].append(new_r2)
  players[playerB1].append(new_r3)
  players[playerB2].append(new_r4)

  return 'Partido Procesado'

def calculate_score_TrueSkill(rating):
  k = 3
  return rating.mu-k*rating.sigma

def init_players(data):
  players_names = set(list(data['playerA1'])+list(data['playerA2'])+list(data['playerB1'])+list(data['playerB2']))
  players = { i : [Rating()] for i in players_names }
  [update_TrueSkill(players, row[0], row[1], row[2], 
                                    row[3], row[4]) for row in zip(data['playerA1'], data['playerA2'], 
                                    data['playerB1'], data['playerB2'], data['result'])]
  
  return players




