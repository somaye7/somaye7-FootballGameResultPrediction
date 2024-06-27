import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.patches import Arc
import streamlit as st
import helper


# comparison goals and expected goals for each league - in each season
def comparisonLeaguesByGoals(leagueID):
    season = [2014, 2015, 2016, 2017, 2018, 2019, 2020]
    leagues_data = pd.read_csv('data\\leagues.csv', index_col=0)
    totalGoals = helper.totalStatsOfLeaguesBySeason(leagueID, 'goals')
    totalxGoals = helper.totalStatsOfLeaguesBySeason(leagueID, 'xGoals')
    leaguesName = helper.naming(leagueID, 'name', leagues_data)
    fig = plt.figure()
    ax1 = fig.add_subplot(1, 1, 1)
    plt.title(f'total goals and xGoals of {leaguesName}')
    plt.plot(season, totalGoals, label=f'{leaguesName} Goals', color='blue')
    plt.plot(season, totalxGoals, label=f'{leaguesName} XGoals', color='purple')
    plt.xlabel('Season')
    plt.ylabel('Frequency')
    ax1.legend()
    st.pyplot(plt)


# the pitch plot source: https://fcpython.com/visualisation/drawing-pitchmap-adding-lines-circles-matplotlib
def shotsPosition(season, playerID):
    try:
        # Create figure
        fig = plt.figure()
        ax = fig.add_subplot(1, 1, 1)
        plt.title(f'Cristiano Ronaldo Shots in {season}')
        shots_data = pd.read_csv('data\\shots.csv')
        selected_season = helper.gameIDOfEachseason(season)

        # shots of input player for given season
        selected_season_mask = (shots_data['gameID'].isin(selected_season)) & (shots_data['shooterID'] == playerID)
        selected_shots = shots_data[selected_season_mask]

        # blocked shot
        nonGoal = selected_shots[selected_shots['shotResult'] != 'Goal']
        nonGoal_x = nonGoal['positionX'] * 130
        nonGoal_y = nonGoal['positionY'] * 90
        plt.scatter(nonGoal_x, nonGoal_y, label='Missed Shots', color='blue')

        # goal shot
        goal = selected_shots[selected_shots['shotResult'] == 'Goal']
        goal_x = goal['positionX'] * 130
        goal_y = goal['positionY'] * 90
        plt.scatter(goal_x, goal_y, label='Goal', color='green')

        # Pitch Outline & Centre Line
        plt.plot([0, 0], [0, 90], color="black")
        plt.plot([0, 130], [90, 90], color="black")
        plt.plot([130, 130], [90, 0], color="black")
        plt.plot([130, 0], [0, 0], color="black")
        plt.plot([65, 65], [0, 90], color="black")

        # Left Penalty Area
        plt.plot([16.5, 16.5], [65, 25], color="black")
        plt.plot([0, 16.5], [65, 65], color="black")
        plt.plot([16.5, 0], [25, 25], color="black")

        # Right Penalty Area
        plt.plot([130, 113.5], [65, 65], color="black")
        plt.plot([113.5, 113.5], [65, 25], color="black")
        plt.plot([113.5, 130], [25, 25], color="black")

        # Left 6-yard Box
        plt.plot([0, 5.5], [54, 54], color="black")
        plt.plot([5.5, 5.5], [54, 36], color="black")
        plt.plot([5.5, 0.5], [36, 36], color="black")

        # Right 6-yard Box
        plt.plot([130, 124.5], [54, 54], color="black")
        plt.plot([124.5, 124.5], [54, 36], color="black")
        plt.plot([124.5, 130], [36, 36], color="black")

        # Prepare Circles
        centreCircle = plt.Circle((65, 45), 9.15, color="black", fill=False)
        centreSpot = plt.Circle((65, 45), 0.8, color="black")
        leftPenSpot = plt.Circle((11, 45), 0.8, color="black")
        rightPenSpot = plt.Circle((119, 45), 0.8, color="black")

        # Draw Circles
        ax.add_patch(centreCircle)
        ax.add_patch(centreSpot)
        ax.add_patch(leftPenSpot)
        ax.add_patch(rightPenSpot)

        # Prepare Arcs
        leftArc = Arc((11, 45), height=18.3, width=18.3, angle=0, theta1=310, theta2=50, color="black")
        rightArc = Arc((119, 45), height=18.3, width=18.3, angle=0, theta1=130, theta2=230, color="black")

        # Draw Arcs
        ax.add_patch(leftArc)
        ax.add_patch(rightArc)
        ax.legend()
        # Tidy Axes
        # plt.axis('off')
        # Display Pitch
        st.pyplot(plt)
    except:
        st.write("Something went wrong in create function")
