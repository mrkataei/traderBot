from pathlib import Path
import numpy as np
import pandas as pd
import tensorflow as tf
from keras.layers import Conv1D, Conv1DTranspose
from keras.layers import Dense, Input
from keras.models import Model
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split
from sklearn import svm
import pandas_ta as ta
from sklearn.metrics import confusion_matrix, accuracy_score


# creates a neighborhood of data points around each timestamp
def create_neighborhood(train, window_size):
    new_dataset = []
    for i in range(window_size, train.shape[0] - window_size):
        new_dataset.append(train[i - window_size:i + window_size + 1])
    return np.array(new_dataset)


def feature_extractor(train_x, test_x, mode):
    """
    An autoencoder used to extract features from the training data. It has three different entry modes for 3 different
    feature extraction schemes:
        1: is used when we want to extract data from the statistical features of a point
        neighborhood, meaning the data in the input are not structurally related to each other.
        2: is used when we want to extract data from the actual values of the point
        neighborhood, meaning the data in the input are structurally related to each other and we use a convolution layer.
        3: A combination of the two forms above. Still not written
    """

    batch_size = 32
    epochs = 100
    train_dataset = tf.data.Dataset.from_tensor_slices((train_x, train_x)).batch(batch_size)
    input_layer = Input(shape=(train_x.shape[1], train_x.shape[2]))

    # Encoder
    if mode == 1:
        layer1 = Dense(16)(input_layer)
    elif mode == 2:
        layer1 = Conv1D(16, 3, padding='same')(input_layer)
    elif mode == 3:
        layer1 = Conv1D(16, 3, padding='valid')(input_layer)
    layer1 = tf.keras.layers.LeakyReLU(alpha=0.3, name='layer1-relu')(layer1)
    layer2 = Dense(8)(layer1)
    layer2 = tf.keras.layers.LeakyReLU(alpha=0.3, name='layer2-relu')(layer2)
    # layer2 = tf.keras.layers.Dropout(0.2)(layer2)
    encodings = Dense(5, name='encodings')(layer2)

    # Decoder
    layer2_ = Dense(8)(encodings)
    layer2_ = tf.keras.layers.LeakyReLU(alpha=0.3, name='layer2-reluT')(layer2_)
    # layer2_ = tf.keras.layers.Dropout(0.2)(layer2_)
    if mode == 1:
        layer1_ = Dense(16)(layer2_)
    if mode == 2:
        layer1_ = Conv1DTranspose(16, 3, padding='same')(layer2_)
    if mode == 3:
        layer1_ = Conv1D(16, 3, padding='valid')(layer2_)
    layer1_ = tf.keras.layers.LeakyReLU(alpha=0.3, name='layer1-reluT')(layer1_)
    decoded = Dense(train_x.shape[2], activation="relu", name='decodings')(layer1_)
    autoencoder = Model(input_layer, decoded)
    # optimizer = tf.optimizers.Adam(clipvalue=0.5)
    autoencoder.compile(optimizer='sgd', loss='mean_squared_error')
    print(autoencoder.summary())
    # A condition on which the training process stops
    es_callback = tf.keras.callbacks.EarlyStopping(monitor='val_loss', patience=5)

    # 3 different callings of the fit function
    # autoencoder.fit(train_dataset, epochs=epochs, verbose=2, callbacks = [es_callback])
    # autoencoder.fit(train_x, train_x, validation_split=0.30, batch_size=batch_size, epochs=epochs, verbose=2,callbacks=[es_callback])
    autoencoder.fit(train_x, train_x, validation_data=(test_x, test_x), batch_size=batch_size, epochs=epochs, verbose=1)

    encoder = Model(input_layer, encodings)
    return encoder


# prepares the data into a format acceptable by the model
def data_prepration(train_x, test_x, column, window_size):
    scaler = MinMaxScaler()

    # reshaping train data
    train_x[column] = scaler.fit_transform(train_x[column].to_numpy().reshape(-1, 1))
    train_x = train_x[column].values
    train_x = np.pad(train_x, (window_size, window_size), 'constant', constant_values=(train_x[0], train_x[-1]))
    train_x = create_neighborhood(train_x, window_size)
    train_x = train_x.reshape(train_x.shape[0], 1, train_x.shape[1])

    # reshaping test data
    test_x[column] = scaler.transform(test_x[column].to_numpy().reshape(-1, 1))
    test_x = test_x[column].values
    test_x = np.pad(test_x, (window_size, window_size), 'constant', constant_values=(test_x[0], test_x[-1]))
    test_x = create_neighborhood(test_x, window_size)
    test_x = test_x.reshape(test_x.shape[0], 1, test_x.shape[1])
    return train_x, test_x, scaler


# This function extracts features from points around each point with no additional information
def feature_extraction_original_data(data, column, window_size):
    train_x, test_x, train_y, test_y = train_test_split(data, data, test_size=0.3, shuffle=False)
    train_x, test_x, scaler = data_prepration(train_x, test_x, column, window_size)
    encoder = feature_extractor(train_x, test_x, 2)
    # encoder = None
    return train_x, test_x, encoder, scaler


