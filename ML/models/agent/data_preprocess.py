import os
import sys

import numpy as np
import pandas as pd
import pandas_ta as ta
import itertools
from Libraries.data_collector import *
from ML import data
from inspect import getmembers, isfunction

# ROOT = sys.path[1] + '/data/'
ROOT = '/home/afshin/tmp/pycharm_project_266/data/'


# ROOT = '../../../../data/'


def get_data_from_exchange(exchange, symbols, number, unit, save=True):
    datasets = []
    for sym in symbols:
        data = get_all_candles(exchange=exchange, symbol=sym, number=number, unit=unit, save_csv=False)
        datasets.append(data)
        if save:
            data.to_csv(ROOT + 'coins/' + f'{sym.value}_{unit}_{number}.csv')
    return datasets


def difference_percentage_calculator(df: pd.DataFrame, column_name):
    shifted_column = df[column_name].shift(periods=1, fill_value=df[column_name].iloc[0])
    df['difference'] = (df[column_name] - shifted_column) / shifted_column * 100
    return df


def merge_datasets(datasets, merged_address, save=True, difference_calculator=True, drop_nan=True,
                   indicator_names_list=None, difference_column_name='close'):
    start_date = []
    columns_name = []
    for dataset in datasets:
        start_date.append(dataset.date.min())
    min_date = max(start_date)
    for i, dataset in enumerate(datasets):
        if indicator_names_list is not None:
            dataset, columns_name = add_indicators(dataset, indicator_names_list)
        datasets[i] = dataset[dataset.date >= min_date].reset_index()
        datasets[i] = difference_percentage_calculator(datasets[i], difference_column_name)

    result = pd.concat(datasets, axis=1)
    if drop_nan:
        result = result.dropna()
    if save:
        result.to_csv(ROOT + 'coins/' + merged_address)
    return result


def read_merged_data_offline(address):
    dataset = pd.read_csv(ROOT + 'coins/' + address)
    if 'Unnamed: 0' in dataset.columns:
        dataset.drop(columns=['Unnamed: 0'], inplace=True)
    return dataset


def set_indicator(df):
    indicators = {'stochRsi': [{'dataframe': df, 'length': 14, 'rsi_length': 14, 'k': 3, 'd': 3}],
                  'sma': [{'dataframe': df, 'length': 14}], 'mfi': [{'dataframe': df, 'length': 14}]}
    return indicators


def add_indicators(df: pd.DataFrame, indicator_name_list):
    indicator_dict = set_indicator(df)
    function_name_list = [element[0] for element in getmembers(data, isfunction)]
    function_list = [element[1] for element in getmembers(data, isfunction)]
    indicator_columns_name = []
    for indicator_name in indicator_name_list:
        indicator_parameters_list = indicator_dict.get(indicator_name, 0)
        if indicator_parameters_list != 0:
            for i, indicator_parameters in enumerate(indicator_parameters_list):
                temp = function_list[function_name_list.index(indicator_name)].__call__(
                    **indicator_parameters)
                df = pd.concat([df, temp], axis=1)
                indicator_columns_name.append(list(temp.columns))

    return df.dropna(), list(itertools.chain.from_iterable(indicator_columns_name))


def agent_data_preparation(dataset: pd.DataFrame, columns,
                           calculate_difference_column_name='close', n_coins=None):
    if 'Unnamed: 0' in dataset.columns:
        dataset.drop(columns=['Unnamed: 0'], inplace=True)
    if n_coins == 1:
        dataset = difference_percentage_calculator(dataset, calculate_difference_column_name)
    columns_we_need = []
    for column in columns:
        column_names = [column]
        for i in range(1, n_coins):
            column_names.append(f'{column}.{i}')
        columns_we_need.append(dataset[column_names].values)
    return np.stack(columns_we_need, axis=1)


def preprocess(address, columns, n_coins):
    # TODO: make it dynamic
    calculate_difference_column_name = 'close'
    dataset = read_merged_data_offline(address)
    values = agent_data_preparation(dataset, columns, calculate_difference_column_name, n_coins)
    return values


if __name__ == '__main__':
    print(ROOT)
    symbols = [Symbols.BTCUSDT, Symbols.ETHUSDT, Symbols.ETCUSDT]
    unit = 'h'
    number = 4
    merged_address = f'combined_{unit}_{number}.csv'
    difference_column_name = 'close'
    datasets = get_data_from_exchange(Exchange.bitfinex, symbols, number, unit)
    # print(datasets)
    # add_indicators(datasets[0], ['sma','stochRsi'])
    # print(datasets[0])
    result = merge_datasets(datasets, merged_address, indicator_names_list=['sma', 'mfi'],
                            difference_column_name=difference_column_name)
    merged_data = read_merged_data_offline(merged_address)
    # columns = ['close'+'.'+str(i) for i in range(len(symbols))]
    # columns_we_want = ['close', 'difference', 'STOCHRSIk_14_14_3_3', 'STOCHRSId_14_14_3_3']
    # preprocess(merged_address, columns=columns_we_want, n_coins=3)
    # values = agent_data_preparation(dataset=merged_data, columns=['close'])
    # df = pd.read_csv(ROOT + 'coins/ethereum_D_1.csv')
    # difference_percentage_calculator(df, 'close')
