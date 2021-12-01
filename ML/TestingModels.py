import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import pandas_datareader as web
import datetime as dt
import pandas_ta as ta

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.layers import Dense, Dropout, LSTM, GRU
from tensorflow.keras.models import Sequential
from sklearn import preprocessing

from tensorflow.python.keras import Input



import random
random.seed(42)
import numpy
numpy.random.seed(42)
import tensorflow as tf
tf.random.set_seed(42)



def correlation(dataset, threshold):
    col_corr = set()  # Set of all the names of correlated columns
    corr_matrix = dataset.corr()
    for i in range(len(corr_matrix.columns)):
        for j in range(i):
            if abs(corr_matrix.iloc[i, j]) > threshold: # we are interested in absolute coeff value
                colname = corr_matrix.columns[i]  # getting the name of column
                col_corr.add(colname)
    return col_corr




name='ETHUSDT4h'


data = pd.read_csv('Static/'+name+'.csv')

data.head()






data['hl2'] = (ta.hl2(high=data['high'], low=data['low'])).values
data['hlc3'] = (ta.hlc3(high=data['high'], low=data['low'], close=data['close'])).values
data['ohlc4'] = (ta.ohlc4(high=data['high'], low=data['low'], close=data['close'],open_=data['open'])).values

korosh = ta.macd(data['hl2'])
data['hl2_MD'] = korosh['MACD_12_26_9']
data['hl2_MDh'] = korosh['MACDh_12_26_9']
data['hl2_MDs'] = korosh['MACDs_12_26_9']


korosh = ta.macd(data['hlc3'])
data['hlc3_MD'] = korosh['MACD_12_26_9']
data['hlc3_MDh'] = korosh['MACDh_12_26_9']
data['hlc3_MDs'] = korosh['MACDs_12_26_9']



korosh = ta.macd(data['ohlc4'])
data['ohlc4_MD'] = korosh['MACD_12_26_9']
data['ohlc4_MDh'] = korosh['MACDh_12_26_9']
data['ohlc4_MDs'] = korosh['MACDs_12_26_9']

data=data.dropna()
data = data.reset_index(drop=True)



data.sort_values(by=['date'],ascending=[True],inplace=True)
data.head(10)
#%%
sns.heatmap(data.corr(), annot=True, cmap='RdYlGn', linewidths=0.1, vmin=0)
plt.show()

#%%

data = data.drop(['date' , 'open', 'low', 'high'] , axis =1)
Y = data[['close']]


# from matplotlib.pyplot import figure
#
# figure(figsize=(10, 8))
# sns.heatmap(X.corr(), annot=True, cmap='RdYlGn', linewidths=0.1, vmin=0)
# plt.show()

corr_features = correlation(data, 0.85)
X = data.drop(corr_features,axis=1)



X = X.iloc[: , :].values
Y = Y.iloc[: , :].values


#%%
f_transformer = preprocessing.MinMaxScaler((-1, 1))
f_transformer = f_transformer.fit(X)
X = f_transformer.transform(X)

cnt_transformer = preprocessing.MinMaxScaler((-1, 1))
cnt_transformer = cnt_transformer.fit(Y)
Y = cnt_transformer.transform(Y)


X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.2, shuffle = False)

#dump(f_transformer, '//Users//saad//Desktop//Bitcoin LSTM//minmax_scalar_x.bin', compress=True)
#dump(cnt_transformer, '//Users//saad//Desktop//Bitcoin LSTM//minmax_scalar_y.bin', compress=True)




#CREATE LAGGING DATASET FOR TIMESERIES
def create_dataset(X, y, time_steps=1):
    Xs, ys = [], []
    for i in range(len(X) - time_steps):
        v = X[i:(i + time_steps)]
        Xs.append(v)
        ys.append(y[i + time_steps])
    return np.array(Xs), np.array(ys)

time_steps = 90
# reshape to [samples, time_steps, n_features]



X_train_f, y_train_f = create_dataset(X_train, y_train, time_steps)
X_test_f, y_test_f = create_dataset(X_test, y_test, time_steps)

print("*** SHAPES")
print(X_train_f.shape, y_train_f.shape)
print(X_test_f.shape, y_test_f.shape)
#print(X_train_trans.shape, y_train_trans.shape)
#print(X_test_trans.shape, y_test_trans.shape)

#%%


model = Sequential()
model.add(Input(shape=((X_train_f.shape[1], X_train_f.shape[2]))))
# model.add(GRU(90, return_sequences=True, activation = 'tanh'))
model.add(GRU(300, return_sequences=False, activation = 'tanh'))
model.add(Dense(units=1 ,activation='linear'))
model.compile(loss='mean_squared_error', optimizer='SGD')








model.summary()



hist = model.fit(X_train_f, y_train_f, batch_size = 64, epochs = 1000, shuffle=False)

#%%
y_pred = model.predict(X_test_f)

y_test_inv = cnt_transformer.inverse_transform(y_test_f)
y_pred_inv = cnt_transformer.inverse_transform(y_pred)
combined_array = np.concatenate((y_test_inv,y_pred_inv),axis=1)
combined_array2 = np.concatenate((X_test[time_steps:],combined_array),axis=1)

df_final = pd.DataFrame(data = combined_array, columns=["actual", "predicted"])
print("size: %d" % (len(combined_array)))
df_final



from sklearn.metrics import accuracy_score
from sklearn.metrics import mean_squared_error

results = model.evaluate(X_test_f, y_test_f)
print("mse: %s" % (mean_squared_error(y_test_inv, y_pred_inv)))
print(results)
# print(accuracy_score(y_test_inv, y_pred_inv))

#%%


#%%
model.save_weights('E:\Work\\5571.h5')
df_final.to_csv('E:\Work\\5571.csv')
print(np.shape(y_test_inv))
print(np.shape(y_pred_inv))