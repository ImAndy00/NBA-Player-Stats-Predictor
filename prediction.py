from recentGamesStats import recentGameStats
from statsVsSpecificTeam import statsVsSpecificTeam

#Get the player
playerName = input("Enter a Player: ")

#Call other files functions to get both data
dataVsTeam = statsVsSpecificTeam(playerName)
recentData = recentGameStats(playerName)

#Gather stat(s) and ensure they are valid
stats = input("\nStat(PTS, AST, REB, FG3M, STL, BLK): ").upper()
stats = stats.split(',')
statList = [stat.strip() for stat in stats]
validStats = ['PTS', 'AST', 'REB', 'FG3M', 'STL', 'BLK']
for stat in statList:
    if stat not in validStats:
        raise ValueError("Entered stat is not valid")
        #stat = input("Stat(PTS, AST, REB, FG3M, STL, BLK): ").upper()

#Input combination of all stats entered into Total column
dataVsTeam['Total'] = dataVsTeam[statList].sum(axis=1)
recentData['Total'] = recentData[statList].sum(axis=1)

#Store these totals in a variable
statsVsTeam = dataVsTeam['Total']
statsRecent = recentData['Total']

# User input for prop line
threshold = float(input("Stat Prop Line: "))

# Define stat ranges (for calculations if player got close to line in previous games)
statRanges = {'PTS': 15, 'AST': 5, 'REB': 5, 'FG3M': 3, 'STL': 1, 'BLK': 1}
statRange = sum(statRanges.get(stat, 1) for stat in statList)

# Count the number of games where total is equal to or greater than the threshold, also include games that came close (with in a range)
recentProb = sum(1 if total > threshold else 0.4 if total + 0.2 * statRange > threshold else 0 for total in statsRecent) / len(statsRecent)
teamsLength = len(statsVsTeam)

#If no data vs team, only consider recent games
if statsVsTeam.empty:
    weightRecent = 1.00
    overallProb = (weightRecent * recentProb)
else:
    #Get weight of statsVsTeam by considering how many games have been played against the team
    weightHistorical = teamsLength / 11.5
    weightRecent = 1 - weightHistorical
    historicalProb = sum(1 if total > threshold else 0.4 if total + 0.2 * statRange > threshold else 0 for total in statsVsTeam) / len(statsVsTeam)
    overallProb = (weightHistorical * historicalProb) + (weightRecent * recentProb)
statDisplay = ' + '.join(statList)
print(f"\nOverall probability of exceeding {threshold} {statDisplay}: {overallProb * 100:.2f}%")