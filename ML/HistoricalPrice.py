import numpy as np
# from numpy.core.numeric import NaN
import pandas as pd
# import plotly.graph_objects as go
# from plotly.subplots import make_subplots
import tensorflow as tf
from tensorflow.keras import *
from tensorflow.keras.layers import *
import matplotlib.pyplot as plt

plt.style.use('seaborn')
IBM_path = 'Static/IBM.csv'
df = pd.read_csv(IBM_path, delimiter=',', usecols=['Date', 'Open', 'High', 'Low', 'Close', 'Volume'])


# based on https://towardsdatascience.com/the-beginning-of-a-deep-learning-trading-bot-part1-95-accuracy-is-not-enough-c338abc98fc2
def preprocess(data: pd.DataFrame):
    data['Date'] = pd.to_datetime(data['Date'])
    return data


# def plot_historical(data:pd.DataFrame):
#     fig = make_subplots(specs=[[{"secondary_y": True}]])
#     fig.add_trace(go.Candlestick(x=data['Date'], open=data['Open'], high=data['High'], low=data['Low'], close=data['Close']),
#                   secondary_y=False)
#     fig.show()
class CNN:
    def __init__(self):
        pass

    def A(self, layer_in, filter):
        branch1x1 = Conv1D(filter, kernel_size=1, padding="same", use_bias=False, activation='relu')(layer_in)

        branch5x5 = Conv1D(filter, kernel_size=1, padding='same', use_bias=False, activation='relu')(layer_in)
        branch5x5 = Conv1D(filter, kernel_size=5, padding='same', use_bias=False, activation='relu')(branch5x5)

        branch3x3 = Conv1D(filter, kernel_size=1, padding='same', use_bias=False, activation='relu')(layer_in)
        branch3x3 = Conv1D(filter, kernel_size=3, padding='same', use_bias=False, activation='relu')(branch3x3)
        branch3x3 = Conv1D(filter, kernel_size=3, padding='same', use_bias=False, activation='relu')(branch3x3)

        branch_pool = AveragePooling1D(pool_size=(3), strides=1, padding='same')(layer_in)
        branch_pool = Conv1D(filter, kernel_size=1, padding='same', use_bias=False, activation='relu')(branch_pool)

        outputs = Concatenate(axis=-1)([branch1x1, branch5x5, branch3x3, branch_pool])
        return outputs

    def B(self, layer_in, filter):
        branch3x3 = Conv1D(filter, kernel_size=3, padding="same", strides=2, use_bias=False, activation='relu')(
            layer_in)

        branch3x3dbl = Conv1D(filter, kernel_size=1, padding="same", use_bias=False, activation='relu')(layer_in)

        branch3x3dbl = Conv1D(filter, kernel_size=3, padding="same", use_bias=False, activation='relu')(branch3x3dbl)

        branch3x3dbl = Conv1D(filter, kernel_size=3, padding="same", strides=2, use_bias=False, activation='relu')(
            branch3x3dbl)

        branch_pool = MaxPooling1D(pool_size=3, strides=2, padding="same")(layer_in)

        outputs = Concatenate(axis=-1)([branch3x3, branch3x3dbl, branch_pool])
        return outputs

    def C(self, layer_in, filter):
        branch1x1_1 = Conv1D(filter, kernel_size=1, padding="same", use_bias=False)(layer_in)
        branch1x1 = BatchNormalization()(branch1x1_1)
        branch1x1 = ReLU()(branch1x1)

        branch7x7_1 = Conv1D(filter, kernel_size=1, padding="same", use_bias=False)(layer_in)
        branch7x7 = BatchNormalization()(branch7x7_1)
        branch7x7 = ReLU()(branch7x7)
        branch7x7 = Conv1D(filter, kernel_size=(7), padding="same", use_bias=False)(branch7x7)
        branch7x7 = BatchNormalization()(branch7x7)
        branch7x7 = ReLU()(branch7x7)
        branch7x7 = Conv1D(filter, kernel_size=(1), padding="same", use_bias=False)(branch7x7)
        branch7x7 = BatchNormalization()(branch7x7)
        branch7x7 = ReLU()(branch7x7)

        branch7x7dbl_1 = Conv1D(filter, kernel_size=1, padding="same", use_bias=False)(layer_in)
        branch7x7dbl = BatchNormalization()(branch7x7dbl_1)
        branch7x7dbl = ReLU()(branch7x7dbl)
        branch7x7dbl = Conv1D(filter, kernel_size=(7), padding="same", use_bias=False)(branch7x7dbl)
        branch7x7dbl = BatchNormalization()(branch7x7dbl)
        branch7x7dbl = ReLU()(branch7x7dbl)
        branch7x7dbl = Conv1D(filter, kernel_size=(1), padding="same", use_bias=False)(branch7x7dbl)
        branch7x7dbl = BatchNormalization()(branch7x7dbl)
        branch7x7dbl = ReLU()(branch7x7dbl)
        branch7x7dbl = Conv1D(filter, kernel_size=(7), padding="same", use_bias=False)(branch7x7dbl)
        branch7x7dbl = BatchNormalization()(branch7x7dbl)
        branch7x7dbl = ReLU()(branch7x7dbl)
        branch7x7dbl = Conv1D(filter, kernel_size=(1), padding="same", use_bias=False)(branch7x7dbl)
        branch7x7dbl = BatchNormalization()(branch7x7dbl)
        branch7x7dbl = ReLU()(branch7x7dbl)

        branch_pool = AveragePooling1D(pool_size=3, strides=1, padding='same')(layer_in)
        branch_pool = Conv1D(filter, kernel_size=1, padding='same', use_bias=False)(branch_pool)
        branch_pool = BatchNormalization()(branch_pool)
        branch_pool = ReLU()(branch_pool)

        outputs = Concatenate(axis=-1)([branch1x1, branch7x7, branch7x7dbl, branch_pool])
        return outputs


