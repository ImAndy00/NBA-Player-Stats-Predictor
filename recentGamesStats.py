from nba_api.stats.endpoints import PlayerGameLogs, TeamGameLogs
from nba_api.stats.static import players
import pandas as pd
from datetime import datetime

#Get player ID
def getPlayerIdByName(playerName):
        nbaPlayers = players.get_players()
        playerInfo = next((player for player in nbaPlayers if player['full_name'].lower() == playerName.lower()), None)
    
        if playerInfo:
            return playerInfo['id']
        else:
            raise ValueError(f"Player with name '{playerName}' not found.")

#Get today's date for recent games
def getCurrentDate():
    return datetime.now().strftime('%m/%d/%Y')

#Gather 7 most recent games of a player ("Only including 7 recent games they logged minutes")
def recentGameStats(playerName):
    playerId = getPlayerIdByName(playerName)
    currDate = getCurrentDate()
    recentGames = PlayerGameLogs(player_id_nullable=playerId, season_nullable='2023-24', date_to_nullable=currDate)
    playerLogsDF = recentGames.get_data_frames()[0]
    playerLogsDF = playerLogsDF.sort_values(by='GAME_DATE', ascending=False).head(7)
    statsColumns = ['GAME_DATE', 'MIN', 'PTS', 'REB', 'AST', 'STL', 'BLK', 'FGM', 'FGA', 'FG_PCT', "FG3M", "FG3A", "FG3_PCT", 'FTM', 'FTA', 'FT_PCT']
    filteredPlayerLogsDF = playerLogsDF[statsColumns]
    filteredPlayerLogsDF.loc[:, 'GAME_DATE'] = pd.to_datetime(filteredPlayerLogsDF['GAME_DATE']).dt.date
    print(f"\n{playerName.upper()} 7 most recent games:")
    print(filteredPlayerLogsDF)
    return filteredPlayerLogsDF
