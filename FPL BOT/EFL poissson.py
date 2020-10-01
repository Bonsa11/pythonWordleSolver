# -*- coding: utf-8 -*-
"""
Created on Wed Sep  2 17:12:32 2020

@author: Sam
"""

# packages
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# importing data
df_results = pd.read_csv('C:/Users/Sam/Documents/Python Projects/FPL BOT/results.csv')
df_results.head(3)

df_stats = pd.read_csv('C:/Users/Sam/Documents/Python Projects/FPL BOT/stats.csv')
df_stats.head(3)

# showing unique values in all columns
cols = df_results.columns
for col in cols:
    print(col,df_results[col].unique())
    print('')


# comparing home vs away goals
sum_home = df_results['home_goals'].sum()
sum_away = df_results['away_goals'].sum()

print(df_results[df_results['season']=='2006-2007']['home_goals'].sum())
    
sns.distplot(df_results['home_goals'], kde=False, color = 'blue', label = 'home goals')
sns.distplot(df_results['away_goals'], kde=False, color = 'red', label = 'away goals')
plt.legend(prop={'size': 12})
plt.title('Home vs Away Goals 08-18')
plt.xlabel('Goals Scored')
plt.ylabel('Density')

# spliiting into seasons
season17_18_results = df_results[df_results['season'] == '2017-2018'] 
season16_17_results = df_results[df_results['season'] == '2016-2017']
season15_16_results = df_results[df_results['season'] == '2015-2016']
season14_15_results = df_results[df_results['season'] == '2014-2015']
season13_14_results = df_results[df_results['season'] == '2013-2014']

season17_18_stats = df_stats[df_stats['season'] == '2017-2018'] 
season16_17_stats = df_stats[df_stats['season'] == '2016-2017']
season15_16_stats = df_stats[df_stats['season'] == '2015-2016']
season14_15_stats = df_stats[df_stats['season'] == '2014-2015']
season13_14_stats = df_stats[df_stats['season'] == '2013-2014']

goals_per_season_home = [0] * len(df_results['season'].unique())
goals_per_season_away = [0] * len(df_results['season'].unique())

seasons = df_results['season'].unique()

for i in range(len(seasons)):
    goals_per_season_home[i] = df_results[df_results['season']== seasons[i]]['home_goals'].sum()
    goals_per_season_away[i] = df_results[df_results['season']== seasons[i]]['away_goals'].sum()

goals_tracker = [seasons,goals_per_season_home,goals_per_season_away]
goals_tracker = pd.DataFrame(goals_tracker)
goals_tracker = goals_tracker.T
goals_tracker = goals_tracker.rename({0:'season', 1:'goals_at_home', 2:'goals_away'}, axis='columns')

sns.stripplot(x=goals_tracker['season'], y=goals_tracker['goals_at_home'], color = 'blue')
sns.stripplot(x=goals_tracker['season'], y=goals_tracker['goals_away'], color = 'red')
plt.legend(prop={'size': 12})
plt.title('Home vs Away Goals 08-18')
plt.xlabel('Goals Scored')
plt.ylabel('Density')