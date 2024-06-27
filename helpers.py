import pandas as pd


def naming(columnId: str, columnName: str, targetTable):
    return targetTable.loc[columnId][columnName]


# calculate sum of numeric values such goals/ xGoals for selected league for each season
def totalStatsOfLeaguesBySeason(leagueID, statsName: str):
    teamstats_data = pd.read_csv('data\\teamstats.csv')
    teamstats_data['result'] = teamstats_data['result'].map({'W': 3, 'L': 0, 'D': 1})
    games_data = pd.read_csv('data\\games.csv')
    leaguesId = games_data[['gameID', 'leagueID']]
    # Concatenating for having League Id for every team game - group by season
    merged = teamstats_data.merge(leaguesId, how='inner', on='gameID')
    teamsOfLeague = merged[(merged['leagueID'] == leagueID)]
    total = []
    for season in [2014, 2015, 2016, 2017, 2018, 2019, 2020]:
        teams = teamsOfLeague[teamsOfLeague['season'] == season]
        total.append(teams[statsName].sum())
    return total


def gameIDOfEachseason(season):
    teamstats_data = pd.read_csv('data\\teamstats.csv')
    specificSeason = (teamstats_data['season'] == season)
    gamesIdOfSeason = teamstats_data[specificSeason]['gameID']
    return gamesIdOfSeason
