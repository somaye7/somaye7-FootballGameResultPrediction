import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import param
import seaborn as sns
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split, RandomizedSearchCV
from sklearn.ensemble import RandomForestClassifier
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
teamstats_data = pd.read_csv('data\\teamstats.csv')

# Remove extra columns and replace value of location (home or away) to numerical value
features = teamstats_data.drop(['gameID', 'date', 'yellowCards', 'result'], axis=1) # .replace({'location':{'h':1,'a':0}})
features = pd.get_dummies(features)
features_columns = list(features.columns)
label_encoder = LabelEncoder().fit_transform(teamstats_data["result"])
label = to_categorical(label_encoder)

x_train, x_test, y_train, y_test = train_test_split(features, label, test_size=0.25, random_state=42)
print('Training data shape : ', x_train.shape, y_train.shape)
print('Testing data shape : ', x_test.shape, y_test.shape)

'''# Find a threshold for measuring prediction acc
threshold_preds = x_test[:, features_columns.index('average')]
baseline_errors = abs(threshold_preds - y_test)
print('Average threshold error: ', round(np.mean(baseline_errors), 2))'''

'''# Create model
model = RandomForestClassifier()
# Train model
model.fit(x_train, y_train)

prediction = model.predict(x_test)
accuracy = accuracy_score(y_test, prediction)
print("Accuracy:", accuracy)
'''
# Create model
model = Sequential()
model.add(Dense(8, activation='relu'))
model.add(Dense(3, activation='softmax'))

# Compile model
model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

# Train model
model.fit(x_train, y_train, epochs=24, batch_size=6)

test_loss, test_acc = model.evaluate(x_test, y_test)
