from nba_api.stats.endpoints import PlayerGameLogs, TeamGameLogs
from nba_api.stats.static import players, teams
import pandas as pd
import re

def statsVsSpecificTeam(playerName):
    # Use player name to get their ID, raises value error for player not found 
    def getPlayerIdByName(playerName):
        nbaPlayers = players.get_players()
        playerInfo = next((player for player in nbaPlayers if player['full_name'].lower() == playerName.lower()), None)
    
        if playerInfo:
            return playerInfo['id']
        else:
            raise ValueError(f"Player with name '{playerName}' not found.")

    # Find full teams name by their nickname (Ex. Celtics -> Boston Celtics, Heat -> Miami Heat)
    def findTeamsByNickname(teamName):
        nbaTeams = teams.get_teams()
        matchingTeams = [team for team in nbaTeams if teamName.lower() in team['nickname'].lower()]
        while not matchingTeams:
            teamName = input("Enter Opposing Team: ")
            #raise ValueError(f"Team with name '{teamName}' not found.")
        return matchingTeams
    # Checks if each season inputted reflects 20XX-XX format
    def validateEachSeason(season):
        pattern = re.compile(r'^20\d{2}-\d{2}$')
        return bool(re.match(pattern, season))
    
    # Checks multiple seasons if inputted
    def validateSeasonsFormat(seasonList):

        # Validate each season in the list
        for season in seasonList:
            if not validateEachSeason(season):
                raise ValueError(f"Invalid season format. Please use the format 20XX-XX for {season}.")
        return True

    #Gather all inputs and validate them
    allSeasonsData = []
    playerId = getPlayerIdByName(playerName)
    teamName = input("Enter Opposing Team: ")
    matchingTeams = findTeamsByNickname(teamName)
    seasons = input("Enter Seasons(20XX-XX): ")
    seasons = seasons.split(',')
    seasonList = [season.strip() for season in seasons]
    validateSeasonsFormat(seasonList)

    #Ensure team entered is valid
    if len(matchingTeams) > 0:
        teamId = matchingTeams[0]['id']
    else:
        raise ValueError(f"No teams found with the nickname '{teamName}'.")

    #Gather stats for each season inputted
    for season in seasonList:
        playerVSTeam = PlayerGameLogs(player_id_nullable=playerId, opp_team_id_nullable=teamId, season_nullable=season)
        playerLogsDF = playerVSTeam.get_data_frames()[0]
        statsColumns = ['GAME_DATE', 'MIN', 'PTS', 'REB', 'AST', 'STL', 'BLK', 'FGM', 'FGA', 'FG_PCT', "FG3M", "FG3A", "FG3_PCT", 'FTM', 'FTA', 'FT_PCT']
        filteredPlayerLogsDF = playerLogsDF[statsColumns]
        filteredPlayerLogsDF.loc[:, 'GAME_DATE'] = pd.to_datetime(filteredPlayerLogsDF['GAME_DATE']).dt.date
        if filteredPlayerLogsDF.empty:
            print(f"\nNo data available for {playerName.upper()} against {teamName.upper()} in the {season} season.\n")
        else:
            print(f"\n{playerName.upper()} stats vs {teamName.upper()} for the {season} season:")
            print(f"{filteredPlayerLogsDF}")
            allSeasonsData.append(filteredPlayerLogsDF)
    #Combine all season stats together
    if allSeasonsData:
        mergedData = pd.concat(allSeasonsData, ignore_index=True)
        return mergedData
    else:
        return filteredPlayerLogsDF