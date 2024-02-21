import pandas as pd
from sklearn.model_selection import train_test_split
from keras.models import Sequential
from keras.layers import Dense
from keras.utils import to_categorical
from sklearn.preprocessing import LabelEncoder

# Read and organize data

games_data = pd.read_csv('data\\games.csv')
leagues_data = pd.read_csv('data\\leagues.csv', index_col=0)
players_data = pd.read_csv('data\\players.csv', encoding='ISO-8859-1', index_col=0)
shots_data = pd.read_csv('data\\shots.csv')
teams_data = pd.read_csv('data\\teams.csv', index_col=0)
teamstats_data = pd.read_csv('data\\teamstats.csv', index_col=1)

# Remove extra columns and replace value of location (home or away) to numerical value
features = teamstats_data.drop(['gameID', 'date', 'yellowCards', 'result'], axis=1).replace({'location':{'h':1,'a':0}})

label_encoder = LabelEncoder().fit_transform(teamstats_data["result"])
label = to_categorical(label_encoder)

x_train, x_test, y_train, y_test = train_test_split(features, label, test_size=0.4, random_state=42)

# Create model - https://github.com/somaye7/somaye7-FootballGameResultPrediction

model = Sequential()
model.add(Dense(16, activation='relu'))
model.add(Dense(16, activation='relu'))
model.add(Dense(16, activation='relu'))
model.add(Dense(3, activation='softmax'))

# Compile model
model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

# Train model
model.fit(x_train, y_train, epochs=9, batch_size=18)

test_loss, test_acc = model.evaluate(x_test, y_test)
