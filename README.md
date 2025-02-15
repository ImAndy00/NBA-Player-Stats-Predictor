# NBA-Player-Stats-Predictor
The NBA Player Stats Predictor is a Python-based tool designed to analyze and predict the performance of NBA players in specific statistical categories such as points (PTS), assists (AST), rebounds (REB), three-pointers made (FG3M), steals (STL), and blocks (BLK). The tool leverages historical player data against specific teams and recent game statistics to generate insights into the likelihood of a player surpassing a given statistical threshold in an upcoming game.

How to use:
- Download zip
- Extract files and open folder in IDE (ex. VS Code)
- Download python and pandas if not already installed, "python -m pip install pandas" <- (Windows)
- Download nba_api if not installed, "pip install nba_api"
- Run prediction.py

Usages:
(Enter a Player:) - Enter a players full name, not case sensitive (ex. Lebron James, kevin durant, stephen Curry)
(Enter Opposing Team:) - Enter an NBA teams name, not case sensitive (ex. Heat, cavaliers, celtics)
(Enter Seasons(20XX-XX):) - Enter the seasons you want to see the stats vs the opposing team, can enter multiple seasons seperated by commas (ex. 2021-22, 2022-23, 2023-24)
(Stat:) - Enter PTS, AST, REB, FG3M, STL, or BLK. Multiple stats can be inputted for cases like PTS + AST + REB(comma-seperated). (Ex. Pts, Ast, Reb)
(Stat Prop Line:) - Enter the stat line from sportsbook (Ex. 26.5)

Key Features:
- View last 7 game stats for player
- View stats for specific team matchups for number of seasons entered
- Recieve percentage estimate for player to exceed stat prop line
