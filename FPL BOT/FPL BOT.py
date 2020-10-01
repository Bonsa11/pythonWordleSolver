# -*- coding: utf-8 -*-
"""
Created on Wed Sep 23 11:23:32 2020

@author: Sam
"""

"""
FPL BOT

AIM: Create a bot that picks an initial starting 15 players based on last years players
                + make transfers based on form and upcomoing fixtures
        
        1. Find data for:
                         This Seasons Players (TSP)
                         Upcoming Fixtures (UF)
                    
        2. Create model based on last season points and new seasons prices
                        
                        - find useful variables  NOT INCLUDING FIXTURES
                        - predict points vs actual points
                        - workout upcoming fixture difficulty
                            - Using Ben Crellins FDR sheet
                            - Use next 5 GW's difficulty to determine if good fixtures or not
                        - Single Number!!! 
                        
          3. Remove NP + Injured Players
          
          4. Create template for 15 players
                        
                        1. 2 GK
                        2. 5 DEFS
                        3. 5 MIDS
                        4. 3 FWDS
                        
                        
        5. Pick Formation (PF)
                        - Pick formation
                        - User Entry
                        
        6. Fill in Team
                        Josh Bull ()- Team strategy
                        
                1. 5-6 costly players + cheap fillers over 1-2 costly + mid range 
                2. Bench substitution - players @Home over players @Away. 
                3. Formation is not really a factor (choose best based on your players)
                
                Tranfer strategy
                1. Form over fixtures 
                2. Transfer out underperformer over Transfer in last week's best performer/jumping a bandwagon
                
                Captain strategy
                1. Fixtures over form
                2. If a tie: home over away

"""

import requests
import pandas as pd
from boruta import BorutaPy
import numpy as np
from sklearn.ensemble import RandomForestRegressor
import scipy as sp
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
from sklearn import preprocessing
import scipy.stats as stats
from datetime import date
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score


def normalise(v):
    v = (v-min(v))/(max(v)-min(v))
    return(v)


gameweek = 5
max_budget = 100
formation = [1,3,4,3]

##################################################################################################
"""

Accessing API

"""
##################################################################################################  

# https://towardsdatascience.com/boruta-explained-the-way-i-wish-someone-explained-it-to-me-4489d70e154a for Boruta

url = 'https://fantasy.premierleague.com/api/bootstrap-static/'
r = requests.get(url)
json = r.json()
    
json.keys()
    
elements_df = pd.DataFrame(json['elements'])
elements_types_df = pd.DataFrame(json['element_types'])
teams_df = pd.DataFrame(json['teams'])
events_df = pd.DataFrame(json['events'])

slim_elements_df = elements_df
slim_elements_df['position'] = slim_elements_df.element_type.map(elements_types_df.set_index('id').singular_name)
slim_elements_df['team'] = slim_elements_df.team.map(teams_df.set_index('id').name)
slim_elements_df['selected_by_percent'] = slim_elements_df.selected_by_percent.astype(float)
slim_elements_df['value'] = slim_elements_df.value_season.astype(float)
slim_elements_df['now_cost'] = slim_elements_df['now_cost']/10
slim_elements_df['ROI'] = slim_elements_df['total_points'] / slim_elements_df['now_cost']

df = slim_elements_df[['id','web_name','team_code','element_type', 'form', 'ep_this', 'ep_next' , 'bonus','selected_by_percent','now_cost','minutes','transfers_in' ,'transfers_in_event', 'transfers_out' , 'transfers_out_event', 'total_points', 'dreamteam_count', 'points_per_game', 'value_form', 'value_season', 'goals_scored', 'assists', 'clean_sheets', 'influence', 'creativity', 'threat']]        

##################################################################################################
"""

Modelling Points

"""
##################################################################################################  

X = df.drop(columns = ['web_name', 'total_points'])
y = df['total_points']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33, random_state=42)

