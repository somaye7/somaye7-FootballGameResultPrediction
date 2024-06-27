import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sb
from sklearn.preprocessing import LabelEncoder
# from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.model_selection import train_test_split, RandomizedSearchCV
from keras.models import Sequential
from keras.layers import Dense
from keras.utils import to_categorical
import streamlit as st
import plots

# Project title
st.title("Football Games Result Prediction")
st.subheader("Game statistics of the top 5 Leagues from 2014 to 2020")

# Read data
games_data = pd.read_csv('data\\games.csv')
leagues_data = pd.read_csv('data\\leagues.csv')
players_data = pd.read_csv('data\\players.csv', encoding='ISO-8859-1', index_col=0)
shots_data = pd.read_csv('data\\shots.csv')
teams_data = pd.read_csv('data\\teams.csv', index_col=0)
teamstats_data = pd.read_csv('data\\teamstats.csv')

# Convert 'location' to numeric
teamstats_data['location'] = teamstats_data['location'].map({'h': 0, 'a': 1})

# Organize different parts in Streamlit for presentation
dataTab, chartTab, analysisTab = st.tabs(['Data Information📅', 'Charts📊', 'Analysis📈'])
with dataTab:
    # show some information about the dataset used for the project
    # st.header('Data Information')
    st.subheader('Leagues Information')
    st.write(leagues_data, leagues_data.describe())

    st.subheader('\nTeams Information')
    st.write(teams_data, teams_data.describe())

    st.subheader('\nShots Information')
    st.write(shots_data.head(5), shots_data.describe())

    st.subheader('\nTeam statistics for each game')
    st.write(teamstats_data.head(5), teamstats_data.describe())

    st.subheader('\nCorrelation between features')
    feature = teamstats_data.drop(['gameID', 'date'], axis=1)
    # feature['location'] = feature['location'].map({'h': 1, 'a': 0})
    feature['result'] = feature['result'].map({'W': 1, 'D': 0, 'L': -1})
    fig, ax = plt.subplots()
    sb.heatmap(feature.corr(), ax=ax)
    st.pyplot(fig)

    st.subheader('\nChecking null values and filling them')
    st.write('\n Checking null values of teams statistics')
    st.table(teamstats_data.isnull().sum())
    # fill the null value with mean of that column
    teamstats_data['yellowCards'].fillna(teamstats_data['yellowCards'].mean(), inplace=True)

    st.write('\n Checking null values of shots tables')
    st.table(shots_data.isnull().sum())

with chartTab:
    st.subheader('Total goals and expected goals for each leagues from 2014 to 2020')
    st.expander('1: Premier League,2: Serie A,3: Bundesliga, 4: La Liga,5: Ligue 1')
    selected_league = st.selectbox('Choose the league', leagues_data['leagueID'])
    plots.comparisonLeaguesByGoals(selected_league)

    st.subheader('Position of Cristiano Ronaldo\t''s shots in the selected season')
    selected_season = st.selectbox('Choose the season: ', teamstats_data['season'].unique())
    plots.shotsPosition(selected_season, 2371)

with analysisTab:
    st.subheader('Deep learingn model is used for this project')
    st.write(
        'As you can see team statistic table, I used useful features to predict the result of game in 3 classes: Wins, Losses, Draws')
    st.subheader('\nTeam statistics for each game')
    st.write(teamstats_data.head(5))
    # Preprocessing data

    # Encode the 'result' column
    teamstats_data['result'] = LabelEncoder().fit_transform(teamstats_data['result'])

    # Drop columns that are not useful for modeling & Separate features and target
    features = teamstats_data.drop(['gameID', 'teamID', 'season', 'date', 'ppda', 'fouls', 'result'], axis=1)
    label = to_categorical(teamstats_data['result'])

    # Split the data into training and testing sets
    st.subheader('Splitting data and allocating 20 percents of data to test')
    x_train, x_test, y_train, y_test = train_test_split(features, label, test_size=0.2, random_state=42)
    st.write('\nTraining data shape : ', x_train.shape, y_train.shape)
    st.write('\nTesting data shape : ', x_test.shape, y_test.shape)

    # Create model
    model = Sequential()
    model.add(Dense(9, activation='relu'))
    model.add(Dense(16, activation='relu'))
    model.add(Dense(16, activation='relu'))
    model.add(Dense(16, activation='relu'))
    model.add(Dense(3, activation='softmax'))

    # Compile model
    model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

    # Train model & predict
    model.fit(x_train, y_train, epochs=24, batch_size=64)
    test_loss, test_acc = model.evaluate(x_test, y_test)
    st.write("Accuracy of model:", test_acc * 100)
    st.write("Loss of model:", test_loss)
    # predict = model.predict(x_test)
