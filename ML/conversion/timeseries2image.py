import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
import cv2
from matplotlib import pyplot as plt
import math


def read_data(address):
    df = pd.read_csv(address)
    df['difference'] = ((df['close'] - df['open']) / df['open']) * 100
    scaler_positive = MinMaxScaler(feature_range=(0, 255))
    scaler_negative = MinMaxScaler(feature_range=(0, 255))
    scaler_positive.fit(df[df['difference'] >= 0]['difference'].to_numpy().reshape(-1, 1))
    scaler_negative.fit(df[df['difference'] <= 0]['difference'].to_numpy().reshape(-1, 1))
    negative = df[df['difference'] < 0]
    positive = df[df['difference'] >= 0]
    positive['color'] = scaler_positive.transform(positive['difference'].to_numpy().reshape(-1, 1))
    negative['color'] = -1 * scaler_negative.transform(negative['difference'].to_numpy().reshape(-1, 1))
    data = pd.concat([positive, negative])
    data = data.sort_values(by=['date'])
    return data


# These numbers were set with 5-min timeframe in mind
def color_conversion(data):
    colors = data['color'].values
    size1 = (224, 84, 24)
    size2 = (224, 168, 12)
    size3 = (364, 288)
    # total = 168*12*224
    total = 364 * 288
    colors = colors[:total]
    # colors1 = colors.reshape(size1)
    colors3 = colors.reshape(size3)
    # test = colors1[0,:,:]
    test = colors3
    # colors2 = colors.reshape(size2)
    # img_size1 = np.zeros((224,84,24,3))
    # img_size2 = np.zeros((224,168,12,3))
    # for i in colors:
    #     if i < 0:
    #         img_size1[]
    return test


# test = test.reshape(84,24)
# t = np.zeros((84,24,3))


# for i in test:
#     print(i)
def assign_pixel(image, data):
    temp = data.flatten()
    for i in range(data.flatten().shape[0]):
        if temp[i] < 0:
            image[i // 288, i % 288, 0] = math.floor(-1 * temp[i])
        else:
            image[i // 288, i % 288, 1] = math.floor(temp[i])
    return image


def show_converted_timeseries(test):
    t = np.zeros((364, 288, 3))
    t = assign_pixel(t, test)

    # i = 5
    # t[i//24,i%24,1] =

    # for i in colors1:
    t = np.float32(t)
    t = cv2.cvtColor(t, cv2.COLOR_BGR2RGB)
    # cv2.imwrite('color_img.jpg', t)
    plt.imshow(t)
    # cv2.waitKey()