###initialize Boruta
forest = RandomForestRegressor(
   n_jobs = -1, 
   max_depth = 7
)
boruta = BorutaPy(
   estimator = forest, 
   n_estimators = 'auto',
   max_iter = 200 # number of trials to perform
)
### fit Boruta (it accepts np.array, not pd.DataFrame)
boruta.fit(np.array(X), np.array(y))
### print results
green_area = X.columns[boruta.support_].to_list()
blue_area = X.columns[boruta.support_weak_].to_list()

df_chosen = df[green_area]


### initialise linear regression for points predicitons
reg = LinearRegression().fit(X_train, y_train)

predictions = reg.predict(X)


m, b = np.polyfit(y, predictions, 1)

bestfit = m*y + b

performance = predictions

#performance = normalise(performance)

fig, axs = plt.subplots(2)
fig.suptitle('Performance')
axs[0].plot(y,predictions ,'x')
axs[0].plot(y, bestfit )
axs[1].hist(performance)

df_chosen['web_name'] = df['web_name'] # this is our dataframe for player stats
df_chosen['performance'] = performance
df_chosen['now_cost'] = df['now_cost']
df_chosen['team'] = slim_elements_df['team']
df_chosen['position'] = slim_elements_df['position']
df_chosen['total_points'] = slim_elements_df['total_points']


##################################################################################################
"""

Sorting Fixtures

"""
##################################################################################################  

fixtures = pd.read_csv('C:/Users/Sam/Documents/Python Projects/FPL BOT/FDR sched.csv')
fixtures = fixtures.rename(columns = {'Gameweek:': 'Team'})

# gameweek = int(input())sdfl;kjh

columns = ['Team','1', '2', '3', '4', '5', 'Difficulty']
index = range(20)
upcoming_fixtures = pd.DataFrame(index = index, columns = columns)

for i in range(5):
    upcoming_fixtures[str(i+1)] = fixtures[str(i+gameweek)]
    
upcoming_fixtures['Team'] = df_chosen['team'].unique()
#upcoming_fixtures['Difficulty'] = normalise(upcoming_fixtures.mean(axis=1))
upcoming_fixtures['Difficulty'] = upcoming_fixtures.mean(axis=1)

dict = {} # creating dictionary

for j in range(len(upcoming_fixtures)):  
    dict.update({upcoming_fixtures['Team'][j]:upcoming_fixtures['Difficulty'][j]})

Fixture_rating = np.zeros(len(df_chosen))

for j in range(len(df_chosen)):
    Fixture_rating[j] = dict.get(df_chosen['team'][j])
    
df_chosen['fixture_rating'] = Fixture_rating
df_chosen['minutes'] = df['minutes']
df_chosen['status'] = slim_elements_df['status']

##################################################################################################
"""

Setting performance things  - "I forgot the word"

"""
##################################################################################################  

df_chosen['Player_Score'] = normalise(df_chosen['fixture_rating'] * df_chosen['performance'])
df_chosen['Predicted_ROI'] = (predictions/(df_chosen['now_cost']))


##################################################################################################    

"""

Josh Bull (last years winner / genius)- Team strategy
                        
                1. 5-6 costly players + cheap fillers over 1-2 costly + mid range 
                2. Bench substitution - players @Home over players @Away. 
                3. Formation is not really a factor (choose best based on your players)
                
                Tranfer strategy
                1. Form over fixtures 
                2. Transfer out underperformer over Transfer in last week's best performer/jumping a bandwagon
                
                Captain strategy
                1. Fixtures over form
                2. If a tie: home over away


"""

##################################################################################################
"""

Picking Best Players within formation

"""
##################################################################################################


possible_players = df_chosen[df_chosen['minutes'] > np.mean(df_chosen['minutes'])] # limiting to players thaty get minutes
possible_players = possible_players[possible_players['status'] == 'a' ] # need to add 'n' to this

possibleGKPS = possible_players[possible_players['position']=='Goalkeeper']
possibleDEFS = possible_players[possible_players['position']=='Defender']
possibleMIDS = possible_players[possible_players['position']=='Midfielder']
possibleFWDS = possible_players[possible_players['position']=='Forward']

initial_team = possible_players.sort_values(by='Player_Score', ascending=False)[0:6] # initial six players
possible_players = possible_players[~possible_players['web_name'].isin(initial_team['web_name'])]