def read_data(address):
    df = pd.read_csv("ETHUSDTm_30.csv")
    df['hl2'] = (ta.hl2(high=df['high'], low=df['low'])).values
    df['hlc3'] = (ta.hlc3(high=df['high'], low=df['low'], close=df['close'])).values
    df['ohlc4'] = (ta.ohlc4(high=df['high'], low=df['low'], close=df['close'], open_=df['open'])).values
    indicator = ta.macd(df['hl2'])
    df['hl2_MD'] = indicator['MACD_12_26_9']
    df['hl2_MDh'] = indicator['MACDh_12_26_9']
    df['hl2_MDs'] = indicator['MACDs_12_26_9']
    indicator = ta.macd(df['hlc3'])
    df['hlc3_MD'] = indicator['MACD_12_26_9']
    df['hlc3_MDh'] = indicator['MACDh_12_26_9']
    df['hlc3_MDs'] = indicator['MACDs_12_26_9']
    indicator = ta.macd(df['ohlc4'])
    df['ohlc4_MD'] = indicator['MACD_12_26_9']
    df['ohlc4_MDh'] = indicator['MACDh_12_26_9']
    df['ohlc4_MDs'] = indicator['MACDs_12_26_9']
    og_df = df.copy()
    # reducing the data to the close column for now
    df = df[['close']]
    return df


def rescaler(reshaped_train_data, reshaped_test_data):
    t_train = reshaped_train_data.reshape(reshaped_train_data.shape[0] * reshaped_train_data.shape[2])
    rescaled_train_data = scaler.inverse_transform(t_train.reshape(-1, 1))
    t_test = reshaped_test_data.reshape(reshaped_test_data.shape[0] * reshaped_test_data.shape[2])
    rescaled_test_data = scaler.inverse_transform(t_test.reshape(-1, 1))
    rescaled_train_data = rescaled_train_data.reshape(reshaped_train_data.shape[0], reshaped_train_data.shape[2])
    rescaled_test_data = rescaled_test_data.reshape(reshaped_test_data.shape[0], reshaped_test_data.shape[2])
    return rescaled_train_data, rescaled_test_data


# A simple labeler that labels the candles based on the increase on decrease in the price
def naive_simple_labeler(rescaled_train_data, rescaled_test_data, window_size, threshold, info=True):
    train_classes = []
    test_classes = []
    for neighborhood in rescaled_train_data:
        difference = neighborhood[-1] - neighborhood[window_size]
        if difference >= threshold:
            train_classes.append(0)  # buy
        elif difference <= -1 * threshold:
            train_classes.append(1)  # sell
        else:
            train_classes.append(2)  # hold
    train_classes = np.array(train_classes)

    test_classes = []
    for neighborhood in rescaled_test_data:
        difference = neighborhood[-1] - neighborhood[window_size]
        if difference >= threshold:
            test_classes.append(0)  # buy
        elif difference <= -1 * threshold:
            test_classes.append(1)  # sell
        else:
            test_classes.append(2)  # hold
    test_classes = np.array(test_classes)
    # print some information about the density of each class
    if info:
        (unique, count) = np.unique(train_classes, return_counts=True)
        train_frequencies = np.asarray((unique, count)).T
        print(train_frequencies)

        (unique, count) = np.unique(test_classes, return_counts=True)
        test_frequencies = np.asarray((unique, count)).T
        print(test_frequencies)

    return train_classes, test_classes


if __name__ == '__main__':
    address = "ETHUSDTm_30.csv"
    df = read_data(address)
    window_size = 6
    reshaped_train_data, reshaped_test_data, encoder, scaler = feature_extraction_original_data(df, 'close',
                                                                                                window_size)

    # reshaping and rescaling the data back into the proper form and scale for the classification algorithms
    rescaled_train_data, rescaled_test_data = rescaler(reshaped_train_data, reshaped_test_data)

    number_of_classes = 3  # Will use 3 classes for now
    threshold = 5  # if there is a increase of 10 at the end of the window, the class is 0, else 1 - should be dynamic
    neighborhood_size = (2 * window_size) + 1
    train_classes, test_classes = naive_simple_labeler(rescaled_train_data, rescaled_test_data, window_size, threshold,
                                                       info=True)
    train_features = encoder.predict(reshaped_train_data).reshape(reshaped_train_data.shape[0], 5)
    train_df = pd.DataFrame(train_features, columns=['feature1', 'feature2', 'feature3', 'feature4', 'feature5'])
    train_df['class'] = train_classes

    test_features = encoder.predict(reshaped_test_data).reshape(reshaped_test_data.shape[0], 5)
    test_df = pd.DataFrame(test_features, columns=['feature1', 'feature2', 'feature3', 'feature4', 'feature5'])
    test_df['class'] = test_classes