class ML:
    __data = None
    __train = None
    __valid = None
    __test = None
    __model = None
    __callback = None
    X_train, y_train = None, None
    X_val, y_val = None, None
    X_test, y_test = None, None

    def __init__(self, data: pd.DataFrame, model=None, seq_len: int = 128, timefram: int = 1):
        self.seq_len = seq_len
        self.timefram = timefram
        self.__model = model
        self.__data = preprocess(data)
        self.__preprocess(timeframe=self.timefram)
        self.__normalizedata()
        self.__split()
        self.__make_sequntial_array()
        if self.__model == None:
            self.__model = self.create_model()
        print("initialize has been done.")

    def __preprocess(self, timeframe):
        self.__data['Volume'].replace(to_replace=0, method='ffill', inplace=True)
        self.__data.sort_values('Date', inplace=True)
        self.__data['Open'] = self.__data['Open'].pct_change(periods=timeframe)
        self.__data['High'] = self.__data['High'].pct_change(periods=timeframe)
        self.__data['Low'] = self.__data['Low'].pct_change(periods=timeframe)
        self.__data['Close'] = self.__data['Close'].pct_change(periods=timeframe)  # Create arithmetic returns column
        self.__data['Volume'] = self.__data['Volume'].pct_change(periods=timeframe)
        self.__data.dropna(how='any', axis=0, inplace=True)  # Drop all rows with NaN values

    def __normalizedata(self):
        '''Normalize price columns'''
        op = self.__data.nsmallest(20, columns=["Open"]).Open.sum() / 20
        hi = self.__data.nsmallest(20, columns=["High"]).High.sum() / 20
        lo = self.__data.nsmallest(20, columns=["Low"]).Low.sum() / 20
        cl = self.__data.nsmallest(20, columns=["Close"]).Close.sum() / 20
        op2 = self.__data.nlargest(20, columns=["Open"]).Open.sum() / 20
        hi2 = self.__data.nlargest(20, columns=["High"]).High.sum() / 20
        lo2 = self.__data.nlargest(20, columns=["Low"]).Low.sum() / 20
        cl2 = self.__data.nlargest(20, columns=["Close"]).Close.sum() / 20
        min_return = min(op, hi, lo, cl)
        max_return = max(op2, hi2, lo2, cl2)
        # Min-max normalize price columns (0-1 range)
        self.__data['Open'] = (self.__data['Open'] - min_return) / (max_return - min_return)
        self.__data['High'] = (self.__data['High'] - min_return) / (max_return - min_return)
        self.__data['Low'] = (self.__data['Low'] - min_return) / (max_return - min_return)
        self.__data['Close'] = (self.__data['Close'] - min_return) / (max_return - min_return)
        '''Normalize volume column'''
        vl = self.__data.nsmallest(20, columns=["Volume"]).Volume.sum() / 20
        vl2 = self.__data.nlargest(20, columns=["Volume"]).Volume.sum() / 20
        min_volume = vl
        max_volume = vl2

        # Min-max normalize volume columns (0-1 range)
        self.__data['Volume'] = (self.__data['Volume'] - min_volume) / (max_volume - min_volume)
        print(self.__data)

    def __split(self):
        times = sorted(self.__data.index.values)
        last_10pct = sorted(self.__data.index.values)[-int(0.1 * len(times))]  # Last 10% of series
        last_20pct = sorted(self.__data.index.values)[-int(0.2 * len(times))]  # Last 20% of series

        self.__train = self.__data[(self.__data.index < last_20pct)]  # Training data are 80% of total data
        self.__valid = self.__data[(self.__data.index >= last_20pct) & (self.__data.index < last_10pct)]
        self.__test = self.__data[(self.__data.index >= last_10pct)]
        # Remove date column
        self.__train.drop(columns=['Date'], inplace=True)
        self.__valid.drop(columns=['Date'], inplace=True)
        self.__test.drop(columns=['Date'], inplace=True)

    def __make_sequntial_array(self):
        # Convert pandas columns into arrays
        self.__train = self.__train.values
        self.__valid = self.__valid.values
        self.__test = self.__test.values
        print('Training data shape: {}'.format(self.__train.shape))
        print('Validation data shape: {}'.format(self.__valid.shape))
        print('Test data shape: {}'.format(self.__test.shape))
        # Training data
        self.X_train, self.y_train = [], []
        for i in range(self.seq_len, len(self.__train) - (self.timefram - 1)):
            self.X_train.append(
                self.__train[i - self.seq_len:i])  # Chunks of training data with a length of 128 df-rows
            self.y_train.append(
                self.__train[:, 3][i + (self.timefram - 1)])  # Value of 4th column (Close Price) of df-row 128+1
        self.X_train, self.y_train = np.array(self.X_train), np.array(self.y_train)

        ###############################################################################

        # Validation data
        self.X_val, self.y_val = [], []
        for i in range(self.seq_len, len(self.__valid) - (self.timefram - 1)):
            self.X_val.append(self.__valid[i - self.seq_len:i])
            self.y_val.append(self.__valid[:, 3][i + (self.timefram - 1)])
        self.X_val, self.y_val = np.array(self.X_val), np.array(self.y_val)

        ###############################################################################

        # Test data
        self.X_test, self.y_test = [], []
        for i in range(self.seq_len, len(self.__test) - (self.timefram - 1)):
            self.X_test.append(self.__test[i - self.seq_len:i])
            self.y_test.append(self.__test[:, 3][i + (self.timefram - 1)])
        self.X_test, self.y_test = np.array(self.X_test), np.array(self.y_test)

    def create_model(self):

        in_seq = Input(shape=(self.seq_len, 5))
        cnn = CNN()
        x = cnn.A(in_seq, 32)
        x = cnn.A(x, 32)
        x = cnn.B(x, 32)
        x = cnn.B(x, 32)
        x = cnn.C(x, 32)
        x = cnn.C(x, 32)
        x = Bidirectional(LSTM(128, return_sequences=True))(x)
        # x = Bidirectional(LSTM(64, return_sequences=True))(in_seq)
        # avg_pool = GlobalAveragePooling1D()(x)
        # max_pool = GlobalMaxPooling1D()(x)
        x = x[:, -1, :]
        # conc = concatenate([avg_pool, max_pool,x])
        conc = Dense(64, activation="relu")(x)
        out = Dense(1, activation="linear")(conc)
        model = Model(inputs=in_seq, outputs=out)
        model.compile(loss="mse", optimizer="adam", metrics=['mae', 'mape'])
        # model.summary()
        # callback = tf.keras.callbacks.EarlyStopping(monitor='val_loss', patience=2)
        self.__callback = tf.keras.callbacks.ModelCheckpoint('Static/ARAN_model.hdf5', monitor='val_loss',
                                                             save_best_only=True, verbose=1)

        return model

    def predict(self):
        self.__model.fit(self.X_train, self.y_train, batch_size=2048,
                         verbose=2,
                         callbacks=[self.__callback],
                         epochs=5,
                         # shuffle=True,
                         validation_data=(self.X_val, self.y_val), )
        '''Calculate predictions and metrics'''

        # Calculate predication for training, validation and test data
        train_pred = self.__model.predict(self.X_train)
        # val_pred = self.__model.predict(self.X_val)
        test_pred = self.__model.predict(self.X_test)

        # Print evaluation metrics for all datasets
        train_eval = self.__model.evaluate(self.X_train, self.y_train, verbose=0)
        val_eval = self.__model.evaluate(self.X_val, self.y_val, verbose=0)
        test_eval = self.__model.evaluate(self.X_test, self.y_test, verbose=0)
        print(' ')
        print('Evaluation metrics')
        print('Training Data - Loss: {:.4f}, MAE: {:.4f}, MAPE: {:.4f}'.format(train_eval[0], train_eval[1],
                                                                               train_eval[2]))
        print('Validation Data - Loss: {:.4f}, MAE: {:.4f}, MAPE: {:.4f}'.format(val_eval[0], val_eval[1], val_eval[2]))
        print('Test Data - Loss: {:.4f}, MAE: {:.4f}, MAPE: {:.4f}'.format(test_eval[0], test_eval[1], test_eval[2]))

        fig = plt.figure(figsize=(60, 5))
        st = fig.suptitle("Bi-LSTM Model", fontsize=22)
        st.set_y(1.02)

        # Plot training data results
        ax11 = fig.add_subplot(311)
        ax11.plot(self.__train[128 + self.timefram - 1:, 3], label='IBM Closing Returns')
        ax11.plot(train_pred[:], color='yellow', linewidth=3, label='Predicted IBM Closing Returns')
        ax11.set_title("Training Data", fontsize=18)
        ax11.set_xlabel('Date')
        ax11.set_ylabel('IBM Closing Returns')
        ax22 = fig.add_subplot(312)
        ax22.plot(self.__test[128 + self.timefram - 1:, 3], label='IBM Closing Returns')
        ax22.plot(test_pred[:], color='yellow', linewidth=3, label='Predicted IBM Closing Returns')
        ax22.set_title("test Data", fontsize=18)
        ax22.set_xlabel('Date')
        ax22.set_ylabel('IBM Closing Returns')


# model = tf.keras.models.load_model('Static/ARAN_model.hdf5')
a = ML(df, seq_len=128, timefram=1)
a.predict()