def build_initial(initial_team, possible_players):
    
    team_GKPS = initial_team[initial_team['position']=='Goalkeeper'] # splitting inital team into types of players
    team_DEFS = initial_team[initial_team['position']=='Defender']
    team_MIDS = initial_team[initial_team['position']=='Midfielder']
    team_FWDS = initial_team[initial_team['position']=='Forward']
    
    if (len(initial_team) < 6): 
        next_player = possible_players.sort_values(by='Player_Score', ascending=False).iloc[0]
        next_player = pd.DataFrame(next_player).T
        initial_team = initial_team.append(next_player)
    
    if (len(team_FWDS) > formation[3]):
        dropfwd = team_FWDS.sort_values(by='Player_Score', ascending=True).iloc[0]
        dropfwd = pd.DataFrame(dropfwd).T
        team_FWDS = team_FWDS[~team_FWDS['web_name'].isin(dropfwd['web_name'])]
        initial_team = initial_team[~initial_team['web_name'].isin(dropfwd['web_name'])]       
        
    if (len(team_MIDS) > formation[2]):
        dropmid = team_MIDS.sort_values(by='Player_Score', ascending=True).iloc[0]
        dropmid = pd.DataFrame(dropmid).T
        team_MIDS = team_MIDS[team_MIDS['web_name'].isin(dropmid['web_name'])]
        initial_team = initial_team[~initial_team['web_name'].isin(dropmid['web_name'])]
         
    if (len(team_DEFS) > formation[1]):
        dropdef = team_DEFS.sort_values(by='Player_Score', ascending=True).iloc[0]
        dropdef = pd.DataFrame(dropdef).T
        team_DEFS = team_DEFS[team_DEFS['web_name'].isin(dropdef['web_name'])]
        initial_team = initial_team[~initial_team['web_name'].isin(dropdef['web_name'])]
    
    if (len(team_GKPS) > formation[0]):
        dropgkp = team_GKPS.sort_values(by='Player_Score', ascending=True).iloc[0]
        dropgkp = pd.DataFrame(dropgkp).T
        team_GKPS = team_GKPS[team_GKPS['web_name'].isin(dropgkp['web_name'])]
        initial_team = initial_team[~initial_team['web_name'].isin(dropgkp['web_name'])]
     
    initial_team2 = initial_team
    possible_players2 = possible_players[~possible_players['web_name'].isin(initial_team['web_name'])]       
        
    if ((len(initial_team2) != 6) or (len(team_FWDS) > formation[3]) or (len(team_MIDS) > formation[2]) or (len(team_DEFS) > formation[1]) or (len(team_GKPS) > formation[0])):
        return(build_initial(initial_team2, possible_players2))
    else:
        return(initial_team2)

initial_team = build_initial(initial_team, possible_players)
    

possible_players = possible_players[~possible_players['web_name'].isin(initial_team['web_name'])]
possibleGKPS = possible_players[possible_players['position']=='Goalkeeper']
possibleDEFS = possible_players[possible_players['position']=='Defender']
possibleMIDS = possible_players[possible_players['position']=='Midfielder']
possibleFWDS = possible_players[possible_players['position']=='Forward']
team_GKPS = initial_team[initial_team['position']=='Goalkeeper']
team_DEFS = initial_team[initial_team['position']=='Defender']
team_MIDS = initial_team[initial_team['position']=='Midfielder']
team_FWDS = initial_team[initial_team['position']=='Forward']

if len(team_GKPS) == 0:
    FirstGKP = (possibleGKPS.sort_values(by='Player_Score', ascending=False).iloc[0])
    FirstGKP = pd.DataFrame(FirstGKP).T
    initial_team = initial_team.append(FirstGKP)

