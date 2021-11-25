import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import pandas_datareader as web
import datetime as dt

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.layers import Dense, Dropout, LSTM
from tensorflow.keras.models import Sequential
from sklearn import preprocessing

from tensorflow.python.keras import Input
from tensorflow.python.keras.layers import BatchNormalization

name='ETHUSDT4h'


data = pd.read_csv('Static/'+name+'.csv')

data.head()


# data = data.values
# X = data[['open', 'high', 'low', 'volume']]
#SPLIT DATA INTO TEST AND TRAIN
# np.random.seed(7)



data.sort_values(by=['date'],ascending=[True],inplace=True)
data.head(10)

#%%
#X = data[['open', 'high', 'low', 'volume', 'close']]
X = data[['high', 'low', 'volume', 'close']]
Y = data[['close']]
#X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.3, shuffle = False)


#NORMALIZATION
f_transformer = preprocessing.MinMaxScaler((-1, 1))
f_transformer = f_transformer.fit(X)
#X_train_trans = f_transformer.transform(X_train)
#X_test_trans = f_transformer.transform(X_test)

cnt_transformer = preprocessing.MinMaxScaler((0, 1))
cnt_transformer = cnt_transformer.fit(Y)
#y_train_trans = cnt_transformer.transform(y_train)
#y_test_trans = cnt_transformer.transform(y_test)

X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.2, shuffle = False)

X_train_trans = f_transformer.transform(X_train)
X_test_trans = f_transformer.transform(X_test)

y_train_trans = cnt_transformer.transform(y_train)
y_test_trans = cnt_transformer.transform(y_test)

#dump(f_transformer, '//Users//saad//Desktop//Bitcoin LSTM//minmax_scalar_x.bin', compress=True)
#dump(cnt_transformer, '//Users//saad//Desktop//Bitcoin LSTM//minmax_scalar_y.bin', compress=True)

print("*** SHAPES")
print("X_train: %s, %s" % (X_train.shape[0],X_train.shape[1]))
print("X_test: %s, %s" % (X_test.shape[0],X_test.shape[1]))
print("y_train: %s, %s" % (y_train.shape[0],y_train.shape[1]))
print("y_test: %s, %s" % (y_test.shape[0],y_test.shape[1]))

print("\n*** MIN MAX")

print("TRAIN COST: %d, %d" % (X_train.close.min(), X_train.close.max()))
print("TEST COST: %d, %d" % (X_test.close.min(), X_test.close.max()))
print("TRAIN VOL: %d, %d" % (X_train['volume'].min(), X_train['volume'].max()))
print("TEST VOL: %d, %d" % (X_test['volume'].min(), X_test['volume'].max()))

print("\n*** MIN MAX PARAMETER")
print(f_transformer.data_min_)
print(f_transformer.data_max_)
print(cnt_transformer.data_min_)
print(cnt_transformer.data_max_)


#CREATE LAGGING DATASET FOR TIMESERIES
def create_dataset(X, y, time_steps=1):
    Xs, ys = [], []
    for i in range(len(X) - time_steps):
        v = X[i:(i + time_steps)]
        Xs.append(v)
        ys.append(y[i + time_steps])
    return np.array(Xs), np.array(ys)

time_steps = 48
# reshape to [samples, time_steps, n_features]
X_train_f, y_train_f = create_dataset(X_train_trans, y_train_trans, time_steps)
X_test_f, y_test_f = create_dataset(X_test_trans, y_test_trans, time_steps)

print("*** SHAPES")
print(X_train_f.shape, y_train_f.shape)
print(X_test_f.shape, y_test_f.shape)
#print(X_train_trans.shape, y_train_trans.shape)
#print(X_test_trans.shape, y_test_trans.shape)

#%%
model = Sequential()
model.add(Input(shape=((X_train_f.shape[1], X_train_f.shape[2]))))
#model.add(layers.Bidirectional(layers.LSTM(300, activation = 'tanh', return_sequences=False)))
#model.add(layers.LSTM(300, return_sequences=False, activation = 'tanh'))
model.add(LSTM(300, return_sequences=False, activation = 'tanh'))
# model.add(Dropout(0.4))
# model.add(LSTM(200, return_sequences=True))
# model.add(Dropout(0.4))
# model.add(LSTM(100, return_sequences=True))
# model.add(Dropout(0.4))
# model.add(LSTM(50))
# model.add(Dropout(0.4))
# model.add(Dropout(0.2))
# model.add(BatchNormalization())
#model.add(layers.Bidirectional(layers.LSTM(120,activation='relu', return_sequences=True)))
#model.add(keras.layers.Dropout(rate=0.2))
#model.add(layers.Flatten())
#model.add(keras.layers.Dense(units=10, activation = 'relu'))

# model.add(LSTM(50, return_sequences=True, activation = 'tanh'))
# model.add(Dropout(0.2))
# model.add(LSTM(50, return_sequences=True, activation = 'tanh'))
# model.add(Dropout(0.2))
# model.add(LSTM(50, activation = 'tanh'))

model.add(Dense(units=1))
model.compile(loss='mean_squared_error', optimizer='adam')
# model.compile(loss='mean_squared_error', optimizer='adam', metrics=['accuracy'])
model.summary()

# model = Sequential()
#
# model.add(LSTM(units = 50, return_sequences = True, input_shape = (60, 4)))
# model.add(Dropout(0.2))
# model.add(LSTM(units = 50, return_sequences = True))
# model.add(Dropout(0.2))
# model.add(LSTM(units = 50))
# model.add(Dropout(0.2))
# model.add(Dense(units = 1))
#
# model.compile(optimizer = 'adam', loss = 'mean_squared_error')
# model.fit(x_saeid, y_saeid, epochs= 25 , batch_size = 32)

hist = model.fit(X_train_f, y_train_f, batch_size = 200, epochs = 150, shuffle=False, validation_split=0.1)

import math

y_pred = model.predict(X_test_f)

y_test_inv = cnt_transformer.inverse_transform(y_test_f)
y_pred_inv = cnt_transformer.inverse_transform(y_pred)
combined_array = np.concatenate((y_test_inv,y_pred_inv),axis=1)
combined_array2 = np.concatenate((X_test.iloc[time_steps:],combined_array),axis=1)

df_final = pd.DataFrame(data = combined_array, columns=["actual", "predicted"])
print("size: %d" % (len(combined_array)))
df_final

#%%

from sklearn.metrics import accuracy_score
from sklearn.metrics import mean_squared_error

results = model.evaluate(X_test_f, y_test_f)
print("mse: %s" % (mean_squared_error(y_test_inv, y_pred_inv)))
print(results)
# print(accuracy_score(y_test_inv, y_pred_inv))

#%%
print(np.shape(y_test_inv))
print(np.shape(y_pred_inv))