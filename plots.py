import pandas as pd
import helpers
import matplotlib.pyplot as plt

# 1: total points of teams for each 4 top leagues

y = totalPoints
fig, axs = plt.subplots(2, 2)
axs[0, 0].plot(laligaTeams, y)
axs[0, 0].set_title("La Liga")
axs[1, 0].plot(premierLeagueTeams, y)
axs[1, 0].set_title("Premier League")
axs[1, 0].sharex(axs[0, 0])
axs[0, 1].plot(boundesligaTeams, y)
axs[0, 1].set_title("Bundesliga")
axs[1, 1].plot(serieATeams, y)
axs[1, 1].set_title("Serie A")
fig.tight_layout()



# 6. Position of Shots of Cristiano Ronaldo
shots_data = pd.read_csv('data\\shots.csv')
# cristianoRonaldo_shots =
# helpers.createPitch()