possible_players = possible_players[~possible_players['web_name'].isin(initial_team['web_name'])]
possibleGKPS = possible_players[possible_players['position']=='Goalkeeper']
possibleDEFS = possible_players[possible_players['position']=='Defender']
possibleMIDS = possible_players[possible_players['position']=='Midfielder']
possibleFWDS = possible_players[possible_players['position']=='Forward']
team_GKPS = initial_team[initial_team['position']=='Goalkeeper']
team_DEFS = initial_team[initial_team['position']=='Defender']
team_MIDS = initial_team[initial_team['position']=='Midfielder']
team_FWDS = initial_team[initial_team['position']=='Forward']   

remaining_budget = max_budget-initial_team['now_cost'].sum()

##################################################################################################
"""

Picking cheap players to fill bench

"""
##################################################################################################

spots = [2,5,5,3]
bench = [0,0,0,0]

secondary_team = initial_team

for i in range(len(formation)):
    bench[i] = spots[i] - formation[i]

bench_GKP = possibleGKPS.sort_values(by=['now_cost', 'Player_Score'], ascending=(True, False)).iloc[0]
bench_GKP = pd.DataFrame(bench_GKP).T
secondary_team = secondary_team.append(bench_GKP)

bench_DEF = possibleDEFS.sort_values(by=['now_cost', 'Player_Score'], ascending=(True, False)).iloc[0:(bench[1])]
bench_DEF = pd.DataFrame(bench_DEF)
secondary_team = secondary_team.append(bench_DEF)

bench_MID = possibleMIDS.sort_values(by=['now_cost', 'Player_Score'], ascending=(True, False)).iloc[0:(bench[2])]
bench_MID = pd.DataFrame(bench_MID)
secondary_team = secondary_team.append(bench_MID)

bench_FWD = possibleFWDS.sort_values(by=['now_cost', 'Player_Score'], ascending=(True, False)).iloc[0:(bench[3])]
bench_FWD = pd.DataFrame(bench_FWD)
secondary_team = secondary_team.append(bench_FWD)

possible_players = possible_players[~possible_players['web_name'].isin(secondary_team['web_name'])]
possibleGKPS = possible_players[possible_players['position']=='Goalkeeper']
possibleDEFS = possible_players[possible_players['position']=='Defender']
possibleMIDS = possible_players[possible_players['position']=='Midfielder']
possibleFWDS = possible_players[possible_players['position']=='Forward']
team_GKPS = secondary_team[secondary_team['position']=='Goalkeeper']
team_DEFS = secondary_team[secondary_team['position']=='Defender']
team_MIDS = secondary_team[secondary_team['position']=='Midfielder']
team_FWDS = secondary_team[secondary_team['position']=='Forward']

##################################################################################################
"""

Remaining Filler players

"""
##################################################################################################

remaining_budget = max_budget-secondary_team['now_cost'].sum()

def_needed = spots[1] - len(team_DEFS)
mid_needed = spots[2] - len(team_MIDS)
fwd_needed = spots[3] - len(team_FWDS)

final_team = secondary_team

filler_def = possibleDEFS.sort_values(by=['Predicted_ROI'], ascending=(False)).iloc[0:def_needed]
filler_def = pd.DataFrame(filler_def)
final_team = final_team.append(filler_def)

filler_mid = possibleMIDS.sort_values(by=['Predicted_ROI'], ascending=(False)).iloc[0:mid_needed]
filler_mid = pd.DataFrame(filler_mid)
final_team = final_team.append(filler_mid)

filler_fwd = possibleFWDS.sort_values(by=['Predicted_ROI'], ascending=(False)).iloc[0:fwd_needed]
filler_fwd = pd.DataFrame(filler_fwd)
final_team = final_team.append(filler_fwd)

##################################################################################################
"""

Final Checks

"""
##################################################################################################

remaining_budget = max_budget-final_team['now_cost'].sum()
    
teams = final_team['team'].unique()

for team in teams:
    if len(final_team['team'] == team) < 4:
        print('time to fix the team amount', team)
    else:
        print(team, 'is good')
        
if (remaining_budget > 0):
    print('BUDGET IS GOOD', remaining_budget)
else:
    print('time to sort this rather than ignore the budget issue')

    
if len(final_team) == 15:
    print('LETS GO')
    print(final_team.sort_values(by = ['Player_Score'], ascending = False)['web_name'])
else:
    print('check the team')




