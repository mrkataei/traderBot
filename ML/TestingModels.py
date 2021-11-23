import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import pandas_datareader as web
import datetime as dt
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.layers import Dense, Dropout, LSTM
from tensorflow.keras.models import Sequential

#%%

name='ETHUSDT4h'


data = pd.read_csv('Static/'+name+'.csv')

data.head()


# data = data.values
X = data[['open', 'high', 'low', 'volume']]
Y = data[['close']]
X = X.values
Y = Y.values
prediction_days = 60


x_saeid = []
y_saeid = []
for x in range(prediction_days, len(data)):

  x_saeid.append(X[x - prediction_days : x , : ])
  y_saeid.append(Y[x , : ])

#%%
print(np.shape(x_saeid))
print(np.shape(y_saeid))
#%%
# X = data[['open', 'high', 'low', 'volume']].values
# y = data[['close']].values

# x_train, y_train = np.array(x_train), np.array(y_train)
# x_train = np.reshape(x_train, (x_train.shape[0], x_train.shape[1], 1))
#%%
# Splitting the dataset into the Training set and Test set
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(x_saeid, y_saeid, test_size = 0.2, random_state = 1)


# Feature Scaling
from sklearn.preprocessing import StandardScaler
sc = StandardScaler()
X_train = sc.fit_transform(X_train)
X_test = sc.transform(X_test)
#%%

np.shape(X_train)

#%%

X_train = np.reshape(X_train, (len(X_train), 1, X_train.shape[1]))
X_test = np.reshape(X_test, (len(X_test), 1, X_test.shape[1]))
np.shape(X_train)
#%%



model = Sequential()

model.add(LSTM(units = 50, return_sequences = True, input_shape = (60, 4)))
model.add(Dropout(0.2))
model.add(LSTM(units = 50, return_sequences = True))
model.add(Dropout(0.2))
model.add(LSTM(units = 50))
model.add(Dropout(0.2))
model.add(Dense(units = 1))

model.compile(optimizer = 'adam', loss = 'mean_squared_error')
model.fit(x_saeid, y_saeid, epochs= 25 , batch_size = 32)
